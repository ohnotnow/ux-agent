#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml",
#     "markdown",
# ]
# ///
"""Render a user-guide doc.yaml (+ its clips/) into one self-contained HTML page.

Usage:
    uv run render.py --input docs/user-guides/<slug>/doc.yaml [--output page.html]

The default output is preview.html next to the input file. Video paths in
doc.yaml are relative to the doc, so the page must live beside the clips
for them to resolve.

The output makes no external requests — no CDN, no web fonts. It's one file
you can email round or drop on a shared drive.
"""

import argparse
import sys
from datetime import date
from html import escape
from pathlib import Path
from string import Template

import markdown
import yaml

# ---------------------------------------------------------------------------
# House style — swap this block for yours.
#
# Our house look: navy masthead, arrow bullets, Noto Sans wherever the
# reader's machine already has it — but never fetched, because self-contained
# output is a hard requirement, so there is no web-font link. Other teams:
# replace the variables in :root and anything else that offends you.
# ---------------------------------------------------------------------------
STYLESHEET = """\
:root {
  --brand-blue: #011451;
  --brand-dark-blue: #005398;
  --brand-blue-80: #344374;
  --brand-blue-60: #677297;
  --brand-blue-40: #99a1b9;
  --brand-blue-20: #ccd0dc;
  --brand-blue-10: #e6e7ee;

  --brand-ink: #1a1a1a;
  --brand-text: #323232;
  --brand-muted: #666666;
  --brand-rule: #cccccc;
  --brand-panel: #f5f5f5;
  --brand-panel-edge: #e6e6e6;

  --brand-paper: #ffffff;
  --brand-highlight: #ffdd00;
  --brand-arrow: #c5413a;

  --font-body: "Noto Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", monospace;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-7: 32px;
  --space-8: 40px;
  --space-9: 48px;
  --space-10: 56px;
  --space-11: 64px;
  --space-12: 96px;

  --measure: 72ch;
}

* { box-sizing: border-box; }

html {
  font-size: 17px;
  -webkit-text-size-adjust: 100%;
}

body {
  margin: 0;
  font-family: var(--font-body);
  font-weight: 400;
  line-height: 1.6;
  color: var(--brand-text);
  background: var(--brand-paper);
  font-feature-settings: "kern", "liga";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.page {
  max-width: 80ch;
  margin: 0 auto;
  padding: 0 clamp(20px, 4vw, 48px) clamp(40px, 6vw, 80px);
}

/* --- masthead: full-viewport-bleed navy ribbon --- */
.page-head {
  background: var(--brand-blue);
  color: #fff;
  width: 100%;
  margin-bottom: var(--space-9);
}
.page-head-inner {
  max-width: 80ch;
  margin: 0 auto;
  padding: var(--space-6) clamp(20px, 4vw, 48px);
  min-height: 56px;
  display: flex;
  align-items: center;
}
.page-heading {
  font-family: var(--font-body);
  color: #fff;
  font-size: clamp(1.6rem, 3.4vw, 2.2rem);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.005em;
  line-height: 1.15;
  margin: 0;
  padding: 0;
  border: none;
}

/* --- body --- */
.page-body { font-size: 1rem; }

p, ul, ol, dl, blockquote, table, pre {
  max-width: var(--measure);
}

p { margin: 0 0 var(--space-5); }

strong { font-weight: 700; color: var(--brand-ink); }
em { font-style: italic; }

/* --- the guide intro, set as a lede --- */
.intro p {
  font-size: 1.1rem;
  color: var(--brand-ink);
  line-height: 1.55;
}

/* --- headings --- */
h2, h3, h4, h5, h6 {
  font-family: var(--font-body);
  color: var(--brand-blue);
  line-height: 1.15;
  margin: 0;
  font-feature-settings: "kern", "liga";
}

h2 {
  font-size: clamp(1.35rem, 2.4vw, 1.55rem);
  font-weight: 700;
  margin: var(--space-10) 0 var(--space-4);
}

h3 {
  font-size: 1.15rem;
  font-weight: 700;
  margin: var(--space-8) 0 var(--space-3);
}

h4 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--brand-ink);
  margin: var(--space-6) 0 var(--space-2);
}

h5, h6 {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--brand-muted);
  margin: var(--space-5) 0 var(--space-2);
}

/* --- numbered step circles --- */
.step-number {
  display: inline-block;
  width: 1.6rem;
  height: 1.6rem;
  line-height: 1.6rem;
  text-align: center;
  border-radius: 50%;
  background: var(--brand-blue);
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  margin-right: var(--space-3);
  vertical-align: 0.14em;
}

/* --- step videos --- */
video {
  display: block;
  width: 100%;
  max-width: var(--measure);
  margin: var(--space-4) 0 var(--space-6);
  border: 1px solid var(--brand-panel-edge);
  background: var(--brand-ink);
}

/* --- links --- */
a {
  color: var(--brand-dark-blue);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 0.18em;
  text-decoration-color: rgba(0, 83, 152, 0.4);
  transition: text-decoration-color 160ms ease, color 160ms ease;
}
a:hover {
  text-decoration-color: var(--brand-dark-blue);
  color: var(--brand-blue);
}
a:focus-visible {
  outline: 3px solid var(--brand-highlight);
  outline-offset: 2px;
  text-decoration: none;
  background: var(--brand-highlight);
  color: var(--brand-blue);
}

/* --- lists with the corporate arrow accent --- */
ul, ol { margin: 0 0 var(--space-5); padding: 0; }

ul { list-style: none; padding-left: 0; }
ul > li {
  position: relative;
  padding-left: 1.65em;
  margin-bottom: var(--space-3);
}
ul > li::before {
  content: "\\2192";
  position: absolute;
  left: 0;
  top: 0;
  color: var(--brand-arrow);
  font-weight: 700;
  font-size: 1em;
  line-height: 1.6;
}
ul ul, ol ul { margin-top: var(--space-3); margin-bottom: var(--space-3); }
ul ul > li::before { color: var(--brand-blue-60); }

ol {
  list-style: none;
  counter-reset: guide-ol;
  padding-left: 0;
}
ol > li {
  position: relative;
  padding-left: 2em;
  margin-bottom: var(--space-3);
  counter-increment: guide-ol;
}
ol > li::before {
  content: counter(guide-ol) ".";
  position: absolute;
  left: 0;
  top: 0;
  color: var(--brand-blue);
  font-weight: 700;
  min-width: 1.5em;
}

li > p { margin-bottom: var(--space-2); }
li > p:last-child { margin-bottom: 0; }

/* --- definition lists --- */
dl { margin: 0 0 var(--space-5); }
dt {
  font-weight: 700;
  color: var(--brand-blue);
  margin-top: var(--space-3);
}
dd { margin: 0 0 var(--space-2) 0; padding-left: var(--space-4); }

/* --- horizontal rule --- */
hr {
  border: none;
  border-top: 1px solid var(--brand-rule);
  margin: var(--space-9) 0;
  max-width: var(--measure);
}

/* --- blockquote: light-grey panel --- */
blockquote {
  margin: var(--space-6) 0;
  padding: var(--space-5) var(--space-6);
  background: var(--brand-panel);
  border: 1px solid var(--brand-panel-edge);
  color: var(--brand-ink);
  font-size: 1rem;
  position: relative;
}
blockquote p { margin-bottom: var(--space-3); }
blockquote p:last-child { margin-bottom: 0; }
blockquote::before {
  content: "";
  display: block;
  width: 28px;
  height: 2px;
  background: var(--brand-arrow);
  margin-bottom: var(--space-3);
}

/* --- code --- */
code, pre, kbd, samp { font-family: var(--font-mono); font-size: 0.92em; }
code {
  background: var(--brand-blue-10);
  padding: 0.1em 0.35em;
  border-radius: 2px;
  color: var(--brand-blue);
}
pre {
  background: var(--brand-panel);
  border: 1px solid var(--brand-panel-edge);
  padding: var(--space-4);
  overflow-x: auto;
  margin: var(--space-5) 0;
  line-height: 1.5;
  color: var(--brand-ink);
}
pre code { background: none; padding: 0; color: inherit; font-size: 0.95em; }

/* --- tables --- */
table {
  border-collapse: collapse;
  width: 100%;
  margin: var(--space-6) 0;
  font-size: 0.95rem;
}
thead th {
  text-align: left;
  font-weight: 700;
  color: #fff;
  background: var(--brand-blue);
  padding: var(--space-3) var(--space-4);
  vertical-align: bottom;
}
tbody td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--brand-panel-edge);
  vertical-align: top;
}
tbody tr:nth-child(even) { background: var(--brand-panel); }
tbody tr:hover { background: var(--brand-blue-10); }

/* --- images --- */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: var(--space-5) 0;
}

/* --- footer --- */
.page-foot {
  margin-top: var(--space-12);
  padding-top: var(--space-5);
  border-top: 4px solid var(--brand-blue);
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  flex-wrap: wrap;
  gap: var(--space-3);
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}
.foot-title { color: var(--brand-ink); font-weight: 600; }
.foot-year { color: var(--brand-muted); }

/* --- selection --- */
::selection { background: var(--brand-highlight); color: var(--brand-blue); }

/* --- responsive --- */
@media (max-width: 640px) {
  html { font-size: 16px; }
  .page { padding: 0 16px 32px; }
  .page-head { margin-bottom: var(--space-7); }
  .page-head-inner { padding: var(--space-4) 16px; min-height: 48px; }
  table { font-size: 0.88rem; }
  thead th, tbody td { padding: var(--space-2) var(--space-3); }
  .page-foot { flex-direction: column; align-items: flex-start; }
}

/* --- print --- */
@media print {
  body { background: white; color: #000; }
  .page { max-width: none; padding: 0; }
  .page-head { background: white; color: var(--brand-blue); margin: 0 0 24px; border-bottom: 2px solid var(--brand-blue); }
  .page-head-inner { padding: 0 0 12px; min-height: 0; }
  .page-heading { color: var(--brand-blue); font-size: 1.6rem; }
  a { color: #000; text-decoration: none; }
  h2, h3 { break-after: avoid; }
  pre, blockquote, table { break-inside: avoid; }
  thead th { background: white !important; color: var(--brand-blue) !important; border-bottom: 2px solid var(--brand-blue); -webkit-print-color-adjust: exact; }
}

/* --- reduced motion --- */
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
"""
# --------------------------- end of house style ---------------------------

