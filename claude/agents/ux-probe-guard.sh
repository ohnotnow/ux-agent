#!/bin/bash
# PreToolUse guard for the ux-journey-probe agent.
#
# The probe must experience the app the way an end user would: browser only.
# This guard confines its file access to browser snapshots (.playwright-cli/)
# and its own journey output (docs/ux-journeys/), and its Bash usage to
# playwright-cli plus a few harmless utilities. It is a belt, not a vault —
# its job is to stop honest drift towards "I'll just peek at the code",
# not to defeat a determined adversary.
#
# Exit 0 = allow, exit 2 = block (stderr is shown to the agent).

# The hook's JSON arrives on stdin, but `python3 -` needs stdin for the
# program itself - so pass the JSON through the environment instead.
INPUT="$(cat)" python3 - <<'PY'
import json, os, re, sys

data = json.loads(os.environ.get("INPUT") or "{}")
tool = data.get("tool_name", "")
tool_input = data.get("tool_input", {})

ALLOWED_PATHS = re.compile(r'(docs/ux-journeys|\.playwright-cli)/')

def block(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)

if tool in ("Read", "Write", "Edit"):
    path = tool_input.get("file_path", "")
    if not ALLOWED_PATHS.search(path):
        block(
            "Blocked: the UX probe may only read browser snapshots "
            "(.playwright-cli/) and read/write its own journey files "
            "(docs/ux-journeys/). A real user cannot see the codebase. "
            "If you believe this access is genuinely necessary, do not retry "
            "variants — explain the need in your final reply instead."
        )

elif tool == "Bash":
    cmd = tool_input.get("command", "")
    # First word of each ;, &&, ||, | separated segment must be allow-listed.
    ALLOWED_FIRST = {
        "playwright-cli", "mkdir", "ls", "sleep", "echo", "cat",
        "pwd", "date", "true",
    }
    for segment in re.split(r'[;|]|&&|\|\|', cmd):
        words = segment.strip().split()
        if not words:
            continue
        if words[0] not in ALLOWED_FIRST:
            block(
                f"Blocked: '{words[0]}' is not part of the UX probe's remit. "
                "The probe interacts with the app only through playwright-cli "
                "and writes only its own journey log/screenshots. If this "
                "command is genuinely necessary, do not retry variants — "
                "explain the need in your final reply instead."
            )
    # cat may only be used to append to the journey log (cat >> docs/...),
    # or to read snapshots/journey files.
    if re.search(r'(^|[;&|]\s*)cat\b', cmd) and not ALLOWED_PATHS.search(cmd):
        block(
            "Blocked: cat is only allowed against .playwright-cli/ snapshots "
            "or docs/ux-journeys/ files."
        )
    # Any output redirection must land in the journey directory.
    if ">" in cmd and not ALLOWED_PATHS.search(cmd):
        block(
            "Blocked: output redirection is only allowed into docs/ux-journeys/."
        )

sys.exit(0)
PY
