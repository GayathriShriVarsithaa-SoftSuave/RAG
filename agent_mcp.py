"""
Week 12 - Claims Triage Agent.

Usage:
    python agent_mcp.py CLAIM_ID POLICY_NUMBER

Example:
    python agent_mcp.py CLM-2026-00004 POL-HO-1001

The policy number must be supplied from a verified claim-policy association.
The agent never decides coverage or calculates a payout.
"""

import argparse
import asyncio
import json
import time

from google.genai import types

from mcp_client import MCPToolbox
from claim_llm import call_llm, cost_of, parse_json
from triage_tools import TriageSession, LOCAL_TOOL_SPECS


MAX_ITERS = 8
MAX_TOKENS = 20000
MAX_COST = 0.05
MAX_SECONDS = 90

SYSTEM = """
You are a claims triage assistant.

IMPORTANT COMPLIANCE RULES:
- Never decide whether a claim is covered or excluded.
- Never approve, decline, reject, or deny a claim.
- Never calculate or recommend a payout.
- Your job is to gather claim facts, retrieve the applicable policy wording,
  check policy dates, and refer the claim to a human adjuster.
- Never invent a policy number, product, policy wording, or citation.
- Use only information returned by tools.

FOLLOW THIS WORKFLOW:

1. Call get_claim with the supplied claim ID.
2. If the claim does not exist or its notes are empty, stop.
   Return a NEEDS_INFO result. Do not continue.
3. Call lookup_policy using the supplied policy number.
4. Read the product returned by lookup_policy.
5. Call check_coverage_in_force using the policy number and the claim's
   date_of_loss.
   IMPORTANT: Even if in_force is false, DO NOT STOP. A policy-period
   mismatch is not a reason to skip adjuster referral.
6. ALWAYS call search_policy_wording after the in-force check, using:
   - a concise description of the loss from the claim notes,
   - the product returned by lookup_policy,
   - the claim's exact date_of_loss.
7. Use the retrieved chunk IDs as citations.
8. Call refer_to_adjuster with:
   - the supplied policy number,
   - the exact loss date,
   - retrieved chunk IDs,
   - a factual summary of the claim,
   - a neutral referral reason.
9. ALWAYS call refer_to_adjuster after wording retrieval, even when
   the policy is not in force. The tool records the in-force status.
10. Do not produce a final referral yourself. The refer_to_adjuster tool
    must perform the referral.
11. Continue calling tools until refer_to_adjuster succeeds or a genuine
    validation error prevents referral. Never stop merely because the
    policy is expired.

If the cause of loss is explicitly undetermined, do not guess the cause.
Do not invent missing facts.

Your facts_summary and referral_reason must contain factual language only.
Do not use coverage-decision language.
"""


def is_error(result):
    return isinstance(result, dict) and bool(result.get("error"))


def budget_hit(tokens, cost, seconds, limits):
    if tokens >= limits["max_tokens"]:
        return f"max_tokens (limit {limits['max_tokens']}, used {tokens})"
    if cost >= limits["max_cost"]:
        return f"max_cost (limit ${limits['max_cost']}, used ${cost:.4f})"
    if seconds >= limits["max_seconds"]:
        return f"max_seconds (limit {limits['max_seconds']}s, used {seconds:.1f}s)"
    return None


