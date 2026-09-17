"""
Thin search layer shared by app.py (the API) and eval_hitrate.py (the
offline scoring script), so both use the exact same retrieval code path.
"""

from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

from ingest import EMBED_MODEL_NAME, COLLECTION_NAIVE, COLLECTION_STRUCTURED, get_client

_embedder = None


def get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL_NAME)
    return _embedder


def resolve_collection(strategy: str) -> str:
    if strategy == "naive":
        return COLLECTION_NAIVE
    if strategy == "structured":
        return COLLECTION_STRUCTURED
    raise ValueError("strategy must be 'naive' or 'structured'")


def search_unfiltered(query: str, strategy: str = "structured", top_k: int = 5) -> list[dict]:
    """Plain vector search, no metadata filter."""
    collection = resolve_collection(strategy)
    vector = get_embedder().encode(query, normalize_embeddings=True).tolist()
    hits = get_client().query_points(
        collection_name=collection,
        query=vector,
        limit=top_k,
    ).points
    return _format_hits(hits)


def search_filtered(query: str, policy_line: str, strategy: str = "structured", top_k: int = 5) -> list[dict]:
    """Vector search restricted to a single policy_line via a Qdrant payload filter."""
    collection = resolve_collection(strategy)
    vector = get_embedder().encode(query, normalize_embeddings=True).tolist()
    qdrant_filter = Filter(
        must=[FieldCondition(key="policy_line", match=MatchValue(value=policy_line))]
    )
    hits = get_client().query_points(
        collection_name=collection,
        query=vector,
        query_filter=qdrant_filter,
        limit=top_k,
    ).points
    return _format_hits(hits)


def _format_hits(hits) -> list[dict]:
    results = []
    for hit in hits:
        results.append({
            "chunk_id": hit.payload["chunk_id"],
            "score": hit.score,
            "payload": hit.payload,
        })
    return results