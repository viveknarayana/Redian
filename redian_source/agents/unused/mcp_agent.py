import subprocess
import os
import json

class MCPAgent:
    """
    Agent for interacting with an MCP server via Docker/stdio.
    """
    def __init__(self, token, mcp_image, MCP_TOKEN_NAME):
        self.token = token
        self.mcp_image = mcp_image
        self.MCP_TOKEN_NAME = MCP_TOKEN_NAME
        self.proc = subprocess.Popen(
            [
                "docker", "run", "-i", "--rm",
                "-e", f"{MCP_TOKEN_NAME}={token}", # CHANGE THE GITHUB PERSONAL ACCESS TOKEN TO AN ENV
                mcp_image
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    def list_tools(self):
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
        self.proc.stdin.write(json.dumps(request) + '\n')
        self.proc.stdin.flush()
        response_line = self.proc.stdout.readline()
        try:
            response = json.loads(response_line)
            return response.get("result", response)
        except Exception as e:
            raise RuntimeError(f"Error parsing response: {e}\nRaw: {response_line}")
    def terminate(self):
        self.proc.terminate()
    def call_tool(self, tool_name, args):
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args
            }
        }
        self.proc.stdin.write(json.dumps(request) + '\n')
        self.proc.stdin.flush()
        response_line = self.proc.stdout.readline()
        try:
            response = json.loads(response_line)
            return response.get("result", response)
        except Exception as e:
            return {"error": str(e), "raw": response_line} 