"""
Week 8 - THE TRAJECTORY EVAL. Re-runs the agent on the same 10 Week-7 claims and checks not just
the final answer (the OUTCOME eval, from Week 7) but the PATH it took to get there.

    python trajectory_eval.py | tee trajectory_before.txt

Four trajectory numbers:
  tool-choice accuracy   : did the SEQUENCE of tool names match one of the accepted paths?
  argument validity rate : were the arguments to every tool call real (matched the actual claim
                            data), not hallucinated? Also: was the exclusion_id in the FINAL answer
                            actually returned by a search_policy call, or invented?
  step efficiency         : tool calls made / minimum tool calls needed (1.0 = perfectly efficient)
  cost per claim          : p50 and max (not the mean - the one expensive run is the one that matters)

Plus the outcome-vs-trajectory GAP: outcome pass rate minus trajectory pass rate, and the trace of
one claim that passed the outcome eval while failing the trajectory eval.
"""

import json
import statistics
import sys

from claims_data import CLAIMS, RACE, grade
from claim_tools import search_policy
from claim_agent import run_agent
from trajectory_data import EXPECTED, STEPS_NEEDED


def check_arguments(claim_id, trajectory, final_answer):
    """Checks every tool call's arguments against the real claim data (not hallucinated).
    Returns (list of {tool, args, ok, why}, exclusion_grounded: bool)."""
    claim = CLAIMS.get(claim_id, {})
    checks = []
    found_exclusion_ids = set()

    for call in trajectory:
        name, args = call["tool"], call["args"]
        if name == "get_claim":
            ok = args.get("claim_id") == claim_id
            why = "claim_id matches the claim being processed" if ok else "claim_id does not match the claim being processed"
        elif name == "search_policy":
            query = args.get("query", "")
            ok = isinstance(query, str) and query.strip() != ""
            why = "non-empty query" if ok else "empty or missing query"
            if ok:
                found_exclusion_ids |= {m["id"] for m in search_policy(query)["matches"]}
        elif name == "compute_payout":
            ok = bool(claim) and args.get("loss_amount") == claim.get("loss_amount") and args.get("excess") == claim.get("excess")
            why = "loss_amount/excess match the real claim record" if ok else "loss_amount/excess do NOT match the real claim record (fabricated numbers)"
        else:
            ok, why = False, f"unknown tool {name}"
        checks.append({"tool": name, "args": args, "ok": ok, "why": why})

    exclusion_id = (final_answer or {}).get("exclusion_id")
    exclusion_grounded = True if exclusion_id is None else exclusion_id in found_exclusion_ids
    return checks, exclusion_grounded


def tool_choice_ok(claim_id, trajectory):
    actual = tuple(call["tool"] for call in trajectory)
    return actual in EXPECTED[claim_id], actual


def run_trajectory_eval(verbose_progress=True):
    rows = []
    for claim_id, kind, _, _ in RACE:
        out = run_agent(claim_id, verbose=False)
        trajectory, answer = out["trajectory"], out["answer"]

        outcome_pass = grade(answer, claim_id)
        choice_ok, actual_seq = tool_choice_ok(claim_id, trajectory)
        arg_checks, exclusion_grounded = check_arguments(claim_id, trajectory, answer)
        args_ok = all(c["ok"] for c in arg_checks) and exclusion_grounded
        trajectory_pass = choice_ok and args_ok

        steps_needed = STEPS_NEEDED[claim_id]
        steps_taken = len(trajectory)

        row = {
            "claim_id": claim_id, "kind": kind,
            "outcome_pass": outcome_pass, "trajectory_pass": trajectory_pass,
            "tool_choice_ok": choice_ok, "actual_sequence": list(actual_seq),
            "expected_sequences": [list(s) for s in sorted(EXPECTED[claim_id])],
            "arg_checks": arg_checks, "exclusion_grounded": exclusion_grounded,
            "steps_taken": steps_taken, "steps_needed": steps_needed,
            "efficiency": round(steps_taken / steps_needed, 2) if steps_needed else 1.0,
            "cost": out["cost"], "answer": answer, "laps": out["laps"],
        }
        rows.append(row)
        if verbose_progress:
            print(f"{claim_id} {kind:19} outcome={'PASS' if outcome_pass else 'FAIL':4} "
                  f"trajectory={'PASS' if trajectory_pass else 'FAIL':4} "
                  f"seq={actual_seq} steps={steps_taken}/{steps_needed} cost=${out['cost']:.4f}")
    return rows


def summarise(rows, label="RESULTS"):
    n = len(rows)
    outcome_rate = 100 * sum(r["outcome_pass"] for r in rows) / n
    trajectory_rate = 100 * sum(r["trajectory_pass"] for r in rows) / n
    tool_choice_rate = 100 * sum(r["tool_choice_ok"] for r in rows) / n

    all_checks = [c["ok"] for r in rows for c in r["arg_checks"]] + [r["exclusion_grounded"] for r in rows]
    arg_validity_rate = 100 * sum(all_checks) / len(all_checks) if all_checks else 100.0

    mean_efficiency = statistics.mean(r["efficiency"] for r in rows)
    costs = [r["cost"] for r in rows]
    cost_p50, cost_max = statistics.median(costs), max(costs)

    print("\n" + "=" * 78)
    print(label)
    print("-" * 78)
    print(f"outcome pass rate        : {outcome_rate:.1f}%  ({sum(r['outcome_pass'] for r in rows)}/{n})")
    print(f"trajectory pass rate     : {trajectory_rate:.1f}%  ({sum(r['trajectory_pass'] for r in rows)}/{n})")
    print(f"GAP (outcome - trajectory): {outcome_rate - trajectory_rate:.1f} points")
    print(f"tool-choice accuracy     : {tool_choice_rate:.1f}%")
    print(f"argument validity rate   : {arg_validity_rate:.1f}%  ({sum(all_checks)}/{len(all_checks)} checks)")
    print(f"step efficiency (mean)   : {mean_efficiency:.2f}  (1.00 = no wasted steps)")
    print(f"cost per claim           : p50 ${cost_p50:.4f}  |  max ${cost_max:.4f}")
    print("=" * 78)

    print("\nRight-answer-wrong-path cases (outcome PASS, trajectory FAIL):")
    found_any = False
    for r in rows:
        if r["outcome_pass"] and not r["trajectory_pass"]:
            found_any = True
            print(f"\n  {r['claim_id']} ({r['kind']})")
            print(f"    actual path  : {r['actual_sequence']}")
            print(f"    expected path(s): {r['expected_sequences']}")
            for c in r["arg_checks"]:
                if not c["ok"]:
                    print(f"    bad argument : {c['tool']}({c['args']}) - {c['why']}")
            if not r["exclusion_grounded"]:
                print(f"    exclusion_id in the final answer was NOT returned by any search_policy call")
    if not found_any:
        print("  none found in this run")

    return {"outcome_rate": outcome_rate, "trajectory_rate": trajectory_rate, "gap": outcome_rate - trajectory_rate,
            "tool_choice_rate": tool_choice_rate, "arg_validity_rate": arg_validity_rate,
            "mean_efficiency": mean_efficiency, "cost_p50": cost_p50, "cost_max": cost_max}


if __name__ == "__main__":
    rows = run_trajectory_eval()
    with open("trajectory_run.json", "w") as f:
        json.dump(rows, f, indent=2, default=str)
    summarise(rows)
    print("\nSaved trajectory_run.json")
