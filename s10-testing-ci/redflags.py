"""redflags.py: the Section 8 red-flag rules as a library, so tests and CI can use them."""
import json
import re

RED_FLAGS = {
    "hidden-instruction tag": r"<\s*(important|system|instructions?)\s*>",
    "secrecy request": r"do not (mention|tell|show)|don'?t (mention|tell)",
    "file or secret access": r"secret|password|token|\.ssh|\.env|api[_ ]key|credentials?",
    "other tools or servers": r"before using|instead of|other tool|when calling",
}


def flags(tool) -> list[str]:
    text = (tool.description or "") + " " + json.dumps(tool.input_schema)
    return [name for name, rx in RED_FLAGS.items() if re.search(rx, text, re.I)]
