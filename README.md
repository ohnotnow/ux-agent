# ux-agent

Ask your coding agent to *use* your web app the way a person would, then hand you the evidence:

> *"Record me a video of that broken dialog — on mobile, like the user reported."*
>
> *"Make a user guide for adding a new user to a team."*
>
> *"Honestly, how hard is it to move a job from one team to another? Try it and tell me where it hurts."*

ux-agent is a set of Claude Code skills and a sub-agent built on
[playwright-cli](https://github.com/microsoft/playwright-cli). Three modes,
one theme: the agent drives the real app in a real browser, and what you get
back is something a human can actually use. A video, a documented
walkthrough, or a first-person usability report.

## What's in the box

**`record-bug-video`** — reproduces a flow under the conditions the developer
describes (viewport, browser, logged-in role, app state) and records it raw.
No staging, no overlays — the mess is the point. Pairs the video with the
console and network evidence a video can't show. "Couldn't reproduce" is a
reported finding, not a failure.

**`user-guide-video`** — produces end-user documentation: short, human-paced
video clips (one per step, typed at human speed, with highlight rings on the
control that matters), stitched together by prose in a `doc.yaml`, rendered
to a preview HTML page. A replay script ships alongside each guide, so when
the UI changes you re-run it and the videos re-film themselves.

**`ux-journey`** (plus the `ux-journey-probe` agent) — task-driven UX
discovery. A context-free sub-agent is given only a URL, a login, and a task
in the words a manager would use. It attempts the task cold, keeping an
in-the-moment think-aloud log (expectation, action, result, written down
*before* each click resolves), with screenshots at every "...now what?" moment.
The session then compiles that log into a journey report: a first-person
account of friction, wrong turns, and dead ends, with a stats footer
("4 clicks became 18 across 7 pages"). The probe is tool-restricted and
hook-guarded so it can't peek at your codebase: its ignorance is the
instrument.

The judgement stays with you. The probe reports experience; whether a rough
edge is a bug or a deliberate trade-off is a decision for the developer with
the code and the context in front of them.

## Show me

The `examples/` directory holds real output from the first runs of each
skill, against a Laravel/Livewire app:

- [`examples/user-guides/create-a-new-user/`](examples/user-guides/create-a-new-user/) —
  a five-step guide with clips: open `preview.html` and you're watching it.
- [`examples/user-guides/silencing-a-job/`](examples/user-guides/silencing-a-job/) —
  the first guide ever produced; three steps, one of which found a real
  data-loss bug while being filmed.
- [`examples/ux-journeys/team-cronjob/`](examples/ux-journeys/team-cronjob/) —
  a journey report (`report.html`) where the cold probe hit a genuinely
  confusing dead end, worked out the unwritten rule gating it, and reported
  the whole experience, including the near-miss where a hastier user would
  have created a duplicate team.

## Install

You'll need [Claude Code](https://claude.com/claude-code),
`@playwright/cli` (`npm install -g @playwright/cli`), `ffmpeg`, and
[uv](https://docs.astral.sh/uv/) (the user-guide render CLI is a
single-file uv-run Python script).

```bash
git clone git@github.com:ohnotnow/ux-agent.git
cd ux-agent
cp -r claude/skills/* ~/.claude/skills/
cp claude/agents/* ~/.claude/agents/
```

That's the whole install. The skills don't reference the clone, so nothing
else to wire up. Prefer it per-project rather than global? Copy the same
files into an app's `.claude/skills/` and `.claude/agents/` instead.

## A word about house conventions

These skills encode *our* habits: Laravel + Livewire apps, Lando local dev
(`*.lndo.site`, self-signed certs), a seeded `admin2x`/`secret` login in
every app, Laravel Debugbar to hide or ignore. The mechanics are
stack-agnostic; the conventions are not. Read the skills through and swap in
your own before adopting. Each one keeps its conventions in a clearly
marked section. That includes the look of the rendered user guides: the
house stylesheet sits in one marked block at the top of
`claude/skills/user-guide-video/render.py`, ready to be swapped for your
own brand.

## Not using Claude Code?

The skills are plain markdown: point your harness at `claude/skills/`
(via `AGENTS.md` or whatever your tool reads) and you have most of the
value. The `ux-journey-probe` agent's isolation and its no-peeking guard
hook are Claude Code-specific; if your harness supports restricted
sub-agents, the probe's markdown tells you exactly what to recreate.

## Status

Early days, shared as-is. The `preview.html` files in the examples are
genuine output from the render CLI
(`claude/skills/user-guide-video/render.py`). Expect the odd rename while
things settle.

## Licence

[MIT](LICENSE).
