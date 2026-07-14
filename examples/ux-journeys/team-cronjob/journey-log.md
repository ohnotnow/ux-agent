# UX Journey: Create a team cronjob ("Nightly Photo Backups")

**Persona:** staff member with an admin account (`admin2x`)
**Task as given by manager:** "Create a new cronjob for 'Nightly Photo Backups' that runs daily, grace period of 2hrs, personal. Once it's created, change it to belong to the 'Fulfilment' team."
**Date:** 2026-07-13

---

## 1. Arriving at the app

EXPECT: Going to https://cronmon.lndo.site will show me either a login page or maybe a public landing page with a "Log in" link. I expect username/password boxes since I've been given credentials.

DO: Opened the browser and went to https://cronmon.lndo.site.

SAW: Redirected straight to a login page ("Cronmon Login") with Username and Password boxes and a "Log In" button. Matches my expectation. There's some developer debug toolbar stuff at the bottom of the page (request timings etc.) which I'll ignore — presumably because this is a dev copy.

## 2. Logging in

EXPECT: Entering admin2x / secret and clicking "Log In" should land me on some kind of dashboard or list of monitored cron jobs.

DO: Typed my username and password into the two boxes and clicked "Log In".

SAW: Logged straight in, landed on a "Your jobs" dashboard — exactly what I hoped for. There's a sidebar (Home, New job, Admin, My settings, Logout), tabs for "My jobs" / "Team jobs" / "Alerting jobs", a list of existing jobs (things like nightly-backup.sh, rotate-logs), and a clear "New job" button at the top right of the main panel. Screenshot: shots/02-logged-in-dashboard.png

## 3. Starting the new job

EXPECT: Clicking the "New job" button in the top right should open a creation form (page or modal) with fields for at least a name and schedule. I'm hoping to see something for "daily", a grace period field, and some personal/team choice, since my manager specifically said "personal".

DO: Clicked the "New job" button at the top right of the jobs panel.

