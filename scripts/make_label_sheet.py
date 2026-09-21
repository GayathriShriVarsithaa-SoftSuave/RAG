"""
STEP 1 of the blind protocol. Makes the 25 answers you will label BY HAND.
The judge is NOT run here and never sees anything in this step.

Run from the project root:
    python scripts/make_label_sheet.py

Why the score gate is lifted here: the refusal threshold (taxonomy mode M2) makes the app refuse
almost everything, which would leave nothing to label. We raise the scores so the MODEL itself
decides whether to answer or refuse.
"""

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from search import search_unfiltered                      # noqa: E402
from generate import answer_question, build_context       # noqa: E402

EVAL_SET = ROOT / "eval_set.jsonl"
ANSWERS_OUT = ROOT / "answers_to_label.json"
SHEET_OUT = ROOT / "to_label.md"
LABELS_OUT = ROOT / "labels_25.json"

N_LABELS = 25
SEED = 42


def main():
    for path in (ANSWERS_OUT, SHEET_OUT, LABELS_OUT):
        if path.exists():
            sys.exit(f"STOP: {path.name} already exists. Delete it on purpose only if you really want to start over "
                     f"(new answers would make your old labels meaningless).")

    cases = [json.loads(line) for line in EVAL_SET.read_text(encoding="utf-8").splitlines() if line.strip()]
    sample = random.Random(SEED).sample(cases, N_LABELS)
    sample.sort(key=lambda c: c["id"])

    records = []
    for case in sample:
        retrieved = search_unfiltered(case["question"], strategy="naive", top_k=5)
        lifted = [dict(hit, score=1.0) for hit in retrieved]
        try:
            result = answer_question(case["question"], lifted)
        except Exception as exc:  # noqa: BLE001
            sys.exit(f"Generation failed on case {case['id']}: {exc}\n"
                     f"Fix the Gemini key/quota first (this is taxonomy mode M1), then run again.")
        records.append({
            "id": case["id"],
            "question": case["question"],
            "context": build_context(retrieved),
            "answer": result["answer"],
        })
        print(f"[{len(records):2}/{N_LABELS}] case {case['id']:2}  {result['answer'][:60]!r}")

    ANSWERS_OUT.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    LABELS_OUT.write_text(json.dumps({str(r["id"]): "TODO" for r in records}, indent=2), encoding="utf-8")

    lines = [
        "# Label these 25 answers BY HAND (do NOT run the judge first)",
        "",
        "Rule: **PASS** = every factual statement in the ANSWER is supported by the EXCERPTS shown.",
        "**FAIL** = at least one statement is not supported, is invented, or contradicts the excerpts.",
        'An answer that starts with "REFUSE:" makes no claims, so label it PASS.',
        "",
        'Write your labels in `labels_25.json` as "PASS" or "FAIL" for every id.',
        "",
    ]
    for r in records:
        lines += [
            f"## Case {r['id']}",
            f"**Question:** {r['question']}",
            "",
            f"**Answer:** {r['answer']}",
            "",
            "Excerpts the assistant was given:",
            "```",
            r["context"],
            "```",
            "",
        ]
    SHEET_OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nWrote {ANSWERS_OUT.name}, {SHEET_OUT.name}, {LABELS_OUT.name}")
    print("Next: read to_label.md, fill labels_25.json, then COMMIT before running any judge.")


if __name__ == "__main__":
    main()
