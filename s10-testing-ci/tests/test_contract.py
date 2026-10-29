"""10.4 contract tests: the tool list the model sees is pinned in tools.schema.json.
Any change to a name, description or schema fails CI until the snapshot is updated on purpose:
    UPDATE_SCHEMA=1 pytest tests/test_contract.py"""
import json
import os
from pathlib import Path

import pytest
from mcp import Client

SNAP = Path(__file__).parent.parent / "tools.schema.json"
pytestmark = pytest.mark.anyio


async def current(server) -> dict:
    async with Client(server) as c:
        return {t.name: {"description": t.description, "inputSchema": t.input_schema, "outputSchema": t.output_schema}
                for t in (await c.list_tools()).tools}


async def test_tools_match_snapshot(server):
    now = await current(server)
    if os.environ.get("UPDATE_SCHEMA"):
        SNAP.write_text(json.dumps(now, indent=1, sort_keys=True) + "\n")
    pinned = json.loads(SNAP.read_text())
    assert sorted(now) == sorted(pinned), "tools were added or removed"
    for name in pinned:
        assert now[name] == pinned[name], f"contract changed for {name}; review, then UPDATE_SCHEMA=1"


async def test_every_input_property_is_typed(server):
    for name, spec in (await current(server)).items():
        for prop, s in spec["inputSchema"].get("properties", {}).items():
            assert "type" in s, f"{name}.{prop} has no type"
