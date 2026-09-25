"""
Week 7 - the FIXED WORKFLOW: same task, same tools, same model, same rules, same output format.
The steps are hard-coded in order. There is NO loop and the model never chooses a tool.

    python claim_workflow.py CLM-2026-00004

Steps:
  1. get_claim            (code)   stop with NEEDS_INFO if the claim is missing or its notes are empty
  2. read the notes       (model)  -> one short search phrase, and whether the cause is known
  3. search_policy        (code)   using that phrase
  4. decide               (model)  COVERED or EXCLUDED, given the notes + search result
  5. compute_payout       (code)
"""

import json
import sys

from claim_tools import get_claim, search_policy, compute_payout
from claim_llm import call_llm, cost_of, parse_json, normalise, RULES


def run_workflow(claim_id, verbose=True):
    say = print if verbose else (lambda *a, **k: None)
    tokens_in = tokens_out = 0
    seconds = 0.0
    calls = 0

    def result(decision, exclusion_id, payable):
        answer = normalise({"decision": decision, "exclusion_id": exclusion_id, "payable_amount": payable}, claim_id)
        return {"answer": answer, "terminated_by": "done", "laps": calls,
                "tokens_in": tokens_in, "tokens_out": tokens_out, "tokens": tokens_in + tokens_out,
                "cost": cost_of(tokens_in, tokens_out), "seconds": seconds}

    def ask_model(prompt):
        nonlocal tokens_in, tokens_out, seconds, calls
        response, call_seconds, t_in, t_out = call_llm(prompt, {"temperature": 0})
        tokens_in += t_in
        tokens_out += t_out
        seconds += call_seconds
        calls += 1
        return parse_json(response.text)

    # step 1
    claim = get_claim(claim_id)
    if "error" in claim or not claim["notes"].strip():
        say("step 1: claim missing or notes empty -> NEEDS_INFO (no model call needed)")
        return result("NEEDS_INFO", None, 0)
    say("step 1: got the claim")

    # step 2
    notes_reading = ask_model(
        "Read the adjuster notes below and reply with ONLY this JSON:\n"
        '{"cause_known": true or false, "search_query": "short phrase: the cause of loss plus any unusual '
        'condition mentioned, such as vacancy or business use"}\n'
        "Set cause_known to false if the notes say the cause has not been determined.\n\n"
        f"Adjuster notes: {claim['notes']}"
    ) or {}
    say(f"step 2: model read the notes -> {notes_reading}")
    if notes_reading.get("cause_known") is False:
        return result("NEEDS_INFO", None, 0)

    # step 3
    found = search_policy(notes_reading.get("search_query", ""))
    say(f"step 3: policy search -> {[m['id'] for m in found['matches']]}")

    # step 4
    verdict = ask_model(
        f"{RULES}\n\nAdjuster notes: {claim['notes']}\n"
        f"Policy exclusions that matched the search: {json.dumps(found['matches'])}\n\n"
        'Reply with ONLY this JSON: {"decision": "COVERED" or "EXCLUDED", "exclusion_id": "EXC-xx" or null}'
    ) or {}
    decision = str(verdict.get("decision", "")).upper()
    if decision not in ("COVERED", "EXCLUDED"):
        decision = "COVERED" if not found["matches"] else "EXCLUDED"
    exclusion_id = verdict.get("exclusion_id") if decision == "EXCLUDED" else None
    say(f"step 4: model decided -> {decision} {exclusion_id}")

    # step 5
    payable = compute_payout(claim["loss_amount"], claim["excess"], decision)["payable_amount"]
    say(f"step 5: payable -> {payable}")
    return result(decision, exclusion_id, payable)


if __name__ == "__main__":
    out = run_workflow(sys.argv[1])
    print("\nRESULT:", json.dumps(out["answer"]))
    print(f"model calls: {out['laps']} | tokens: {out['tokens']} | cost: ${out['cost']:.4f} | {out['seconds']:.1f}s")
