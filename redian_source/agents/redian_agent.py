import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

class RedianAgent:
    """
    High-level agent that wraps MCP tool integration and LangGraph orchestration using langchain-mcp-adapters.
    Usage:
        agent = RedianAgent(
            mcp_servers={...},
            groq_api_key=..., 
            model="model_name"
        )
        result = agent.run_sync("Do something with tools!")
    """
    def __init__(self, mcp_servers, groq_api_key, model="meta-llama/llama-4-maverick-17b-128e-instruct"):
        self.mcp_servers = mcp_servers
        self.groq_api_key = groq_api_key
        self.model = model
        self._agent = None
        self._tools = None
        self._llm = None
        self._setup_done = False

    async def setup(self):
        """
        Asynchronously set up the MCP client, tools, LLM, and agent.
        """
        client = MultiServerMCPClient(self.mcp_servers)
        self._tools = await client.get_tools()
        #print(self._tools)
        self._llm = ChatOpenAI(
            openai_api_key=self.groq_api_key,
            openai_api_base="https://api.groq.com/openai/v1",
            model_name=self.model
        )
        self._agent = create_react_agent(self._llm, self._tools)
        self._setup_done = True

    async def run(self, prompt):
        """
        Asynchronously run the agent on the given prompt.
        """
        if not self._setup_done:
            await self.setup()
        result = await self._agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
        return result

    def run_sync(self, prompt):
        """
        Synchronously run the agent on the given prompt (for convenience in scripts/tests).
        """
        return asyncio.run(self.run(prompt))

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

