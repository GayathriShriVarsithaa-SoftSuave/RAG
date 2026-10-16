# Verdict: kill

Citing: pass rate (100% single vs 80% multi - 2 real wrong coverage decisions) and p99 latency
(20.6s single vs 25.1s multi). The multi-agent system is also cheaper per claim ($0.00045 vs
$0.00085) and uses fewer total tokens (0.4x multiplier) than the single agent, so cost is NOT
the problem here - accuracy and latency are.

Both real failures traced to the same hand-off: orchestrator->exclusions_worker, which also
consumes 79% of all multi-agent tokens. Decomposing the task decomposed the context too: the
summary worker dropped a critical detail (once by hallucinating a response to empty notes,
once by narrowing a two-part query to one word), and the exclusions worker had no way to
recover what it was never given.

Sunk-cost bias, named out loud: I built this orchestrator, the architecture is more interesting
than the single agent, and the token/cost numbers genuinely favor it - all real pulls toward
keeping it anyway. But a system that gets 1 in 5 real coverage decisions wrong is not a
production claims tool regardless of how cheap or clever it is, and "it's efficient" is not
a reason to ship something less accurate than what already worked.
