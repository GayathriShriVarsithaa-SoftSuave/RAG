"""
One place that configures the Qdrant Cloud client. Both ingest.py and
search.py import get_client() from here, so they can never drift out of
sync with each other.

Qdrant Cloud only — set these two in .env (see .env.example):
    QDRANT_URL=https://xxxxx.cloud.qdrant.io
    QDRANT_API_KEY=your-qdrant-cloud-api-key

There is no local/on-disk fallback: if QDRANT_URL or QDRANT_API_KEY is
missing, get_client() raises instead of silently falling back to a local
instance.
"""

import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from chunkers import load_and_chunk_all

load_dotenv()

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_DIM = 384  # MiniLM-L6-v2 output size

COLLECTION_NAIVE = "endorsements_naive"
COLLECTION_STRUCTURED = "endorsements_structured"


_client = None


def get_client() -> QdrantClient:
    global _client
    if _client is not None:
        return _client

    url = os.environ.get("QDRANT_URL")
    api_key = os.environ.get("QDRANT_API_KEY")

    if not url or not api_key:
        raise RuntimeError(
            "QDRANT_URL and QDRANT_API_KEY must both be set in .env — "
            "this project only talks to Qdrant Cloud, there is no local "
            "fallback. Get these from your cluster's dashboard at "
            "https://cloud.qdrant.io."
        )

    print(f"[qdrant_config] Using Qdrant Cloud at {url}")
    _client = QdrantClient(url=url, api_key=api_key)

    return _client


def _recreate_collection(client: QdrantClient, name: str) -> None:
    """Drops and recreates a collection so re-running ingest.py is idempotent."""
    if client.collection_exists(name):
        client.delete_collection(name)
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
    )


def _upsert_chunks(client: QdrantClient, embedder: SentenceTransformer, collection: str, chunks: list[dict]) -> None:
    if not chunks:
        return
    texts = [c["text"] for c in chunks]
    vectors = embedder.encode(texts, normalize_embeddings=True, show_progress_bar=False)

    points = []
    for chunk, vector in zip(chunks, vectors):
        # chunk_id (e.g. "HO-0304.txt:structured:3") is human-readable but not a
        # valid Qdrant point id, so derive a stable UUID from it and keep the
        # original string as a payload field (used everywhere downstream).
        point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, chunk["chunk_id"]))
        points.append(PointStruct(id=point_id, vector=vector.tolist(), payload=chunk))

    client.upsert(collection_name=collection, points=points)


def ingest_all(data_dir: str = "data/endorsements") -> None:
    client = get_client()
    embedder = SentenceTransformer(EMBED_MODEL_NAME)

    naive_chunks, structured_chunks = load_and_chunk_all(data_dir)

    print(f"[ingest] naive: {len(naive_chunks)} chunks -> {COLLECTION_NAIVE}")
    _recreate_collection(client, COLLECTION_NAIVE)
    _upsert_chunks(client, embedder, COLLECTION_NAIVE, naive_chunks)

    print(f"[ingest] structured: {len(structured_chunks)} chunks -> {COLLECTION_STRUCTURED}")
    _recreate_collection(client, COLLECTION_STRUCTURED)
    _upsert_chunks(client, embedder, COLLECTION_STRUCTURED, structured_chunks)

    print("[ingest] done.")


if __name__ == "__main__":
    ingest_all()