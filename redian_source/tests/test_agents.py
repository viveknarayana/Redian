import os
import traceback
from redian_source.agents.redian_agent import RedianAgent

def test_redian_agent():
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
    print("Streaming RedianAgent result:")
    for chunk in agent.stream_sync(
        "Get my github repositories. Use chain of thought and tool outputs to chain together calls to get necessary information."
    ):
        print(chunk)

if __name__ == "__main__":
    try:
        print("Running RedianAgent integration test...")
        test_redian_agent()
        print("RedianAgent test passed.\n")
    except Exception as e:
        traceback.print_exc()
        print(f"RedianAgent test failed: {e}\n") 