async def run_agent_mcp(
    claim_id,
    policy_number,
    max_iters=MAX_ITERS,
    max_tokens=MAX_TOKENS,
    max_cost=MAX_COST,
    max_seconds=MAX_SECONDS,
    verbose=True,
):
    limits = {
        "max_tokens": max_tokens,
        "max_cost": max_cost,
        "max_seconds": max_seconds,
    }
    say = print if verbose else (lambda *a, **k: None)

    from triage_tools import TriageSession

    box = MCPToolbox()
    session = TriageSession()

    discovery_log = []
    trajectory = []
    tokens_in = 0
    tokens_out = 0
    seconds = 0.0
    laps = 0
    answer = None
    stopped_by = None
    claim = None

    try:
        # Discover MCP tools at runtime.
        discovery_log = await box.connect_all()

        say(f"Discovered {len(box.function_declarations)} MCP tools:")
        for entry in discovery_log:
            say(f"  {entry['server']}: {entry['tools']}")

        all_specs = box.function_declarations + LOCAL_TOOL_SPECS

        config = {
            "system_instruction": SYSTEM,
            "temperature": 0,
            "tools": [{"function_declarations": all_specs}],
        }

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=(
                            f"Triage claim {claim_id}. "
                            f"The supplied policy number is {policy_number}. "
                            "Follow the required workflow and use the tools."
                        )
                    )
                ],
            )
        ]

        say(
            f"Budgets: iters={max_iters}, tokens={max_tokens}, "
            f"cost=${max_cost}, seconds={max_seconds}"
        )

        for lap in range(1, max_iters + 1):
            hit = budget_hit(
                tokens_in + tokens_out,
                cost_of(tokens_in, tokens_out),
                seconds,
                limits,
            )
            if hit:
                stopped_by = hit.split(" ")[0]
                say(f"BUDGET HIT: {hit}. Stopping cleanly.")
                break

            response, call_seconds, t_in, t_out = call_llm(
                contents, config
            )

            laps = lap
            seconds += call_seconds
            tokens_in += t_in
            tokens_out += t_out

            hit = budget_hit(
                tokens_in + tokens_out,
                cost_of(tokens_in, tokens_out),
                seconds,
                limits,
            )
            if hit:
                stopped_by = hit.split(" ")[0]
                say(f"BUDGET HIT: {hit}. Stopping cleanly.")
                break

            if not response.candidates or not response.candidates[0].content:
                stopped_by = "no_response"
                break

            content = response.candidates[0].content
            parts = content.parts or []
            calls = [p.function_call for p in parts if p.function_call]

            if not calls:
                # A text response is not an authorized referral.
                stopped_by = "referral_not_completed"
                say("Agent stopped without calling refer_to_adjuster.")
                break

            say(f"\nLap {lap}:")
            contents.append(content)
            response_parts = []

            for call in calls:
                name = call.name
                args = dict(call.args or {})

                say(f"Tool: {name}")
                tool_start = time.perf_counter()

                if name in box.tool_to_server:
                    tool_result, server = await box.call_tool(name, args)

                    # Keep retrieved wording in the compliance session.
                    if name == "search_policy_wording" and isinstance(tool_result, dict):
                        chunks = tool_result.get("results", [])
                        session.record_wording_results(chunks)

                    # Stop safely if the claim cannot be retrieved.
                    if name == "get_claim":
                        if is_error(tool_result):
                            answer = {
                                "claim_id": claim_id,
                                "action": "NEEDS_INFO",
                                "reason": tool_result["error"],
                            }
                            stopped_by = "claim_not_found"
                            break

                        claim = tool_result

                        if not str(claim.get("notes", "")).strip():
                            answer = {
                                "claim_id": claim_id,
                                "action": "NEEDS_INFO",
                                "reason": "Claim adjuster notes are empty.",
                            }
                            stopped_by = "empty_claim_notes"
                            break

                elif name in {spec["name"] for spec in LOCAL_TOOL_SPECS}:
                    tool_result = session.call(name, args)
                    server = "LOCAL (Week 12 compliance tools)"

                    if name == "refer_to_adjuster":
                        answer = tool_result
                        stopped_by = (
                            "referred"
                            if not is_error(tool_result)
                            else "referral_rejected"
                        )

                else:
                    tool_result = {"error": f"Unknown tool: {name}"}
                    server = "none"

                seconds += time.perf_counter() - tool_start

                trajectory.append({
                    "tool": name,
                    "args": args,
                    "server": server,
                })

                say(f"Result: {json.dumps(tool_result, default=str)}")

                if stopped_by is None:
                    hit = budget_hit(
                        tokens_in + tokens_out,
                        cost_of(tokens_in, tokens_out),
                        seconds,
                        limits,
                    )
                    if hit:
                        stopped_by = hit.split(" ")[0]
                        say(f"BUDGET HIT: {hit}. Stopping cleanly.")

                response_parts.append(
                    types.Part.from_function_response(
                        name=name,
                        response={"result": tool_result},
                    )
                )

                if stopped_by is not None:
                    break

            if stopped_by is not None:
                break

            contents.append(
                types.Content(role="user", parts=response_parts)
            )

        else:
            stopped_by = "max_iters"

    finally:
        await box.close()

    return {
        "claim_id": claim_id,
        "policy_number": policy_number,
        "answer": answer,
        "terminated_by": stopped_by,
        "laps": laps,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "tokens": tokens_in + tokens_out,
        "cost": cost_of(tokens_in, tokens_out),
        "seconds": round(seconds, 3),
        "trajectory": trajectory,
        "discovery_log": discovery_log,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("claim_id")
    parser.add_argument("policy_number")
    parser.add_argument("--max-iters", type=int, default=MAX_ITERS)
    parser.add_argument("--max-tokens", type=int, default=MAX_TOKENS)
    parser.add_argument("--max-cost", type=float, default=MAX_COST)
    parser.add_argument("--max-seconds", type=float, default=MAX_SECONDS)
    args = parser.parse_args()

    output = asyncio.run(
        run_agent_mcp(
            args.claim_id,
            args.policy_number,
            max_iters=args.max_iters,
            max_tokens=args.max_tokens,
            max_cost=args.max_cost,
            max_seconds=args.max_seconds,
        )
    )

    print("\n========== WEEK 12 RESULT ==========")
    print(json.dumps(output, indent=2, default=str))
    print("====================================")
