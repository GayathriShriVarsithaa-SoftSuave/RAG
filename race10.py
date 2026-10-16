"""
Week 10 - races the SINGLE agent (Week 7's claim_agent.py) against the orchestrator on the
SAME 10 claims used in Weeks 7/8 (Week-6's own eval set belongs to a different app - the
Neurora endorsement search - so it has no claims or exclusions at all; these 10 are the real
comparable dataset for this domain).

    python race10.py
"""
import csv
import json
import statistics

from claims_data import RACE, grade
from claim_agent import run_agent          # the single agent, from Week 7
from orchestrator import run_orchestrator  # this week's new multi-agent pipeline

ARMS = [("single", run_agent), ("multi", run_orchestrator)]


def p99(values):
    if len(values) < 2:
        return max(values)
    values = sorted(values)
    idx = min(len(values) - 1, round(0.99 * (len(values) - 1)))
    return values[idx]


def main():
    rows = []
    all_handoffs = []
    for claim_id, kind, _, _ in RACE:
        for arm, runner in ARMS:
            out = runner(claim_id, verbose=False)
            passed = grade(out["answer"], claim_id)
            latency = out.get("seconds") or out.get("total_latency_s", 0)
            tokens = out.get("tokens") or out.get("total_tokens", 0)
            cost = out.get("cost") or out.get("total_cost", 0)
            rows.append({"arm": arm, "claim_id": claim_id, "kind": kind, "passed": passed,
                        "latency_s": round(latency, 2), "tokens": tokens, "cost_usd": round(cost, 6)})
            if arm == "multi":
                for h in out["handoffs"]:
                    all_handoffs.append({"claim_id": claim_id, **h})
            print(f"{arm:6} {claim_id} {'PASS' if passed else 'FAIL'}  tokens={tokens}  cost=${cost:.5f}  latency={latency:.1f}s")

    with open("handoffs.log", "w") as f:
        for h in all_handoffs:
            f.write(json.dumps(h) + "\n")

    summary = {}
    for arm, _ in ARMS:
        arm_rows = [r for r in rows if r["arm"] == arm]
        lat = [r["latency_s"] for r in arm_rows]
        summary[arm] = {
            "pass_rate": round(100 * sum(r["passed"] for r in arm_rows) / len(arm_rows), 1),
            "p50_latency": round(statistics.median(lat), 2),
            "p99_latency": round(p99(lat), 2),
            "total_tokens": sum(r["tokens"] for r in arm_rows),
            "cost_per_claim": round(sum(r["cost_usd"] for r in arm_rows) / len(arm_rows), 6),
        }

    multiplier = round(summary["multi"]["total_tokens"] / summary["single"]["total_tokens"], 1)

    handoff_totals = {}
    for h in all_handoffs:
        name = h["handoff"].split(" (lap")[0]   # merge exclusions_worker laps into one bucket
        handoff_totals[name] = handoff_totals.get(name, 0) + h["tokens_total"]
    grand_total = sum(handoff_totals.values())
    dominant = max(handoff_totals, key=handoff_totals.get)
    dominant_pct = round(100 * handoff_totals[dominant] / grand_total, 0)

    print("\n" + "=" * 70)
    print(f"{'metric':<16}{'single':>12}{'multi':>12}")
    for metric in ("pass_rate", "p50_latency", "p99_latency", "total_tokens", "cost_per_claim"):
        print(f"{metric:<16}{summary['single'][metric]:>12}{summary['multi'][metric]:>12}")
    print("=" * 70)
    print(f"context re-send multiplier: {multiplier}x  (multi tokens / single tokens)")
    print(f"dominant hand-off: {dominant} - {dominant_pct:.0f}% of all multi-agent tokens")

    with open("race_table.md", "w") as f:
        f.write("# Week 10 race - single agent vs orchestrator\n\n")
        f.write(f"Same {len(RACE)} claims as Week 7/8: {[c[0] for c in RACE]}\n\n")
        f.write("| metric | single | multi |\n|---|---|---|\n")
        for metric in ("pass_rate", "p50_latency", "p99_latency", "total_tokens", "cost_per_claim"):
            f.write(f"| {metric} | {summary['single'][metric]} | {summary['multi'][metric]} |\n")
        f.write(f"\ncontext re-send multiplier: **{multiplier}x**\n")
        f.write(f"dominant hand-off: **{dominant}** - {dominant_pct:.0f}% of all multi-agent tokens\n")

    print("\nSaved race_table.md and handoffs.log")


if __name__ == "__main__":
    main()
