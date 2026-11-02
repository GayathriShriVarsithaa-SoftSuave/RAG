# drill.md

Complaint given: "an adjuster says it told a claimant something was covered when the policy
excludes it, sometime yesterday." No trace id, no claim number, no timestamp.

## Time to find
00:23 (mm:ss)

## Slice that found it
Combined filter: output_decision == COVERED AND free-text "water" across both input notes and
output text (`python3 search_logs.py --decision COVERED --text water`). This was the first
query tried and it returned exactly 1 match out of 57 logged requests.

## Why it worked
The complaint describes the OUTPUT ("told a claimant something was covered"), not the input,
so filtering on output_decision was the natural starting point. Combining it with a text search
for water-damage language narrowed 22 COVERED decisions down to the one claim whose notes
describe flood-pattern damage ("creek... burst its banks... water poured across the ground
floor") worded without the literal word "flood" - the only COVERED entry that looks out of
place next to burglary/fire/pipe-burst claims.

## Found
trace_id: f58feb98-07d0-4474-9400-6428457f34df
claim_id: CLM-2026-00011
retrieved_context_ids: [] - confirms this is a genuine retrieval-layer gap: the policy-exclusions
search found zero matching exclusions for this claim's wording.

## Important honest follow-up
Reproducing this live (not from the logs) showed the real agent today actually gets
CLM-2026-00011 right: it rewrites its search query to include the word "flood" before calling
search_policy, compensating for the keyword gap. So the keyword gap is real, but it did not
cause a live wrong-coverage decision when re-tested. The actual reproducible failure found while
investigating was different: a cost/efficiency bug (CLM-2026-00012, see eval_before.txt /
eval_after.txt) where the agent burns 7-8 retry loops hunting a non-existent exclusion instead
of accepting an empty search_policy result as final. That became the RED->GREEN eval case.
