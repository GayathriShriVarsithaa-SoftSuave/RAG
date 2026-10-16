"""
Week 10 - the MULTI-AGENT orchestrator: decomposes one claim into two narrow-scope workers,
then synthesises the final answer. Every call between steps is a HAND-OFF, and every hand-off
re-sends context (full system prompt + whatever text it's handed) - that's the cost this week
measures.

Pipeline:
  1. get_claim (plain Python, no model call - same as the single agent)
  2. HAND-OFF 1: orchestrator -> notes_summary_worker
     Narrow job, no tools: summarise the cause of loss + any special condition from raw notes.
  3. HAND-OFF 2: orchestrator -> exclusions_worker
     Narrow job, ONLY 2 tools (search_policy, compute_payout - NOT get_claim, deliberately
     fewer tools than the single agent's 3). Gets the SUMMARY from step 2, not the raw notes.
  4. HAND-OFF 3: orchestrator -> synthesis
     One more call that must produce the SAME output contract as the single agent, given the
     summary + the exclusions worker's structured result.

    python orchestrator.py CLM-2026-00004
    python orchestrator.py CLM-2026-00004 --inject-failure   # forces search_policy to 500 on this claim
"""
import argparse
import json

from claim_tools import TOOL_FUNCS, search_policy as real_search_policy
from claim_llm import call_llm, cost_of, parse_json, normalise
from claims_data import CLAIMS

SUMMARY_SYSTEM = "You summarise insurance adjuster notes in one sentence: the cause of loss, and any special condition (vacancy, business use, etc.), nothing else."
EXCLUSIONS_SYSTEM = """You check ONE thing: does any policy exclusion apply to this claim?
Use search_policy once with the cause of loss. Then use compute_payout with the claim's real
loss_amount and excess and the correct claim_status.
Reply with ONLY this JSON: {"decision": "COVERED" or "EXCLUDED", "exclusion_id": "EXC-xx" or null, "payable_amount": a number}"""
SYNTHESIS_SYSTEM = """You are given a note summary and a coverage-worker's result for one claim.
Combine them into the final answer. If the claim status could not be determined, use NEEDS_INFO.
Reply with ONLY this JSON: {"claim_id": "...", "decision": "COVERED"/"EXCLUDED"/"NEEDS_INFO", "exclusion_id": "EXC-xx" or null, "payable_amount": a number}"""

EXCLUSIONS_TOOLS = [
    {"name": "search_policy", "description": "Look up policy exclusions by keyword.",
     "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]}},
    {"name": "compute_payout", "description": "Compute the payable amount.",
     "parameters": {"type": "OBJECT", "properties": {
         "loss_amount": {"type": "NUMBER"}, "excess": {"type": "NUMBER"},
         "claim_status": {"type": "STRING", "enum": ["COVERED", "EXCLUDED"]}},
         "required": ["loss_amount", "excess", "claim_status"]}},
]


def run_orchestrator(claim_id, inject_failure=False, verbose=True):
    from google.genai import types
    say = print if verbose else (lambda *a, **k: None)
    claim = CLAIMS.get(claim_id)
    handoffs = []
    if claim is None:
        # mirrors what get_claim-as-a-tool lets the single agent do gracefully; here the
        # orchestrator fetches the claim in plain Python BEFORE any model call, so without this
        # guard a missing claim crashes the whole pipeline instead of degrading - a real,
        # UNPLANTED robustness gap found while testing, worth noting in the verdict.
        return {"answer": {"claim_id": claim_id, "decision": "NEEDS_INFO", "exclusion_id": None, "payable_amount": 0.0},
                "handoffs": [], "total_tokens": 0, "total_cost": 0.0, "total_latency_s": 0.0}
    total_tokens_in = total_tokens_out = 0

    def record(name, t_in, t_out, latency):
        nonlocal total_tokens_in, total_tokens_out
        total_tokens_in += t_in
        total_tokens_out += t_out
        handoffs.append({"handoff": name, "tokens_in": t_in, "tokens_out": t_out,
                         "tokens_total": t_in + t_out, "cost": cost_of(t_in, t_out), "latency_s": latency})

    # --- hand-off 1: summary worker ---
    resp, lat, t_in, t_out = call_llm(claim["notes"], {"system_instruction": SUMMARY_SYSTEM, "temperature": 0})
    summary = resp.text.strip()
    record("orchestrator->notes_summary_worker", t_in, t_out, lat)
    say(f"[summary worker] {summary}")

    # --- hand-off 2: exclusions worker (own small tool loop, 2 tools, NOT get_claim) ---
    def search_policy_maybe_failing(query):
        if inject_failure:
            return {"error": "500 Internal Server Error (injected failure)"}
        return real_search_policy(query)

    tool_funcs = {"search_policy": search_policy_maybe_failing, "compute_payout": TOOL_FUNCS["compute_payout"]}
    contents = [types.Content(role="user", parts=[types.Part(
        text=f"Claim summary: {summary}\nloss_amount: {claim['loss_amount']}, excess: {claim['excess']}")])]
    config = {"system_instruction": EXCLUSIONS_SYSTEM, "temperature": 0,
              "tools": [{"function_declarations": EXCLUSIONS_TOOLS}]}
    exclusions_result, exclusions_text = None, None
    for lap in range(4):
        resp, lat, t_in, t_out = call_llm(contents, config)
        record(f"orchestrator->exclusions_worker (lap {lap+1})", t_in, t_out, lat)
        content = resp.candidates[0].content if resp.candidates else None
        parts = content.parts if content else []
        calls = [p.function_call for p in parts if p.function_call]
        if not calls:
            exclusions_text = "".join(p.text for p in parts if p.text)
            exclusions_result = parse_json(exclusions_text)
            break
        contents.append(content)
        response_parts = []
        for c in calls:
            args = dict(c.args or {})
            result = tool_funcs[c.name](**args)
            say(f"  [exclusions worker] {c.name}({args}) -> {result}")
            response_parts.append(types.Part.from_function_response(name=c.name, response={"result": result}))
        contents.append(types.Content(role="user", parts=response_parts))

    # --- hand-off 3: synthesis ---
    synth_prompt = (f"Claim id: {claim_id}\nSummary: {summary}\n"
                    f"Exclusions worker result: {json.dumps(exclusions_result)}")
    resp, lat, t_in, t_out = call_llm(synth_prompt, {"system_instruction": SYNTHESIS_SYSTEM, "temperature": 0})
    record("orchestrator->synthesis", t_in, t_out, lat)
    answer = normalise(parse_json(resp.text), claim_id)

    return {
        "answer": answer, "handoffs": handoffs,
        "total_tokens": total_tokens_in + total_tokens_out,
        "total_cost": cost_of(total_tokens_in, total_tokens_out),
        "total_latency_s": sum(h["latency_s"] for h in handoffs),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("claim_id")
    parser.add_argument("--inject-failure", action="store_true")
    args = parser.parse_args()
    out = run_orchestrator(args.claim_id, args.inject_failure)
    print("\nRESULT:", json.dumps(out["answer"]))
    print(f"total tokens: {out['total_tokens']} | cost: ${out['total_cost']:.4f} | {out['total_latency_s']:.1f}s")
    for h in out["handoffs"]:
        print(f"  {h['handoff']}: {h['tokens_total']} tokens")
