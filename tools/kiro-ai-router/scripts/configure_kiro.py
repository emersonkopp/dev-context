"""Merge MCP configuration without overwriting existing servers."""
import json
import sys
from pathlib import Path

python = sys.argv[1]
path = Path.home() / '.kiro/settings/mcp.json'
path.parent.mkdir(parents=True, exist_ok=True)
data = json.loads(path.read_text()) if path.exists() else {}
if not isinstance(data, dict):
    raise ValueError('Existing MCP config must be a JSON object')
servers = data.setdefault('mcpServers', {})
if 'ai-router' in servers:
    raise RuntimeError('ai-router already exists: inspect and merge manually')
servers['ai-router'] = {'command': python, 'args': ['-m', 'kiro_ai_router.server'], 'disabled': False}
path.write_text(json.dumps(data, indent=2) + '\n')
try:
    path.chmod(0o600)
except OSError:
    pass
print('Updated', path)
