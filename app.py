"""
Run with:  uvicorn app:app --reload
Then open: http://127.0.0.1:8000/docs

Endpoints:
  GET  /query/unfiltered   -> vector search only, no metadata filter
  GET  /query/filtered     -> vector search restricted to one policy_line
  POST /generate           -> retrieval + Gemini answer, with citations or a forced refusal
"""

from fastapi import FastAPI, Query
from pydantic import BaseModel

from search import search_unfiltered, search_filtered
from generate import answer_question

app = FastAPI(title="Endorsement Claims Assistant - Week 3 Task D")


@app.get("/query/unfiltered")
def query_unfiltered(
    q: str = Query(..., description="Your question"),
    strategy: str = Query("structured", description="'naive' or 'structured'"),
    top_k: int = Query(5, ge=1, le=20),
):
    """Search-only endpoint, no policy_line filter. Returns the raw ranked chunks."""
    results = search_unfiltered(q, strategy=strategy, top_k=top_k)
    return {"query": q, "strategy": strategy, "filtered": False, "results": results}


@app.get("/query/filtered")
def query_filtered(
    q: str = Query(..., description="Your question"),
    policy_line: str = Query(..., description="e.g. HO3, HO4, HO5, HO6"),
    strategy: str = Query("structured", description="'naive' or 'structured'"),
    top_k: int = Query(5, ge=1, le=20),
):
    """Same search, restricted to a single policy_line via a Qdrant metadata filter."""
    results = search_filtered(q, policy_line=policy_line, strategy=strategy, top_k=top_k)
    return {"query": q, "strategy": strategy, "filtered": True, "policy_line": policy_line, "results": results}


class GenerateRequest(BaseModel):
    question: str
    strategy: str = "structured"
    top_k: int = 5


@app.post("/generate")
def generate(req: GenerateRequest):
    """Retrieves context, then asks Gemini to answer with citations or refuse."""
    retrieved = search_unfiltered(req.question, strategy=req.strategy, top_k=req.top_k)
    result = answer_question(req.question, retrieved)
    return {"question": req.question, "retrieved_chunk_ids": [r["chunk_id"] for r in retrieved], **result}
