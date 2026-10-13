"""
Week 9 - the ONE place that knows how to talk MCP. The agent module never imports mcp directly;
it only calls connect_all()/call_tool() from here. This is what keeps agent_mcp.py unchanged
when a server is added to mcp_config.json: the agent only ever sees "a list of tools", built
fresh from whatever mcp_config.json lists.
"""

import json
from contextlib import AsyncExitStack
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CONFIG_PATH = Path(__file__).resolve().parent / "mcp_config.json"


def _mcp_type_to_gemini(schema):
    """MCP tool schemas are plain JSON Schema (lowercase types: 'object','string',...).
    Gemini's function_declarations want the same shape but UPPERCASE type names. This copies
    the schema and uppercases every 'type', recursively (through properties/items)."""
    if not isinstance(schema, dict):
        return schema
    out = {}
    for key, value in schema.items():
        if key == "type" and isinstance(value, str):
            out[key] = value.upper()
        elif key == "properties" and isinstance(value, dict):
            out[key] = {k: _mcp_type_to_gemini(v) for k, v in value.items()}
        elif key == "items":
            out[key] = _mcp_type_to_gemini(value)
        elif key in ("title",):
            continue  # Gemini doesn't use JSON-Schema "title"; harmless to drop
        else:
            out[key] = value
    return out


def _get(obj, *names):
    """Reads the first attribute name that exists on obj - different mcp SDK versions/builds
    expose the same field as snake_case or camelCase, so this checks both without guessing."""
    for name in names:
        if hasattr(obj, name):
            return getattr(obj, name)
    raise AttributeError(f"none of {names} found on {type(obj).__name__}")


class MCPToolbox:
    """Holds one live connection per configured server, the merged tool list (Gemini format),
    and a routing table so a tool_name can be sent back to the right server."""

    def __init__(self):
        self.stack = AsyncExitStack()
        self.sessions = {}          # server_name -> ClientSession
        self.tool_to_server = {}    # tool_name -> server_name
        self.function_declarations = []   # Gemini-format tool specs, built from ALL servers
        self.discovery_log = []     # [{"server": ..., "tools": [...names...]}] for reporting

    async def connect_all(self, config_path=CONFIG_PATH):
        config = json.loads(Path(config_path).read_text())
        for server in config["servers"]:
            params = StdioServerParameters(command=server["command"], args=server["args"])
            read, write = await self.stack.enter_async_context(stdio_client(params))
            session = await self.stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self.sessions[server["name"]] = session

            tools_result = await session.list_tools()
            names = []
            for tool in tools_result.tools:
                self.tool_to_server[tool.name] = server["name"]
                schema = _get(tool, "inputSchema", "input_schema")
                self.function_declarations.append({
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": _mcp_type_to_gemini(schema),
                })
                names.append(tool.name)
            self.discovery_log.append({"server": server["name"], "tools": names})
        return self.discovery_log

    async def call_tool(self, name, args):
        import json as _json
        server_name = self.tool_to_server[name]
        session = self.sessions[server_name]
        result = await session.call_tool(name, args)
        text = result.content[0].text if result.content else ""
        is_error = _get(result, "isError", "is_error")
        if is_error:
            return {"error": text}, server_name

        structured = None
        for name_variant in ("structuredContent", "structured_content"):
            if hasattr(result, name_variant):
                structured = getattr(result, name_variant)
                break
        if structured is not None:
            return structured, server_name
        try:                                    # the tool returned a plain dict; parse the JSON text ourselves
            return _json.loads(text), server_name
        except (ValueError, TypeError):
            return {"result": text}, server_name

    async def close(self):
        await self.stack.aclose()
