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
        self.groq_api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("Groq API key must be provided via argument or GROQ_API_KEY env var.")
        self.groq = Groq(api_key=self.groq_api_key)

    def send_prompt(self, prompt):
        """
        Send a prompt to the Groq LLM using the Groq SDK and return the response.
        """
        response = self.groq.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response 