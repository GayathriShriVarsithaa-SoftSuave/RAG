"""
Week 9 - the (simulated) THIRD-PARTY claims-system MCP server. Exposes claim status and the
adjuster note history as ONE MCP tool. In the task narrative this is the server the claims
platform team "stood up" - we did not write the real one, so this stands in for it.

    python mcp_servers/claims_server.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from claims_data import CLAIMS

mcp = FastMCP("claims-system")


@mcp.tool()
def get_claim(claim_id: str) -> dict:
    """Fetch ONE claim's status and adjuster notes by its claim number, in the form
    CLM-YYYY-NNNNN (for example CLM-2026-00004). Returns the claim's status, date of loss,
    loss amount, excess, and the adjuster's free-text notes. Raises a clear error if the
    claim number is not found or is not in the right format.
    """
    claim_id = str(claim_id).strip()
    claim = CLAIMS.get(claim_id)
    if claim is None:
        raise ToolError(
            f"claim {claim_id} not found: claim numbers look like CLM-YYYY-NNNNN "
            f"(for example CLM-2026-00004) - check the number and try again."
        )
    return claim


if __name__ == "__main__":
    mcp.run(transport="stdio")
