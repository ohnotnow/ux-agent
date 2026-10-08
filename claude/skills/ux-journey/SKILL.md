---
name: ux-journey
description: Task-driven UX discovery for a local Laravel app. A context-free subagent attempts a realistic end-user task cold ("create a cronjob for team X, silenced, daily") and the session compiles its think-aloud log into a journey report — a first-person "user report" of friction, wrong turns, and dead ends. Use when the user asks for a UX journey/probe/discovery, "how hard is it for a user to...", or "try doing X as a user and tell me where it hurts". Has a screen-reader mode (needs a11y-agent): use it when the user asks what a task is like with a screen reader, or for an a11y journey.
---

# UX journeys

Give a fresh agent a realistic *goal* and watch where the app fights it.
The task is the probe — never a heuristic checklist. Friction that surfaces
while genuinely trying to get something done arrives pre-ranked; findings
hunted for their own sake arrive as noise.

The traversal is done by the `ux-journey-probe` agent (installed alongside
this skill): context-free, browser-only, its file access confined by a guard
hook to browser snapshots and its own output. The ignorance is the
instrument — protect it. If the agent isn't in your available agent types,
it needs installing — see the ux-agent repo's README.

## What gets produced

```
docs/ux-journeys/<slug>/
├── journey-log.md   # the probe's in-the-moment think-aloud log (evidence)
├── shots/           # screenshots at milestones and "…now what?" moments
└── report.html      # the compiled journey report (the deliverable)
```

## Division of judgement (the point of the design)

- **The probe** reports *experience*: what it expected, did, and saw. Its
  findings describe friction and cost, plus at most a "smallest possible
  fix" hint. It never sees the code and never issues verdicts.
- **The report** is a user report, as-presented to the developer — a
  journey, not a list of selectors and DOM events.
