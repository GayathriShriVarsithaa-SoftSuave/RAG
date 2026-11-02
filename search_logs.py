"""
Week 11 - search request_logs.jsonl by time / user / prompt_version / input_type / cost outlier,
and by free text across BOTH the input notes AND the output decision text (the complaint
describes the OUTPUT - so output must be searchable too, not just input).

Examples:
    python search_logs.py --decision COVERED --text water
    python search_logs.py --since 2026-10-12T14:00 --until 2026-10-12T18:00
    python search_logs.py --cost-outliers 3
    python search_logs.py --user adjuster.patel
    python search_logs.py --prompt-version v2
    python search_logs.py --trace-id <id>          # once you've found a candidate, see everything
"""
import argparse
import json


def load(path="request_logs.jsonl"):
    return [json.loads(line) for line in open(path) if line.strip()]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--since")
    p.add_argument("--until")
    p.add_argument("--user")
    p.add_argument("--prompt-version")
    p.add_argument("--input-type")
    p.add_argument("--decision")
    p.add_argument("--text", help="search input_notes AND output_text, case-insensitive")
    p.add_argument("--cost-outliers", type=int, help="show the top N most expensive requests")
    p.add_argument("--trace-id", help="show the full record for one trace_id")
    args = p.parse_args()

    logs = load()

    if args.trace_id:
        logs = [r for r in logs if r["trace_id"].startswith(args.trace_id)]
        print(json.dumps(logs[0], indent=2) if logs else "not found")
        return

    if args.cost_outliers:
        logs = sorted(logs, key=lambda r: -r["total_cost_usd"])[:args.cost_outliers]
    if args.since:
        logs = [r for r in logs if r["timestamp"] >= args.since]
    if args.until:
        logs = [r for r in logs if r["timestamp"] <= args.until]
    if args.user:
        logs = [r for r in logs if r["user"] == args.user]
    if args.prompt_version:
        logs = [r for r in logs if r["prompt_version"] == args.prompt_version]
    if args.input_type:
        logs = [r for r in logs if r["input_type"] == args.input_type]
    if args.decision:
        logs = [r for r in logs if r["output_decision"] == args.decision]
    if args.text:
        needle = args.text.lower()
        logs = [r for r in logs if needle in r["input_notes"].lower() or needle in r["output_text"].lower()]

    print(f"{len(logs)} matching log(s)\n")
    for r in logs:
        print(f"trace_id={r['trace_id'][:8]}  {r['timestamp']}  user={r['user']}  "
              f"prompt={r['prompt_version']}  claim={r['claim_id']}  decision={r['output_decision']}  "
              f"cost=${r['total_cost_usd']:.5f}")
        print(f"  notes: {r['input_notes'][:90]}")
        print(f"  output: {r['output_text']}")
        print()


if __name__ == "__main__":
    main()
