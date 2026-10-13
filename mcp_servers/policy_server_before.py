"""
Week 9 - the ORIGINAL (bad) version of search_policy, kept ONLY to generate the before/after
comparison. Not used by mcp_config.json or the real agent.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP
from claims_data import EXCLUSIONS

mcp = FastMCP("policy-document-search-BEFORE")


@mcp.tool()
def search_policy(query: str) -> dict:
    """Search policy."""
    if not query or not query.strip():
        raise ValueError("bad query")
    q = query.lower()
    matches = []
    for exc in EXCLUSIONS:
        if any(word in q for word in exc["keywords"]):
            matches.append({"id": exc["id"], "title": exc["title"], "wording": exc["wording"]})
    return {"matches": matches}


if __name__ == "__main__":
    mcp.run(transport="stdio")
