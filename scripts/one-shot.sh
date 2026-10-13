#!/usr/bin/env bash
set -Eeuo pipefail
export LC_ALL=C
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOME_WORKSPACE="$HOME/samwise"
[[ -f "$ROOT/AGENTS.md" ]] || { echo "Missing AGENTS.md"; exit 1; }
[[ -f "$HOME_WORKSPACE/docs/CONTEXT.md" && -f "$HOME_WORKSPACE/docs/GLOSSARY.md" ]] || { echo "Existing Samwise docs missing; stop"; exit 1; }
printf '\033[3J\033[2J\033[H'
printf '\n       *           SAMWISE\n      /_\\          PIXEL 11\n     /___\\         ONE-SHOT\n    /_____\\        AGENT SETUP\n   /_______\\\n      |||\n\n'
printf '== CANONICAL SOURCE ==\n'
git -C "$ROOT" remote -v
git -C "$ROOT" status --short
printf '\n== HOST/VM/NETWORK ==\n'
uname -a
tailscale ip -4
systemctl is-active ssh
printf '\n== AGENT ENGINE ==\n'
if ! command -v opencode >/dev/null 2>&1 && [[ ! -x "$HOME/.local/bin/opencode" ]]; then
  mkdir -p "$HOME/.local"
  npm install --global --prefix "$HOME/.local" opencode-ai
fi
export PATH="$HOME/.local/bin:$PATH"
command -v opencode || { echo 'OpenCode executable missing after npm installation'; exit 1; }
opencode --version
printf '\n== MATT POCOCK SKILLS ==\n'
cd "$ROOT"
npx --yes skills@latest add mattpocock/skills -a opencode -s '*' -y
printf '\n== SKILL VERIFICATION ==\n'
npx --yes skills@latest list -a opencode
test -f "$ROOT/.agents/skills/setup-matt-pocock-skills/SKILL.md" || test -f "$ROOT/.opencode/skills/setup-matt-pocock-skills/SKILL.md" || { echo 'setup skill missing'; exit 1; }
printf '\n== EXISTING DOCUMENTS UNMODIFIED ==\n'
ls -l "$HOME_WORKSPACE/docs/CONTEXT.md" "$HOME_WORKSPACE/docs/GLOSSARY.md"
printf '\n== SOURCE CONTROL ==\n'
git -C "$ROOT" status --short | head -50
printf '\n== READY ==\n'
printf '  cd %s\n  opencode\n' "$ROOT"
printf '  First task: inspect AGENTS.md and docs/agents/INITIAL-MISSION.md; audit the entire environment before modification.\n'
