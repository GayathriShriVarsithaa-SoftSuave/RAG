# tenx.md

At 10x today's peak volume (10 claims/hr -> 100 claims/hr = 6.7 Gemini calls/min), nothing
breaks yet: that's under half the 15 calls/min free-tier rate limit, and cost scales from
$0.06/day to $0.60/day - still trivial. The rate limit is still the FIRST wall as volume keeps
growing, though: it breaks at ~22x today's peak (15 / 0.67 calls-per-min-today = 22.4x), while
cost would need roughly 250x volume before it became a real budget concern. So at 10x
specifically: nothing breaks. The first thing that will break, well before cost becomes an
issue, is the Gemini rate limit - and claims like CLM-2026-00012 (pre-fix) make that wall come
sooner than the math above shows, since each retry-loop claim consumes 2x the normal call budget.
