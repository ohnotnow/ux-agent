// Probe-facing wrapper round @guidepup/virtual-screen-reader (window.__a11yVsr).
// Every movement returns "[step N] <phrase>". When the page body has been
// swapped (SPA navigation) or reloaded, the reader is restarted at the top
// (see ensure() for what, if anything, is announced).
(function () {
  if (window.__sr) return;
  var steps = Number(sessionStorage.getItem('__srSteps') || 0);
  var container = null;

  function tag(phrase) {
    steps += 1;
    sessionStorage.setItem('__srSteps', String(steps));
    return '[step ' + steps + '] ' + phrase;
  }

  // A full load announces the title (real readers reliably do). An in-place
  // body swap announces NOTHING: what a real reader says there is unknown, and
  // inventing an announcement would hide a possible "silent navigation" finding.
  // Restarting at the top after a swap is itself a simulation assumption.
  async function ensure() {
    var v = window.__a11yVsr;
    if (container === document.body) return null;
    var fullLoad = container === null;
    try { await v.stop(); } catch (e) {}
    await v.start({ container: document.body });
    container = document.body;
    return fullLoad ? 'new page loaded, title: ' + document.title : 'swapped';
  }

  async function move(fn) {
    var v = window.__a11yVsr;
    var fresh = await ensure();
    if (fresh && fresh !== 'swapped') return tag(fresh);
    await fn(v);
    return tag(liveState(v.activeNode, await v.lastSpokenPhrase()));
  }

  // The reader reads a native checkbox/radio's `checked` ATTRIBUTE, not its
  // live state, so it never hears the box being ticked. Real readers do;
  // correct the phrase from the element itself.
  function liveState(node, phrase) {
    if (!node || node.nodeName !== 'INPUT' || !/^(checkbox|radio)$/.test(node.type)) return phrase;
    return phrase.replace(/\b(not checked|checked)\b/, node.checked ? 'checked' : 'not checked');
  }

  // After act() the reader announces the control's OLD state: its view of
  // the page catches up with ARIA changes (e.g. a switch) only after a short
  // delay. Wait, then step off and back (uncounted) to hear the new state.
  function activate() {
    return move(async function (v) {
      var toggle = /^(checkbox|radio|switch)\b/.test(await v.lastSpokenPhrase());
      await v.act();
      if (toggle) {
        await new Promise(function (resolve) { setTimeout(resolve, 200); });
        await v.previous();
        await v.next();
      }
    });
  }

  window.__sr = {
    next: function () { return move(function (v) { return v.next(); }); },
    previous: function () { return move(function (v) { return v.previous(); }); },
    jump: function (kind) {
      return move(function (v) { return v.perform(v.commands['moveToNext' + kind]); });
    },
    jumpBack: function (kind) {
      return move(function (v) { return v.perform(v.commands['moveToPrevious' + kind]); });
    },
    activate: activate,
    // The reader's press() sends synthetic keys, which never toggle a native
    // checkbox or a switch; Space on a real reader does, so route it to act().
    press: function (key) {
      if (key === 'Space' || key === ' ') return activate();
      return move(function (v) { return v.press(key); });
    },
    type: function (text) { return move(function (v) { return v.type(text); }); },
    steps: function () { return steps; },
  };
})();
