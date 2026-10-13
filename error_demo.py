"""
Week 9 - the SAME failing call (search_policy with an empty query) against the BEFORE and AFTER
versions of the tool. Gets the real raw tool-side error message from each, then asks Gemini
(in one plain, real message - no fabricated history) what it would do next on seeing each.

    python error_demo.py
"""
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from claim_llm import call_llm


async def get_tool_error(script):
    params = StdioServerParameters(command="python3", args=[script])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("search_policy", {"query": ""})
            return result.content[0].text if result.content else ""


def ask_model_to_react(tool_error_text):
    prompt = (
        "You are triaging an insurance claim. You tried to call the search_policy tool with an "
        "empty query and got back this result from the tool:\n\n"
        f'"{tool_error_text}"\n\n'
        "In 1-2 sentences, what do you do next? Be specific: if you now know what went wrong, "
        "say what you would call instead."
    )
    response, _, _, _ = call_llm(prompt, {"temperature": 0})
    return response.text


async def main():
    results = {}
    for label, script in [("before", "mcp_servers/policy_server_before.py"),
                          ("after", "mcp_servers/policy_server.py")]:
        tool_error = await get_tool_error(script)
        model_reaction = ask_model_to_react(tool_error)
        results[label] = {"tool_error_shown_to_model": tool_error, "model_reaction": model_reaction}
        print(f"\n=== {label.upper()} ===")
        print("tool error text:", tool_error)
        print("model's reaction:", model_reaction)

    with open("error_before_after.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved error_before_after.json")


if __name__ == "__main__":
    asyncio.run(main())
