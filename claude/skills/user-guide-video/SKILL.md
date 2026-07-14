---
name: user-guide-video
description: Produce end-user how-to documentation with per-step screen recordings for a local Laravel app — a doc.yaml of prose steps, short human-paced mp4 clips, a replay script for re-filming, and an HTML preview. Use when the user asks for a user guide video, a how-to video, end-user docs with videos, or to "create a video showing users how to...".
allowed-tools: Bash(playwright-cli:*) Bash(ffmpeg:*) Bash(ffprobe:*)
---

# User-guide videos

Turn "show users how to <do a thing>" into a directory of end-user
documentation: short human-paced video clips, one per step, stitched together
by prose. The deliverable is the *doc*, with videos as attachments — not one
long screen recording.

Browser mechanics live in the `playwright-cli` skill (see especially its
`references/video-recording.md` for the screencast/overlay API). This skill
is the pipeline, the house conventions, and the rakes already stepped on.

## What gets produced

```
docs/user-guides/<slug>/
├── doc.yaml        # source of truth: title, intro, steps (prose + video)
├── record.js       # replay script — re-run to re-film after a UI change
├── preview.html    # rendered stand-in until the render CLI exists
└── clips/
    ├── 01-<step>.mp4
    └── 02-<step>.mp4
```

(If the project has no `docs/` convention yet, default to `docs/user-guides/`
and mention the choice when reporting back.)

### doc.yaml schema

```yaml
title: Silencing alerts for a job
intro: |
  One short paragraph: when and why a user would do this.
steps:
  - heading: Log in
    body: |
      Prose for this step. Markdown allowed.
    video: clips/01-log-in.mp4
```

## The pipeline

**1. Rehearse.** Drive the whole flow with plain playwright-cli commands
first. Collect the locators from the generated-code output — the script needs
them. While rehearsing, *verify each change actually persists* (reload and
check): Livewire fields with deferred or `.blur` models can silently fail to
sync. **If the flow cannot be completed as intended, you have found a bug —
report it to the user, never document around it.**

**2. Plan the steps.** One clip per user-meaningful step, usually 3–6 steps
of 5–15 seconds each. Short clips beat one long video: users jump straight to
the step they're stuck on, and a botched step is re-filmed alone.

**3. Write `record.js`** — a hero script run via
`playwright-cli run-code --filename=docs/user-guides/<slug>/record.js`:

- **Prep first, unrecorded**: put the app into the state the guide assumes
  (log out, reset toggles, seed data), so the recording starts honest.
- One `page.screencast.start({ path, size })` / `stop()` pair per step.
- **Clip paths must be absolute** — relative paths resolve against the
  playwright-cli daemon's cwd, not the project. Put a `CLIP_DIR` const at the
  top with a comment saying to adjust it.
- Pacing (validated, feels natural): type with
  `pressSequentially(text, { delay: 70 })`; ~900ms settle at clip start;
  ~400ms "thinking" pause before a click; 1200–1600ms hold at clip end.
- Viewport 1280×800, and the screencast `size` must match.
- Hide the debugbar on every navigation via `page.addInitScript` injecting
  `.phpdebugbar { display: none !important; }`.
- At most one highlight per clip: a `page.screencast.showOverlay()` ring
  around the control about to be used (overlays are `pointer-events: none`,
  so clicking through them is safe). Dispose it after the click.

Skeleton:

```js
async page => {
  const BASE = 'https://<app>.lndo.site';
  const CLIP_DIR = '/absolute/path/to/docs/user-guides/<slug>/clips';
  const SIZE = { width: 1280, height: 800 };

  await page.addInitScript(() => {
    const hide = () => {
      const style = document.createElement('style');
      style.textContent = '.phpdebugbar { display: none !important; }';
      document.head.appendChild(style);
    };
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', hide);
    } else { hide(); }
  });

  // ---- Prep (not recorded): reset state, log out ----
  // ...
  await page.context().clearCookies();

  // ---- Clip 1 ----
  await page.goto(BASE + '/login');
  await page.screencast.start({ path: CLIP_DIR + '/01-log-in.webm', size: SIZE });
  await page.waitForTimeout(900);
  // ... actions, human-paced ...
  await page.waitForTimeout(1400);
  await page.screencast.stop();

  // ---- Clip 2 ... ----
  return 'done';
}
```

**4. Convert** each clip to mp4 (end users' players are fussy about webm),
then delete the webm:

```bash
ffmpeg -i clip.webm -c:v libx264 -pix_fmt yuv420p -crf 23 -movflags +faststart clip.mp4
```

**5. Write the prose** in doc.yaml. Conventions:

- British English, end-user voice; no developer jargon (say "the filter box",
  not "the Livewire search input").
- Describe the **intended** UX. Where reality disagrees, that's a bug to
  report (see step 1), not prose to fudge.
- Keep credentials generic in prose ("sign in with your usual username and
  password") even though the seeded `admin2x` account appears on screen.
- Bold the UI labels the user must find: click the **Silenced** switch.

**6. Generate `preview.html`** — a self-contained page rendering the same
content: title, intro, then per step a numbered `<h2>`, the prose, and
`<video controls preload="metadata" src="clips/...">`. Simple readable
styling, max-width ~46rem. (This stands in for the future
`render --input doc.yaml` CLI; keep doc.yaml as the source of truth.)

**7. Verify before handing over.** `ffprobe` each clip's duration against the
script's arithmetic, then extract a frame or two
(`ffmpeg -ss <t> -i clip.mp4 -frames:v 1 frame.png`) and *look at them*:
debugbar hidden? highlight ring visible? text actually typed? Report what you
checked.

## House conventions

- Lando apps: `https://<app>.lndo.site`, self-signed cert. Needs
  `.playwright/cli.config.json` in the project root:

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

- Seeded local login: `admin2x` / `secret`.

## Rakes already stepped on

- **Clicking a switch's label toggles the switch.** To blur a field, click
  something genuinely neutral (a plain heading), never a form label.
- **`wire:model.blur` / deferred fields may never reach the server.** Verify
  persistence with a reload during rehearsal, not by trusting the UI.
- **playwright-cli mangles negative numeric arguments** (`mousewheel 0 -800`
  parses as flags and silently does nothing) — use `run-code` for those.
- **Relative screencast paths land in the daemon's cwd** — always absolute.
- **The daemon adopts the cwd of the shell that first opens the browser** —
  start playwright-cli sessions from the project root, or its
  `.playwright-cli` artefacts (snapshots, console logs) scatter into whatever
  directory you happened to be in.

## Afterwards

- Leave app state honest: reset what the recording changed, or say exactly
  what was left changed.
- `playwright-cli close`, then check for strays: `ps` for
  `playwright_chromiumdev_profile` or `cliDaemon.js` — orphaned daemons from
  old sessions linger and eat CPU.
