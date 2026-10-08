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
import json, os, re, shlex, sys

data = json.loads(os.environ.get("INPUT") or "{}")
tool = data.get("tool_name", "")
tool_input = data.get("tool_input", {})

ALLOWED_PATHS = re.compile(r'(docs/ux-journeys|\.playwright-cli)/')

def block(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)

def allowed_path(path):
    # Shell expansion ($VAR, ~, globs, braces) would change the path after
    # this check.
    if re.search(r'[$~*?\[{]', path):
        return False
    return bool(ALLOWED_PATHS.search(os.path.realpath(path) + "/"))

def shell_words(text, msg):
    # Split the way the shell does, so quoted arguments stay whole. The shell
    # only starts a comment at a word boundary (`a#b > x` still redirects), so
    # don't let shlex treat # as a comment at all. Unparseable: fail closed.
    lex = shlex.shlex(text, posix=True, punctuation_chars=True)
    lex.commenters = ""
    lex.whitespace_split = True  # keep `docs/x/$VAR` as one word, like the shell
    try:
        return list(lex)
    except ValueError:
        block(msg)

if tool in ("Read", "Write", "Edit"):
    path = tool_input.get("file_path", "")
    if not allowed_path(path):
        block(
            "Blocked: the UX probe may only read browser snapshots "
            "(.playwright-cli/) and read/write its own journey files "
            "(docs/ux-journeys/). A real user cannot see the codebase. "
            "If you believe this access is genuinely necessary, do not retry "
            "variants — explain the need in your final reply instead."
        )

elif tool == "Bash":
    cmd = tool_input.get("command", "")
    # Command substitution runs commands the checks below never see, and
    # the probe has no use for it.
    if re.search(r'\$\(|`|[<>]\(', cmd):
        block(
            "Blocked: command substitution ($(...), backticks, <(...)) is not "
            "part of the UX probe's remit. Run each command on its own."
        )
    # First word of each command segment must be allow-listed. Newlines and a
    # lone & (background) separate commands just as ;, &&, || and | do.
    ALLOWED_FIRST = {
        "playwright-cli", "mkdir", "ls", "sleep", "echo", "cat",
        "pwd", "date", "true",
    }
    segments = re.split(r'[;|&\n]', cmd)
    for segment in segments:
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
    # cat may only read snapshots/journey files: every file it is given must
    # resolve there. (Redirect targets are checked separately below.)
    cat_msg = ("Blocked: cat is only allowed against .playwright-cli/ snapshots "
               "or docs/ux-journeys/ files.")
    for segment in segments:
        words = shell_words(segment, cat_msg)
        if not words or words[0] != "cat":
            continue
        skip_next = False
        for word in words[1:]:
            if skip_next:
                skip_next = False
            elif set(word) <= set("<>|&"):
                skip_next = True
            elif not word.startswith("-") and not allowed_path(word):
                block(cat_msg)
    # Any output redirection must land in the journey directory. Tokenising
    # means a `>` inside a quoted argument (a JS arrow function passed to
    # `playwright-cli run-code`) isn't mistaken for a redirect.
    redirect_msg = "Blocked: output redirection is only allowed into docs/ux-journeys/."
    tokens = shell_words(cmd, redirect_msg)
    for i, token in enumerate(tokens):
        if ">" not in token or not set(token) <= set("<>|&"):
            continue
        target = tokens[i + 1] if i + 1 < len(tokens) else ""
        if not allowed_path(target):
            block(redirect_msg)

sys.exit(0)
PY
