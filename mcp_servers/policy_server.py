"""
Week 12 MCP server for loss-date-aware policy wording retrieval.

Run with: python mcp_servers/policy_server.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from wording_store import search_wording

mcp = FastMCP("policy-document-search")


@mcp.tool()
def search_policy_wording(query: str, product: str, loss_date: str) -> dict:
    """Search policy wording for one product, resolved against the loss date.

    Returns retrieved chunks with their chunk IDs, clause, form number,
    edition date and text. This tool reports wording only; it does not
    make coverage decisions.
    """
    query = (query or "").strip()
    product = (product or "").strip().upper()
    loss_date = (loss_date or "").strip()

    if not query:
        raise ToolError("query must be a non-empty description of the loss")
    if not product:
        raise ToolError("product is required (for example HO3 or MO1)")
    if not loss_date:
        raise ToolError("loss_date is required in YYYY-MM-DD format")

    try:
        hits = search_wording(
            query,
            product=product,
            loss_date=loss_date,
            top_k=5,
        )
    except ValueError as exc:
        raise ToolError(str(exc)) from exc

    chunks = []

    for hit in hits:
        chunk = hit.get("payload", hit)

        chunks.append({
            "chunk_id": chunk["chunk_id"],
            "policy_line": chunk["policy_line"],
            "form_number": chunk["form_number"],
            "edition_date": chunk["edition_date"],
            "clause": chunk["clause"],
            "text": chunk["text"],
            "score": hit.get("score"),
        })

    return {
        "product": product,
        "loss_date": loss_date,
        "results": chunks,
        "result_count": len(chunks),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")