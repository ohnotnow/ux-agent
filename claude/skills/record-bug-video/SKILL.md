---
name: record-bug-video
description: Record a video of a bug or misbehaving flow in a local Laravel app so the developer can watch what actually happens. Use when the user asks to record/capture a video of a bug, a failing or odd flow, or "show me what happens when..." — reproduces the flow under the conditions they describe (viewport, browser, user role) and records it raw.
allowed-tools: Bash(playwright-cli:*) Bash(ffmpeg:*) Bash(ffprobe:*)
---

# Record a bug video

Reproduce a flow the developer describes and hand back a video of what
actually happens, plus anything noticed along the way. This is a debugging
aid, not documentation: record raw, at natural automation speed, with no
overlays, chapters, or staged pacing. The mess is the point.

Mechanics of driving the browser are in the `playwright-cli` skill — this
skill is the house conventions and the debugging posture.

## The conditions are the brief

The bug lives under specific conditions. Before recording, pin down and
reproduce them — don't record the happy path on a desktop viewport when the
report says "on mobile":

- **Viewport**: "on mobile" → `playwright-cli resize 390 844` (or set it in
  the config file) before recording. "when I shrink the window" → record the
  resize itself.
- **Browser**: Safari-ish bugs → `playwright-cli open --browser=webkit`.
- **Who's logged in**: role-dependent bugs need the right user. The seeded
  local admin is `admin2x` / `secret`; ask if a different role is needed.
- **App state**: if the bug needs existing data ("when a job is already
  silenced..."), set that up first, unrecorded.

## House conventions

- Start playwright-cli sessions from the project root — the daemon adopts
  your shell's cwd and scatters its `.playwright-cli` artefacts there.
- Local apps run under Lando at `https://<app>.lndo.site` with a self-signed
  cert. Create `.playwright/cli.config.json` in the project root before
  opening the browser:

  ```json
  {
    "browser": {
      "contextOptions": {
        "ignoreHTTPSErrors": true,
        "viewport": { "width": 1280, "height": 800 }
      }
    }
  }
  ```

- **Leave the debugbar visible.** This is the developer's real environment
  and the debugbar may show the query/request that misbehaves. Only hide it
  if it physically covers the UI under investigation (common on mobile
  viewports) — say so if you do.
- Save recordings to `bug-videos/<short-slug>-<yyyy-mm-dd>.webm` in the
  project root. webm is fine for local viewing; convert to mp4 only if the
  developer wants to attach it to an issue:
  `ffmpeg -i in.webm -c:v libx264 -pix_fmt yuv420p -movflags +faststart out.mp4`

## Workflow

1. Rehearse the flow once with plain playwright-cli commands to confirm you
   can reach the failure. Reset any state you disturbed.
2. Record the reproduction — `playwright-cli video-start <path>` … actions …
   `video-stop` is usually enough. Use a `run-code` script instead when the
   repro needs precise sequencing.
3. While recording (or just after), gather the evidence a video can't show:
   `playwright-cli console` and `playwright-cli requests`. A 500 or a missing
   Livewire update request next to the video is usually the diagnosis.
4. Report: the video path, the conditions reproduced, and what you observed —
   including console/network findings. If you could NOT reproduce the bug,
   that is the finding; say exactly what you tried and under what conditions.

## Afterwards

- Put any app state you changed back the way you found it, or say plainly
  what was left changed.
- `playwright-cli close`, then check for strays: a `ps` for
  `playwright_chromiumdev_profile` or `cliDaemon.js` — orphaned daemons from
  crashed sessions linger for days and eat CPU.
