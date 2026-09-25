"""
Week 8 - compares the BEFORE and AFTER trajectory_eval runs and reports:
  - the top failure mode's count, before -> after
  - the price paid (cost per claim, before -> after)
  - a per-claim-kind regression table, so any mode that got worse is named, not hidden

    python regression_check.py trajectory_run_before.json trajectory_run_after.json
"""
import json
import statistics
import sys


def load(path):
    return json.load(open(path))


def is_redundant_call_case(row):
    """The failure mode we are mitigating: the SAME tool name appears more than once in the
    actual sequence."""
    names = row["actual_sequence"]
    return len(names) != len(set(names))


def summarise_run(rows, label):
    n = len(rows)
    redundant = [r for r in rows if is_redundant_call_case(r)]
    costs = [r["cost"] for r in rows]
    print(f"\n{label}")
    print(f"  outcome pass rate    : {100*sum(r['outcome_pass'] for r in rows)/n:.1f}%")
    print(f"  trajectory pass rate : {100*sum(r['trajectory_pass'] for r in rows)/n:.1f}%")
    print(f"  tool-choice accuracy : {100*sum(r['tool_choice_ok'] for r in rows)/n:.1f}%")
    print(f"  redundant-call mode  : {len(redundant)}/{n}  claims: {[r['claim_id'] for r in redundant]}")
    print(f"  mean step efficiency : {statistics.mean(r['efficiency'] for r in rows):.2f}")
    print(f"  cost per claim       : p50 ${statistics.median(costs):.4f}  max ${max(costs):.4f}  mean ${statistics.mean(costs):.5f}")
    return {"redundant_count": len(redundant), "redundant_ids": [r["claim_id"] for r in redundant],
            "mean_cost": statistics.mean(costs), "p50_cost": statistics.median(costs), "max_cost": max(costs),
            "trajectory_rate": 100 * sum(r["trajectory_pass"] for r in rows) / n}


def per_kind_table(before, after):
    kinds = sorted(set(r["kind"] for r in before))
    print("\nPer-mode (claim-kind) regression table: trajectory pass count, before -> after")
    worsened = []
    for k in kinds:
        b = [r for r in before if r["kind"] == k]
        a = [r for r in after if r["kind"] == k]
        b_pass = sum(r["trajectory_pass"] for r in b)
        a_pass = sum(r["trajectory_pass"] for r in a)
        flag = "  <-- WORSENED" if a_pass < b_pass else ""
        if flag:
            worsened.append(k)
        print(f"  {k:19} {b_pass}/{len(b)}  ->  {a_pass}/{len(a)}{flag}")
    if not worsened:
        print("  none worsened. Checked:", ", ".join(kinds))
    return worsened


if __name__ == "__main__":
    before_path, after_path = sys.argv[1], sys.argv[2]
    before, after = load(before_path), load(after_path)
    b = summarise_run(before, "BEFORE")
    a = summarise_run(after, "AFTER")

    print(f"\nTop failure mode (redundant tool call) count: {b['redundant_count']}/10 -> {a['redundant_count']}/10")
    delta = a["mean_cost"] - b["mean_cost"]
    print(f"Price paid (mean cost per claim): ${b['mean_cost']:.5f} -> ${a['mean_cost']:.5f}  (delta ${delta:+.5f})")

    per_kind_table(before, after)
