import os
from groq import Groq

class LLMAgent:
    """
    LLM agent that can use tools via a tool agent (e.g., MCPAgent).
    Supports Groq LLMs using the Groq SDK.
    """
    def __init__(self, model, tool_agent, groq_api_key=None):
        self.model = model
        self.tool_agent = tool_agent
        self.llm_tools = []
        self.llm_tool_summaries = []
        self.groq_api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("Groq API key must be provided via argument or GROQ_API_KEY env var.")
        self.groq = Groq(api_key=self.groq_api_key)
        # Fetch and store tools if tool_agent is provided
        self.fetch_and_store_tools()

    def fetch_and_store_tools(self):
        """
        Fetch tools from the tool agent (e.g., MCPAgent) and store both
        the full schemas and summaries for LLM use.
        """
        if not self.tool_agent:
            self.llm_tools = []
            self.llm_tool_summaries = []
            return
        raw_tools = self.tool_agent.list_tools()
        self.llm_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("inputSchema", {})
                }
            }
            for tool in raw_tools.get("tools", [])
        ]
        self.llm_tool_summaries = [
            {
                "name": tool["function"]["name"],
                "description": tool["function"]["description"]
            }
            for tool in self.llm_tools
        ]

    def send_prompt(self, prompt):
        """
        Send a prompt to the Groq LLM using the Groq SDK and return the response.
        """
        response = self.groq.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response

    def get_langchain_llm(self):
        from langchain_community.chat_models import ChatOpenAI
        return ChatOpenAI(
            openai_api_key=self.groq_api_key,
            openai_api_base="https://api.groq.com/openai/v1",
            model_name=self.model
        ) 