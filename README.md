# Redian: Red Teaming Python Framework for LLMs

Redian is a modular Python framework for automating red teaming and security evaluation of LLM agents, with support for multi-turn tool-based workflows, dynamic prompt injection attacks, and robust evaluation using Google Gemini.

---

## Features

- **Stateful LLM Agent**: The `RedianAgent` uses `langgraph` to orchestrate complex, multi-step tool interactions with Google Gemini.
- **Dynamic Tool Integration**: Seamlessly connects to one or more MCP (Model-Controlled-Process) servers to fetch and utilize external tools.
- **Sophisticated Attack Simulation**: The `PromptInjectionAttack` module uses a meta-LLM to dynamically craft context-aware attack payloads, probing for subtle vulnerabilities in agent logic.
- **Automated Evaluation**: An LLM-based judge automatically evaluates attack success by analyzing the agent's execution trace for logical consistency and task completion.
- **Extensible by Design**: Easily add new agents, attacks, and toolchains with minimal code.

---

## Installation

```bash
git clone https://github.com/yourusername/redian.git
cd redian
pip install -r requirements.txt
```

---

## Directory Structure

```
redian_source/
  agents/      # Core agent logic (RedianAgent)
  attacks/     # Attack modules (PromptInjectionAttack)
  config/      # Configuration files
  runner/      # Scripts for running agents and attacks
  tests/       # Unit and integration tests
```

---

## Quickstart

### 1. Set Up Environment

Create a `.env` file in your project root with your Google Gemini API key:

```
GEMINI_API_KEY=your-gemini-api-key
```

### 2. Define MCP Servers

Define your MCP server configurations. For example, in a Python script:

```python
mcp_servers = [
    {
        "name": "Github",
        "image": "ghcr.io/foundational-models/mcp/github:latest",
        "credentials": {
            "name": "github-pat",
            "value": os.environ.get("GITHUB_PAT")
        }
    }
]
```

### 3. Initialize the RedianAgent

The `RedianAgent` is the core of the framework. It connects to the specified MCP servers and prepares the tools for the LLM.

```python
import asyncio
from redian_source.agents.redian_agent import RedianAgent

async def main():
    agent = RedianAgent(
        mcp_servers=mcp_servers,
        gemini_api_key="YOUR_GEMINI_API_KEY"
    )
    await agent.setup()
    
    # The agent is now ready to run prompts
    result = await agent.run("Create a new GitHub repository named 'test-repo'.")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Dynamic Prompt Injection Attacks

Redian's main strength is its ability to simulate sophisticated, dynamic prompt injection attacks. The `PromptInjectionAttack` module uses a meta-LLM to generate a malicious prompt tailored to the agent's available tools.

```python
import asyncio
from redian_source.agents.redian_agent import RedianAgent
from redian_source.attacks.prompt_injection import PromptInjectionAttack

async def run_attack():
    # Initialize the agent
    agent = RedianAgent(
        mcp_servers=mcp_servers,
        gemini_api_key="YOUR_GEMINI_API_KEY",
        debug=True
    )

    # Initialize the attack
    attack = PromptInjectionAttack(
        gemini_api_key="YOUR_GEMINI_API_KEY",
        iterations=1,
        debug=True
    )

    # Run the attack (no payload needed, it will be generated dynamically)
    attack_result = await attack.run(agent)
    
    # Print the results
    attack_result.pretty_print()

if __name__ == "__main__":
    asyncio.run(run_attack())
```

The attack module will:
1.  Inspect the agent's tools.
2.  Use a meta-LLM to craft a malicious, multi-step prompt.
3.  Execute the prompt against the agent.
4.  Use a judge-LLM to evaluate if the agent's behavior was compromised.

---

## Testing

To run the integration tests:

```bash
python -m redian_source.tests.test_agents
```

---

## Requirements

- Python 3.8+
- Docker (for MCP tool access)
- Google Gemini API Key
- See `requirements.txt` for all dependencies.

---

## Vision

Automate red teaming for LLM agents, including multi-turn and tool-based attacks, to improve the security and robustness of AI systems.

---

## License

MIT