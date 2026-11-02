"""
Week 11 - builds a day of SYNTHETIC historical request logs (not live Gemini calls - this is
background/noise data for the search drill) plus ONE planted bad coverage answer, matching
exactly what the real system would produce for claim CLM-2026-00011 today (verified: the
keyword miss is real, see Step 1).

Run once. Writes request_logs.jsonl. Keeps the planted trace_id in plant_answer.txt - DO NOT
open this until after you've found it yourself and want to check your time.
"""
import json
import random
import uuid
from datetime import datetime, timedelta

random.seed(7)

USERS = ["adjuster.chen", "adjuster.patel", "adjuster.osei", "adjuster.reyes", "adjuster.khan"]
DAY = datetime(2026, 10, 12, 8, 0, 0)  # "yesterday"

CLAIMS_FOR_LOGS = [
    ("CLM-2026-00001", "Kitchen pipe burst overnight. Plumber confirmed a failed joint on a two-year-old fitting.", "COVERED", None, 3700.0),
    ("CLM-2026-00002", "Burglary while the family was at work. Rear window forced, laptop and jewellery taken.", "COVERED", None, 2750.0),
    ("CLM-2026-00003", "Kitchen fire from an overheated pan. Fire brigade attended. Smoke damage only.", "COVERED", None, 11000.0),
    ("CLM-2026-00004", "The river overflowed after three days of rain. Ground floor flooded to 30cm.", "EXCLUDED", "EXC-01", 0.0),
    ("CLM-2026-00005", "Ceiling stains spreading for years, roof tiles old and worn out.", "EXCLUDED", "EXC-02", 0.0),
    ("CLM-2026-00006", "Pipe burst upstairs, water through the lounge ceiling. House vacant since March.", "EXCLUDED", "EXC-04", 0.0),
    ("CLM-2026-00010", "Fire in the spare room. Owner runs an online shop; stock destroyed.", "EXCLUDED", "EXC-05", 0.0),
]

SPAN_NAMES = ["get_claim", "search_policy", "compute_payout", "generation"]


def make_spans(cost_multiplier=1.0):
    spans = []
    total_tokens = total_cost = total_latency = 0
    for name in SPAN_NAMES:
        latency_ms = random.randint(300, 1800)
        tok_in = random.randint(500, 900)
        tok_out = random.randint(15, 60)
        cost = round((tok_in / 1_000_000 * 0.25 + tok_out / 1_000_000 * 1.50) * cost_multiplier, 6)
        spans.append({"span": name, "latency_ms": latency_ms, "tokens_in": tok_in, "tokens_out": tok_out, "cost_usd": cost})
        total_tokens += tok_in + tok_out
        total_cost += cost
        total_latency += latency_ms
    return spans, total_tokens, round(total_cost, 6), total_latency


def log_entry(claim_id, notes, decision, exclusion_id, payable, ts, user, prompt_version,
             input_type="claim_triage", cost_multiplier=1.0, retrieved_ids=None):
    spans, tokens, cost, latency = make_spans(cost_multiplier)
    return {
        "trace_id": str(uuid.uuid4()),
        "timestamp": ts.isoformat(),
        "user": user,
        "prompt_version": prompt_version,
        "input_type": input_type,
        "claim_id": claim_id,
        "input_notes": notes,
        "retrieved_context_ids": retrieved_ids or [],
        "output_decision": decision,
        "output_exclusion_id": exclusion_id,
        "output_payable_amount": payable,
        "output_text": (f"Based on the adjuster notes, this claim is {decision.lower()}"
                        + (f" under exclusion {exclusion_id}." if exclusion_id else
                           f"; the payable amount is ${payable:,.2f}.")),
        "spans": spans,
        "total_tokens": tokens,
        "total_cost_usd": cost,
        "total_latency_ms": latency,
    }


logs = []
t = DAY

for i in range(55):
    claim_id, notes, correct_decision, correct_exc, correct_payable = random.choice(CLAIMS_FOR_LOGS)
    user = random.choice(USERS)
    prompt_version = "v1" if t.hour < 15 else "v2"   # v2 "shipped" mid-afternoon
    t += timedelta(minutes=random.randint(4, 14))
    retrieved = [correct_exc] if correct_exc else []
    logs.append(log_entry(claim_id, notes, correct_decision, correct_exc, correct_payable, t, user, prompt_version, retrieved_ids=retrieved))

# one real cost OUTLIER - a run that looped hunting a non-existent exclusion - NOT the bug we want found
outlier = log_entry("CLM-2026-00003", CLAIMS_FOR_LOGS[2][1], "COVERED", None, 11000.0,
                    DAY + timedelta(hours=5, minutes=12), "adjuster.reyes", "v1", cost_multiplier=9.0)
logs.append(outlier)

# the PLANTED bad entry - matches exactly what the real buggy retrieval produces today
bad_ts = DAY + timedelta(hours=6, minutes=47)
bad_entry = log_entry("CLM-2026-00011",
                      "The creek behind the property burst its banks after two days of heavy rain and water poured across the ground floor, ruining the flooring and furniture.",
                      "COVERED", None, 11200.0, bad_ts, "adjuster.patel", "v2", retrieved_ids=[])
planted_trace_id = bad_entry["trace_id"]
logs.append(bad_entry)

random.shuffle(logs)
with open("request_logs.jsonl", "w") as f:
    for entry in logs:
        f.write(json.dumps(entry) + "\n")

with open("plant_answer.txt", "w") as f:
    f.write(f"planted trace_id: {planted_trace_id}\nclaim: CLM-2026-00011\nbug: search_policy keywords miss 'creek'/'burst its banks'\n")

print(f"Wrote {len(logs)} log entries to request_logs.jsonl")
print("(answer key written to plant_answer.txt - don't peek until you've timed yourself)")
