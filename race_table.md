# Week 10 race - single agent vs orchestrator

Same 10 claims as Week 7/8: ['CLM-2026-00001', 'CLM-2026-00002', 'CLM-2026-00003', 'CLM-2026-00004', 'CLM-2026-00005', 'CLM-2026-00006', 'CLM-2026-00007', 'CLM-2026-00008', 'CLM-2026-00009', 'CLM-2026-00010']

| metric | single | multi |
|---|---|---|
| pass_rate | 100.0 | 80.0 |
| p50_latency | 11.63 | 19.09 |
| p99_latency | 20.58 | 25.05 |
| total_tokens | 28629 | 11717 |
| cost_per_claim | 0.000854 | 0.000452 |

context re-send multiplier: **0.4x**
dominant hand-off: **orchestrator->exclusions_worker** - 79% of all multi-agent tokens
