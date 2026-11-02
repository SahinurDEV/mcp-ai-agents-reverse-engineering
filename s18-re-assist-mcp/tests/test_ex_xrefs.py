"""Exercise 18 tests: who_calls is gated like every other tool (no Ghidra needed for the refusals)."""
import os, sys, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mcp import Client
import ex_xrefs

pytestmark = pytest.mark.anyio

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.parametrize("binary", ["../s16-crackmes-b/inbox/trackb-easy-1.0/tb_lic", "/bin/ls", "nope"])
async def test_who_calls_refuses_out_of_scope(binary):
    async with Client(ex_xrefs.mcp) as c:
        r = await c.call_tool("who_calls", {"binary": binary, "function": "strcmp"})
        assert r.is_error and "refused" in r.content[0].text

async def test_who_calls_rejects_odd_function_names():
    async with Client(ex_xrefs.mcp) as c:
        r = await c.call_tool("who_calls", {"binary": "cm_strcmp", "function": "x; rm -rf /"})
        assert r.is_error and "plain identifier" in r.content[0].text

async def test_who_calls_is_read_only():
    async with Client(ex_xrefs.mcp) as c:
        t = {t.name: t for t in (await c.list_tools()).tools}["who_calls"]
        assert t.annotations.read_only_hint is True
