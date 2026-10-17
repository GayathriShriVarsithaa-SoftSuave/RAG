# canary_rollback.md

Canary: ship v2 to 5% of claim-triage traffic for 24h; promote to 100% only if the
v2 slice's eval suite stays 9/9 and its p99 search_policy call count stays <=2 laps.
Rollback: if either check fails, flip PROMPT_VERSION back to v1 in claim_llm.py and redeploy -
no data migration needed since the fix is prompt-only, not a schema or retrieval-index change.
