"""
THE ONE COMMAND.  Runs every case in eval_set.jsonl through the app, applies the assertions,
applies the judge, and prints the pass rate BY MODE (not just one overall number).

    python scripts/run_eval.py                  # judge = judge_v2.txt if it exists, else judge_v1.txt
    python scripts/run_eval.py --no-judge       # assertions only, no judge calls
    python scripts/run_eval.py | tee eval_table.txt     # also save the table as evidence

A case PASSES only if every assertion passes AND the judge says PASS.
This calls the app the way production does (score gate ON), so the M2 threshold bug shows up here.
It does NOT write to traces.jsonl, so your real Week 5 traces stay untouched.
"""

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from search import search_unfiltered                                   # noqa: E402
from generate import answer_question, build_context, MIN_SCORE          # noqa: E402
from checks import run_assertions, judge, ASSERTION_NAMES, JUDGED_CRITERIA  # noqa: E402

EVAL_SET = ROOT / "eval_set.jsonl"
TRACES = ROOT / "traces.jsonl"
OUT = ROOT / "eval_run.json"

MODE_NAMES = {
    "M1": "generation backend unavailable (403)",
    "M2": "refusal threshold wrongly refuses",
    "M3": "correct refusal (not in corpus)",
    "M4": "reranker ranks wrong chunk first",
    "M5": "typo / informal phrasing",
    "M6": "compound question",
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def answer_with_retry(question, retrieved):
    """Calls the app; waits and retries if the free-tier rate limit (15/min) is hit."""
    for _ in range(6):
        try:
            result = answer_question(question, retrieved)
            if retrieved and retrieved[0]["score"] >= MIN_SCORE:   # a real Gemini call was made
                time.sleep(4.5)
            return result
        except Exception as exc:  # noqa: BLE001
            if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                print("  (rate limit hit, waiting 30s...)", file=sys.stderr)
                time.sleep(30)
            else:
                raise
    raise RuntimeError("still rate-limited after 6 tries")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default=None, help="judge prompt file (default: judge_v2.txt if present, else judge_v1.txt)")
    parser.add_argument("--no-judge", action="store_true", help="assertions only")
    args = parser.parse_args()

    cases = read_jsonl(EVAL_SET)
    traces = {t["trace_id"]: t for t in read_jsonl(TRACES)}

    # Regression cases must be replayed VERBATIM from the real trace -> verify, don't trust.
    for c in cases:
        if c["regression"]:
            trace = traces.get(c["trace_id"])
            if trace is None or trace["question"] != c["question"]:
                sys.exit(f"Regression case {c['id']} does not match its trace {c['trace_id']} word for word.")

    prompt_text, prompt_name = None, None
    if not args.no_judge:
        prompt_name = args.prompt or ("judge_v2.txt" if (ROOT / "judge_v2.txt").exists() else "judge_v1.txt")
        prompt_text = (ROOT / prompt_name).read_text(encoding="utf-8")

    results = []
    for n, case in enumerate(cases, start=1):
        trace = traces.get(case["trace_id"])
        strategy = trace["strategy"] if case["regression"] else "naive"
        top_k = trace["top_k"] if case["regression"] else 5

        retrieved = search_unfiltered(case["question"], strategy=strategy, top_k=top_k)
        answer, error = None, None
        try:
            answer = answer_with_retry(case["question"], retrieved)["answer"]
        except Exception as exc:  # noqa: BLE001
            error = str(exc)

        checks = run_assertions(case["expect"], answer, [r["chunk_id"] for r in retrieved], error)

        verdict, reason = None, None
        if prompt_text and answer and not error:
            try:
                verdict, reason = judge(prompt_text, case["question"], build_context(retrieved), answer)
            except Exception as exc:  # noqa: BLE001
                verdict, reason = "ERROR", str(exc)[:150]

        judge_ok = verdict is None or verdict == "PASS"
        passed = all(checks.values()) and judge_ok
        results.append({
            "id": case["id"], "mode": case["mode"], "regression": case["regression"],
            "question": case["question"], "expect": case["expect"],
            "answer": answer, "error": error,
            "assertions": checks, "judge_verdict": verdict, "judge_reason": reason,
            "passed": passed,
        })
        print(f"[{n:2}/{len(cases)}] {case['mode']} {'PASS' if passed else 'FAIL'}  {case['question'][:60]}", file=sys.stderr)

    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    by_mode = defaultdict(list)
    for r in results:
        by_mode[r["mode"]].append(r)

    print("\n" + "=" * 84)
    print(f"{'MODE':<5} {'WHAT':<38} {'CASES':>5} {'PASSED':>7} {'PASS RATE':>10}")
    print("-" * 84)
    for mode in sorted(by_mode):
        rows = by_mode[mode]
        ok = sum(r["passed"] for r in rows)
        print(f"{mode:<5} {MODE_NAMES.get(mode, ''):<38} {len(rows):>5} {ok:>7} {100 * ok / len(rows):>9.1f}%")
    print("-" * 84)
    total_ok = sum(r["passed"] for r in results)
    print(f"{'ALL':<5} {'(one number hides the modes above)':<38} {len(results):>5} {total_ok:>7} {100 * total_ok / len(results):>9.1f}%")
    print("=" * 84)

    reg = [r for r in results if r["regression"]]
    print(f"regression cases (replayed verbatim from real failed traces): {sum(r['passed'] for r in reg)}/{len(reg)} pass")
    print(f"assertions: {len(ASSERTION_NAMES)}  |  judged criteria: {len(JUDGED_CRITERIA)}   ({', '.join(ASSERTION_NAMES)} | {', '.join(JUDGED_CRITERIA)})")
    print(f"judge prompt: {prompt_name or 'none (--no-judge)'}")

    print("\nFailures:")
    for r in results:
        if r["passed"]:
            continue
        why = [name for name, ok in r["assertions"].items() if not ok]
        if r["judge_verdict"] not in (None, "PASS"):
            why.append(f"judge={r['judge_verdict']}")
        if r["error"]:
            why.append(f"error: {r['error'][:60]}")
        print(f"  case {r['id']:2} [{r['mode']}] {', '.join(why)}")
    print(f"\nFull detail saved to {OUT.name}")


if __name__ == "__main__":
    main()
