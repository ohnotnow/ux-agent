#!/bin/bash
# Install the ux-agent skills and agents for Claude Code.
#
#   ./install.sh                       # global: ~/.claude/
#   ./install.sh ~/code/some-project   # per-project: <path>/.claude/
#
# Safe to re-run; existing copies are updated in place.

set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)"

if [ $# -gt 1 ]; then
    echo "usage: $0 [project-path]" >&2
    exit 1
fi

if [ $# -eq 1 ]; then
    if [ ! -d "$1" ]; then
        echo "error: '$1' is not a directory" >&2
        exit 1
    fi
    target="$(cd "$1" && pwd)/.claude"
else
    target="$HOME/.claude"
fi

mkdir -p "$target/skills" "$target/agents"

echo "Installing into $target"

for skill in "$src"/claude/skills/*; do
    [ -d "$skill" ] || continue
    cp -R "$skill" "$target/skills/"
    echo "  skill: $(basename "$skill")"
done

for agent in "$src"/claude/agents/*; do
    dest="$target/agents/$(basename "$agent")"
    # In this repo's own .claude/, the agents are symlinks back to
    # claude/agents/ - copying a file onto itself would fail, and there
    # is nothing to update anyway.
    if [ -e "$dest" ] && [ "$agent" -ef "$dest" ]; then
        echo "  agent: $(basename "$agent") (already linked to this repo - skipped)"
        continue
    fi
    cp "$agent" "$dest"
    echo "  agent: $(basename "$agent")"
done

# The ux-journey-probe's guard hook resolver requires the guard to be
# executable - belt and braces in case the copy lost the mode bit.
chmod +x "$target/agents/ux-probe-guard.sh"

echo
echo "Done. Restart any running Claude Code session to pick up the new agents."
