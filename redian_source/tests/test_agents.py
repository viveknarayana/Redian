import os
from dotenv import load_dotenv

try:
    load_dotenv()
except ImportError:
    # Fallback: simple .env parser
    def load_dotenv():
        if os.path.exists('.env'):
            with open('.env') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        k, v = line.strip().split('=', 1)
                        os.environ[k] = v
    load_dotenv()

from redian_source import MCPAgent, LLMAgent

def test_mcp_agent_list_tools_real():
    token = os.environ.get("TOKEN")
    mcp_image = os.environ.get("MCP_IMAGE", "ghcr.io/github/github-mcp-server")
    mcp_token_name = os.environ.get("MCP_TOKEN_NAME", "GITHUB_PERSONAL_ACCESS_TOKEN")
    agent = MCPAgent(token=token, mcp_image=mcp_image, MCP_TOKEN_NAME=mcp_token_name)
    print("Agent created")
    tools = agent.list_tools()
    print("MCP tools:", tools)
    agent.terminate()

def test_llm_agent_send_prompt_real():
    groq_api_key = os.environ.get("GROQ_API_KEY")
    token = os.environ.get("TOKEN")
    mcp_image = os.environ.get("MCP_IMAGE", "ghcr.io/github/github-mcp-server")
    mcp_token_name = os.environ.get("MCP_TOKEN_NAME", "GITHUB_PERSONAL_ACCESS_TOKEN")
    tool_agent = MCPAgent(token=token, mcp_image=mcp_image, MCP_TOKEN_NAME=mcp_token_name)
    llm_agent = LLMAgent(model="gemma2-9b-it", tool_agent=tool_agent, groq_api_key=groq_api_key)
    print("Groq tools:", llm_agent.llm_tools)
    print("Groq tool summaries:", llm_agent.llm_tool_summaries)
    tool_agent.terminate()

if __name__ == "__main__":
    try:
        print("Running MCPAgent integration test...")
        test_mcp_agent_list_tools_real()
        print("MCPAgent test passed.\n")
    except Exception as e:
        print(f"MCPAgent test failed: {e}\n")
    try:
        print("Running LLMAgent integration test...")
        test_llm_agent_send_prompt_real()
        print("LLMAgent test passed.\n")
    except Exception as e:
        print(f"LLMAgent test failed: {e}\n") 