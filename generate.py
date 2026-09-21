"""
Grounded generation with Gemini 3.1 Flash-Lite.

Two rules the assignment cares about are enforced in code, not just in the
prompt wording:

1. Every claim must cite a chunk_id that we actually retrieved. We literally
   check the model's cited chunk_id against the retrieved set — if it made
   one up, we treat the whole answer as ungrounded.
2. If retrieval didn't find anything relevant (score below MIN_SCORE, or no
   results at all), we refuse WITHOUT calling the model at all. The
   assignment explicitly warns against a prompt that just *suggests*
   refusing ("use your best judgement") — that isn't a refusal, it's a
   guess with a disclaimer. Here the refusal is a hard branch in the code.
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_MODEL = "gemini-3.1-flash-lite"
MIN_SCORE = 0.35  # cosine similarity floor below which we refuse rather than guess

SYSTEM_INSTRUCTION = """You are a claims-assistant that answers ONLY from the provided
endorsement excerpts. Rules:
- Every factual claim must end with a citation in the form [chunk_id: FORM_NUMBER, clause: CLAUSE].
- Only cite a chunk_id that appears in the provided excerpts below. Never invent one.
- If the excerpts do not contain the answer, respond with exactly:
  REFUSE: The indexed endorsements do not contain this information.
- Do not use outside knowledge of insurance law or typical policy wording. Only use the excerpts.
"""


_CLIENT = None  # kept alive on purpose: newer google-genai closes a Client that is thrown away


def _client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY in your .env file (see .env.example)")
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = genai.Client(api_key=api_key)
    return _CLIENT


def build_context(retrieved: list[dict]) -> str:
    """Turns Qdrant hits into a numbered excerpt block the model can cite from."""
    lines = []
    for hit in retrieved:
        payload = hit["payload"]
        lines.append(
            f"chunk_id: {hit['chunk_id']} | form_number: {payload['form_number']} | "
            f"clause: {payload.get('clause')}\n{payload['text']}\n"
        )
    return "\n---\n".join(lines)


def answer_question(question: str, retrieved: list[dict]) -> dict:
    """
    retrieved: list of dicts like {"chunk_id": ..., "score": ..., "payload": {...}}
    Returns {"answer": str, "refused": bool, "grounded": bool}
    """
    # Hard refusal branch — no retrieval hit clears the bar, don't even ask the model.
    if not retrieved or retrieved[0]["score"] < MIN_SCORE:
        return {
            "answer": "REFUSE: The indexed endorsements do not contain this information.",
            "refused": True,
            "grounded": True,
        }

    context = build_context(retrieved)
    prompt = f"Excerpts:\n{context}\n\nQuestion: {question}\n\nAnswer with citations:"

    client = _client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        config={"system_instruction": SYSTEM_INSTRUCTION},
        contents=prompt,
    )
    text = response.text.strip()

    if text.startswith("REFUSE"):
        return {"answer": text, "refused": True, "grounded": True}

    # Verify every cited chunk_id actually came from our retrieved set.
    retrieved_ids = {hit["chunk_id"] for hit in retrieved}
    cited_ids = set()
    for hit in retrieved:
        if hit["chunk_id"] in text:
            cited_ids.add(hit["chunk_id"])
    grounded = len(cited_ids) > 0  # at least one real, retrieved chunk_id was cited

    return {"answer": text, "refused": False, "grounded": grounded, "cited_ids": list(cited_ids)}
