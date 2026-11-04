# Claims Triage & Coverage Assistant
## Week 12 — MCP-Based Agent

An AI-powered claims triage assistant that retrieves claim information, checks policy details, searches relevant policy wording, and prepares claims for human adjuster review.

The system uses a Gemini-powered agent, Model Context Protocol (MCP) servers, semantic policy wording retrieval, and deterministic local compliance tools.

**Important:** The agent does not make final coverage decisions or calculate claim payouts. Its final action is to refer the claim to a human adjuster.

---

## Technology Stack

- Python
- Google Gemini 3.1 Flash-Lite
- Model Context Protocol (MCP)
- FastMCP
- Sentence Transformers (all-MiniLM-L6-v2)
- Cross-Encoder reranking
- Qdrant / policy wording retrieval components
- JSON-based policy configuration
- python-dotenv

---

## Architecture

The application uses two MCP servers and a set of local compliance tools.

```text
                 Claims Triage Agent
                       |
                  Gemini LLM
                       |
                    MCP Client
                       |
          +------------+-------------+
          |                          |
          v                          v
     Claims System             Policy Document
       MCP Server                Search MCP Server
          |                          |
          v                          v
      get_claim()             search_policy_wording()
          |                          |
          +------------+-------------+
                       |
                       v
             Local Compliance Tools
                       |
          +------------+-------------+
          |            |             |
          v            v             v
      lookup_policy  check_coverage  refer_to_adjuster
                       |
                       v
                Final Referral
                 to Adjuster
```

### MCP Servers

**1. Claims System — `mcp_servers/claims_server.py`**

Exposes:
- `get_claim(claim_id)`

Retrieves claim details from the claims data source.

**2. Policy Document Search — `mcp_servers/policy_server.py`**

Exposes:
- `search_policy_wording(query, product, loss_date)`

Searches policy wording and returns relevant excerpts, including chunk IDs, policy form numbers, edition dates, clauses, and text.

### Local Compliance Tools

Implemented in `triage_tools.py`:

| Tool | Responsibility |
|---|---|
| `lookup_policy` | Retrieves product, policy period, and available sub-limits |
| `check_coverage_in_force` | Checks whether the policy was active on the loss date |
| `refer_to_adjuster` | Validates evidence and prepares the adjuster referral |

The compliance tools enforce rules in code rather than relying only on instructions given to the LLM.

---

## Project Structure

```text
.
├── agent_mcp.py
├── mcp_client.py
├── mcp_config.json
│
├── mcp_servers/
│   ├── claims_server.py
│   └── policy_server.py
│
├── triage_tools.py
├── policy_rules.py
├── policy_table.json
│
├── claims_data.py
├── wording_store.py
├── chunkers.py
│
├── data/
│   ├── endorsements/
│   └── policy_wordings/
│
├── claim_llm.py
├── generate.py
│
├── test_triage_tools.py
├── test_policy_rules.py
│
├── requirements.txt
├── .env.example
└── README.md
```

### Important Files

- `agent_mcp.py` — Main MCP-based agent loop, tool orchestration, budget enforcement, and final output.
- `mcp_client.py` — Dynamically connects to configured MCP servers, discovers tools, and dispatches tool calls.
- `mcp_config.json` — Defines the MCP servers and their commands.
- `triage_tools.py` — Implements deterministic compliance checks and adjuster referral validation.
- `policy_rules.py` — Handles policy periods, effective editions, deductibles, sub-limits, and policy limits.
- `policy_table.json` — Contains sample policy and product data.
- `claims_data.py` — Contains sample claim records.
- `wording_store.py` — Retrieves and ranks policy wording excerpts.
- `claim_llm.py` — Shared Gemini call, token tracking, and cost calculation utilities.

---

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install mcp
```

The MCP Python SDK is installed separately because it is not currently listed in the project's `requirements.txt`.

### 3. Configure Gemini API key

Create your `.env` file:

```bash
cp .env.example .env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

Get an API key from:

https://aistudio.google.com/

Do not commit `.env` or expose your API key.

### 4. Verify MCP configuration

The `mcp_config.json` file defines the two MCP servers:

