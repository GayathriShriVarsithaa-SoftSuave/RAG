# Week 3 Task D — Endorsement RAG (beginner build)

Stack: **Qdrant** (local, on-disk, no server needed) + **MiniLM-L6-v2**
(`sentence-transformers`) for embeddings + **Gemini 3.1 Flash-Lite**
(`gemini-3.1-flash-lite`) for grounded generation, served with **FastAPI**.

## File map
```
data/endorsements/   sample endorsement .txt files
chunkers.py          naive fixed-size chunker + structure-aware chunker
ingest.py            embeds + upserts both chunk sets into two Qdrant collections
search.py            shared retrieval helper (unfiltered + policy_line-filtered)
generate.py          Gemini wrapper: cites real chunk_ids, refuses when ungrounded
app.py               FastAPI app: /query/unfiltered, /query/filtered, /generate
```

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then paste your Gemini API key into .env
```

## 1. Ingest
```bash
python ingest.py
```
This chunks the 6 files two ways and creates two Qdrant collections on disk
under `./qdrant_data`: `endorsements_naive` and `endorsements_structured`.
Only these 6 endorsements are indexed — no base wording library is touched.

## 2. Run the API (for requirement of two query endpoints)
```bash
uvicorn app:app --reload
```
Open `http://127.0.0.1:8000/docs` and try:
- `GET /query/unfiltered?q=does E-17 apply to a burst supply line&strategy=structured`
- `GET /query/filtered?q=coverage limit&policy_line=HO6&strategy=structured`
- `POST /generate` with `{"question": "..."}`



## Swapping in real data
Replace the files in `data/endorsements/` with your real endorsements, but
keep the same header format at the top of each file:
```
FORM_NUMBER: ...
POLICY_LINE: ...
EFFECTIVE_DATE: ...
TITLE: ...
```
