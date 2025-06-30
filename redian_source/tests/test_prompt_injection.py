import os
import json
from redian_source.agents.redian_agent import RedianAgent
from redian_source.attacks.prompt_injection import PromptInjectionAttack

def test_prompt_injection():
    # Set up environment variables or replace with your actual values
    token = os.environ.get("TOKEN")
    mcp_image = os.environ.get("MCP_IMAGE", "mcp-url")
    mcp_token_name = os.environ.get("MCP_TOKEN_NAME", "mcp-token-name")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    mcp_servers = {
        "default": {
            "command": "docker",
            "args": [
                "run", "-i", "--rm",
                "-e", f"{mcp_token_name}={token}",
                mcp_image
            ],
            "transport": "stdio",
        }
    }

    agent = RedianAgent(
        mcp_servers=mcp_servers,
        gemini_api_key=gemini_api_key,
        model="gemini-1.5-flash"
    )

    attack = PromptInjectionAttack(gemini_api_key=gemini_api_key, log_dir="./logs", iterations=1, debug=False)
    results = attack.run(agent)
    results.pretty_print()

if __name__ == "__main__":
    test_prompt_injection()