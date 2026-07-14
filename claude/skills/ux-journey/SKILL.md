---
name: ux-journey
description: Task-driven UX discovery for a local Laravel app. A context-free subagent attempts a realistic end-user task cold ("create a cronjob for team X, silenced, daily") and the session compiles its think-aloud log into a journey report — a first-person "user report" of friction, wrong turns, and dead ends. Use when the user asks for a UX journey/probe/discovery, "how hard is it for a user to...", or "try doing X as a user and tell me where it hurts".
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
