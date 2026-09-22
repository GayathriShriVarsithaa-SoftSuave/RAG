The decision rule is whether the path varies by input. Across all 10 claims, mine does not:
get claim -> read notes -> search policy (only if a cause is named) -> decide -> compute payout is
the same four-or-five-step shape every time, including the 4 claims where step 3's query depends on
what step 2 found in the notes. No claim needed branching logic an agent's freedom would justify.

The workflow matched the agent's 100% pass rate while using about half the latency (6.0s vs 12.8s
p50), a tenth of the tokens (2,618 vs 27,853), and an eighth of the cost ($0.0001 vs $0.0008 per
claim), because it skips the extra model call the agent spends deciding which tool to call next.

No claim in this set needs an agent. If a future claim required an open-ended number of lookups
(e.g. chasing a chain of related prior claims), that would justify one.
