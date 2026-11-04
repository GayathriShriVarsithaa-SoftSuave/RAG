"""
Week 12 - the policy-wording store. Builds a small IN-MEMORY Qdrant collection from
data/policy_wordings/*.txt every time the process starts (16 chunks, a few seconds), so there is
no cloud cluster, no API key and no ingest step: a stranger can clone the repo and run it.

It reuses your Week 3-4 pieces: chunkers.structure_chunk (one chunk per exclusion row, tagged
with form_number / edition_date / clause), the same MiniLM embedder, and the same cross-encoder
reranker from search.py.

    from wording_store import search_wording
    hits = search_wording("is flood damage excluded?", product="HO3")
"""
from functools import lru_cache
from pathlib import Path

from chunkers import structure_chunk

COLLECTION = "policy_wordings"
DATA_DIR = Path(__file__).resolve().parent / "data" / "policy_wordings"


def build_chunks(data_dir=DATA_DIR) -> list[dict]:
    chunks = []
    for path in sorted(Path(data_dir).glob("*.txt")):
        for chunk in structure_chunk(path.read_text(encoding="utf-8"), path.name):
            chunk["edition_int"] = int(chunk["edition_date"].replace("-", ""))  # 2025-03-01 -> 20250301
            chunks.append(chunk)
    return chunks


@lru_cache(maxsize=1)
def get_store():
    """Builds the in-memory collection once per process and reuses it."""
    import uuid
    from qdrant_client import QdrantClient
    from qdrant_client.models import VectorParams, Distance, PointStruct
    from search import get_embedder
    from ingest import EMBED_DIM

    chunks = build_chunks()
    client = QdrantClient(":memory:")
    client.create_collection(collection_name=COLLECTION,
                             vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE))
    vectors = get_embedder().encode([c["text"] for c in chunks], normalize_embeddings=True, show_progress_bar=False)
    client.upsert(collection_name=COLLECTION, points=[
        PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, c["chunk_id"])), vector=v.tolist(), payload=c)
        for c, v in zip(chunks, vectors)])
    return client


def search_wording(query: str, product: str, top_k: int = 3, loss_date: str | None = None) -> list[dict]:
    """Product-scoped wording search.

    loss_date=None  -> NOT date-scoped: the Step 1 baseline that shows the failure.
    loss_date given -> the edition in force on that date is resolved IN CODE (policy_rules) and
                       Qdrant only ever sees chunks of that one edition, so a later or superseded
                       wording cannot be retrieved however well it ranks. Returns [] when no
                       wording was in force on that date - the caller must handle that.
    """
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    from search import get_embedder, _rerank, _format_hits
    from policy_rules import edition_in_force

    must = [FieldCondition(key="policy_line", match=MatchValue(value=product))]
    if loss_date is not None:
        edition = edition_in_force(product, loss_date)
        if edition is None:
            return []
        must.append(FieldCondition(key="edition_int", match=MatchValue(value=edition["edition_int"])))

    vector = get_embedder().encode(query, normalize_embeddings=True).tolist()
    hits = get_store().query_points(collection_name=COLLECTION, query=vector, limit=25,
                                    query_filter=Filter(must=must)).points
    return _rerank(query, _format_hits(hits), top_k)
