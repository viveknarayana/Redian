import os
from redian_source.agents.redian_agent import RedianAgent
from redian_source.attacks.prompt_injection import PromptInjectionAttack

def test_prompt_injection():
    # Set up environment variables or replace with your actual values
    token = os.environ.get("TOKEN")
    mcp_image = os.environ.get("MCP_IMAGE", "mcp-url")
    mcp_token_name = os.environ.get("MCP_TOKEN_NAME", "mcp-token-name")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")

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
        model="gemini-2.0-flash"
    )

    attack = PromptInjectionAttack()
    result = attack.run(agent)
    print("Prompt Injection Attack Result:")
    print(result)

if __name__ == "__main__":
    test_prompt_injection() 