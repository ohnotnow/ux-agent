# Journey log: NAS backup job (screen-reader variant)

Task: "One of your jobs backs up the home NAS. Can you find out when it last checked in, and how long it's allowed to be late before anyone gets alerted?"

Persona: blind member of staff using a screen reader. Already logged in as admin.

## 1. Orientation

EXPECT: The start page will probably be a dashboard or a list of jobs. I'll first move to the next item to hear where I am.
DO: Pressed "next" to hear the first item.
SAW: [step 1] "new page loaded, title: Cronmon". [step 2] "link, Cronmon" - presumably the app logo/home link. So the app is called Cronmon. Fine so far.

## 2. Looking for structure

EXPECT: A page like this should have headings (e.g. "Jobs" or "Dashboard") and a main landmark I can skip to.
DO: Jumped to next heading (step 3), then to Main (step 4), then to any landmark (step 5).
SAW: Heading jump: nothing - I stayed on "link, Cronmon". Main jump: nothing either. That is a worry: no headings at all and no main region? Landmark jump found "navigation" (step 5). So there is a nav bar, but I've no headings to orient on the page content. Mild "...now what?" - I'll have to walk the page item by item.

## 3. Walking the navigation

EXPECT: Nav links like Home, Jobs, Settings. Hoping for a "Jobs" list.
DO: Pressed next a few times (steps 6-9), then switched to jumping link by link (steps 10-11) because item-by-item was slow.
SAW: "link, Home" / "Home" / "end of link, Home" - three stops for one link, a bit chatty. Then "link, New job", "link, Admin", "link, My settings". No "Jobs" link as such - I guessed Home is where the jobs live, and I'm already on it.

## 4. Finding the NAS job

EXPECT: After the nav, the page content should list my jobs.
DO: Jumped to the next link (step 12).
SAW: "link, Personal home NAS backup 1 × Daily · 6 hours grace · Location: Home Last check-in 3 days ago". Found it straight away - and the link text itself carries both answers: 6 hours grace, last check-in 3 days ago. Nice that it's all in one utterance, though it is a long one, and the "1 ×" was puzzling (one what? one alert? one tag?). The "·" separators were read literally as dots, which is fine. "3 days ago" is vague - I'd like an actual date/time for my manager, so I'll open the job.

## 5. Opening the job - did anything happen?

EXPECT: Activating the link should take me to the job's page, and the reader should tell me a new page loaded (as it did at step 1), ideally with a title naming the job.
DO: Activated the link (step 13), then pressed next (step 14), tried a heading jump (step 15), then jumped through links (steps 16-20).
SAW: Step 13 just re-read the same link text - no "new page loaded" announcement this time, and no new title. Genuine "...now what? did it work?" moment. Next took me to "link, Cronmon" (top of a page). Heading jump: still no headings. Link jumps: Home, New job, Admin, My settings, then wrapped back round to Cronmon - the job link (and any other job links) are gone. So I deduce I am on a different page, presumably the job's page, but only by noticing the link list changed. Nothing told me. Also this page seems to have no links of its own beyond the nav.

## 6. Reading the job page line by line

EXPECT: Since there are no headings, I'll have to arrow through the content after the nav. I expect a title, then the schedule/grace details, then some kind of history.
DO: Jumped back to the "My settings" link (step 21) and pressed next repeatedly (steps 22-58).
SAW: After the nav there was a second "navigation" containing just a Logout button inside a form (steps 25-29) - odd to hear "end of navigation" then "navigation" again, I briefly thought I'd wrapped round. Then at step 30: "Personal home NAS backup" - plain text, not announced as a heading, so a heading jump would never have found it. That confirms I'm on the right job (good, but I only know because I walked to it). Then Edit and Delete buttons, then label-like text with each value in its own paragraph, each paragraph costing me three stops ("paragraph" / value / "end of paragraph"):
- "Schedule" ... "1 × daily" (steps 33-36) - so "1 ×" means "once daily". Makes sense now, but hearing "one times daily" is clumsy.
- (no label heard) ... "6 hours grace" (steps 37-39). That's the answer to the second half: 6 hours. I'm assuming "grace" means how late it can be before an alert - the term was never explained anywhere I heard.
- "Owner" ... "Personal — Jenny MacAdmin"; "Created by Jenny MacAdmin"; "Location: Home" (steps 40-49).
- "Check-in URL", an explanation, a read-only textbox containing a long URL, and a "Copy to clipboard" button (steps 50-55).
- A "Silenced" switch, not checked, with a helpful description that silenced jobs won't alert (step 57). Good to know it's NOT silenced, so alerts would actually fire.
Things like "Schedule", "Owner", "Check-in URL", "Recent check-ins" sound like headings but are spoken as plain text, so I can't jump between them.

