"""
Week 9 - the MCP-aware agent. Discovers its tools from mcp_config.json at startup; it never
hardcodes a tool list or a server name anywhere. Adding a server to mcp_config.json is the
ONLY thing that changes what this agent can do - this file does not change.

    python agent_mcp.py CLM-2026-00004

The only tool NOT discovered over MCP is compute_payout: pure local arithmetic the agent
already has, not a capability any external system provides, so it is kept as one local
Python function rather than put behind a second server for no reason.
"""

import argparse
import asyncio
import json

from mcp_client import MCPToolbox
from claim_llm import call_llm, cost_of, parse_json, normalise, RULES, OUTPUT_CONTRACT

MAX_ITERS = 8

LOCAL_TOOL_SPEC = {
    "name": "compute_payout",
    "description": ("Calculate the amount to pay on ONE claim: a COVERED claim pays loss_amount "
                    "minus excess (never below zero), an EXCLUDED claim pays 0. Pure arithmetic: "
                    "it never reads claims and never searches the policy."),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "loss_amount": {"type": "NUMBER", "description": "Total loss claimed, from the claim record"},
            "excess": {"type": "NUMBER", "description": "Excess (deductible) from the claim record"},
            "claim_status": {"type": "STRING", "enum": ["COVERED", "EXCLUDED"],
                             "description": "COVERED if no exclusion applies, EXCLUDED if one does"},
        },
        "required": ["loss_amount", "excess", "claim_status"],
    },
}


def compute_payout_local(loss_amount, excess, claim_status):
    if claim_status not in ("COVERED", "EXCLUDED"):
        return {"error": "claim_status must be COVERED or EXCLUDED"}
    if claim_status == "EXCLUDED":
        return {"payable_amount": 0.0}
    return {"payable_amount": round(max(0.0, float(loss_amount) - float(excess)), 2)}


SYSTEM = f"""You triage insurance claims. Use the tools to look things up; do not guess.
{RULES}
Use the compute_payout tool for the payable amount.
{OUTPUT_CONTRACT}"""


async def run_agent_mcp(claim_id, max_iters=MAX_ITERS, verbose=True):
    say = print if verbose else (lambda *a, **k: None)
    from google.genai import types

    box = MCPToolbox()
    discovery_log = await box.connect_all()
    say(f"Discovered {len(box.function_declarations)} tool(s) from {len(discovery_log)} server(s):")
    for entry in discovery_log:
        say(f"  {entry['server']}: {entry['tools']}")

    all_specs = box.function_declarations + [LOCAL_TOOL_SPEC]
    config = {"system_instruction": SYSTEM, "temperature": 0,
              "tools": [{"function_declarations": all_specs}]}
    contents = [types.Content(role="user", parts=[types.Part(text=f"Triage claim {claim_id}.")])]

    tokens_in = tokens_out = 0
    trajectory = []
    answer, stopped_by = None, None

    try:
        for lap in range(1, max_iters + 1):
            response, call_seconds, t_in, t_out = call_llm(contents, config)
            tokens_in += t_in
            tokens_out += t_out

            if not response.candidates or not response.candidates[0].content:
                stopped_by = "no_response"
                break
            content = response.candidates[0].content
            parts = content.parts or []
            calls = [p.function_call for p in parts if p.function_call]

            if not calls:
                text = "".join(p.text for p in parts if p.text)
                answer = normalise(parse_json(text), claim_id)
                stopped_by = "final_answer" if answer else "bad_final_answer"
                say(f"lap {lap}: final answer")
                break

            names = ", ".join(f"{c.name}({dict(c.args or {})})" for c in calls)
            say(f"lap {lap}: tool calls -> {names}")

            contents.append(content)
            response_parts = []
            for c in calls:
                args = dict(c.args or {})
                if c.name == "compute_payout":
                    tool_result, server = compute_payout_local(**args), "LOCAL (not MCP)"
                elif c.name in box.tool_to_server:
                    tool_result, server = await box.call_tool(c.name, args)
                else:
                    tool_result, server = {"error": f"unknown tool {c.name}"}, "none"
                trajectory.append({"tool": c.name, "args": args, "server": server})
                response_parts.append(types.Part.from_function_response(name=c.name, response={"result": tool_result}))
            contents.append(types.Content(role="user", parts=response_parts))
        else:
            stopped_by = "max_iters"
    finally:
        await box.close()

    return {"answer": answer, "terminated_by": stopped_by, "trajectory": trajectory,
            "tokens": tokens_in + tokens_out, "cost": cost_of(tokens_in, tokens_out),
            "discovery_log": discovery_log, "tool_count": len(box.function_declarations)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("claim_id")
    args = parser.parse_args()
    out = asyncio.run(run_agent_mcp(args.claim_id))
    print("\nRESULT:", json.dumps(out["answer"]))
    print(f"stopped by: {out['terminated_by']} | tokens: {out['tokens']} | cost: ${out['cost']:.4f}")
    print(f"tool-call trace: {[(t['tool'], t['server']) for t in out['trajectory']]}")
