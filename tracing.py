"""
Minimal trace logging for Week 5 error analysis.

run_traced_query() runs one question through retrieval + generation and
writes ONE line to traces.jsonl with everything needed to replay it later
from the trace alone: prompt_version, retrieved chunk_ids + scores,
model + params, and the raw output.

It never raises: if generation fails (e.g. a broken API key), that failure
is captured IN the trace as an `error` field instead of crashing the
caller -- a broken generation call is itself a real thing you want visible
in your sample this week, not something to hide by retrying until it works.

Note on redaction: this corpus (a product PRD) never contains claimant
names or claim numbers to begin with, so `redacted_before_write` is
trivially true here. In a real deployment with actual claimant data, this
is exactly where you would strip/hash identifiers before the write, not
after.
"""

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from search import search_unfiltered
from generate import answer_question, GEMINI_MODEL, MIN_SCORE

PROMPT_VERSION = "v1-hard-refusal-min-score-0.35"
TRACE_LOG_PATH = Path(__file__).resolve().parent / "traces.jsonl"


def log_trace(record: dict) -> None:
    with open(TRACE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def run_traced_query(question: str, strategy: str = "naive", top_k: int = 5) -> dict:
    trace_id = str(uuid.uuid4())
    started = time.perf_counter()

    retrieved = search_unfiltered(question, strategy=strategy, top_k=top_k)
    retrieved_summary = [{"chunk_id": r["chunk_id"], "score": r["score"]} for r in retrieved]

    error = None
    result = None
    try:
        result = answer_question(question, retrieved)
    except Exception as exc:  # noqa: BLE001 -- goes IN the trace, not raised
        error = str(exc)

    latency_ms = round((time.perf_counter() - started) * 1000, 2)

    record = {
        "trace_id": trace_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "redacted_before_write": True,  # see module docstring
        "prompt_version": PROMPT_VERSION,
        "strategy": strategy,
        "top_k": top_k,
        "model": GEMINI_MODEL,
        "params": {"min_score": MIN_SCORE},
        "retrieved": retrieved_summary,
        "raw_output": result.get("answer") if result else None,
        "refused": result.get("refused") if result else None,
        "grounded": result.get("grounded") if result else None,
        "error": error,
        "latency_ms": latency_ms,
    }
    log_trace(record)
    return record