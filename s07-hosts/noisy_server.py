"""noisy_server.py: a broken server that prints a banner to stdout, which corrupts the JSON-RPC stream."""
from mcp.server.mcpserver import MCPServer

print("notes server starting...")            # BUG: stdout is the protocol channel; log to stderr instead

mcp = MCPServer("noisy")


@mcp.tool()
def ping() -> str:
    return "pong"


if __name__ == "__main__":
    mcp.run()
