// Replay script for the "Silencing alerts for a job" end-user doc.
// Re-run to re-record the clips after a UI change:
//
//   playwright-cli run-code --filename=examples/user-guides/silencing-a-job/record.js
//
// Then convert the webm clips to mp4 (see README note in doc.yaml) or re-run
// the ffmpeg loop. Assumes the .playwright/cli.config.json in the project root
// (ignores the Lando self-signed cert, 1280x800 viewport).
//
// CLIP_DIR must be absolute: relative paths resolve against the playwright-cli
// daemon's working directory, which is not necessarily the project root.

async page => {
  const BASE = 'https://cronmon.lndo.site';
  const CLIP_DIR = '/ABSOLUTE/PATH/TO/ux-agent/examples/user-guides/silencing-a-job/clips';
  const SIZE = { width: 1280, height: 800 };

  // Hide the Laravel debugbar on every page load - dev-environment noise,
  // not something an end user would see.
  await page.addInitScript(() => {
    const hide = () => {
      const style = document.createElement('style');
      style.textContent = '.phpdebugbar { display: none !important; }';
      document.head.appendChild(style);
    };
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', hide);
    } else {
      hide();
    }
  });

  // ---- Prep (not recorded): job must start unsilenced, user logged out ----
  await page.goto(BASE + '/jobs/311');
  const prepSwitch = page.getByRole('switch', { name: 'Silenced' });
  if (await prepSwitch.isChecked()) {
    await Promise.all([
      page.waitForResponse(r => r.url().includes('/update')),
      prepSwitch.click(),
    ]);
  }
  await page.context().clearCookies();

  // ---- Clip 1: Log in ----
  await page.goto(BASE + '/login');
  await page.screencast.start({ path: CLIP_DIR + '/01-log-in.webm', size: SIZE });
  await page.waitForTimeout(900);
  const username = page.getByRole('textbox', { name: 'Username' });
  await username.click();
  await username.pressSequentially('admin2x', { delay: 70 });
  const password = page.getByRole('textbox', { name: 'Password' });
  await password.click();
  await password.pressSequentially('secret', { delay: 70 });
  await page.waitForTimeout(400);
  await page.getByRole('button', { name: 'Log In' }).click();
  await page.waitForURL(BASE + '/');
  await page.waitForTimeout(1400);
  await page.screencast.stop();

  // ---- Clip 2: Find the job ----
  await page.screencast.start({ path: CLIP_DIR + '/02-find-the-job.webm', size: SIZE });
  await page.waitForTimeout(900);
  const filter = page.getByRole('textbox', { name: 'Filter by name, description, or location' });
  await filter.click();
  await filter.pressSequentially('rotate', { delay: 80 });
  await page.waitForTimeout(1200);
  await page.getByRole('link', { name: /rotate-logs/ }).click();
  await page.waitForURL(BASE + '/jobs/311');
  await page.waitForTimeout(1400);
  await page.screencast.stop();

  // ---- Clip 3: Silence the job ----
  await page.screencast.start({ path: CLIP_DIR + '/03-silence-the-job.webm', size: SIZE });
  await page.waitForTimeout(900);

  const silenced = page.getByRole('switch', { name: 'Silenced' });
  const box = await silenced.boundingBox();
  const ring = await page.screencast.showOverlay(`
    <div style="position: absolute;
      top: ${box.y - 8}px; left: ${box.x - 8}px;
      width: ${box.width + 16}px; height: ${box.height + 16}px;
      border: 3px solid #4f46e5; border-radius: 9999px;"></div>
  `);
  await page.waitForTimeout(1300);
  await silenced.click();
  await ring.dispose();

  const reason = page.getByRole('textbox', { name: 'Reason (optional)' });
  await reason.waitFor();
  await page.waitForTimeout(900);
  await reason.click();
  await reason.pressSequentially('service is being upgraded', { delay: 70 });
  await page.waitForTimeout(400);
  // Blur onto something neutral. NOT the "Silenced" label - clicking a
  // switch's label toggles the switch.
  await page.getByText('Recent check-ins', { exact: true }).click();
  await page.waitForTimeout(1600);
  await page.screencast.stop();

  return 'Recorded 3 clips to ' + CLIP_DIR;
}