```json
{
  "servers": [
    {
      "name": "policy-document-search",
      "command": "python3",
      "args": ["mcp_servers/policy_server.py"]
    },
    {
      "name": "claims-system",
      "command": "python3",
      "args": ["mcp_servers/claims_server.py"]
    }
  ]
}
```

The MCP client starts the configured servers and discovers their available tools dynamically.

Run commands from the project root directory.

---

## Running the Agent

Run the agent with a claim ID and its policy number:

```bash
python agent_mcp.py CLM-2026-00004 POL-HO-1003
```

The agent follows this workflow:

1. Retrieve the claim using `get_claim`.
2. Retrieve policy details using `lookup_policy`.
3. Check whether the policy was active on the loss date.
4. Search relevant policy wording using the policy search MCP server.
5. Validate the evidence and refer the claim to an adjuster.

The agent stops when the claim is successfully referred or when a configured budget limit is reached.

**Note:** The claim ID and policy number must be valid entries in the sample data. The sample data does not establish a verified claim-to-policy relationship. Use the correct policy number for real claim processing.

---

## Agent Budgets

The agent enforces four limits inside its execution loop.

| Budget | Default limit |
|---|---:|
| Maximum iterations | 8 |
| Maximum tokens | 20,000 |
| Maximum cost | $0.05 |
| Maximum execution time | 90 seconds |

These limits prevent the agent from running indefinitely or exceeding its configured resource budget.

### Customize budgets

```bash
python agent_mcp.py CLM-2026-00004 POL-HO-1003 \
  --max-iters 2 \
  --max-tokens 5000 \
  --max-cost 0.01 \
  --max-seconds 30
```

Available arguments:

- `--max-iters`
- `--max-tokens`
- `--max-cost`
- `--max-seconds`

### View command options

```bash
python agent_mcp.py --help
```

---

## Compliance and Safety Rules

The local compliance tools enforce the following:

- Policy dates are validated.
- Policy coverage periods are checked using inclusive date boundaries.
- The policy wording edition is resolved based on the loss date.
- Only retrieved policy wording chunk IDs can be cited.
- The cited wording must match the product and applicable edition.
- Referral summaries and reasons must not contain final coverage decisions or payout conclusions.
- A referral requires the necessary policy and wording checks.
- An expired policy can still be referred for human review.
- The system does not independently approve or reject claims.

The adjuster referral is a handoff for human review, not a final insurance coverage determination.

---

## Testing

The project includes two standalone test scripts.

### 1. Test compliance tools

```bash
python test_triage_tools.py
```

### 2. Test policy rules

```bash
python test_policy_rules.py
```

These scripts use direct Python checks rather than pytest test functions.

### 3. Check Python syntax

```bash
python -m py_compile agent_mcp.py mcp_client.py triage_tools.py policy_rules.py
```

### 4. Check agent command-line options

```bash
python agent_mcp.py --help
```

---

## Sample Final Output

A successful referral produces an output similar to:

```json
{
  "action": "REFER_TO_ADJUSTER",
  "policy_number": "POL-HO-1003",
  "product": "HO3",
  "policy_in_force": false,
  "wording_resolved_against": {
    "form_number": "HO-0125 ed. 03-25",
    "edition_date": "2025-03-01"
  },
  "citations": [
    "HO3-2025.txt:structured:1"
  ],
  "deductible": 500,
  "sub_limit": {
    "name": "water_damage",
    "amount": 15000
  },
  "policy_limit": 250000
}
```

The example is illustrative. Actual citations and referral details are populated from the tools during execution.

The final agent result also includes:
- Claim ID
- Policy number
- Termination reason
- Model call count
- Input and output tokens
- Total token usage
- Estimated LLM cost
- Execution time
- Tool execution trajectory
- MCP discovery log

---

## Notes

- Sample claims and policy records are used for this implementation.
- Gemini API access is required to run the LLM-powered agent.
- MCP servers communicate with the client using standard input/output.
- Policy wording retrieval uses the policy documents available under `data/policy_wordings/`.
- The older Week 3 RAG and Week 7 agent files remain in the repository for earlier implementation stages. The main Week 12 entry point is `agent_mcp.py`.EOF
