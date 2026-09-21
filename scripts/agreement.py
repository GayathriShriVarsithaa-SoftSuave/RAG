"""
Steps 2-4: run the judge on your 25 hand labels and measure agreement.

    python scripts/agreement.py --prompt judge_v1.txt                   # -> agreement BEFORE
    python scripts/agreement.py --prompt judge_v1.txt --make-v2 3 17    # builds judge_v2.txt from 2 of v1's own disagreements
    python scripts/agreement.py --prompt judge_v2.txt                   # -> agreement AFTER

Two safety gates:
  * The judge will NOT run unless labels_25.json is already committed in git and unchanged.
  * judge_v2.txt will NOT be built unless prediction.txt is already committed.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from checks import judge  # noqa: E402

LABELS_PATH = ROOT / "labels_25.json"
ANSWERS_PATH = ROOT / "answers_to_label.json"
PREDICTION_PATH = ROOT / "prediction.txt"
V2_PATH = ROOT / "judge_v2.txt"


def git(*args) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def require_committed(path: Path):
    """Exits unless the file is committed and unchanged. Returns (commit_hash, commit_time)."""
    name = path.name
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", name],
                             cwd=ROOT, capture_output=True).returncode == 0
    if not tracked or git("status", "--porcelain", "--", name):
        sys.exit(f"STOP: {name} is not committed (or has changes since its last commit).\n"
                 f'Commit it first:   git add {name}  &&  git commit -m "add {name}"')
    commit, when = git("log", "-1", "--format=%H|%cI", "--", name).split("|")
    return commit, when


def load_labels(answers):
    labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    bad = [k for k, v in labels.items() if v not in ("PASS", "FAIL")]
    if bad:
        sys.exit(f'labels_25.json still has non-PASS/FAIL values for ids: {bad}')
    if set(labels) != {str(a["id"]) for a in answers}:
        sys.exit("labels_25.json ids do not match the ids in answers_to_label.json")
    return labels


def is_refusal(text: str) -> bool:
    return text.strip().upper().startswith("REFUSE")


def example_ids_in(prompt_text: str) -> list[int]:
    m = re.search(r"EXAMPLE_IDS:\s*([\d,\s]+)", prompt_text)
    return [int(x) for x in re.findall(r"\d+", m.group(1))] if m else []


def pct(matches: int, total: int) -> float:
    return round(100 * matches / total, 1) if total else 0.0


def run_measurement(prompt_path: Path):
    answers = json.loads(ANSWERS_PATH.read_text(encoding="utf-8"))

    labels_commit, labels_time = require_committed(LABELS_PATH)
    require_committed(ANSWERS_PATH)
    labels = load_labels(answers)

    prompt_text = prompt_path.read_text(encoding="utf-8")
    items = []
    for a in answers:
        try:
            verdict, reason = judge(prompt_text, a["question"], a["context"], a["answer"])
        except Exception as exc:  # noqa: BLE001
            sys.exit(f"Judge call failed on case {a['id']}: {exc}")
        human = labels[str(a["id"])]
        items.append({
            "id": a["id"], "human": human, "judge": verdict, "reason": reason,
            "agree": verdict == human, "is_refusal": is_refusal(a["answer"]),
        })
        print(f"  judged case {a['id']:2}: human={human} judge={verdict}")

    run_at = datetime.now(timezone.utc)
    matches = sum(i["agree"] for i in items)
    total = len(items)

    non_ref = [i for i in items if not i["is_refusal"]]
    ex_ids = example_ids_in(prompt_text)
    held_out = [i for i in items if i["id"] not in ex_ids]

    summary = {
        "prompt_file": prompt_path.name,
        "labels_commit": labels_commit,
        "labels_committed_at": labels_time,
        "judge_run_at": run_at.isoformat(),
        "agreement_pct": pct(matches, total),
        "matches": matches,
        "total": total,
        "agreement_pct_non_refusal_only": pct(sum(i["agree"] for i in non_ref), len(non_ref)),
        "few_shot_example_ids": ex_ids,
        "agreement_pct_excluding_examples": pct(sum(i["agree"] for i in held_out), len(held_out)),
        "items": items,
    }
    out_path = ROOT / f"judge_run_{prompt_path.stem}.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    ordering_ok = datetime.fromisoformat(labels_time) < run_at
    answers_by_id = {a["id"]: a for a in answers}

    print("\n" + "=" * 78)
    print(f"judge prompt        : {prompt_path.name}")
    print(f"labels committed    : {labels_commit[:8]}  at {labels_time}")
    print(f"judge run at        : {run_at.isoformat()}   ->  labels came first: {'YES' if ordering_ok else 'NO (!!)'}")
    print(f"AGREEMENT           : {matches}/{total} = {summary['agreement_pct']}%")
    print(f"  non-REFUSE only   : {summary['agreement_pct_non_refusal_only']}%   (refusals are easy PASSes, so this is the harder number)")
    if ex_ids:
        print(f"  excluding few-shot examples {ex_ids}: {summary['agreement_pct_excluding_examples']}%   (the honest number: those {len(ex_ids)} were shown to the judge)")
    print("=" * 78)

    disagreements = [i for i in items if not i["agree"]]
    print(f"\nDisagreements ({len(disagreements)}):")
    for i in disagreements:
        a = answers_by_id[i["id"]]
        print(f"\n  case {i['id']}: human={i['human']}  judge={i['judge']}")
        print(f"    Q: {a['question'][:100]}")
        print(f"    A: {a['answer'][:200]!r}")
        print(f"    judge's reason: {i['reason']}")

    v1_file = ROOT / "judge_run_judge_v1.json"
    if prompt_path.stem != "judge_v1" and v1_file.exists():
        before = json.loads(v1_file.read_text(encoding="utf-8"))["agreement_pct"]
        print(f"\nagreement_before -> agreement_after :  {before}%  ->  {summary['agreement_pct']}%")

    print(f"\nSaved {out_path.name}. Commit it as your evidence.")


def make_v2(base_prompt_path: Path, ids: list[int]):
    run_file = ROOT / f"judge_run_{base_prompt_path.stem}.json"
    if not run_file.exists():
        sys.exit(f"Run the judge on {base_prompt_path.name} first (no {run_file.name} yet).")
    if V2_PATH.exists():
        sys.exit("judge_v2.txt already exists. Delete it on purpose if you want to rebuild it.")

    if not PREDICTION_PATH.exists() or not PREDICTION_PATH.read_text(encoding="utf-8").strip():
        sys.exit("Write prediction.txt first: ONE sentence saying what the iteration will fix.")
    pred_commit, pred_time = require_committed(PREDICTION_PATH)

    run = json.loads(run_file.read_text(encoding="utf-8"))
    disagree = {i["id"]: i for i in run["items"] if not i["agree"]}
    for case_id in ids:
        if case_id not in disagree:
            sys.exit(f"case {case_id} is not one of the judge's own disagreements. Pick from: {sorted(disagree)}")

    answers = {a["id"]: a for a in json.loads(ANSWERS_PATH.read_text(encoding="utf-8"))}
    base_text = base_prompt_path.read_text(encoding="utf-8").rstrip()

    parts = [
        base_text,
        "",
        f"EXAMPLE_IDS: {', '.join(str(i) for i in ids)}",
        "",
        "Below are real cases where an earlier version of this judge got it wrong.",
        "The human verdict is the correct one. Learn from them.",
    ]
    for n, case_id in enumerate(ids, start=1):
        a, d = answers[case_id], disagree[case_id]
        print(f"\n--- case {case_id} ---")
        print(f"Q: {a['question']}")
        print(f"A: {a['answer']}")
        print(f"human said {d['human']}, judge said {d['judge']} because: {d['reason']}")
        why = input(f"In ONE sentence, why is the human ({d['human']}) right? > ").strip()
        parts += [
            "",
            f"--- EXAMPLE {n} ---",
            "EXCERPTS:", a["context"], "",
            f"QUESTION: {a['question']}", "",
            "ANSWER:", a["answer"], "",
            "CORRECT OUTPUT:",
            f"VERDICT: {d['human']}",
            f"REASON: {why}",
        ]

    V2_PATH.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"\nWrote judge_v2.txt  (prediction was committed {pred_commit[:8]} at {pred_time}, before this).")
    print("See what changed:   diff judge_v1.txt judge_v2.txt")
    print("Now measure it:     python scripts/agreement.py --prompt judge_v2.txt")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True, help="judge_v1.txt or judge_v2.txt")
    parser.add_argument("--make-v2", nargs=2, type=int, metavar=("ID1", "ID2"),
                        help="build judge_v2.txt from 2 of the judge's own disagreements")
    args = parser.parse_args()

    prompt_path = ROOT / args.prompt
    if not prompt_path.exists():
        sys.exit(f"{args.prompt} not found in the project root")

    if args.make_v2:
        make_v2(prompt_path, args.make_v2)
    else:
        run_measurement(prompt_path)


if __name__ == "__main__":
    main()
