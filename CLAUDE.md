# ux-agent — notes for Claude

Skills + a guarded sub-agent that drive a browser (playwright-cli) against
a locally-running web app to produce bug videos, user-guide videos, and
cold UX journey reports. The README covers the what; this file is the
working knowledge that took a day to learn.

**Session start:** `ant foundation` (the project's vision + principles) and
`ait ready` (what's next — the render CLI is the standing P1). Both tools
are initialised here.

## Repo layout quirks (the bit that WILL bite)

- `claude/` is the **canonical, tracked** home of skills and agents.
- `.claude/skills/` is a **gitignored local copy** so the skills work when
  running Claude Code in this repo. Edit `claude/skills/...` first, then
  sync with `./install.sh .` (it re-copies the skills and safely skips
  the symlinked agents). (History: directory symlinks
  broke both git pathspecs and agent-commit; file symlinks were fine, so
  `.claude/agents/*` ARE symlinks into `claude/agents/`.)
- The dir is named `playwright-test-video` locally but the project/repo is
  **ux-agent** (github.com/ohnotnow/ux-agent, public as of mid-July 2026).
- The two `examples/user-guides/*/preview.html` files must stay genuine
  output of `claude/skills/user-guide-video/render.py` — the README's
  Status section promises it. After ANY change to render.py, re-render
  both (`uv run claude/skills/user-guide-video/render.py --input
  examples/user-guides/<slug>/doc.yaml` for each slug) and ship them in
  the same commit. render.py lives in a skill dir, so the `.claude/skills`
  re-copy rule above applies to it too.

## Testing the skills

The worked examples ran against **cronmon** (`https://cronmon.lndo.site`),
one of the user's Laravel/Livewire apps — their Lando needs to be up. Login
`admin2x` / `secret`. `.playwright/cli.config.json` in this repo handles
the self-signed cert (that's why browsers must be **opened from this repo's
root** — the config is cwd-relative, and the daemon also dumps its
`.playwright-cli/` artefacts into whatever cwd it inherits).

Known cronmon quirk: the job-page "Silenced until"/"Reason" fields use
`wire:model.blur` and **never persist** (blur fires no Livewire request —
verified with DOM listeners + network watch, 13 Jul 2026). Reported to the
user; unfixed at time of writing. Don't burn an hour rediscovering it.

playwright-cli rakes already paid for: negative numeric args get eaten as
flags (route through `run-code`); clicking a switch's *label* toggles the
switch; always `playwright-cli close` when done and check for orphaned
daemons (`ps -axo pid,etime,command | grep -E 'cliDaemon|playwright_chromiumdev_profile'`
— a leaked one once sat for 2 days chewing CPU).

## The guard hook

`claude/agents/ux-probe-guard.sh` confines the ux-journey-probe agent.
Wrinkle inside: the hook's JSON arrives on stdin but `python3 -` needs
stdin for the program, so the script passes it via an `INPUT` env var.
Test it by echoing tool-call JSON at it and checking the exit code
(0 allow / 2 block) — there are worked examples in the session that built
it, and the resolver line in `ux-journey-probe.md` frontmatter looks for
the guard project-local first, then `~/.claude/agents/`, failing open.

## Git and hygiene

- Commits via `agent-commit` ONLY (raw add/commit are blocked): explicit
  relative file paths (it refuses dirs — and collapsed `?? dir/` entries
  from plain `git status --porcelain`; use `-uall`), two-step preview then
  `--yes TOKEN`, Conventional Commits, **zero AI attribution, ever**.
- Before any public flip or new shipped content: leak scan over the
  **tracked file list** (`git ls-files`), not a directory grep — tracked
  session artefacts once hid from a scan that excluded "ignored" dirs.
  The pattern list lives in the gitignored ant foundation note (`ant
  foundation`), so this tracked file doesn't ship the strings it hunts.
- Outputs the skills generate in *target* apps go to `docs/user-guides/`
  and `docs/ux-journeys/`; in *this* repo, worked examples live under
  `examples/`.

## Working with this user on this project

- Design conversations happen one point at a time with a stated position —
  no walls of options. Questions are questions, not work orders.
- Never write an "Open Questions" section into a doc or issue — ask the
  user in the moment, then record the *answer*.
- British English in all prose.
