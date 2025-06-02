import argparse
import os
import subprocess
import sys
import json
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

def list_tools_stdio(token: str, mcp_image: str):
    print(f"Starting MCP server via Docker (image: {mcp_image}) and listing tools...")
    docker_cmd = [
        "docker", "run", "-i", "--rm",
        "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={token}",
        mcp_image
    ]
    proc = subprocess.Popen(
        docker_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    request = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    proc.stdin.write(json.dumps(request) + '\n')
    proc.stdin.flush()
    response_line = proc.stdout.readline()
    try:
        response = json.loads(response_line)
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}\nRaw: {response_line}")
    proc.terminate()

def main():
    load_dotenv()
    token = os.environ.get('TOKEN')
    mcp_image = os.environ.get('MCP_IMAGE')
    if not token or not mcp_image:
        print("Please set TOKEN and MCP_IMAGE in your .env file.")
        sys.exit(1)
    list_tools_stdio(token, mcp_image)

if __name__ == "__main__":
    main() 