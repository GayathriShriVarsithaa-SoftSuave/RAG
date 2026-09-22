"""
Week 7 - the RACE: agent vs workflow over the same 10 claims.

    python race.py

Writes race.csv (the 8 numbers) and race_detail.csv (one row per claim per system).
Latency = time spent in model calls + tools (the rate-limit pauses are not counted).
"""

import csv
import statistics

from claims_data import RACE, grade
from claim_agent import run_agent
from claim_workflow import run_workflow

detail = []
for claim_id, kind, _, _ in RACE:
    for system, runner in (("agent", run_agent), ("workflow", run_workflow)):
        out = runner(claim_id, verbose=False)
        passed = grade(out["answer"], claim_id)
        detail.append({"system": system, "claim_id": claim_id, "kind": kind, "passed": passed,
                       "latency_s": round(out["seconds"], 2), "tokens": out["tokens"],
                       "cost_usd": round(out["cost"], 6), "model_calls": out["laps"],
                       "stopped_by": out["terminated_by"],
                       "answer": out["answer"]})
        print(f"{system:9} {claim_id} {kind:19} {'PASS' if passed else 'FAIL'}  calls={out['laps']} tokens={out['tokens']}  stopped_by={out['terminated_by']}")

with open("race_detail.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(detail[0].keys()))
    writer.writeheader()
    writer.writerows(detail)

summary = []
for system in ("agent", "workflow"):
    rows = [r for r in detail if r["system"] == system]
    summary.append({
        "system": system,
        "pass_rate_pct": round(100 * sum(r["passed"] for r in rows) / len(rows), 1),
        "p50_latency_s": round(statistics.median(r["latency_s"] for r in rows), 2),
        "total_tokens": sum(r["tokens"] for r in rows),
        "cost_per_claim_usd": round(sum(r["cost_usd"] for r in rows) / len(rows), 6),
    })

with open("race.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
    writer.writeheader()
    writer.writerows(summary)

print("\n" + "=" * 78)
print(f"{'system':<10}{'pass rate':>11}{'p50 latency':>14}{'total tokens':>15}{'cost / claim':>15}")
print("-" * 78)
for s in summary:
    print(f"{s['system']:<10}{s['pass_rate_pct']:>10}%{s['p50_latency_s']:>13}s{s['total_tokens']:>15}{'$' + format(s['cost_per_claim_usd'], '.6f'):>15}")
print("=" * 78)

print("\nPass count by claim class (this is what the verdict is about):")
for kind in ("clean", "exclusion-in-notes", "missing-or-unclear"):
    line = f"  {kind:<19}"
    for system in ("agent", "workflow"):
        rows = [r for r in detail if r["system"] == system and r["kind"] == kind]
        line += f"  {system}: {sum(r['passed'] for r in rows)}/{len(rows)}"
    print(line)
print("\nSaved race.csv and race_detail.csv")
