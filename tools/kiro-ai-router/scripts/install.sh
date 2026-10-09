#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.local/share/kiro-ai-router/app"
mkdir -p "$DEST" "$HOME/.config/kiro-ai-router" "$HOME/.kiro/settings" "$HOME/.kiro/agents"
# Restrict access to router data/config directories (may hold paths/state).
chmod 700 "$HOME/.local/share/kiro-ai-router" "$HOME/.config/kiro-ai-router" 2>/dev/null || true
python3 -m venv "$DEST/.venv"
"$DEST/.venv/bin/python" -m pip install --upgrade pip
"$DEST/.venv/bin/pip" install "$ROOT"
CFG="$HOME/.config/kiro-ai-router/config.yaml"
if [[ ! -f "$CFG" ]]; then cp "$ROOT/config/router.example.yaml" "$CFG"; fi
chmod 600 "$CFG" 2>/dev/null || true
"$DEST/.venv/bin/python" "$ROOT/scripts/configure_kiro.py" "$DEST/.venv/bin/python"
echo "Installed. Restart Kiro CLI; inspect $CFG and ~/.kiro/settings/mcp.json"
