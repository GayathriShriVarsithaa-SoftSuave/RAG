"""
Week 11 - the eval suite. Two kinds of assertion:
  - most cases: the DECISION must be correct
  - CLM-2026-00012: the decision must be correct AND it must resolve efficiently (<=4 laps) -
    this is the real failure found while reproducing the log drill (an 8-lap retry loop hunting
    a non-existent exclusion, nearly 2x normal cost)
"""
import sys

from claim_agent import run_agent

SUITE = [
    ("CLM-2026-00001", "COVERED", None, None),
    ("CLM-2026-00002", "COVERED", None, None),
    ("CLM-2026-00003", "COVERED", None, None),
    ("CLM-2026-00004", "EXCLUDED", "EXC-01", None),
    ("CLM-2026-00005", "EXCLUDED", "EXC-02", None),
    ("CLM-2026-00006", "EXCLUDED", "EXC-04", None),
    ("CLM-2026-00010", "EXCLUDED", "EXC-05", None),
    ("CLM-2026-00011", "EXCLUDED", "EXC-01", None),   # regression guard: found via log drill, already correct
    ("CLM-2026-00012", "COVERED", None, 4),            # the real RED case: max 4 laps allowed
]


def main():
    passed = 0
    for claim_id, expected_decision, expected_exclusion, max_laps in SUITE:
        out = run_agent(claim_id, verbose=False)
        answer = out["answer"] or {}
        decision_ok = (answer.get("decision") == expected_decision
                       and answer.get("exclusion_id") == expected_exclusion)
        laps_ok = max_laps is None or out["laps"] <= max_laps
        ok = decision_ok and laps_ok
        passed += ok
        extra = f"  laps={out['laps']}" + (f" (max {max_laps})" if max_laps else "")
        print(f"{'PASS' if ok else 'FAIL'}  {claim_id:16} expected={expected_decision}/{expected_exclusion}  "
              f"got={answer.get('decision')}/{answer.get('exclusion_id')}{extra}")
    print(f"\n{passed}/{len(SUITE)} passed")
    return passed == len(SUITE)


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
