"""lab/fix_readonly.py: turn an OSError on save into a clear tool error, and bump the version to 1.0.1."""
from pathlib import Path

src = Path("src/notes_mcp/server.py")
s = src.read_text()
old = '    path.write_text(f"# {title}\\n\\n{body}\\n")\n'
new = ('    try:\n'
       '        path.write_text(f"# {title}\\n\\n{body}\\n")\n'
       '    except OSError as e:\n'
       '        raise ToolError(f"cannot save note \'{note_id}\': {e.strerror}; the notes folder may be read-only")\n')
assert old in s, "already fixed?"
src.write_text(s.replace(old, new).replace('__version__ = "1.0.0"', '__version__ = "1.0.1"'))
p = Path("pyproject.toml")
p.write_text(p.read_text().replace('version = "1.0.0"', 'version = "1.0.1"'))
print("patched server.py and pyproject.toml to 1.0.1")
