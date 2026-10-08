# Journey log: find the home NAS backup job's last check-in and its lateness allowance

Persona: member of staff with an admin account.
Task (manager's words): "One of your jobs backs up the home NAS. Can you find out when it last checked in, and how long it's allowed to be late before anyone gets alerted?"

Running action count is shown in each DO.

## 1. Open the app
EXPECT: A login page. The app's name may tell me what kind of tool it is.
DO: Opened the app URL (action 1, page load).
SAW: A plain login page titled "Cronmon Login" with Username and Password fields and a Log In button. "Cronmon" sounds like a cron-job monitor, which fits the "jobs check in" wording in my task. As expected.

## 2. Log in
EXPECT: After logging in, a dashboard or list of jobs, hopefully with some search box, because I don't know what the NAS job is called.
DO: Typed my username and password and clicked Log In (actions 2-4).
SAW: Landed on "Your jobs" with tabs My jobs / Team jobs / Alerting jobs and a filter box. Under My jobs there is exactly one card: "Personal home NAS backup", with the line "1 x Daily · 6 hours grace · Location: Home" and "Last check-in 3 days ago". Better than expected: both halves of my answer are sort of on the card already. Screenshot: shots/02-logged-in.png.
Two small doubts, though. "3 days ago" is vague; my manager probably wants an actual date and time. And "6 hours grace" is likely the "how late before alerting" figure, but I'm guessing at the meaning of "grace". Also slightly odd: a daily job that last checked in 3 days ago, and the subtitle says awol jobs come to the top, but this card shows no warning colour or badge that I can see. Is it late or not?

## 3. Open the job
EXPECT: A detail page with an exact last check-in timestamp and, ideally, a plain-words explanation of the alerting rule (e.g. "alerts if no check-in within X after expected").
DO: Clicked the "Personal home NAS backup" card (action 5, page load).
SAW: Job page with a Schedule box ("1 x daily", "6 hours grace"), an Owner box (Personal, Jenny MacAdmin, Location: Home), the check-in URL, a "Silenced" switch (currently off), and a "Recent check-ins" table. The top row reads "Mon, Oct 5, 2026 7:14 AM (3 days ago)", so that is the exact last check-in. Earlier ones were Sun 4 Oct and Sat 3 Oct, both at 9:14 AM. Screenshot: shots/03-job-page.png.
First half answered with confidence. Second half: "6 hours grace" is still the only clue, with no explanation of what grace counts from (the expected run time? the last check-in plus a day?). I'm fairly sure it means "6 hours late before alerting", but it's a guess.
The bigger surprise: nothing on this page tells me the job's status. It's a daily job, three days quiet, not silenced, yet I see no "late", "awol" or "OK" badge, no "next expected" time, and no "alert sent" note. So I can't tell my manager whether anyone has already been alerted, which is the obvious follow-up question. (Should I check the "Alerting jobs" tab? Possibly, but the job page itself ought to say.)
Also noticed: the check-in table's dates are in US style (Oct 5, 12-hour AM) and there is no time zone shown, so "7:14 AM" is a bit ambiguous.

## 4. Peek at the Edit form to confirm what "grace" means
EXPECT: The edit form will have a labelled field for grace, maybe with help text. I'll cancel without saving; I only want to read it. (Slightly nervous about opening an edit form just to read something.)
DO: Clicked the pencil (Edit) button at the top right of the job page (action 6).
SAW: An "Edit job" dialog. The section "Grace period" has the help text "How late can it be before we alert?" and is set to 6 Hours. That's exactly my manager's question in the app's own words, and it confirms my guess. Screenshot: shots/04-edit-form.png.
It's a shame this sentence only appears inside the Edit form. On the read-only page it's just "6 hours grace".
The form also shows "Email overrides: Alerts go to / Alerts come from", both blank ("Leave blank to use the owner's defaults"), so alerts would go to the owner (Jenny MacAdmin) by default. That's useful for "before anyone gets alerted": "anyone" here means the owner.

## 5. Back out of the form and check whether the job is alerting
EXPECT: Cancel closes the dialog with nothing changed. Then, since the job seems overdue, I expect to find the NAS job under the "Alerting jobs" tab.
DO: Clicked Cancel (action 7), clicked Home in the sidebar (action 8, page load), clicked the "Alerting jobs" tab (action 9), and typed "NAS" into the filter box (action 10).
SAW: Cancel closed the dialog cleanly. The unfiltered Alerting tab lists several other jobs, each with a helpful line like "Last check-in 5 days ago · Awol since 3 days ago" (shots/05-alerting-tab.png). So other cards do show an awol status, and the NAS card on My jobs showed none. With "NAS" in the filter, the tab says "Nothing is currently alerting." (shots/06-alerting-filtered-nas.png).
Two reactions. First, that message is misleading with a filter active. It should say something like "No alerting jobs match 'NAS'"; on a bad day I might read it as "all clear everywhere". Second, now what? By my arithmetic the NAS job (daily, last seen Monday 7:14 AM, 6 hours grace, today Thursday afternoon) should have gone awol a couple of days ago, yet the app says it isn't alerting. Maybe "1 x daily" with no fixed time is measured differently, or personal jobs behave differently, but nothing on screen explains it. I can answer the question my manager asked, but I'd have to add "and oddly, it isn't flagged as late".

## Closing reflection

**Did I complete the task?** Yes, with high confidence for both parts:
- Last check-in: Monday 5 October 2026 at 7:14 AM (shown as "3 days ago"; no time zone is displayed).
- Allowed lateness: a 6-hour grace period. The Edit form explicitly describes the grace period as "How late can it be before we alert?". With no email overrides set, alerts would go to the owner's default address.

**Effort:** about 6 actions to get both answers (open, 3 for login, open job, open Edit to confirm), plus 4 more on a follow-up I chose to make (cancel, home, Alerting tab, filter). The core task went smoothly: the job card on the home page shows "6 hours grace" and "Last check-in 3 days ago" straight away, and the job page gives the exact timestamp.

**Moments of real friction:**
1. "Grace" isn't explained on the read-only job page or the dashboard card. The plain-words explanation ("How late can it be before we alert?") only appears inside the Edit form, so I had to open an edit dialog just to read a definition. It would help to show that sentence, or "alerts if 6 hours late", on the job page.
2. The job page has no status. No OK/late/awol badge, no "next check-in expected by", no "alerted at". The Alerting tab cards have "Awol since…" but the job's own page doesn't. That's the first thing a manager will ask after "when did it last check in?".
3. A possible correctness concern: a daily job with no check-in for over three days, not silenced, isn't shown as awol or alerting. I can't tell from the UI whether this is a bug or a rule I don't understand (e.g. how "1 x daily" is measured). Worth a developer's look.
4. With a filter active, the empty Alerting tab says "Nothing is currently alerting.", which reads like a global all-clear.
5. Minor: US-style dates and 12-hour times with no time zone, in what looks like a UK institution's tool.

**Expected vs offered:** I expected a job page that answers "when did it last run, when is it next due, and is it late?" in one glance. The app answers the first well, states the grace period tersely, and leaves "is it late / has anyone been told?" unanswered (and, from the Alerting tab, apparently answers "no" when I'd expect "yes").
