# Week 5 — notes.md

## Seeded random sample

seed = 42
population size = 27 traces (traces.jsonl)
sample size = 20

| trace_id | question |
|---|---|
| e62f5bfd-8022-4002-81c6-4c9d42452519 | wat divices does neurora capture intergrate with for eye tracking |
| 287f0226-0667-4253-b0d2-ce0624e53b38 | Would a participant be able to get unrestricted, unsupervised access to someone else's raw biometric recordings? |
| ebed9bc7-e2bb-44f6-a443-a6c98a5a2d06 | Does this platform ingest raw vehicle CAN-bus or ECU data as part of its normal operation? |
| 2fcf1ee2-1837-46c6-ad70-8a9104507ecd | What form number and version does this PRD document carry? |
| dc987d4e-484a-4abb-be11-38526798b913 | In the end-to-end Neurora workflow, what does a trainer do first, before any device is connected? |
| 4377f098-b536-4515-9719-36d05ee871e9 | What kind of access does a participant get through Neurora Selfview, and is it a full raw-data analytics view? |
| 08739f90-bc60-4168-8707-902b9fb4ed88 | is lane detction curently enabled in teh product |
| 022aac3f-3391-4e6e-958d-bf6737221fbe | Is lane detection or tracking a feature that is actively working right now in the shipped product? |
| 1b127ddc-ff76-449e-94c5-e58eeded5a23 | Is real-time collision intervention something this platform actually does? |
| 0b552a76-0fc2-465f-a6bc-14b1d1b9e651 | Does the platform support both autonomous driving and medical diagnosis features? |
| 125168d9-9f4c-4967-8fba-cb5e57f3da48 | Is the platform able to drive the vehicle itself or take over vehicle control? |
| ee4f1077-bd93-44ea-9b8d-d1d0e5615916 | Does Neurora offer a mobile app for iOS and Android? |
| b7fb839e-926d-4939-8271-719c61ce4a44 | How many exclusion codes are listed in the Exclusions Table? |
| 390a7cf3-51d3-4610-87b2-a8cca4340cc3 | What is the pricing for the enterprise tier of the Neurora platform? |
| 136f0b51-7169-4514-a3ef-3066a6a2db98 | Can the system step in to intervene and help a driver avoid a collision while it's happening? |
| 52203603-b0b9-47ac-b067-6ebfdb8bf4d4 | Is the biometric data encrypted, and who exactly is allowed to see it unencrypted? |
| 47118233-efcf-4361-b54f-a48682e6006c | According to the Claims Note, what should a trainer be able to trace an automated finding back to? |
| 8783507d-8044-4a7e-bd4f-46703b3f3f01 | can this thing drive the car by itself lol |
| 7066be1e-76d8-41ba-abfe-9100288d8c98 | Who is the CEO of the company that makes Neurora? |
| e5d8eab7-7a6f-4322-9f3d-c78315dc6137 | What access controls and security measures does the platform require for handling biometric data? |

## Redaction confirmation

This corpus (a product requirements document) never contains claimant names or claim numbers, so there is no identifier to strip. `tracing.py` writes `"redacted_before_write": true` on every record as a standing confirmation of this, checked at write time, not after — in a deployment with real claimant data, this is exactly where identifier stripping/hashing would happen before the `log_trace()` call, not as a later cleanup pass.

## Replay evidence

Replayed trace `e62f5bfd-8022-4002-81c6-4c9d42452519` using only the fields logged in the trace (question, strategy="naive", top_k=5). Result: identical retrieved chunk_ids, identical scores, identical raw_output ("REFUSE: ..."). Confirms the trace is fully replayable from itself.

One field the trace does NOT capture: the literal prompt template text, only a `prompt_version` string. If the template in `generate.py` (`SYSTEM_INSTRUCTION`) is edited without bumping `PROMPT_VERSION`, a replay would silently use the new template and look identical in the log — this is a known gap, not fixed here.

Replayed latency was much higher than the original (6.7s vs 429ms) because the cross-encoder model had to reload fresh in a new process — not a determinism issue.

## Open-coded observations (one sentence per trace, no diagnosis, no fix)

1. **e62f5bfd** — Typo'd version of the Capture-devices question retrieved the same chunk (naive:3) at rank 1 as the clean phrasing, with a positive score (0.14), but it was still below the 0.35 refusal cutoff, so the assistant refused anyway.
2. **287f0226** — Retrieval found a strong top match (naive:6, score 3.05) for the biometric-access question, well above the refusal cutoff, but the Gemini call failed with a 403 permission error before any answer was generated.
3. **ebed9bc7** — The CAN-bus/ECU question retrieved the chunk we know is correct (naive:14) at rank 1, but its score was negative (-0.95), and the assistant refused despite having the right content in hand.
4. **2fcf1ee2** — The form-number question retrieved a strong top match (naive:0, score 1.32) but generation failed with a 403 error, so no answer was produced despite good retrieval.
5. **dc987d4e** — The workflow-first-step question retrieved a very strong top match (naive:7, score 5.53) but generation again failed with a 403 error.
6. **4377f098** — The Selfview-access question retrieved a strong top match (naive:5, score 5.19) but generation failed with the same 403 error.
7. **08739f90** — The heavily typo'd version of the lane-detection question ("detction", "curently", "teh") retrieved only very low, negative scores across all 5 candidates (best -9.98) — noticeably worse than the same question asked cleanly — and was refused.
8. **022aac3f** — The clean lane-detection question retrieved naive:17 (the Claims Note chunk) at rank 1 instead of naive:15 (the chunk that actually discusses lane detection), which only appeared at rank 3 with a negative score, and the assistant refused.
9. **1b127ddc** — A rephrased collision-intervention question retrieved the chunk we know is correct (naive:14) at rank 1, but with a negative score (-2.74), and was refused.
10. **0b552a76** — The compound question about both autonomous driving and medical diagnosis retrieved only weak, negative scores across every candidate (best -4.66), and was refused.
11. **125168d9** — The autonomous-driving question retrieved naive:15 at rank 1 instead of naive:14 (the chunk that actually contains that exclusion row), with a negative score, and was refused.
12. **ee4f1077** — The mobile-app question, which is genuinely outside this PRD's content, retrieved only near-zero/negative scores and was refused.
13. **b7fb839e** — The exclusion-code-count question retrieved a positive top match (naive:14, score 1.16) but generation failed with a 403 error.
14. **390a7cf3** — The enterprise-pricing question, genuinely outside this PRD's content, retrieved only strongly negative scores and was refused.
15. **136f0b51** — The collision-avoidance question retrieved the chunk we know is correct (naive:14) at rank 1, but with a strongly negative score (-5.52) — more negative than the same chunk scored for question 9's phrasing — and was refused.
16. **52203603** — The compound question about biometric encryption and access retrieved naive:13 at rank 1 with a negative score (-3.17) and was refused.
17. **47118233** — The Claims-Note traceability question retrieved a very strong top match (naive:17, score 7.62) but generation failed with a 403 error.
18. **8783507d** — The casually-phrased "can this thing drive the car by itself lol" version of the autonomous-driving question retrieved the same chunk (naive:14) as the clean phrasing, but with a much more negative score (-11.05 vs -3.98 for the clean version), and was refused.
19. **7066be1e** — The CEO question, genuinely outside this PRD's content, retrieved only strongly negative scores and was refused.
20. **e5d8eab7** — The security-controls question retrieved a strong top match (naive:13, score 5.49) but generation failed with a 403 error.