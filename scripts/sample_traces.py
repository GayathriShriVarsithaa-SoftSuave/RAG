"""
Draws a seeded random sample of 20 trace_ids from traces.jsonl -- not the
ones you remember, not the interesting-looking ones. Paste the printed seed
and trace_id list straight into notes.md as your documented sample.

Run from the project root:
    python scripts/sample_traces.py
    python scripts/sample_traces.py --seed 99   # to use a different seed
"""

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACES_PATH = ROOT / "traces.jsonl"

DEFAULT_SEED = 42
SAMPLE_SIZE = 20


def load_traces():
    traces = []
    with open(TRACES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                traces.append(json.loads(line))
    return traces


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    traces = load_traces()
    if len(traces) < SAMPLE_SIZE:
        print(f"Only {len(traces)} traces available, need at least {SAMPLE_SIZE}.")
        print("Run scripts/generate_traces.py again with more questions first.")
        sys.exit(1)

    rng = random.Random(args.seed)
    sample = rng.sample(traces, SAMPLE_SIZE)

    print(f"seed = {args.seed}")
    print(f"population size = {len(traces)}")
    print(f"sample size = {SAMPLE_SIZE}\n")
    print("Sampled trace_ids (paste this list into notes.md):\n")
    for t in sample:
        status = "ERROR" if t["error"] else ("REFUSED" if t["refused"] else "ANSWERED")
        print(f"  {t['trace_id']}  [{status:8}]  {t['question'][:60]}")

    out_path = ROOT / "sampled_trace_ids.json"
    out_path.write_text(
        json.dumps({"seed": args.seed, "trace_ids": [t["trace_id"] for t in sample]}, indent=2),
        encoding="utf-8",
    )
    print(f"\nAlso saved to {out_path} for scripts/replay_trace.py to use.")


if __name__ == "__main__":
    main()