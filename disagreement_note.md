# Week 6 Task D - results note

## Numbers
- agreement_before (judge_v1.txt): 84.0% (21/25)
- agreement_after  (judge_v2.txt): 92.0% (23/25)
- on the 23 cases NOT shown to the judge as examples: 91.3% before, 91.3% after (no change)
- my 4 hand-labelled FAILs (cases 10, 18, 19, 25) caught by the judge: 0/4 before, 2/4 after (only the 2 it was shown)
- assertions: 4 | judged criteria: 1
- eval set: 27 cases, 6 regression cases from real failed traces

## Eval table (pass rate by mode)
| Mode | What | Cases | Passed | Rate |
|---|---|---|---|---|
| M1 | generation backend (was 403) | 10 | 8 | 80.0% |
| M2 | refusal threshold wrongly refuses | 4 | 0 | 0.0% |
| M3 | correct refusal (not in corpus) | 5 | 5 | 100.0% |
| M4 | reranker ranks wrong chunk first | 3 | 0 | 0.0% |
| M5 | typo / informal phrasing | 2 | 0 | 0.0% |
| M6 | compound question | 3 | 0 | 0.0% |
| ALL | | 27 | 13 | 48.1% |

Regression cases (real failed traces, replayed verbatim): 0/6 pass.
The overall 48.1% hides four modes at 0%. 12 of the 14 failures are wrong refusals; in my labelling run
the model answered 11 of those once the score gate was lifted, consistent with the Week 5 M2 finding.

## Blind-protocol evidence
- labels_25.json committed: a7a295f, 2026-09-21T06:40:39+05:30
- first judge run (v1): 2026-09-21T01:16:57 UTC (06:46:57 IST), from judge_run_judge_v1.json - after the labels
- prediction.txt committed: f0a9514, 06:54:33 IST - before judge_v2.txt was built
- judge v2 run: 2026-09-21T01:33:47 UTC (07:03:47 IST)

## Criteria moved from the judge into code
The repo had no judge before this task, so the judge started with only the one criterion below.
The rest of the "is this answer good?" checklist is implemented as code:

| Criterion | Where it lives |
|---|---|
| refuses only when it should | assertion refusal_matches_expectation |
| has a [chunk_id: ..., clause: ...] citation | assertion has_citation |
| a really-retrieved chunk is cited | assertion cites_retrieved_chunk |
| any denial/exclusion statement names an E-xx code | assertion denial_cites_exclusion_code |
| every claim is supported by the excerpts | judge (faithful_to_excerpts) |

The task's claim-number / date-of-loss / excess assertions do not apply: this corpus has none of those fields.

## Two disagreements (judge vs me)

### Case 10 (Total Eyes-Off-Road Time metric)
- me: FAIL, judge: PASS (in both v1 and v2)
- who was right, and why: I was right: the excerpt only names the metric and never says it measures eyes-off-road time.

### Case 18 (autonomous driving and medical diagnosis)
- me: FAIL, judge: PASS (in both v1 and v2)
- who was right, and why: I was right, but it is a close call: the exclusions table supports "excluded" for both features, but the "outside the active scope" sentence in chunk 16 names medical diagnosis and not autonomous driving, so the answer's claim that both are outside the active scope is not explicitly supported. The judge treated "excluded" and "outside the active scope" as the same thing, which is a reasonable lenient reading.

## Prediction vs outcome
- Prediction (prediction.txt, committed f0a9514 before v2): "Adding cases 19 and 25 as examples will teach the judge to FAIL answers that state something the excerpts only imply (like "8 is the total" or "recordings contain raw data"), so I expect it to fix cases 10, 19 and 25 but not case 18 (where the excerpts do mention exclusion and scope), and I expect the stricter judge to wrongly start failing one or two of my PASS cases."
- What happened: cases 19 and 25 fixed (the two examples); case 10 not fixed; case 18 not fixed; no new false FAILs on my PASS cases.
- Where my prediction was wrong: (1) I expected the lesson to transfer to case 10 and it did not; (2) I expected 1-2 new false FAILs and there were none.

## Limits and honest caveats
- 21 of my 25 labels are PASS, so an always-PASS judge scores 84%. Before/after, look at FAIL recall (0/4 -> 2/4), not just agreement.
- The whole +8 points came from the 2 examples the judge was shown; on the other 23 cases nothing changed.
- In the full eval the v2 judge marked 8 wrong refusals as FAIL despite its own "REFUSE = PASS" rule. My 25 labels never tested wrong refusals, so that behaviour is unvalidated. It did not change the table (the refusal assertion already failed those cases).
- Judge model is the same Gemini model as the generator.
- Per-trace mode tags were inferred from taxonomy.md counts and notes.md.
- RAGAS bonus not attempted.
