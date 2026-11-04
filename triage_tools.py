"""
Week 12 - the agent's local tools and the compliance rules, enforced IN CODE.

  lookup_policy(policy_number)            -> product, policy period, which sub-limit names exist
  check_coverage_in_force(policy_number, loss_date)
  refer_to_adjuster(...)                  -> the ONLY way a claim ends. It never decides anything.

The wording search is NOT here: it is reached over MCP (Step 4) and discovered at runtime. After
each wording search the agent host calls session.record_wording_results() so refer_to_adjuster can
verify every citation against what was actually retrieved.

What refer_to_adjuster enforces (so the prompt is not the only defence):
  1. check_coverage_in_force must have been run for this policy and loss date first.
  2. every cited chunk id must have been retrieved in THIS run (no invented citations).
  3. every cited chunk must belong to the edition in force on the loss date, for the right product.
  4. deductible, sub-limit and policy limit are attached from policy_table.json by code.
  5. model-written text may not state a coverage decision (decision_language()).
"""
import re

from policy_rules import coverage_in_force, edition_in_force, deductible_and_limits, _table

# A lexical safety net, not a proof: it catches the obvious words, not every paraphrase.
DECISION_WORDS = re.compile(
    r"\b(un)?covered\b|\bapprov(e|ed|es|al)\b|\bdeclin(e|ed|es)\b|\bden(y|ied|ies|ial)\b|\breject(ed|s)?\b"
    r"|\b(is|are|was|were|be)\s+(not\s+)?(excluded|eligible)\b|\bwill\s+(be\s+)?(paid|pay)\b",
    re.IGNORECASE,
)


def decision_language(text: str) -> list[str]:
    """Returns every decision-style phrase found in text (empty list = clean)."""
    return [m.group(0) for m in DECISION_WORDS.finditer(text or "")]


LOCAL_TOOL_SPECS = [
    {"name": "lookup_policy",
     "description": ("Look up ONE policy by its policy number (like POL-HO-1001): returns the product, the policy period "
                     "and the names of its sub-limits. It never checks dates and never reads wording."),
     "parameters": {"type": "OBJECT", "properties": {
         "policy_number": {"type": "STRING", "description": "Policy number, for example POL-HO-1001"}},
         "required": ["policy_number"]}},
    {"name": "check_coverage_in_force",
     "description": ("Check whether ONE policy was in force on the loss date (YYYY-MM-DD). Reports a fact about dates only; "
                     "it says nothing about whether a loss is excluded. Call this before refer_to_adjuster."),
     "parameters": {"type": "OBJECT", "properties": {
         "policy_number": {"type": "STRING", "description": "Policy number, for example POL-HO-1001"},
         "loss_date": {"type": "STRING", "description": "Date of loss as YYYY-MM-DD, for example 2024-08-11"}},
         "required": ["policy_number", "loss_date"]}},
    {"name": "refer_to_adjuster",
     "description": ("End the triage by referring the claim to a human adjuster. You never decide: pass the ids of the wording "
                     "chunks you retrieved that matter, a short facts-only summary, and why a human must look. Deductible, "
                     "sub-limit and policy limit are attached automatically. Do not use words like covered, approved or declined."),
     "parameters": {"type": "OBJECT", "properties": {
         "policy_number": {"type": "STRING"},
         "loss_date": {"type": "STRING", "description": "YYYY-MM-DD"},
         "cited_chunk_ids": {"type": "ARRAY", "items": {"type": "STRING"},
                             "description": "chunk_id values returned by the wording search that are relevant to this loss"},
         "sub_limit_key": {"type": "STRING", "description": "Optional: the sub-limit name relevant to this loss, from lookup_policy"},
         "facts_summary": {"type": "STRING", "description": "Facts only: what happened, when, what the wording says. No conclusion."},
         "referral_reason": {"type": "STRING", "description": "Why a human adjuster must review this claim"}},
         "required": ["policy_number", "loss_date", "cited_chunk_ids", "facts_summary", "referral_reason"]}},
]


