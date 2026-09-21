"""
Week 6 - the two kinds of checks, in one small file.

1. ASSERTIONS  = plain Python/regex. Free, instant, never have a bad day.
2. JUDGE       = one LLM call for the ONE thing code can't check:
                 "is every claim in the answer supported by the excerpts?"

Used by scripts/run_eval.py and scripts/agreement.py.
"""

import re
import time
from pathlib import Path

from generate import _client, GEMINI_MODEL

ROOT = Path(__file__).resolve().parent
JUDGE_MODEL = GEMINI_MODEL  # change here if you want a different model as judge

# ---------------------------------------------------------------------------
# 1. Assertions (moved OUT of the judge prompt)
# ---------------------------------------------------------------------------
CITATION_RE = re.compile(r"\[chunk_id:\s*[^,\]]+,\s*clause:\s*[^\]]*\]")
EXCLUSION_CODE_RE = re.compile(r"\bE-\d{2}\b")
DENIAL_RE = re.compile(
    r"exclu\w*|not supported|out of scope|outside the active scope|currently disabled|not included",
    re.IGNORECASE,
)

ASSERTION_NAMES = [
    "refusal_matches_expectation",
    "has_citation",
    "cites_retrieved_chunk",
    "denial_cites_exclusion_code",
]


def is_refusal(answer: str) -> bool:
    return answer.strip().upper().startswith("REFUSE")


def run_assertions(expect: str, answer, retrieved_ids: list[str], error) -> dict:
    """Returns {assertion_name: True/False}. Assertions that don't apply are left out."""
    if error or not answer:
        return {"refusal_matches_expectation": False}

    refused = is_refusal(answer)
    results = {"refusal_matches_expectation": refused == (expect == "refuse")}

    if not refused:
        results["has_citation"] = bool(CITATION_RE.search(answer))
        results["cites_retrieved_chunk"] = any(cid in answer for cid in retrieved_ids)
        if DENIAL_RE.search(answer):
            results["denial_cites_exclusion_code"] = bool(EXCLUSION_CODE_RE.search(answer))
    return results


# ---------------------------------------------------------------------------
# 2. The judge (ONE binary criterion: faithful to the excerpts)
# ---------------------------------------------------------------------------
JUDGED_CRITERIA = ["faithful_to_excerpts"]

VERDICT_RE = re.compile(r"VERDICT:\s*(PASS|FAIL)", re.IGNORECASE)
REASON_RE = re.compile(r"REASON:\s*(.+)", re.IGNORECASE)


def judge(prompt_text: str, question: str, context: str, answer: str):
    """Returns (verdict, reason). verdict is 'PASS', 'FAIL' or 'UNPARSEABLE'."""
    user_message = f"EXCERPTS:\n{context}\n\nQUESTION: {question}\n\nANSWER:\n{answer}"
    response = None
    for attempt in range(6):
        try:
            response = _client().models.generate_content(
                model=JUDGE_MODEL,
                config={"system_instruction": prompt_text, "temperature": 0},
                contents=user_message,
            )
            break
        except Exception as exc:  # noqa: BLE001
            if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                print("  (rate limit hit, waiting 30s then retrying...)")
                time.sleep(30)
            else:
                raise
    if response is None:
        raise RuntimeError("still rate-limited after 6 tries")
    time.sleep(4.5)  # free tier allows 15 calls per minute, so pace ourselves
    text = (response.text or "").strip()
    verdict_match = VERDICT_RE.search(text)
    reason_match = REASON_RE.search(text)
    verdict = verdict_match.group(1).upper() if verdict_match else "UNPARSEABLE"
    reason = reason_match.group(1).strip() if reason_match else text[:200]
    return verdict, reason
