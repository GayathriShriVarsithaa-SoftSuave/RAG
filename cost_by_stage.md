# cost_by_stage.md

From trace.json (trace_id f58feb98, claim CLM-2026-00011):

| stage | latency_ms | tokens | cost_usd | % of total cost |
|---|---|---|---|---|
| retrieval (get_claim) | 456 | 726 | 0.000234 | 27% |
| retrieval (search_policy) | 863 | 556 | 0.000179 | 21% |
| tools (compute_payout) | 508 | 583 | 0.000217 | 25% |
| generation (final answer) | 884 | 849 | 0.000242 | 28% |
| **total** | **2711** | **2714** | **0.000872** | **100%** |

Retrieval (get_claim + search_policy combined) is 48% of the bill - roughly as much as
generation alone, even though retrieval is "just lookups." Nothing here is free.
