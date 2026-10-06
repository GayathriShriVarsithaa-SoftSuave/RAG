# risk_note.md - claims-system MCP server

1. Who wrote it: the claims platform team, not us - we only wrote the client code that connects to it; we have no visibility into its real implementation or who maintains it.
2. What it can reach: in this exercise, a local in-memory claims dict; in production this stands in for direct read access to the live claims database, including every open claim's adjuster notes.
3. What it logs: unknown - this demo only shows our own client-side request/response log; we have no evidence of what the real server logs, retains, or forwards to a third party.
4. What a stolen token could do: today this demo has no token at all (local stdio, no auth) - in production, a stolen token for this server would let an attacker read adjuster notes on every open claim, which is sensitive personal and financial information.
5. Ship or don't: don't ship as-is - connect only with a scoped, read-only, short-lived token and server-side audit logging in place first; today's stdio demo has neither.
