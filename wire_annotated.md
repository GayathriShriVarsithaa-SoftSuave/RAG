# wire.json, annotated by hand

Captured with wire_capture.py against mcp_servers/claims_server.py (server two, the new
server), bypassing the mcp SDK's parsed Python objects entirely - these are the literal bytes
that went over stdio, one JSON object per line.

## 1. initialize (client -> server)
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {...}}

- jsonrpc: the protocol family. MCP's wire format IS JSON-RPC 2.0 - nothing MCP-specific here.
- id: 1. A request the server must answer gets an id; the client matches the response back to
  this request by id. (The next message, a notification, has none - see below.)
- method: "initialize" - the first call on every MCP connection, before anything else is legal.
- params.protocolVersion: the MCP spec version the client speaks, so client and server can agree
  on a version both understand.
- params.capabilities: what the CLIENT can do (empty here - we didn't declare support for
  sampling, roots, etc.). This is not about what tools exist; that's a separate step below.
- params.clientInfo: just a name/version label for logging, not used for auth or capability.

## 2. initialize (server -> client)
{"jsonrpc": "2.0", "id": 1, "result": {...}}

- id: 1 matches the request above - this is the answer to that specific call.
- result.protocolVersion: the version the SERVER will actually use for this session.
- result.capabilities: what the SERVER supports - tools, resources, prompts, each with a
  listChanged flag (can this list change while connected, so the client should watch for
  updates). We don't use resources/prompts here, only tools.
- result.serverInfo.name: "claims-system" - this is where the agent's discovery log gets the
  server's own name from, not from our config file. (Note: serverInfo.version shows "1.27.0" in
  our real capture - that's the mcp SDK version, not something we set.)

## 3. notifications/initialized (client -> server)
{"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}

- No id at all. In JSON-RPC, a message with no id is a NOTIFICATION: "I'm telling you
  something, I'm not asking a question, don't bother replying." This is the client confirming the
  handshake is complete before it's allowed to call tools/list or tools/call.

## 4. tools/list (client -> server)
{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

- method: "tools/list" - "tell me every tool you expose." This is the discovery call: the
  agent never hardcodes get_claim anywhere; it learns the tool exists from this response.

## 5. tools/list (server -> client)
{"jsonrpc": "2.0", "id": 2, "result": {"tools": [{...}]}}

- result.tools: an array, one entry per tool. Our server exposes exactly one: get_claim.
- Each tool entry has name (what the model will call it), description (this IS the
  get_claim docstring, verbatim - the docstring is not a code comment, it's the prompt the
  model reads to decide when and how to call this tool), and inputSchema (plain JSON Schema:
  type: "object", one required string property claim_id, plus auto-generated "title" fields
  like "Claim Id" and "get_claimArguments" that the SDK adds for readability and that we don't
  use). Our agent's mcp_client.py uppercases the type names before handing them to Gemini,
  because Gemini's function-calling schema wants "OBJECT"/"STRING", not lowercase.

## 6. tools/call (client -> server)
{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_claim", "arguments": {"claim_id": "CLM-2026-00004"}}}

- params.name: which tool to run - this value came straight out of message 5's tool list; the
  client only ever calls a name it was told about.
- params.arguments: the actual argument values. Here they came from this hand-written test
  script; in the real agent they come from Gemini's function_call.args - this is the ONE place
  in the whole exchange where a model's decision shows up on the wire.

## 7. tools/call (server -> client)
{"jsonrpc": "2.0", "id": 3, "result": {"content": [{"type": "text", "text": "{...claim json...}"}], "isError": false}}

- result.content: a list of content blocks (here, one text block holding the claim as a JSON
  string) - this is what a tool "returns" at the protocol level; there is no Python object on the
  wire, only text/structured JSON.
- result.isError: false here. When a tool deliberately raises ToolError (see
  error_before_after.md), this flips to true and content[0].text carries the error message -
  the model sees that text and can react to it, exactly like a normal tool result.

## Where the model call happens, and where it does not
The Gemini call happens only in the agent host (claim_llm.call_llm() in agent_mcp.py),
strictly between MCP exchanges - the model decides what to call next by reading a tools/list
result it was given earlier, and its decision becomes a tools/call request the host sends out.
No model call happens anywhere inside claims_server.py - the server is plain, deterministic
Python (a dictionary lookup) with no knowledge that an LLM exists on the other end of the
connection; it only speaks the request/response shapes above.