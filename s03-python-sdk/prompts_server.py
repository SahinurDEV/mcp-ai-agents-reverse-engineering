"""prompts_server.py - lecture 3.6: prompts as user-selected templates."""
from mcp.server import MCPServer
from mcp.server.mcpserver.prompts.base import AssistantMessage, UserMessage

mcp = MCPServer("re-prompts")

@mcp.prompt()
def triage_binary(binary: str, focus: str = "strings") -> list:
    """Start a careful first look at a course CrackMe."""
    return [
        UserMessage(f"Triage the course CrackMe {binary}. Focus on {focus}."),
        AssistantMessage("I will list functions first, then decompile main, and quote code for every claim."),
        UserMessage("Good. Stop and ask before running the binary."),
    ]

@mcp.prompt(title="Explain a decompiled function")
def explain_function(code: str) -> str:
    """Explain pseudocode line by line for a beginner."""
    return f"Explain this decompiled C for a beginner, line by line:\n\n{code}"

if __name__ == "__main__":
    mcp.run()
