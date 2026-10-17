"""
Week 11 - once you've found the trace_id, this writes trace.json: per-span latency/tokens/cost,
prompt version, and retrieved context ids, in the exact shape the submission checklist wants.

    python extract_trace.py <trace_id>
"""
import json
import sys


def main():
    trace_id = sys.argv[1]
    logs = [json.loads(line) for line in open("request_logs.jsonl") if line.strip()]
    matches = [r for r in logs if r["trace_id"].startswith(trace_id)]
    if not matches:
        sys.exit(f"no trace found starting with {trace_id}")
    if len(matches) > 1:
        sys.exit(f"ambiguous prefix, matches {len(matches)} traces - use more characters")
    record = matches[0]

    trace = {
        "trace_id": record["trace_id"],
        "timestamp": record["timestamp"],
        "user": record["user"],
        "prompt_version": record["prompt_version"],
        "input_type": record["input_type"],
        "claim_id": record["claim_id"],
        "input_notes": record["input_notes"],
        "retrieved_context_ids": record["retrieved_context_ids"],
        "spans": record["spans"],
        "total_tokens": record["total_tokens"],
        "total_cost_usd": record["total_cost_usd"],
        "total_latency_ms": record["total_latency_ms"],
        "output_decision": record["output_decision"],
        "output_exclusion_id": record["output_exclusion_id"],
        "output_payable_amount": record["output_payable_amount"],
        "output_text": record["output_text"],
    }
    with open("trace.json", "w") as f:
        json.dump(trace, f, indent=2)
    print(json.dumps(trace, indent=2))
    print("\nSaved trace.json")


if __name__ == "__main__":
    main()
