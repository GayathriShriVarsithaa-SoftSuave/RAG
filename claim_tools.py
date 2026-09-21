"""
Week 7 - the tools. Each tool = one Python function + one spec (name, description, parameters)
that the model reads to decide which tool to call.

Rule for the descriptions: each names exactly ONE job and none of them overlap.
"""

from claims_data import CLAIMS, EXCLUSIONS


# ---------------------------------------------------------------- the functions
def get_claim(claim_id):
    claim = CLAIMS.get(str(claim_id).strip())
    if claim is None:
        return {"error": f"claim {claim_id} not found"}
    return claim


def search_policy(query):
    q = str(query).lower()
    matches = []
    for exc in EXCLUSIONS:
        if any(word in q for word in exc["keywords"]):
            matches.append({"id": exc["id"], "title": exc["title"], "wording": exc["wording"]})
    return {"matches": matches}


TOOL_FUNCS = {"get_claim": get_claim, "search_policy": search_policy}


# ---------------------------------------------------------------- the specs the model reads
TOOL_SPECS = [
    {
        "name": "get_claim",
        "description": ("Fetch ONE claim record by its claim number: amounts, excess, status and the "
                        "adjuster's free-text notes. Use it first, to see what happened. "
                        "It never reads policy wording and never calculates money."),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "claim_id": {"type": "STRING",
                             "description": "Claim number in the form CLM-YYYY-NNNNN, e.g. CLM-2026-00004"},
            },
            "required": ["claim_id"],
        },
    },
    {
        "name": "search_policy",
        "description": ("Look up policy EXCLUSIONS by keyword. Give a short phrase (e.g. 'flood' or "
                        "'vacant house'); returns the matching exclusion ids and wording, or an empty "
                        "list if none match. It never reads claims and never calculates money."),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {"type": "STRING",
                          "description": "Short keyword phrase for a cause of loss or a condition of the property"},
            },
            "required": ["query"],
        },
    },
]


def run_tool(name, args):
    """Runs one tool by name. Never crashes: a bad call comes back as {"error": ...} for the model to read."""
    func = TOOL_FUNCS.get(name)
    if func is None:
        return {"error": f"unknown tool {name}"}
    try:
        return func(**args)
    except TypeError as exc:
        return {"error": f"bad arguments for {name}: {exc}"}
