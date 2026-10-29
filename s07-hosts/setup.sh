#!/bin/sh
# setup.sh: write the Section 7 host config files with absolute paths for this machine
cd "$(dirname "$0")"; HERE=$PWD; NOTES_SERVER=$(cd ../s05-notes-mcp 2>/dev/null || cd ../s05; pwd)/notes_mcp.py
rm -rf sandbox; mkdir -p proj/.cursor proj/.vscode sandbox
echo "scoped file" > sandbox/readme.txt
(cd proj && ../reset_notes.sh >/dev/null); ./reset_notes.sh >/dev/null
cat > claude_desktop_config.json <<J
{
  "mcpServers": {
    "notes": {
      "command": "python3",
      "args": ["$NOTES_SERVER"],
      "env": { "NOTES_DIR": "$HERE/notes" }
    }
  }
}
J
cat > proj/.cursor/mcp.json <<J
{
  "mcpServers": {
    "notes": {
      "command": "python3",
      "args": ["$NOTES_SERVER"],
      "env": { "NOTES_DIR": "\${workspaceFolder}/notes" }
    }
  }
}
J
cat > proj/.vscode/mcp.json <<J
{
  "servers": {
    "notes": {
      "type": "stdio",
      "command": "python3",
      "args": ["$NOTES_SERVER"],
      "env": { "NOTES_DIR": "\${workspaceFolder}/notes" }
    }
  }
}
J
cat > host.json <<J
{
  "mcpServers": {
    "files": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem@2.1.0", "$HERE/sandbox"]
    },
    "docs": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@4.4.4"]
    }
  }
}
J
echo "configs written"
# broken configs for 7.6
mkdir -p broken
sed 's#s05/notes_mcp.py#s05/note_mcp.py#' claude_desktop_config.json > broken/wrong_path.json
sed 's#"python3"#"python"#' claude_desktop_config.json > broken/wrong_command.json
sed 's#}$#},#' claude_desktop_config.json | sed '$!N;s/},\n  }/}\n  },/;P;D' > /dev/null
printf '{\n  "mcpServers": {\n    "notes": {\n      "command": "python3",\n      "args": ["%s"],\n    }\n  }\n}\n' "$NOTES_SERVER" > broken/trailing_comma.json
sed "s#$NOTES_SERVER#$HERE/noisy_server.py#" claude_desktop_config.json > broken/stdout_print.json