SAW: A "New job" modal opened over the dashboard — better than expected, everything I need looks present: Name, Description, optional Location, a Schedule section ("How many" + "Per" dropdown with Hourly/Daily/Weekly/Monthly, or a cron expression box — nice that I don't have to write cron syntax), a Grace period (number + Minutes/Hours/Days), and a "Team (optional)" dropdown that says "Leave blank to make this a personal job" and currently shows "Personal — just me". One thing catches my eye though: the Team dropdown only lists "Application Development" and "Infrastructure" — I don't see a "Fulfilment" team. That worries me a little for the second half of my task, but the job is meant to start personal anyway, so I'll deal with that after creating it. Screenshot: shots/03-new-job-form.png

## 4. Filling in the form

EXPECT: I'll set Name to "Nightly Photo Backups", schedule "1 × Daily", grace period 2 Hours, and leave Team as "Personal — just me". Clicking "Create job" should close the modal and show my new job in the "My jobs" list.

DO: Typed "Nightly Photo Backups" in Name, left Description and Location blank, left "How many" at 1 and picked "Daily" from the Per dropdown, set the grace period number to 2 and changed its unit to "Hours", left Team on "Personal — just me", then clicked "Create job".

SAW: The modal closed and "Nightly Photo Backups — 1 × Daily · 2 hours grace — No check-ins yet" now sits in my "My jobs" list. Exactly as hoped. First half of the task done. Screenshot: shots/05-job-created.png

## 5. Now to move it to the 'Fulfilment' team

EXPECT: Clicking the new job in the list should open a detail page where I can edit it, including its team. But I'm already suspicious: the create form's Team dropdown only offered "Application Development" and "Infrastructure" — no "Fulfilment". So either the job detail page offers more teams (unlikely), or the Fulfilment team doesn't exist yet and I'll need to create it — presumably somewhere under "Admin" in the sidebar, since I have an admin account.

DO: Clicked on "Nightly Photo Backups" in the My jobs list.

SAW: A job detail page for Nightly Photo Backups — schedule "1 × daily", "2 hours grace", Owner "Personal — Jenny MacAdmin" (apparently that's me!), a check-in URL to curl from the job, a Silenced toggle, and Edit / Delete buttons at the top. So editing looks straightforward.

## 6. Opening the edit form

EXPECT: Clicking "Edit" will reopen the same form as creation, with a Team dropdown. I predict it will still only offer Application Development and Infrastructure, in which case I'll have to go create the Fulfilment team first via the Admin area.

DO: Clicked the "Edit" button on the job detail page.

SAW: The "Edit job" modal opened, pre-filled with everything I entered. And yes — the Team dropdown still only offers "Personal — just me", "Application Development", and "Infrastructure". No "Fulfilment". So my manager has asked me to assign the job to a team that doesn't exist in the system yet. Slight "…now what?" moment here — but as I'm an admin, my best guess is the Admin sidebar link will let me create a team. There's nothing on this form (like a "create new team" option in the dropdown) that would let me do it from here. Screenshot: shots/06-edit-no-fulfilment-team.png

## 7. Off to the Admin area

EXPECT: Cancelling this modal and clicking "Admin" in the sidebar should show me some management area — hopefully with a Teams section where I can add "Fulfilment".

DO: Clicked "Cancel" on the edit modal, then clicked "Admin" in the sidebar.

SAW: The Admin landing page has three tiles — Teams ("Create teams, manage membership, silence as a group"), Users, and API tokens — plus an "Estate health" overview. And here's the surprise: the "By team" table at the bottom lists SEVEN teams, including... "Fulfilment" (3 jobs)! So the team exists after all. The job form's Team dropdown must only show teams *I'm a member of*. That was genuinely confusing — the dropdown gave me no hint that other teams existed but were hidden from me. So my plan changes: I don't need to create the team, I (probably) need to add myself to it — or maybe as an admin I can reassign the job from the Teams admin area directly. Screenshot: shots/07-admin-fulfilment-exists.png

## 8. Into the Teams admin

EXPECT: Clicking the "Teams" tile will list all the teams with some way to manage membership. I'm hoping I can either add myself to Fulfilment, or find a way to move jobs into the team directly.

DO: Clicked the "Teams" tile on the Admin page.

SAW: A Teams table listing all six teams (plus a "New team" button) — Fulfilment is right there with 4 members and 3 jobs, a notification email, and Edit/Delete buttons. The team name itself is a link.

## 9. Looking inside the Fulfilment team

EXPECT: Clicking the "Fulfilment" name will show the team's detail — members and maybe its jobs — with some way to add a member. I plan to add myself, on the theory that being a member is what makes a team show up in the job form's Team dropdown.

DO: Clicked the "Fulfilment" link in the Teams table.

SAW: The Fulfilment team page — team email, a team-wide Silenced toggle, and a Members section listing four people (none of them me) with an "Add a user…" dropdown and an "Add" button. Notably there's nothing here about the team's jobs, so I can't reassign my job from this side; membership looks like the way in. Screenshot: shots/09-fulfilment-team-page.png

## 10. Adding myself to the Fulfilment team

EXPECT: Opening the "Add a user…" dropdown should list user accounts; I'll look for myself ("Jenny MacAdmin" — the name the job page showed as the owner). After clicking "Add" I should appear in the members table.

DO: Clicked the "Add a user…" dropdown to see the list of users.

SAW: The dropdown listed all users by real name and email — I spotted "Jenny MacAdmin (admin2x@example.test)", which matches the name shown as the job's owner, so that's me. Selected it, clicked "Add", and I now appear in the Fulfilment members table. Small nit: I logged in as "admin2x" but had to recognise myself by a display name I'd only seen in passing on the job page — if I hadn't noticed "Jenny MacAdmin" earlier, I'd have been scanning that list for "admin2x". The email containing admin2x saved me. Screenshot: shots/10-added-to-fulfilment.png

## 11. Back to the job to set its team

EXPECT: Now that I'm a Fulfilment member, the Team dropdown on the job's edit form should include "Fulfilment". I'll go Home, open Nightly Photo Backups, hit Edit, and switch the Team to Fulfilment.

DO: Clicked "Home" in the sidebar, then clicked "Nightly Photo Backups" in the My jobs list, then clicked "Edit".

SAW: Went Home, the job was still in "My jobs", opened it, clicked Edit — and this time the Team dropdown DID include "Fulfilment". So membership is indeed what gates the dropdown. Picked "Fulfilment", clicked "Save changes", got a green "Job updated." toast, and the job page's Owner box now reads "Team: Fulfilment" (Created by Jenny MacAdmin). Screenshots: shots/11-team-dropdown-has-fulfilment.png, shots/12-job-now-fulfilment.png

## 12. Final double-check on the dashboard

EXPECT: Back on Home, the job should now appear under the "Team jobs" tab (probably grouped under Fulfilment) rather than — or as well as — "My jobs".

DO: Clicked "Home" in the sidebar, then the "Team jobs" tab, and typed "Nightly" into the filter box.

SAW: The Team jobs tab does now contain my job — but there was a small surprise on the way. Typing "Nightly Photo" into the filter matched dozens of other teams' jobs ("Conference Portal — nightly database backup" etc.), so the filter seems to match ANY of the words rather than the whole phrase, and my job wasn't even visible in the viewport. Typing just "Photo" narrowed it to exactly one card: "Nightly Photo Backups — 1 × Daily · 2 hours grace · Team: Fulfilment — No check-ins yet". That's my job, on the right team, with the right schedule and grace period. Screenshots: shots/13-team-jobs-final-check.png (noisy filter), shots/13b-team-jobs-photo-filter.png (final state).

## Closing reflection

**Did I complete the task as asked?** Yes, I believe so, with high confidence. The job "Nightly Photo Backups" exists, runs 1 × Daily, has a 2-hour grace period, was created as personal ("Personal — just me"), and afterwards was changed to be owned by "Team: Fulfilment" — confirmed on the job detail page, by the "Job updated." toast, and by finding it under the Team jobs tab labelled with the team.

**Real friction moments:**

1. **The Team dropdown silently hides teams you're not in.** This was the big one. Both the create and edit forms offered only "Application Development" and "Infrastructure", with no hint that four other teams existed. If I hadn't had admin rights and stumbled on the "By team" table on the Admin page, I would honestly have concluded that Fulfilment didn't exist and gone off to create a duplicate team (the "New team" button was right there — a less patient colleague would have clicked it). A one-line hint under the dropdown like "Only teams you belong to are shown" would have completely defused this. A non-admin user given this same task would have hit a dead end with no way forward except asking around.
2. **Nothing on the team page mentions its jobs.** On the Fulfilment admin page I could manage members and silencing, but there was no way to see or reassign the team's jobs from that side. The only route to "give this job to that team" is via membership + job edit. That's a defensible design, but the route is invisible until you already know it.
3. **Identifying myself in the user list.** I log in as "admin2x" but the app knows me as "Jenny MacAdmin". The only reason I recognised myself in the "Add a user…" list was having noticed "Created by Jenny MacAdmin" on the job page earlier (and the account email happening to contain "admin2x"). A "(you)" marker in user lists would be a nice touch.
4. **The dashboard filter matches any word, not the phrase.** Filtering Team jobs for "Nightly Photo" surfaced a page full of other teams' "nightly database backup" jobs, with mine nowhere in view; only filtering for "Photo" isolated it. Minor, but it briefly made me wonder if my job hadn't been assigned after all.

**Expected vs offered:** I expected a "create new team" barrier; instead the barrier was discovering an *existing* team that was hidden from me. The creation flow itself was genuinely pleasant — the interval picker ("1 × Daily") meant I never had to write a cron expression, the grace period control matched the task phrasing exactly ("2 hours"), and "Leave blank to make this a personal job" answered the "personal" requirement before I could even wonder about it. The Edit modal reusing the create form made the second half of the task feel familiar. The one structural gap: for the very common manager-ask "put this job under team X", the app offers no direct path — you have to deduce that team membership gates the dropdown, and only an admin can act on that deduction alone.
