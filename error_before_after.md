# error_before_after.md

Same failing call both times: search_policy("") - an empty query. Both tool errors and both
model reactions below are real, captured by error_demo.py (see error_before_after.json for the
raw JSON).

## BEFORE (mcp_servers/policy_server_before.py)
Docstring: "Search policy." (terse, says nothing about when to call it or what a query looks like)
Error path: raise ValueError("bad query")

Tool error shown to the model:
"Error executing tool search_policy: bad query"

Model's reaction:
"I now know that the tool requires a valid search term to function, so I will prompt the user to
provide the specific policy number or claimant name. Once I have that information, I will call
search_policy again using the provided details as the query."

This recovery plan is WRONG. search_policy has nothing to do with policy numbers or claimant
names - it searches policy EXCLUSIONS by cause-of-loss keyword. A vague error gave the model
nothing to work with, so it filled the gap with a plausible-sounding but incorrect guess about
what the tool does. Acting on this guess would keep failing with no way to know why.

## AFTER (mcp_servers/policy_server.py)
Docstring: rewritten as a real prompt - explains when to call it, to call it once per claim with
every relevant keyword combined, and gives example queries.
Error path: raise ToolError("search_policy needs a non-empty query describing the cause of loss
or property condition (for example 'flood' or 'vacant house') - an empty string was given.")

Tool error shown to the model:
"Error executing tool search_policy: search_policy needs a non-empty query describing the cause
of loss or property condition (for example 'flood' or 'vacant house') - an empty string was
given."

Model's reaction:
"I now understand that the tool requires a specific description of the loss to function
correctly. I will re-examine the claim documentation to identify the cause of loss and then call
search_policy again using that specific term (e.g., 'water damage' or 'fire')."

This recovery plan is CORRECT: it names the real expected input (a cause-of-loss description)
and gives example terms that actually match what the tool accepts.

## The actual lesson
Both models "recovered" in the sense of not crashing or giving up. The difference that matters
is whether the recovery is grounded in the real failure or a guess filling an information gap.
A vague error doesn't just look bad to a human reading logs - it can cause the model to form an
incorrect mental model of the tool, which then produces confidently wrong behavior on the retry,
not a safe one.