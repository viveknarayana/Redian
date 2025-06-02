# Redian: Red Teaming Python Framework for LLMs

## Getting Started

### 1. Start a Local MCP Server (Node.js)

You need to have Node.js and the MCP server installed (e.g., via @modelcontextprotocol/sdk).

Start the MCP server in a separate terminal:

```bash
node /Users/viveknarayana/Desktop/Projects/Google-MCP/build/index.js
```

By default, this will start the MCP server on `http://localhost:8080`.

### 2. List Tools from Python

In another terminal, from your Redian project directory, run:

```bash
python -m redian_source.runner.list_mcp_tools http://localhost:8080
```

This will connect to the running MCP server and list available tools.

---

## Advanced: Launching MCP Server from Python

You can also use the `MCPClient` helper to launch the Node.js MCP server automatically (see code in `redian_source/agents/mcp_client.py`).

This is a red teaming python framework for LLMs with tool/MCP access.

## Vision
Automate red teaming for LLM agents, including multi-turn and tool-based attacks.

## Structure
- agents/: Adapters for OpenAI, MCP, REST, etc.
- attacks/: Attack modules (prompt injection, jailbreak, etc.)
- tests/: Integration and unit tests
- config/: YAML/JSON configs for tools, endpoints, attacks
- runner/: CLI and automation scripts
