from langchain.tools import Tool

def make_langchain_tools_from_mcp(llm_agent, mcp_agent):
    tools = []
    for tool_schema in llm_agent.llm_tools:
        name = tool_schema["function"]["name"]
        description = tool_schema["function"]["description"]
        def make_tool_func(tool_name):
            def tool_func(args):
                return mcp_agent.call_tool(tool_name, args)
            return tool_func
        tools.append(
            Tool(
                name=name,
                func=make_tool_func(name),
                description=description
            )
        )
    return tools 