"""
Thin search layer shared by app.py (the API) and the eval scripts, so both
use the exact same retrieval code path.

Retrieval change (Week 4 Task Set D): dense retrieval over MiniLM alone was
ranking the correct chunk outside the top-3 for several golden-set
questions, while it was still sitting somewhere in the wider dense
candidate pool (see inspection_report.json). A cross-encoder reranker
jointly scores (query, chunk) pairs and reorders that pool, which fixes
ranking mistakes without a second (lexical) retrieval path -- and needs no
new dependency, since sentence-transformers (already a project dependency)
ships CrossEncoder.
"""

from functools import lru_cache

from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer, CrossEncoder

from ingest import EMBED_MODEL_NAME, COLLECTION_NAIVE, COLLECTION_STRUCTURED, get_client

# Pull a wider dense pool than we ultimately return, so the reranker has
# real work to do: if the correct chunk is misranked but still inside this
# pool, cross-encoding can promote it back into the top_k.
RERANK_CANDIDATE_POOL = 25
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_embedder = None


def get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL_NAME)
    return _embedder


@lru_cache(maxsize=1)
def get_reranker() -> CrossEncoder:
    return CrossEncoder(RERANKER_MODEL_NAME)


def resolve_collection(strategy: str) -> str:
    if strategy == "naive":
        return COLLECTION_NAIVE
    if strategy == "structured":
        return COLLECTION_STRUCTURED
    raise ValueError("strategy must be 'naive' or 'structured'")


def _rerank(query: str, hits: list[dict], top_k: int) -> list[dict]:
    """Reranks a dense candidate pool with a cross-encoder, keeps the top_k."""
    if not hits:
        return hits
    reranker = get_reranker()
    pairs = [(query, h["payload"]["text"]) for h in hits]
    scores = reranker.predict(pairs)
    reranked = sorted(zip(hits, scores), key=lambda pair: pair[1], reverse=True)
    output = []
    for hit, score in reranked[:top_k]:
        hit = dict(hit)
        hit["score"] = float(score)
        output.append(hit)
    return output


def search_unfiltered(query: str, strategy: str = "structured", top_k: int = 5) -> list[dict]:
    """Dense retrieval over RERANK_CANDIDATE_POOL candidates, then cross-encoder rerank down to top_k."""
    collection = resolve_collection(strategy)
    vector = get_embedder().encode(query, normalize_embeddings=True).tolist()
    hits = get_client().query_points(
        collection_name=collection,
        query=vector,
        limit=RERANK_CANDIDATE_POOL,
    ).points
    candidates = _format_hits(hits)
    return _rerank(query, candidates, top_k)


def search_filtered(query: str, policy_line: str, strategy: str = "structured", top_k: int = 5) -> list[dict]:
    """Same as search_unfiltered, restricted to a single policy_line via a Qdrant payload filter."""
    collection = resolve_collection(strategy)
    vector = get_embedder().encode(query, normalize_embeddings=True).tolist()
    qdrant_filter = Filter(
        must=[FieldCondition(key="policy_line", match=MatchValue(value=policy_line))]
    )
    hits = get_client().query_points(
        collection_name=collection,
        query=vector,
        query_filter=qdrant_filter,
        limit=RERANK_CANDIDATE_POOL,
    ).points
    candidates = _format_hits(hits)
    return _rerank(query, candidates, top_k)


def _format_hits(hits) -> list[dict]:
    results = []
    for hit in hits:
        results.append({
            "chunk_id": hit.payload["chunk_id"],
            "score": hit.score,
            "payload": hit.payload,
        })
    return results