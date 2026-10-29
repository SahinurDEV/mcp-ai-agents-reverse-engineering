"""mrtr_peek.py: a tool that needs user input mid-call, seen at the protocol level (2026-07-28)."""
from typing import Annotated

import sys

import anyio
from pydantic import BaseModel

from mcp import Client
from mcp.server.mcpserver import Elicit, MCPServer, Resolve
from mcp.types import ElicitResult

mcp = MCPServer("mrtr-peek")


class Confirm(BaseModel):
    confirm: bool


def ask_confirm() -> Elicit[Confirm]:
    return Elicit("Really delete all notes?", Confirm)


@mcp.tool()
async def notes_purge(answer: Annotated[Confirm, Resolve(ask_confirm)]) -> str:
    """Delete every note, after asking the user to confirm."""
    return "purged 3 notes" if answer.confirm else "cancelled; nothing deleted"


async def on_elicit(context, params):
    if sys.argv[1:] == ["decline"]:
        print(f"  client asked the user: {params.message!r} -> user closed the dialog")
        return ElicitResult(action="decline")
    yes = sys.argv[1:] == ["yes"]
    print(f"  client asked the user: {params.message!r} -> answering confirm={yes}")
    return ElicitResult(action="accept", content={"confirm": yes})


async def main():
    async with Client(mcp, elicitation_callback=on_elicit) as c:
        print("protocol:", c.protocol_version)
        first = await c.session.call_tool("notes_purge", {}, allow_input_required=True)
        print("first leg:", type(first).__name__, "| input_requests:", list(first.input_requests))
        req = first.model_dump(by_alias=True, mode="json")["inputRequests"]["__main__:ask_confirm"]
        print("asks via:", req["method"], "| schema:", req["params"]["requestedSchema"]["properties"])
        print("request_state present:", first.request_state is not None)
        r = await c.call_tool("notes_purge", {})
        print("final result:", r.content[0].text)


anyio.run(main)
