"""
Week 8 - the expected tool-call path for each of the 10 Week-7 claims.

EXPECTED[claim_id] is a SET of valid tool-name sequences (arguments are checked separately).
Most claims have exactly one valid sequence. CLM-2026-00006 has two: its notes mention TWO
separate issues (a burst pipe, which is fine, and the house being vacant, which is excluded),
so a thorough agent may reasonably run one combined search OR two separate searches - both
are correct reasoning, so both are accepted rather than asserting one exact sequence.
"""

CLEAN_OR_SINGLE_EXCLUSION = ("get_claim", "search_policy", "compute_payout")
MISSING_OR_UNCLEAR = ("get_claim",)

EXPECTED = {
    "CLM-2026-00001": {CLEAN_OR_SINGLE_EXCLUSION},
    "CLM-2026-00002": {CLEAN_OR_SINGLE_EXCLUSION},
    "CLM-2026-00003": {CLEAN_OR_SINGLE_EXCLUSION},
    "CLM-2026-00004": {CLEAN_OR_SINGLE_EXCLUSION},
    "CLM-2026-00005": {CLEAN_OR_SINGLE_EXCLUSION},
    "CLM-2026-00006": {                                               # ALTERNATE PATH CASE
        CLEAN_OR_SINGLE_EXCLUSION,                                    # one combined search
        ("get_claim", "search_policy", "search_policy", "compute_payout"),  # two separate searches
    },
    "CLM-2026-00007": {MISSING_OR_UNCLEAR},
    "CLM-2026-00008": {MISSING_OR_UNCLEAR},
    "CLM-2026-00009": {MISSING_OR_UNCLEAR},
    "CLM-2026-00010": {CLEAN_OR_SINGLE_EXCLUSION},
}

# steps NEEDED for step-efficiency: the length of the SHORTEST valid sequence for that claim
STEPS_NEEDED = {claim_id: min(len(seq) for seq in seqs) for claim_id, seqs in EXPECTED.items()}
