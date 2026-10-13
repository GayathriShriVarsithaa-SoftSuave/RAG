"""
Week 9 - OUR OWN MCP server. Exposes the policy-exclusions search as ONE MCP tool.

This is "server one" in the task: the policy-document search server the agent already talks
to. Run standalone to sanity-check it starts cleanly:

    python mcp_servers/policy_server.py

(it will just sit there waiting for a client to connect over stdio - that's normal, Ctrl+C to stop)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # so claims_data.py is importable

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from claims_data import EXCLUSIONS

mcp = FastMCP("policy-document-search")


@mcp.tool()
def search_policy(query: str) -> dict:
    """Look up POLICY EXCLUSIONS by keyword, to check whether a described cause of loss or
    property condition is excluded from cover. Call this ONCE per claim: put every relevant
    keyword from the adjuster notes into ONE short phrase (for example 'flood', 'vacant house',
    'wear and tear') rather than calling it again for a second condition. Returns the matching
    exclusion ids and their wording, or an empty list of matches if nothing in the policy
    excludes the described cause.
    """
    if not query or not query.strip():
        raise ToolError(
            "search_policy needs a non-empty query describing the cause of loss or property "
            "condition (for example 'flood' or 'vacant house') - an empty string was given."
        )
    q = query.lower()
    matches = []
    for exc in EXCLUSIONS:
        if any(word in q for word in exc["keywords"]):
            matches.append({"id": exc["id"], "title": exc["title"], "wording": exc["wording"]})
    return {"matches": matches}


if __name__ == "__main__":
    mcp.run(transport="stdio")