- **The judgement** belongs to the developer (with the orchestrating
  session's help, code access, and full context). A two-screen path may be a
  deliberate trade-off that keeps the code much simpler for a once-yearly
  task; a hidden option may be an authorisation rule doing its job. The
  report supplies the evidence for that conversation; it does not pre-empt
  it. Keep any of your own design opinions out of the report — offer them
  in chat, clearly separated, after presenting the findings.

## The pipeline

**1. Frame the task in manager-voice.** Use the user's phrasing verbatim
where possible ("Create a new cronjob for 'Nightly Photo Backups' that runs
daily, grace period of 2hrs, personal..."). A realistic goal with a concrete
success state. Agree the persona (admin? ordinary staff member?) — it
changes what dead ends are reachable.

**2. Prep the app state yourself if needed** (seed data, reset leftovers
from a previous run) — the probe must arrive at a believable starting state
without being told anything about the app.

**3. Assemble the briefing.** Mechanics yes, domain no:

- YES: app URL, login credentials, persona ("you are a member of staff with
  an admin account"), the task, the output slug/paths.
- NO: anything about the app's layout, where features live, what you suspect
  the friction is, or anything discovered in this conversation. If the
  briefing could help the probe skip a wrong turn, it is contaminated.

**4. Launch** the `ux-journey-probe` agent with the briefing. Expect
roughly 10 minutes / ~100k subagent tokens for a moderate task.

**5. Verify before compiling.** Read the log: entries numbered, expectations
genuinely recorded before outcomes (a log written at the end reads
suspiciously tidy — if it does, say so). Spot-check the pivotal screenshots
against the claims built on them.

**6. Compile `report.html`** from the log — never from memory. Structure:

- Meta block: the task as given, who attempted it (context-free agent,
  date), outcome verdict ("Completed — via an unsignposted detour" /
  "Dead end" / "Completed, no significant friction").
- The journey as short narrative acts, quoting the log's best in-the-moment
  lines verbatim (blockquotes), with screenshots at the pivotal moments.
- Findings, ranked by observed cost, each citing the log entries that
  evidence it and noting who pays (admin detour vs non-admin dead end).
- A stats footer: plausible-ideal actions vs actual actions, pages visited,
  wrong turns, dead ends. ("4 clicks became 18 across 7 pages.")
- Evidence links to journey-log.md and shots/.

Same visual family as the user-guide previews: self-contained, readable,
max-width ~46rem.

**7. Report back in chat**: outcome, the findings in brief, and — separately
and labelled as such — your own design take if you have one. Findings go to
`ait` only after the user has reviewed and accepted them, never auto-filed.

## Screen-reader mode

Use it when the user asks what the app is like with a screen reader ("is
this pleasant to use for a blind user?", "do the a11y journey"). Passing
WCAG checks is not the question here; the question is what the same task
costs someone who can only hear the page. The same probe agent attempts
the same task, perceiving the app only through a virtual screen reader,
and a normal visual probe runs the task too as a baseline. The contrast
("same answer: 6 actions by eye, 86 steps by ear") is the headline.

**Needs a11y-agent** (github.com/ohnotnow/a11y-agent), for its reader
bundle. Find the clone: `command -v a11y` gives a wrapper whose last line
is `exec node "<clone>/dist/cli.js" "$@"`; the bundle is
`<clone>/assets/vsr-bundle.js`. No wrapper: ask the user for the clone
path. No clone: say screen-reader mode needs a11y-agent and stop. The
helper, `sr-helper.js`, sits in this skill's directory.

Output layout: `docs/ux-journeys/<slug>/visual/` (log + shots),
`docs/ux-journeys/<slug>/screen-reader/` (log only), and one `report.html`
at `<slug>/`.

**Setup (you do this, not the probe).** Open a named session from the
project root, log in yourself, then inject bundle and helper into the
browser *context*, so every full page load re-injects them:

```bash
playwright-cli -s=probe-sr open <app-url>/login   # then fill + click to log in
playwright-cli -s=probe-sr --raw run-code "async page => { await page.context().addInitScript({path: '<bundle>'}); await page.context().addInitScript({path: '<skill-dir>/sr-helper.js'}); await page.evaluate(() => sessionStorage.clear()); await page.goto('<start-url>'); return await page.evaluate(() => typeof window.__sr + ' ' + window.__sr.steps()); }"
```

Expect `"object 0"`. If the page has a strict Content-Security-Policy the
script tags will be blocked: stop and tell the user (untried so far).

**The pair: parallel only for read-only tasks.** Launch both probes in one
message when the task only reads. If it creates or changes data, run them
one after the other and reset the app state in between (step 2), or the
second probe meets the first one's leftovers. Don't give each probe its
own account instead: different accounts can see different things, which
breaks the like-for-like comparison. The visual probe gets the normal
briefing with `-s=probe-vis`, its output dir `<slug>/visual/`, and an
instruction to keep its log with the Write tool rather than shell appends.

**Screen-reader briefing.** App URL, task and output dir as usual, then
this, verbatim:

> Persona: you are a member of staff who is blind and uses a screen
> reader. You cannot see the screen at all. Everything you know about the
> app comes from what the screen reader speaks. You are already logged in;
> the browser session `probe-sr` is on the app's start page.
>
> You operate the reader ONLY with commands of exactly this shape, one per
> Bash call: `playwright-cli -s=probe-sr --raw eval "window.__sr.next()"`
>
> Actions (single quotes inside the double-quoted JS; never semicolons,
> pipes, the > character, or arrow functions, which the guard blocks):
> `next()` / `previous()`; `jump('Heading')` / `jumpBack('Heading')`, which
> also take 'Link', 'Landmark', 'Main', 'Navigation', 'Form', 'Region',
> 'HeadingLevel1' to 'HeadingLevel6'; `activate()` to press or follow the
> current item; `press('Space')`, `press('Enter')` etc; `type('text')`.
>
> Each returns "[step N] what the reader said". Note step numbers in your
> log. If a jump finds nothing of that kind you hear the current item
> again; that is how this reader says "none found". Whatever the reader
> does or doesn't tell you when you follow a link is part of the
> experience: note it.
>
> Do NOT take screenshots, run `playwright-cli snapshot`, click, goto,
> fill, eval anything but `window.__sr.*`, read `.playwright-cli` files, or
> read the URL. Keep your journey log with the Write tool (rewrite the
> whole file with the new entry at the end; never change earlier entries),
> not cat or echo. No shots/ folder. Don't copy long URLs, tokens or
> secrets you hear into the log; paraphrase them. Use headings, landmarks
> and link jumps the way a real user would when they help, and say so when
> they don't. When done: closing reflection, `playwright-cli -s=probe-sr
> close`, then reply with whether you completed the task, your answer,
> the total step count, and a one-paragraph summary.

**Verify.** Both logs must end with a `## Closing reflection`. An Anthropic
safety classifier sometimes kills probe runs (`reasoning_extraction`),
before the first action or partway through. A log without its reflection
is truncated: say so plainly, in chat and in the report, and never compile
it as if it were complete. A killed probe never closes its browser: close
its session yourself (`playwright-cli -s=<session> close`), then check no
browsers are left (House conventions).

**Report additions.** Open with the side-by-side: the task, both outcomes,
visual actions vs screen-reader steps. Treat step counts as relative: the
virtual reader announces boundaries ("end of list"; start, text and end of
a paragraph), so a real reader would take fewer. The findings that
matter most are the jumps that should have worked and didn't, and how long
the forced linear walks were. State the simulation's assumptions in the
framing: on a full page load the reader announces the title; after an
in-place page swap (e.g. Livewire `wire:navigate`) it restarts at the top
and announces nothing, because what a real reader says there is unknown.

## Honesty notes

- **A null result is respectable.** "The flow was smooth, nothing worth
  changing" must be a reportable outcome, or the skill will manufacture
  findings to justify its invocation.
- **The evidence is asymmetric.** If the probe struggles, humans very likely
  will; if it breezes through, that proves less — it reads accessibility
  trees, not visual hierarchy, and it is an unusually literate UI user. Say
  this in the report's framing when relevant.
- **The guard is a belt, not a vault.** The probe's hooks stop honest drift
  towards reading the code; they would not stop a determined adversary. That
  is the right trade — the threat model is temptation, not malice.

## House conventions

- Lando apps: `https://<app>.lndo.site`, self-signed cert — needs
  `.playwright/cli.config.json` in the project root (see the
  user-guide-video skill for the snippet). Start any of your own
  playwright-cli sessions from the project root; the probe inherits its cwd
  from the Agent launch, which is already the project root.
- Seeded local login: `admin2x` / `secret` (persona: an admin). Ask the user
  which login to brief for non-admin personas.
- After a run, check the probe closed its browser (`playwright-cli list`,
  and `ps` for stray `cliDaemon`/`playwright_chromiumdev_profile`
  processes).
