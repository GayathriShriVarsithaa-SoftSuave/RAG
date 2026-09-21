"""
Week 7 - ONE shared way to call Gemini. The agent AND the workflow both use it, so they use the
same model, the same token counting and the same cost formula.
"""

import json
import re
import time

from generate import _client, GEMINI_MODEL   # your existing Gemini client + model name

# $ per 1 million tokens for gemini-3.1-flash-lite. CHECK https://ai.google.dev/gemini-api/docs/pricing
# and edit if the page says something different. (Thinking tokens are billed as output.)
INPUT_PRICE_PER_M = 0.25
OUTPUT_PRICE_PER_M = 1.50

# Free tier = 15 calls per minute. We pause after each call so we stay under it.
# This pause is NOT counted in latency.
PAUSE_SECONDS = 4.5

# The rules and the answer format are IDENTICAL for the agent and the workflow.
RULES = """Rules:
- Read the claim's adjuster notes to find the cause of loss and any unusual condition (for example vacancy or business use).
- Check the policy exclusions that could apply. An exclusion applies only if it really matches what the notes describe.
- If the claim cannot be found, the notes are empty, or the notes say the cause is not yet determined, the decision is NEEDS_INFO.
- If the decision is EXCLUDED, payable_amount is 0. If COVERED, payable_amount is the loss amount minus the excess (never below 0)."""

OUTPUT_CONTRACT = """Reply with ONLY this JSON object and nothing else:
{"claim_id": "CLM-YYYY-NNNNN", "decision": "COVERED" or "EXCLUDED" or "NEEDS_INFO", "exclusion_id": "EXC-xx" or null, "payable_amount": a number}"""

DECISIONS = ("COVERED", "EXCLUDED", "NEEDS_INFO")


def cost_of(tokens_in, tokens_out):
    return tokens_in / 1_000_000 * INPUT_PRICE_PER_M + tokens_out / 1_000_000 * OUTPUT_PRICE_PER_M


def call_llm(contents, config):
    """Returns (response, seconds, tokens_in, tokens_out). Waits and retries if rate-limited."""
    for _ in range(6):
        start = time.perf_counter()
        try:
            response = _client().models.generate_content(model=GEMINI_MODEL, contents=contents, config=config)
        except Exception as exc:  # noqa: BLE001
            if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                print("  (rate limit hit, waiting 30s ...)")
                time.sleep(30)
                continue
            raise
        seconds = time.perf_counter() - start
        usage = response.usage_metadata
        tokens_in = usage.prompt_token_count or 0
        tokens_out = max((usage.total_token_count or 0) - tokens_in, 0)   # includes thinking tokens
        time.sleep(PAUSE_SECONDS)
        return response, seconds, tokens_in, tokens_out
    raise RuntimeError("still rate-limited after 6 tries")


def parse_json(text):
    """Finds the first {...} in the model's text and loads it. Returns None if it can't."""
    match = re.search(r"\{.*\}", text or "", re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def normalise(answer, claim_id):
    """Turns the model's JSON into the exact output contract, or None if it is not valid."""
    if not isinstance(answer, dict):
        return None
    decision = str(answer.get("decision", "")).upper()
    if decision not in DECISIONS:
        return None
    try:
        payable = round(float(answer.get("payable_amount", 0)), 2)
    except (TypeError, ValueError):
        return None
    exclusion = answer.get("exclusion_id")
    exclusion = None if str(exclusion).strip().lower() in ("", "none", "null") else str(exclusion).strip()
    return {"claim_id": claim_id, "decision": decision, "exclusion_id": exclusion, "payable_amount": payable}
