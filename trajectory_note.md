# Week 8 Task D - trajectory eval results

## The four trajectory numbers (before mitigation)
- tool-choice accuracy: 90.0% (9/10 claims followed an accepted tool-name sequence)
- argument validity rate: 100.0% (35/35 checks - no hallucinated claim ids, no fabricated
  loss/excess amounts, no invented exclusion ids)
- step efficiency (mean): 1.03 (steps taken / steps needed)
- cost per claim: p50 $0.0010, max $0.0012 (not the mean alone)

## Outcome-vs-trajectory gap
- outcome pass rate: 100.0% (10/10) - every claim reached the right decision and payout
- trajectory pass rate: 90.0% (9/10)
- GAP: 10.0 points

### The right-answer-wrong-path case: CLM-2026-00001
A clean claim (single burst-pipe issue, no exclusion applies). Outcome PASSED (COVERED, correct
payable amount). Trajectory FAILED: the agent called search_policy TWICE
(actual: get_claim -> search_policy -> search_policy -> compute_payout, 4 steps instead of the
3 needed), even though the notes describe only one condition. Both search_policy calls used a
valid, grounded query and returned no matches, so the wrong path did not change the final
number here - but it is exactly the "right payout without ever really checking properly" pattern
the task is about: a wasted, unexplained repeat call that a real audit would flag.

## Mitigation applied: tighter tool description (ONE change only)
Added one instruction to search_policy's description (see mitigation_diff.txt):
"Call this AT MOST ONCE per claim: put every relevant keyword from the notes (the cause of loss
AND any other condition, such as vacancy or business use) into ONE query, rather than calling it
again to check a different condition."

No other change was made (system prompt, other tool descriptions, budgets and code all unchanged).

## Top failure mode: before -> after
- redundant tool call (search_policy called more than once for one claim): 1/10 -> 0/10
- gap: 10.0 points -> 0.0 points
- trajectory pass rate: 90.0% -> 100.0%

## Price paid
- mean cost per claim: $0.00084 -> $0.00085 (delta +$0.00002/claim)
- essentially free: the slightly longer tool description costs a few extra prompt tokens each
  lap, almost exactly offset by no longer paying for the eliminated redundant call.
- p50/max cost per claim also improved: p50 stayed $0.0010, max dropped from $0.0012 to $0.0010,
  since the one expensive outlier run no longer happens.

## Regression check (per claim kind, trajectory pass count)
| Kind | Before | After |
|---|---|---|
| clean | 2/3 | 3/3 |
| exclusion-in-notes | 4/4 | 4/4 |
| missing-or-unclear | 3/3 | 3/3 |

No mode got worse. All three kinds checked; none regressed, and the one broken mode (clean) was fixed.
No new failure mode appeared: tool-choice accuracy, argument validity and outcome pass rate are all
100% after the change, and CLM-2026-00006 (the case with a legitimate two-search alternate path)
still passes, confirming the tighter description did not break that accepted alternate path.

## Alternate-path case
CLM-2026-00006's notes mention two separate issues (a burst pipe, which is fine, and the property
being vacant since March, which is excluded under EXC-04). trajectory_data.py accepts either a
single combined search or two separate search_policy calls as valid for this claim only. In both
the before and after runs, the agent used the single combined-query path, which is one of the two
accepted sequences.

## Limits
- All 10 claims and their expected sequences are invented for this exercise (see claims_data.py,
  Week 7), since the base project has no real claims data.
- Argument validity only checks 3 tool types (get_claim, search_policy, compute_payout); there is
  no fourth "unknown tool" case to validate against in this run.
- Bonus (indirect prompt injection) not attempted.
