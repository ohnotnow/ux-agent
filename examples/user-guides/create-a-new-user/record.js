// Replay script for the "Adding a new user to a team" guide.
// Re-run to re-record the clips after a UI change:
//
//   playwright-cli run-code --filename=examples/user-guides/create-a-new-user/record.js
//
// Start the playwright-cli session from the project root so the daemon's cwd
// (and its .playwright-cli artefacts) land there. Then convert clips to mp4:
//   ffmpeg -i clip.webm -c:v libx264 -pix_fmt yuv420p -crf 23 -movflags +faststart clip.mp4
//
// CLIP_DIR must be absolute: relative paths resolve against the daemon's cwd.

async page => {
  const BASE = 'https://cronmon.lndo.site';
  const CLIP_DIR = '/ABSOLUTE/PATH/TO/ux-agent/examples/user-guides/create-a-new-user/clips';
  const SIZE = { width: 1280, height: 800 };

  // Hide the Laravel debugbar on every page load.
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

  const ringAround = async locator => {
    const box = await locator.boundingBox();
    return page.screencast.showOverlay(`
      <div style="position: absolute;
        top: ${box.y - 8}px; left: ${box.x - 8}px;
        width: ${box.width + 16}px; height: ${box.height + 16}px;
        border: 3px solid #4f46e5; border-radius: 12px;"></div>
    `);
  };

  // ---- Prep (not recorded): delete Jenny McSmith if she exists, log out ----
  await page.goto(BASE + '/admin/users');
  if (page.url().includes('/login')) {
    await page.getByRole('textbox', { name: 'Username' }).fill('admin2x');
    await page.getByRole('textbox', { name: 'Password' }).fill('secret');
    await page.getByRole('button', { name: 'Log In' }).click();
    await page.waitForURL(BASE + '/');
    await page.goto(BASE + '/admin/users');
  }
  const staleRow = page.getByRole('row', { name: /Jenny McSmith/ });
  if (await staleRow.count()) {
    await staleRow.getByRole('button', { name: 'Delete' }).click();
    const dialog = page.getByRole('dialog');
    await dialog.getByRole('textbox').fill('Jenny McSmith');
    await dialog.getByRole('button', { name: 'Delete' }).click();
    await staleRow.waitFor({ state: 'detached' });
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

  // ---- Clip 2: Open the admin area ----
  await page.screencast.start({ path: CLIP_DIR + '/02-open-the-admin-area.webm', size: SIZE });
  await page.waitForTimeout(900);
  const adminLink = page.getByRole('link', { name: 'Admin' });
  const adminRing = await ringAround(adminLink);
  await page.waitForTimeout(1100);
  await adminLink.click();
  await adminRing.dispose();
  await page.waitForURL(BASE + '/admin');
  await page.waitForTimeout(1000);
  await page.getByRole('link', { name: /^Users/ }).click();
  await page.waitForURL(BASE + '/admin/users');
  await page.waitForTimeout(1400);
  await page.screencast.stop();

  // ---- Clip 3: Create the user ----
  await page.screencast.start({ path: CLIP_DIR + '/03-create-the-user.webm', size: SIZE });
  await page.waitForTimeout(900);
  const newUser = page.getByRole('button', { name: 'New user' });
  const newUserRing = await ringAround(newUser);
  await page.waitForTimeout(1100);
  await newUser.click();
  await newUserRing.dispose();

  const dlg = page.getByRole('dialog');
  await dlg.getByRole('textbox', { name: 'Username' }).waitFor();
  await page.waitForTimeout(900);
  const fields = [
    ['Username', 'jmc2s'],
    ['Forenames', 'Jenny'],
    ['Surname', 'McSmith'],
    ['Email', 'jenny.mcsmith@example.com'],
  ];
  for (const [label, value] of fields) {
    const field = dlg.getByRole('textbox', { name: label });
    await field.click();
    await field.pressSequentially(value, { delay: 70 });
    await page.waitForTimeout(300);
  }
  await page.waitForTimeout(400);
  await dlg.getByRole('button', { name: 'Save' }).click();
  await page.getByRole('row', { name: /Jenny McSmith/ }).waitFor();
  await page.waitForTimeout(1600);
  await page.screencast.stop();

  // ---- Clip 4: Find the team ----
  await page.screencast.start({ path: CLIP_DIR + '/04-find-the-team.webm', size: SIZE });
  await page.waitForTimeout(900);
  await page.getByRole('link', { name: 'Admin' }).click();
  await page.waitForURL(BASE + '/admin');
  await page.waitForTimeout(1000);
  await page.getByRole('link', { name: /^Teams/ }).click();
  await page.waitForURL(BASE + '/admin/teams');
  await page.waitForTimeout(1000);
  await page.getByRole('link', { name: /Application Development/ }).click();
  await page.waitForTimeout(1400);
  await page.screencast.stop();

  // ---- Clip 5: Add them to the team ----
  await page.screencast.start({ path: CLIP_DIR + '/05-add-them-to-the-team.webm', size: SIZE });
  await page.waitForTimeout(900);
  const picker = page.getByRole('combobox').first();
  const pickerRing = await ringAround(picker);
  await page.waitForTimeout(1100);
  await picker.click();
  await pickerRing.dispose();
  await page.waitForTimeout(600);
  await page.keyboard.type('jenny', { delay: 70 });
  await page.waitForTimeout(800);
  await page.getByRole('option', { name: /Jenny McSmith/ }).click();
  await page.waitForTimeout(400);
  await page.getByRole('button', { name: 'Add', exact: true }).click();
  await page.getByRole('row', { name: /Jenny McSmith/ }).waitFor();
  await page.waitForTimeout(1600);
  await page.screencast.stop();

  return 'Recorded 5 clips to ' + CLIP_DIR;
}
