"""bad_path.py: a client pointing at a server file that does not exist."""
import sys

import anyio
from mcp import Client, StdioServerParameters

SERVER = StdioServerParameters(command=sys.executable, args=["../s05/notes_mpc.py"])


async def main():
    async with Client(SERVER) as c:
        print(await c.list_tools())


anyio.run(main)
