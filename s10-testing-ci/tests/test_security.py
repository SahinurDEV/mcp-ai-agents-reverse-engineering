"""10.6 security gate: our tools must have no red flags, and the poisoned fixture MUST be flagged.
If the fixture ever passes, the scanner is broken, so CI fails too (a canary for the gate itself)."""
import pytest
from mcp import Client

import redflags

pytestmark = pytest.mark.anyio


async def test_our_tools_have_no_red_flags(server):
    async with Client(server) as c:
        bad = {t.name: redflags.flags(t) for t in (await c.list_tools()).tools if redflags.flags(t)}
    assert not bad, f"red flags in our own tools: {bad}"


async def test_poisoned_fixture_is_caught():
    from tests import poisoned_fixture
    async with Client(poisoned_fixture.mcp) as c:
        tools = {t.name: redflags.flags(t) for t in (await c.list_tools()).tools}
    missed = set(redflags.RED_FLAGS) - set(tools["add"])     # the fixture trips every rule; each rule must still fire
    assert not missed, f"scanner rules no longer fire on the poisoned fixture: {sorted(missed)}"