PAGE_TEMPLATE = Template("""\
<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<style>
$css
</style>
</head>
<body>
<header class="page-head">
  <div class="page-head-inner">
    <h1 class="page-heading">$title</h1>
  </div>
</header>
<div class="page">
  <main class="page-body">
    <div class="intro">
$intro
    </div>
$steps
  </main>
  <footer class="page-foot">
    <span class="foot-title">$title</span>
    <span class="foot-year">$year</span>
  </footer>
</div>
</body>
</html>
""")

STEP_TEMPLATE = Template("""\
<h2><span class="step-number">$number</span>$heading</h2>
$body
""")

VIDEO_TEMPLATE = Template(
    '<video controls preload="metadata" src="$src"></video>\n'
)


def md(text: str) -> str:
    return markdown.markdown(text, extensions=["extra"])


def render_steps(steps: list, doc_dir: Path) -> str:
    parts = []
    for number, step in enumerate(steps, start=1):
        heading = step.get("heading")
        if not heading:
            sys.exit(f"render: step {number} has no heading")
        rendered = STEP_TEMPLATE.substitute(
            number=number,
            heading=escape(heading),
            body=md(step.get("body", "")),
        )
        video = step.get("video")
        if video:
            if not (doc_dir / video).is_file():
                print(
                    f"render: warning: step {number} ({heading!r}): "
                    f"video file not found: {video}",
                    file=sys.stderr,
                )
            rendered += VIDEO_TEMPLATE.substitute(src=escape(video, quote=True))
        parts.append(rendered)
    return "\n".join(parts)


