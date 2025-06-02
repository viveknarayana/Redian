class LLMAgent:
    """
    Stub for an LLM agent that can use tools via a tool agent (e.g., MCPAgent).
    """
    def __init__(self, model, tool_agent):
        self.model = model
        self.tool_agent = tool_agent 