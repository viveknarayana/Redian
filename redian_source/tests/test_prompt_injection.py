import os
import json
from redian_source.agents.redian_agent import RedianAgent
from redian_source.attacks.prompt_injection import PromptInjectionAttack

def pretty_print_result(result):
    """
    Custom print function to handle the complex result object and display it clearly,
    including a full trace of the agent's execution.
    """
    print("--- Dynamic Prompt Injection Attack Result ---")
    
    # Print the attack type and the meta prompt used to generate the payload
    print("\n[Attack Type]:", result.get('attack'))
    print("\n[Meta Prompt Used to Generate Payload]:")
    print("-" * 40)
    print(result.get('meta_prompt', 'Not available.'))
    print("-" * 40)

    # Print the final malicious payload sent to the agent
    print("\n[Final Payload Sent to Agent]:")
    print("-" * 40)
    print(result.get('payload', 'Not available.'))
    print("-" * 40)

    # Extract and print the agent's execution trace
    agent_result = result.get('result', {})
    messages = agent_result.get('messages', [])
    
    print("\n[Agent's Full Execution Trace]:")
    print("-" * 40)

    if messages:
        for i, msg in enumerate(messages):
            msg_class = msg.__class__.__name__
            
            if msg_class == "HumanMessage":
                print(f"\n>> Step {i}: User Input\n")
                print(msg.content)
            
            elif msg_class == "AIMessage":
                print(f"\n>> Step {i}: Agent's Thought\n")
                # Don't print empty AI messages which are just tool calls
                if msg.content:
                    print(msg.content)
                
                if msg.tool_calls:
                    print("\n   Tool Calls:")
                    for tc in msg.tool_calls:
                        args_str = json.dumps(tc['args'], indent=2)
                        print(f"   - Function: {tc['name']}\n     Args: {args_str}")

            elif msg_class == "ToolMessage":
                print(f"\n>> Step {i}: Tool Output (for call id: {msg.tool_call_id})\n")
                print(msg.content)

            # Print a separator unless it's the last message
            if i < len(messages) - 1:
                print("\n" + "-" * 20)

    else:
        # Fallback for unexpected structure
        def default_serializer(o):
            return f"<non-serializable: {type(o).__qualname__}>"
        print(json.dumps(agent_result, indent=2, default=default_serializer))
    
    print("\n" + "-" * 40)


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

    # The attack now requires the api key to power its meta-llm
    attack = PromptInjectionAttack(gemini_api_key=gemini_api_key, log_dir="./logs")
    
    result = attack.run(agent)
    pretty_print_result(result)
    print(result["verdict"])

if __name__ == "__main__":
    test_prompt_injection() 