## 7. Finding the exact last check-in time

EXPECT: "Recent check-ins" (step 59) should be a list or table with the newest at the top.
DO: Kept pressing next through the table (steps 60-79).
SAW: A "Download CSV" button, then "table". Good - it's a real table with column headers: When, Source IP, bytes, files. But walking the header row cost me 14 steps (each header is "columnheader, X" / "X" / "end of columnheader, X"). Then step 79: "row, Mon, Oct 5, 2026 7:14 AM (3 days ago)" followed by an IP address, a byte count and a file count. That's the exact time: Monday 5 October 2026 at 7:14 AM. It matches "3 days ago" from the home page, so I'm fairly confident it's the newest (top) row. The numbers in the row are run together with no column names repeated, so I'd have had to remember the header order to know which number is bytes and which is files.

## 8. Trying to check the next row (abandoned)

EXPECT: I wanted to hear the second row to confirm the table is newest-first.
DO: Jumped to "next link" hoping to skip ahead (step 80), then pressed previous a few times (steps 81-86).
SAW: The link jump wrapped me right back to "link, Cronmon" at the top, since there are no links after the table. Going backwards from the top dropped me at the end of the document, which was developer debug-toolbar noise (ignored). I decided not to walk the whole page again; the "3 days ago" match is good enough evidence for my manager.

## Closing reflection

Completed? Yes, I believe so, with fairly high confidence (around 85%).
- Last check-in: Monday 5 October 2026 at 7:14 AM (3 days ago).
- Allowed lateness: 6 hours grace. It runs once daily and is not silenced, so alerts would go out.
The remaining doubt: "grace" was never explained, so I'm inferring it means "how long late before alerting"; and I didn't confirm the check-ins table is sorted newest-first (only that the top row matches "3 days ago").

Total: 86 reader steps.

What went well:
- The job list link on the home page is superb for a screen-reader user: one link announcement gave me name, schedule, grace period, location and last check-in. I effectively had the answer by step 12.
- The check-ins table is a real table with column headers, and the Silenced switch has a clear description.

Real friction:
- No headings anywhere and no main landmark, on either page. Heading jumps and "Main" jumps did nothing. The job title, and section titles like "Schedule", "Owner", "Check-in URL" and "Recent check-ins", are all spoken as plain text. That turned the job page into a 50-step linear walk instead of a few jumps.
- Following the job link gave no feedback at all: no "page loaded", no new title. I only worked out I'd moved by noticing the link list changed. A sighted user gets this for free.
- The page title seemingly stays "Cronmon" rather than naming the job (I only heard the title once, on the home page).
- Verbosity: every paragraph and column header is three stops (start / text / end). Reading four column headers took 14 steps.
- "1 × daily" reads as "one times daily"; and the grace value had no spoken label in front of it, unlike Schedule and Owner.
- A second "navigation" region holding only a Logout button made me think I'd wrapped round to the top.
- Table data rows are read as one run of numbers; without column names repeated I had to remember which number was bytes vs files (didn't matter for this task).

Expected vs got: I expected a job page with a heading for the job name and headings per section, so I could jump straight to "Recent check-ins". What I got was correct, well-labelled-ish content with no navigable structure - findable, but only by patience.
