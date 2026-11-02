"""ex_xrefs.py: Exercise 18. re-assist-mcp plus one more read-only tool, who_calls.
It goes through the same scope gate as every other tool, so it cannot reach outside the course folder."""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "re_assist"))
import server
from server import RO, ToolError, gate, ghidra, mcp


@mcp.tool(annotations=RO)
async def who_calls(binary: str, function: str) -> list[dict]:
    """Callers of FUNCTION in BINARY (imports like strcmp included), as {caller, at}.
    Answers 'where is the check?' without decompiling every function."""
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,63}", function):
        raise ToolError("function must be a plain identifier")
    p = gate(binary)
    funcs = json.loads(await ghidra(p, "list_functions", {})).get("items", [])
    addrs = [f["address"] for f in funcs if f["name"].split("::")[-1] == function]
    if not addrs:
        raise ToolError(f"no function named {function} in {binary}; call list_functions")
    out = []
    for a in addrs:                                   # an import has a thunk and an external entry
        for x in json.loads(await ghidra(p, "get_xrefs_to", {"address": a})).get("items", []):
            caller = (x.get("from_function") or {}).get("name", "")
            if "CALL" in x.get("type", "") and caller and not caller.startswith("<EXTERNAL>"):  # skip the thunk -> import link
                out.append({"caller": x["from_function"]["name"], "at": x["from"]})
    return out


if __name__ == "__main__":
    mcp.run()