def render_page(doc: dict, doc_dir: Path) -> str:
    title = doc.get("title")
    if not title:
        sys.exit("render: doc.yaml has no title")
    steps = doc.get("steps")
    if not steps:
        sys.exit("render: doc.yaml has no steps")
    return PAGE_TEMPLATE.substitute(
        title=escape(title),
        css=STYLESHEET,
        intro=md(doc.get("intro", "")),
        steps=render_steps(steps, doc_dir),
        year=date.today().year,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a user-guide doc.yaml into a self-contained HTML page."
    )
    parser.add_argument(
        "--input", required=True, help="path to the guide's doc.yaml"
    )
    parser.add_argument(
        "--output",
        help="output HTML path (default: preview.html next to the input)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    try:
        doc = yaml.safe_load(input_path.read_text(encoding="utf-8"))
    except OSError as err:
        sys.exit(f"render: cannot read {input_path}: {err.strerror}")
    except yaml.YAMLError as err:
        sys.exit(f"render: {input_path} is not valid YAML: {err}")
    if not isinstance(doc, dict):
        sys.exit(f"render: {input_path} does not look like a guide doc.yaml")

    page = render_page(doc, input_path.parent)

    output_path = Path(args.output) if args.output else input_path.parent / "preview.html"
    output_path.write_text(page, encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
