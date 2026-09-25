"""
Week 7 - the AGENT: a loop where the MODEL chooses which tool to call next.

    python claim_agent.py CLM-2026-00004
    python claim_agent.py CLM-2026-00004 --max-iters 2 | tee budget_log.txt   # tiny budget: watch it stop cleanly

FOUR budgets, all checked inside the loop:
    MAX_ITERS    how many laps (model calls)
    MAX_TOKENS   total tokens summed over EVERY lap (the loop re-sends the whole history each lap)
    MAX_COST     total dollars over every lap
    MAX_SECONDS  wall-clock time spent working (model calls + tools; the rate-limit pauses are excluded)
"""

import argparse
import json
import time

from google.genai import types

from claim_tools import TOOL_SPECS, run_tool
from claim_llm import call_llm, cost_of, parse_json, normalise, RULES, OUTPUT_CONTRACT

MAX_ITERS = 8
MAX_TOKENS = 20000
MAX_COST = 0.05
MAX_SECONDS = 90

SYSTEM = f"""You triage insurance claims. Use the tools to look things up; do not guess.
{RULES}
Use the compute_payout tool for the payable amount.
{OUTPUT_CONTRACT}"""


def budget_hit(tokens, cost, seconds, limits):
    """Returns the NAME of the first budget that is used up, or None."""
    if tokens >= limits["max_tokens"]:
        return f"max_tokens (limit {limits['max_tokens']}, used {tokens})"
    if cost >= limits["max_cost"]:
        return f"max_cost (limit ${limits['max_cost']}, used ${cost:.4f})"
    if seconds >= limits["max_seconds"]:
        return f"max_seconds (limit {limits['max_seconds']}s, used {seconds:.1f}s)"
    return None


def run_agent(claim_id, max_iters=MAX_ITERS, max_tokens=MAX_TOKENS, max_cost=MAX_COST,
              max_seconds=MAX_SECONDS, verbose=True):
    limits = {"max_tokens": max_tokens, "max_cost": max_cost, "max_seconds": max_seconds}
    say = print if verbose else (lambda *a, **k: None)

    config = {"system_instruction": SYSTEM, "temperature": 0,
              "tools": [{"function_declarations": TOOL_SPECS}]}
    contents = [types.Content(role="user", parts=[types.Part(text=f"Triage claim {claim_id}.")])]

    tokens_in = tokens_out = 0
    seconds = 0.0          # model-call time + tool time
    laps = 0
    trajectory = []        # one entry per tool call: {"tool": name, "args": {...}}, in order

    def result(answer, stopped_by):
        return {"answer": answer, "terminated_by": stopped_by, "laps": laps,
                "tokens_in": tokens_in, "tokens_out": tokens_out, "tokens": tokens_in + tokens_out,
                "cost": cost_of(tokens_in, tokens_out), "seconds": seconds, "trajectory": trajectory}

    say(f"AGENT start: {claim_id}  budgets: iters={max_iters} tokens={max_tokens} cost=${max_cost} seconds={max_seconds}")

    for lap in range(1, max_iters + 1):                       # budget 1: iterations
        response, call_seconds, t_in, t_out = call_llm(contents, config)
        laps = lap
        tokens_in += t_in
        tokens_out += t_out                                    # summed EVERY lap, not just the last
        seconds += call_seconds

        if not response.candidates or not response.candidates[0].content:
            say(f"lap {lap}: model returned nothing. Stopping.")
            return result(None, "no_response")
        content = response.candidates[0].content
        parts = content.parts or []
        calls = [p.function_call for p in parts if p.function_call]

        if not calls:                                          # no tool call = the model is done
            text = "".join(p.text for p in parts if p.text)
            answer = normalise(parse_json(text), claim_id)
            say(f"lap {lap}: final answer | tokens so far {tokens_in + tokens_out} | ${cost_of(tokens_in, tokens_out):.4f}")
            return result(answer, "final_answer" if answer else "bad_final_answer")

        names = ", ".join(f"{c.name}({dict(c.args or {})})" for c in calls)
        say(f"lap {lap}: tool calls -> {names} | tokens so far {tokens_in + tokens_out} | ${cost_of(tokens_in, tokens_out):.4f} | {seconds:.1f}s")

        hit = budget_hit(tokens_in + tokens_out, cost_of(tokens_in, tokens_out), seconds, limits)   # budgets 2, 3, 4
        if hit:
            say(f"BUDGET HIT: {hit}. Stopping cleanly, no answer produced.")
            return result(None, hit.split(" ")[0])

        contents.append(content)                               # keep the model's turn exactly as received
        response_parts = []
        for c in calls:
            trajectory.append({"tool": c.name, "args": dict(c.args or {})})
            start = time.perf_counter()
            tool_result = run_tool(c.name, dict(c.args or {}))
            seconds += time.perf_counter() - start
            response_parts.append(types.Part.from_function_response(name=c.name, response={"result": tool_result}))
        contents.append(types.Content(role="user", parts=response_parts))

    say(f"BUDGET HIT: max_iters (limit {max_iters}, used {laps}). Stopping cleanly, no answer produced.")
    return result(None, "max_iters")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("claim_id")
    parser.add_argument("--max-iters", type=int, default=MAX_ITERS)
    parser.add_argument("--max-tokens", type=int, default=MAX_TOKENS)
    parser.add_argument("--max-cost", type=float, default=MAX_COST)
    parser.add_argument("--max-seconds", type=float, default=MAX_SECONDS)
    args = parser.parse_args()

    out = run_agent(args.claim_id, args.max_iters, args.max_tokens, args.max_cost, args.max_seconds)
    print("\nRESULT:", json.dumps(out["answer"]))
    print(f"stopped by: {out['terminated_by']} | laps: {out['laps']} | tokens: {out['tokens']} | cost: ${out['cost']:.4f} | {out['seconds']:.1f}s")