class TriageSession:
    """State for ONE claim: what was retrieved, which checks ran. Tools never raise; they return {"error": ...}."""

    def __init__(self):
        self.retrieved = {}      # chunk_id -> flat chunk dict
        self.checks = {}         # (policy_number, loss_date) -> coverage_in_force result
        self.referral = None

    def record_wording_results(self, chunks: list[dict]) -> None:
        for chunk in chunks:
            self.retrieved[chunk["chunk_id"]] = chunk

    def call(self, name: str, args: dict) -> dict:
        tools = {"lookup_policy": self.lookup_policy, "check_coverage_in_force": self.check_coverage_in_force,
                 "refer_to_adjuster": self.refer_to_adjuster}
        if name not in tools:
            return {"error": f"unknown tool {name}"}
        try:
            return tools[name](**args)
        except TypeError as exc:
            return {"error": f"bad arguments for {name}: {exc}"}

    # ---------------------------------------------------------------- tools
    def lookup_policy(self, policy_number: str) -> dict:
        number = str(policy_number).strip()
        policy = _table()["policies"].get(number)
        if policy is None:
            return {"error": f"policy {number} not found: policy numbers look like POL-HO-1001"}
        limits = deductible_and_limits(policy["product"])
        return {"policy_number": number, "product": policy["product"],
                "policy_period": f"{policy['in_force_from']} to {policy['in_force_to']}",
                "sub_limit_names": sorted(limits["sub_limits"])}

    def check_coverage_in_force(self, policy_number: str, loss_date: str) -> dict:
        try:
            result = coverage_in_force(policy_number, loss_date)
        except ValueError as exc:
            return {"error": str(exc)}
        if not result["found"]:
            return {"error": result["reason"]}
        self.checks[(result["policy_number"], loss_date)] = result
        return result

    def refer_to_adjuster(self, policy_number: str, loss_date: str, cited_chunk_ids: list,
                          facts_summary: str, referral_reason: str, sub_limit_key: str = None) -> dict:
        number = str(policy_number).strip()
        check = self.checks.get((number, loss_date))
        if check is None:
            return {"error": f"run check_coverage_in_force for {number} and loss date {loss_date} before referring"}

        found = decision_language(facts_summary) + decision_language(referral_reason)
        if found:
            return {"error": f"the referral must not state a coverage decision (found: {sorted(set(found))}); "
                             "describe the facts and quote the wording instead, a human adjuster decides"}

        product = check["product"]
        edition = edition_in_force(product, loss_date)
        citations = []
        for chunk_id in cited_chunk_ids or []:
            chunk = self.retrieved.get(chunk_id)
            if chunk is None:
                return {"error": f"chunk {chunk_id} was never retrieved in this run: cite only chunk_id values returned by the wording search"}
            if edition is None or chunk["edition_date"] != edition["edition_date"] or chunk["policy_line"] != product:
                wanted = edition["form_number"] if edition else "no edition"
                return {"error": f"chunk {chunk_id} is from {chunk['form_number']} (effective {chunk['edition_date']}), "
                                 f"but the wording in force on {loss_date} for {product} is {wanted}: search again with this loss date"}
            citations.append({"chunk_id": chunk_id, "form_number": chunk["form_number"],
                              "edition_date": chunk["edition_date"], "clause": chunk["clause"],
                              "excerpt": chunk["text"][:300]})

        limits = deductible_and_limits(product)
        sub_limit = None
        if sub_limit_key:
            if sub_limit_key not in limits["sub_limits"]:
                return {"error": f"unknown sub_limit_key '{sub_limit_key}': valid for {product} are {sorted(limits['sub_limits'])}"}
            sub_limit = {"name": sub_limit_key, "amount": limits["sub_limits"][sub_limit_key]}

        self.referral = {
            "action": "REFER_TO_ADJUSTER",
            "policy_number": number, "product": product, "loss_date": loss_date,
            "policy_in_force": check["in_force"], "policy_period": f"{check['in_force_from']} to {check['in_force_to']}",
            "wording_resolved_against": {"form_number": edition["form_number"], "edition_date": edition["edition_date"]} if edition else None,
            "citations": citations,
            "deductible": limits["deductible"], "sub_limit": sub_limit, "policy_limit": limits["policy_limit"],
            "facts_summary": facts_summary, "referral_reason": referral_reason,
        }
        return self.referral
