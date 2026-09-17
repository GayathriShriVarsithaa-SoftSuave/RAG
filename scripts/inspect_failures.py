"""
Inspection view. For every golden question this finds:
  - the correct chunk's actual rank across a wide dense pool (not just the
    top-3 the app normally returns), and
  - what generate.answer_question() does when it's given the real top-3
    context for that question.

That's what lets you label each miss:
  R              retrieval fetched the wrong chunks (correct chunk exists,
                 but wasn't in the top-3)
  G              retrieval was fine (correct chunk WAS in the top-3) but the
                 model still produced an ungrounded / refused / wrong answer
  Not-In-Corpus  the golden chunk_id never turns up at all -> golden set or
                 ingest problem, not a retrieval problem

Run from the project root, ideally after eval_hit_rate.py so hit_at_3 is
cross-checked against a second, independent method:
    python scripts/inspect_failures.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search import search_unfiltered  # noqa: E402
from generate import answer_question  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GOLDEN_SET_PATH = ROOT / "golden_set.jsonl"
OUTPUT_PATH = ROOT / "inspection_report.json"

STRATEGY = "naive"
FULL_POOL_SIZE = 25  # deliberately >= the whole naive collection


def load_golden_set():
    items = []
    with open(GOLDEN_SET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def find_rank(expected_chunk_id, ranked_hits):
    for i, h in enumerate(ranked_hits, start=1):
        if h["chunk_id"] == expected_chunk_id:
            return i, h["score"]
    return None, None


def main():
    golden_set = load_golden_set()
    report = []

    for item in golden_set:
        qid = item["id"]
        question = item["question"]
        expected = item["chunk_id"]

        full_ranked = search_unfiltered(question, strategy=STRATEGY, top_k=FULL_POOL_SIZE)
        rank, score = find_rank(expected, full_ranked)

        top3 = full_ranked[:3]

        # Generation can fail independently of retrieval (auth/quota/API issues).
        # R vs Not-In-Corpus only depends on `rank`, computed above from search
        # alone -- so don't let a broken generation call block that labelling.
        gen = {"answer": None, "refused": None, "grounded": None}
        gen_error = None
        try:
            gen = answer_question(question, top3)
        except Exception as exc:  # noqa: BLE001
            gen_error = str(exc)

        hit_at_3 = rank is not None and rank <= 3

        if rank is None:
            label = "Not-In-Corpus"
            evidence = (
                f"chunk_id {expected} never appeared anywhere in the top-{FULL_POOL_SIZE} "
                f"dense candidates -- check the golden set entry against the real ingested chunk_id."
            )
        elif hit_at_3:
            if gen_error is not None:
                label = "HIT (generation unavailable)"
                evidence = (
                    f"Correct chunk ranked #{rank} (score {score:.4f}) -- retrieval is fine. "
                    f"Could not check whether the answer was grounded because generation failed: "
                    f"{gen_error[:180]}"
                )
            else:
                grounded_ok = bool(gen.get("grounded")) and not gen.get("refused", False)
                if grounded_ok:
                    label = "HIT (no failure)"
                    evidence = f"Correct chunk ranked #{rank} (score {score:.4f}); the answer was grounded on it."
                else:
                    label = "G"
                    evidence = (
                        f"Correct chunk ranked #{rank} (score {score:.4f}) and WAS in the context the model "
                        f"saw, but the generated answer was still ungrounded/refused/wrong: "
                        f"{gen['answer'][:180]!r}"
                    )
        else:
            label = "R"
            top1_id = full_ranked[0]["chunk_id"] if full_ranked else None
            evidence = (
                f"Correct chunk ranked #{rank}/{FULL_POOL_SIZE} (score {score:.4f}), pushed out of the "
                f"top-3 by chunk {top1_id!r} sitting at rank 1."
            )

        entry = {
            "id": qid,
            "question": question,
            "expected_chunk_id": expected,
            "hard_token": item.get("hard_token", False),
            "rank_in_full_pool": rank,
            "label": label,
            "evidence": evidence,
            "generated_answer": gen.get("answer"),
            "refused": gen.get("refused"),
            "grounded": gen.get("grounded"),
            "generation_error": gen_error,
        }
        report.append(entry)

        print(f"\nQ{qid} [{label}]: {question}")
        print(f"  evidence: {evidence}")

    tally = {}
    for e in report:
        tally[e["label"]] = tally.get(e["label"], 0) + 1

    print(f"\n{'=' * 90}")
    print("Tally:", tally)

    OUTPUT_PATH.write_text(json.dumps({"tally": tally, "results": report}, indent=2), encoding="utf-8")
    print(f"Full inspection report written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()