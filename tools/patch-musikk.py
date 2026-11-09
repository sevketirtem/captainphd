#!/usr/bin/env python3
"""Valgfri bakgrunnsmusikk («Musikk: på/av») i de seks spillsidene (idempotent).

* <style id="musikk-css"> og <script id="musikk-js"> byttes ut hver gang.
* Musikken spilles ALDRI automatisk: den starter bare etter et brukerklikk (på musikkknappen,
  eller på Start-knappen hvis brukeren har slått den på tidligere).
* Fil: static/audio/tema.mp3 (Google Lyria, KI-generert), to lydelementer med 1,5 s kryssing i sløyfe.
* Lydspill (lydsignaler, nodsignaler) sender hendelsen «cphd:sound» ({sec}); musikken pauses
  mens signalet spilles og fortsetter etterpå. Lydsignaler har musikk av som standard og eget valg.
Kjør etter patch-share.py, patch-more.py og patch-ui.py."""
import re, os
ROOT = os.path.join(os.path.dirname(__file__), '..', 'static')
GAMES = ['lanterner', 'hvem-viker', 'manovrer', 'lydsignaler', 'nodsignaler', 'utkikk-fart', 'definisjoner']

CSS = r"""<style id="musikk-css">
/* MUSIKK-BEGIN */
.musikk { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; margin: 12px 0 0; }
.musikk button { display: inline-flex; align-items: center; gap: 8px; min-height: 40px; padding: 6px 14px; border-radius: 999px;
  border: 1px solid var(--line); background: var(--surface); color: var(--fg); font: inherit; font-size: 14px; cursor: pointer; }
.musikk button:hover { border-color: var(--sea); }
.musikk button[aria-pressed="true"] { background: var(--tint, var(--surface)); border-color: var(--sea); box-shadow: inset 0 0 0 1px var(--sea); }
.musikk button svg { width: 18px; height: 18px; flex: none; }
.musikk .muz-note { font-size: 12px; color: var(--muted); }
/* MUSIKK-END */
</style>
"""

JS = r"""<script id="musikk-js">
/* MUSIKK-BEGIN */
(function () {
  var d = document, root = d.documentElement, game = d.body.dataset.game || '';
  var go = d.getElementById('go'); if (!go || d.getElementById('musikk')) return;
  var KEY = game === 'lydsignaler' ? 'cphd-music-lyd' : 'cphd-music';
  var SRC = (location.pathname.replace(/[^\/]*$/, '').replace(/[^\/]+\/$/, '') || '/') + 'audio/tema.mp3';
  var V = 0.35, X = 1500;
  var T = { nb: { on: 'Musikk: på', off: 'Musikk: av', note: 'Musikk laget med KI (Google Lyria)' },
            en: { on: 'Music: on', off: 'Music: off', note: 'Music made with AI (Google Lyria)' } };
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
                set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  var want = store.get(KEY) === '1';           // brukerens valg (lagres)
  var playing = false, hold = false, cur = 0, timer = null, resumeT = null, started = false;
  var tracks = [new Audio(), new Audio()];
  tracks.forEach(function (a) { a.preload = 'none'; a.volume = 0; a.setAttribute('playsinline', ''); });

  var p = d.createElement('p'); p.className = 'musikk';
  p.innerHTML = '<button type="button" id="musikk" aria-pressed="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18V5l12-2v13M9 18a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM21 16a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/></svg><span></span></button><span class="muz-note"></span>';
  go.parentNode.insertBefore(p, go.nextSibling);
  var btn = p.querySelector('button'), label = btn.querySelector('span'), note = p.querySelector('.muz-note');

  function L() { return T[root.lang === 'en' ? 'en' : 'nb']; }
  function render() { label.textContent = want ? L().on : L().off; btn.setAttribute('aria-pressed', want ? 'true' : 'false'); note.textContent = L().note; }
  function fade(a, to, ms, done) {
    if (a._f) clearInterval(a._f);
    var from = a.volume, t0 = Date.now();
    a._f = setInterval(function () {
      var k = Math.min(1, (Date.now() - t0) / ms); a.volume = Math.max(0, Math.min(1, from + (to - from) * k));
      if (k >= 1) { clearInterval(a._f); a._f = null; if (done) done(); }
    }, 50);
  }
  function begin(i) {
    var a = tracks[i]; if (!a.src) a.src = SRC;
    try { a.currentTime = 0; } catch (e) {}
    var pr = a.play(); if (pr && pr.catch) pr.catch(function () { playing = false; });
    fade(a, V, X);
  }
  function watch() {
    var a = tracks[cur];
    if (playing && a.duration && !a.paused && a.currentTime >= a.duration - X / 1000 - 0.1) {
      fade(a, 0, X, function () { a.pause(); });
      cur = 1 - cur; begin(cur);
    }
  }
  function start() {
    if (playing || hold || !want) return;
    playing = true; begin(cur);
    if (!timer) timer = setInterval(watch, 200);
  }
  function stop(ms) {
    playing = false;
    tracks.forEach(function (a) { fade(a, 0, ms == null ? 500 : ms, function () { if (!playing) a.pause(); }); });
  }
  btn.addEventListener('click', function () {
    want = !want; store.set(KEY, want ? '1' : '0'); render();
    if (want) { hold = false; start(); } else stop();
  });
  /* starter bare etter brukerklikk på Start, hvis brukeren allerede har valgt musikk */
  go.addEventListener('click', function () { if (want) start(); });
  /* signalspill: pause musikken mens lydsignalet spilles */
  d.addEventListener('cphd:sound', function (e) {
    if (!want || !playing) return;
    var sec = (e.detail && e.detail.sec) || 6;
    hold = true; stop(200);
    clearTimeout(resumeT);
    resumeT = setTimeout(function () { hold = false; if (want) start(); }, sec * 1000 + 800);
  });
  d.addEventListener('visibilitychange', function () {
    if (d.hidden) { if (playing) { stop(100); playing = false; started = true; } }
    else if (started && want) { started = false; start(); }
  });
  new MutationObserver(render).observe(root, { attributes: true, attributeFilter: ['lang'] });
  render();
})();
/* MUSIKK-END */
</script>
"""

STYLE_BLOCK = re.compile(r'\n?<style id="musikk-css">.*?</style>\n?', re.S)
SCRIPT_BLOCK = re.compile(r'<script id="musikk-js">.*?</script>\n', re.S)

for slug in GAMES:
    p = os.path.join(ROOT, slug, 'index.html')
    s = open(p, encoding='utf-8').read()
    s = STYLE_BLOCK.sub('', s)
    s = SCRIPT_BLOCK.sub('', s)
    hd, tl = s.split('</head>', 1)
    s = re.sub(r'\n{3,}', '\n\n', hd) + '</head>' + tl
    head_end = s.index('</head>')
    last_style = s.rfind('</style>', 0, head_end)
    assert last_style != -1, slug
    cut = last_style + len('</style>')
    s = s[:cut] + '\n' + CSS + s[cut:]
    s = s.replace('</body>', JS + '</body>', 1)
    assert s.count('id="musikk-css"') == 1 and s.count('id="musikk-js"') == 1, slug
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', slug)
