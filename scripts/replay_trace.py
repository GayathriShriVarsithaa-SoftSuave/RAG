"""
Replays ONE trace strictly from what's logged in traces.jsonl -- proves the
trace has everything needed to reconstruct the call. Shows original output
next to a fresh replayed output.

Run from the project root:
    python scripts/replay_trace.py                     # replays the first sampled trace_id
    python scripts/replay_trace.py --trace-id <uuid>    # replays a specific one
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tracing import run_traced_query  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TRACES_PATH = ROOT / "traces.jsonl"
SAMPLED_PATH = ROOT / "sampled_trace_ids.json"


def load_traces():
    traces = {}
    with open(TRACES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                t = json.loads(line)
                traces[t["trace_id"]] = t
    return traces


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace-id", type=str, default=None)
    args = parser.parse_args()

    traces = load_traces()

    trace_id = args.trace_id
    if trace_id is None:
        sampled = json.loads(SAMPLED_PATH.read_text(encoding="utf-8"))
        trace_id = sampled["trace_ids"][0]

    original = traces.get(trace_id)
    if original is None:
        print(f"trace_id {trace_id} not found in traces.jsonl")
        sys.exit(1)

    print("=" * 90)
    print("ORIGINAL TRACE")
    print("=" * 90)
    print(json.dumps(original, indent=2))

    # Replay using ONLY what the trace logged: the question, strategy, top_k.
    # If anything needed to reconstruct this call weren't in the trace, this
    # is where you'd notice -- e.g. we do NOT log the exact prompt template
    # text itself, only a prompt_version string, so if that template ever
    # changes without bumping the version, a replay would silently use the
    # new template. Note that in your write-up as a real limitation.
    print("\n" + "=" * 90)
    print("REPLAYED (fresh call, same question/strategy/top_k from the trace)")
    print("=" * 90)
    replayed = run_traced_query(
        original["question"],
        strategy=original["strategy"],
        top_k=original["top_k"],
    )
    print(json.dumps(replayed, indent=2))

    print("\n" + "=" * 90)
    print("COMPARISON")
    print("=" * 90)
    print(f"original raw_output : {original['raw_output']!r}")
    print(f"replayed raw_output : {replayed['raw_output']!r}")
    print(f"original retrieved  : {[r['chunk_id'] for r in original['retrieved']]}")
    print(f"replayed retrieved  : {[r['chunk_id'] for r in replayed['retrieved']]}")
    print(f"original error      : {original['error']}")
    print(f"replayed error      : {replayed['error']}")


if __name__ == "__main__":
    main()