# Week 5 — taxonomy.md

| # | Mode | Count | Freq % | Severity | Example trace_id |
|---|---|---|---|---|---|
| 1 | Generation backend totally unavailable (403 permission error) even when retrieval succeeded well | 7 | 35% | **High — wrongly denies via total non-response**; the adjuster gets nothing at all, even when the system found the exact right clause | `47118233-efcf-4361-b54f-a48682e6006c` |
| 2 | Refusal-threshold miscalibrated for the post-rerank score scale, so directly-answerable questions get refused | 4 | 20% | **High — wrongly denies**; the correct chunk is sitting at rank 1 and the system still says it doesn't have the information | `ebed9bc7-e2bb-44f6-a443-a6c98a5a2d06` |
| 3 | Correct refusal on genuinely out-of-corpus questions (not a failure — included as baseline) | 3 | 15% | **None — working as intended** | `ee4f1077-bd93-44ea-9b8d-d1d0e5615916` |
| 4 | Reranker places a topically-adjacent but wrong chunk above the actually-correct one | 2 | 10% | **High — risk of a plausible-but-wrong answer** if generation had succeeded, since the wrong chunk is what would have reached the model | `022aac3f-3391-4e6e-958d-bf6737221fbe` |
| 5 | Informal/typo'd phrasing depresses cross-encoder scores far more than clean phrasing of the same question, even when the same chunk is retrieved | 2 | 10% | **Merely annoys the adjuster** — same chunk found, just scored lower, pushing borderline cases further into refusal | `8783507d-8044-4a7e-bd4f-46703b3f3f01` |
| 6 | Compound/multi-part questions produce diffuse, uniformly weak scores across every candidate | 2 | 10% | **Merely annoys the adjuster** — forces asking one thing at a time rather than producing a wrong answer | `0b552a76-0fc2-465f-a6bc-14b1d1b9e651` |

**Top mode by frequency: #1, generation backend outage (35%).** This is an infrastructure failure (a 403'd Gemini project), not a retrieval or prompt-quality problem — worth noting explicitly since it would be easy to misdiagnose as a model-quality issue.

**Top mode by severity if generation is excluded: #2, threshold miscalibration (20%)** — this is a code bug introduced by last week's retrieval change (cross-encoder rerank scores are unbounded logits, not 0-1 cosine similarities, and `MIN_SCORE = 0.35` was never updated for the new scale).