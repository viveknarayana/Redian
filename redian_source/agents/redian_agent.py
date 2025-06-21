import asyncio
from typing import TypedDict, Annotated, Sequence
import operator

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, END
from langgraph.prebuilt.tool_node import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

class RedianAgent:
    """
    High-level agent that wraps MCP tool integration and a stateful LangGraph
    orchestrator for robust, multi-step tool execution.
    """
    def __init__(self, mcp_servers, gemini_api_key, model="gemini-1.5-flash"):
        self.mcp_servers = mcp_servers
        self.gemini_api_key = gemini_api_key
        self.model = model
        self._agent = None
        self._tools = None
        self._llm = None
        self._setup_done = False
        self.client = None

    async def setup(self):
        """
        Asynchronously sets up the MCP client, tools, LLM, and the stateful agent graph.
        """
        print("[AGENT_SETUP] Initializing agent setup...")
        self.client = MultiServerMCPClient(self.mcp_servers)
        self._tools = await self.client.get_tools()
        print(f"[AGENT_SETUP] Successfully loaded {len(self._tools)} tools.")

        if not self.gemini_api_key:
            raise ValueError("gemini_api_key must be provided to RedianAgent.")
        
        self._llm = ChatGoogleGenerativeAI(
            google_api_key=self.gemini_api_key,
            model=self.model
        )
        
        # Bind the tools to the LLM so it knows how to call them
        llm_with_tools = self._llm.bind_tools(self._tools)

        # Define the nodes for the graph
        def should_continue(state: AgentState):
            last_message = state['messages'][-1]
            # If the LLM made a tool call, keep going. Otherwise, finish.
            if last_message.tool_calls:
                return "continue"
            return "end"

        def call_model(state: AgentState):
            print("[GRAPH] Calling model...")
            response = llm_with_tools.invoke(state['messages'])
            # We return a list, because we want to add it to the state
            return {"messages": [response]}

        # The new agent is a stateful graph
        workflow = StateGraph(AgentState)
        
        # Add the nodes
        workflow.add_node("agent", call_model)
        tool_node = ToolNode(self._tools)
        workflow.add_node("action", tool_node)

        # Define the edges
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "action",
                "end": END,
            },
        )
        workflow.add_edge('action', 'agent')
        
        self._agent = workflow.compile()
        self._setup_done = True
        print("[AGENT_SETUP] Agent setup complete. Graph compiled.")

    async def run(self, prompt):
        """
        Asynchronously run the agent on the given prompt.
        """
        if not self._setup_done:
            await self.setup()
        
        inputs = {"messages": [HumanMessage(content=prompt)]}
        # The final state is returned, we extract the messages
        final_state = await self._agent.ainvoke(inputs)
        return {"messages": final_state['messages']}

    # Synchronous and streaming methods remain for compatibility
    def run_sync(self, prompt):
        return asyncio.run(self.run(prompt))

    def stream_sync(self, prompt, stream_mode="updates"):
        # Note: True streaming with the new graph requires a slightly different setup.
        # This implementation will yield the final result for compatibility.
        # For true streaming, we would use `astream_events`.
        final_result = self.run_sync(prompt)
        yield final_result

    def stream(self, prompt, stream_mode="updates"):
        """
        Synchronously stream agent updates for the given prompt. Yields each chunk as it is produced.
        Usage:
            for chunk in agent.stream("what is the weather in sf"): print(chunk)
        """
        if not self._setup_done:
            asyncio.run(self.setup())
        # Accept both string and dict/list for prompt
        if isinstance(prompt, str):
            inputs = {"messages": [{"role": "user", "content": prompt}]}
        else:
            inputs = prompt
        for chunk in self._agent.stream(inputs, stream_mode=stream_mode):
            yield chunk

    async def astream(self, prompt, stream_mode="updates"):
        """
        Asynchronously stream agent updates for the given prompt. Yields each chunk as it is produced.
        Usage:
            async for chunk in agent.astream("what is the weather in sf"): print(chunk)
        """
        if not self._setup_done:
            await self.setup()
        # Accept both string and dict/list for prompt
        if isinstance(prompt, str):
            inputs = {"messages": [{"role": "user", "content": prompt}]}
        else:
            inputs = prompt
        async for chunk in self._agent.astream(inputs, stream_mode=stream_mode):
            yield chunk

    def stream_sync(self, prompt, stream_mode="updates"):
        """
        Synchronously stream agent updates for the given prompt, bridging async to sync.
        Usage:
            for chunk in agent.stream_sync("prompt"): print(chunk)
        """
        import queue, threading
        q = queue.Queue()
        sentinel = object()

        def run():
            async def runner():
                async for chunk in self.astream(prompt, stream_mode=stream_mode):
                    q.put(chunk)
                q.put(sentinel)
            asyncio.run(runner())

        t = threading.Thread(target=run)
        t.start()
        while True:
            item = q.get()
            if item is sentinel:
                break
            yield item
        t.join()

