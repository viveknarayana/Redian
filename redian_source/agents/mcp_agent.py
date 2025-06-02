import subprocess
import os
import json

class MCPAgent:
    """
    Agent for interacting with an MCP server via Docker/stdio.
    """
    def __init__(self, token, mcp_image):
        self.token = token
        self.mcp_image = mcp_image
        self.proc = subprocess.Popen(
            [
                "docker", "run", "-i", "--rm",
                "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={token}",
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