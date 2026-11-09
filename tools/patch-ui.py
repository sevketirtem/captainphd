#!/usr/bin/env python3
"""Felles brukergrensesnitt for de seks spillsidene (idempotent).

Legger inn:
  * <style id="ui-css"> etter hovedstilen (overstyrer, uavhengig av rekkefølgen til
    patch-share.py og patch-more.py som skriver inn i den første <style>),
  * <script id="ui-js"> før </body> (ikoner på modusknapper, fremdriftslinje,
    poengtelling på resultatskjermen, aria-live, kicker over tittelen),
  * data-game på <body> og theme-color-meta.
Blokkene byttes ut på nytt hver gang. Kjør etter patch-share.py og patch-more.py
(rekkefølgen er likevel uten betydning for utseendet)."""
import re, os
ROOT = os.path.join(os.path.dirname(__file__), '..', 'static')
GAMES = {
 'lanterner':   ('K52 · Regel 20–31',            'K52 · Rules 20–31'),
 'hvem-viker':  ('K52 · Regel 11–19',            'K52 · Rules 11–19'),
 'manovrer':    ('K52 · Regel 8, 15–17, 34',     'K52 · Rules 8, 15–17, 34'),
 'lydsignaler': ('K52 · Regel 32–37',            'K52 · Rules 32–37'),
 'nodsignaler': ('K52 · Regel 37, vedlegg IV',   'K52 · Rule 37, Annex IV'),
 'utkikk-fart': ('K52 · Regel 5–7, 9–10',        'K52 · Rules 5–7, 9–10'),
 'definisjoner': ('K52 · Regel 1–4, 38',          'K52 · Rules 1–4, 38'),
}

CSS = r"""<style id="ui-css">
/* UI-BEGIN */
:root {
  color-scheme: light dark;
  --r: 14px; --r-sm: 10px;
  --shadow: 0 1px 2px rgba(11,34,51,.06), 0 10px 28px rgba(11,34,51,.09);
  --halo: #dbe9f0; --tint: #e7f0f5; --ring: #1d5c7a;
}
@media (prefers-color-scheme: dark) {
  :root { --shadow: 0 1px 2px rgba(0,0,0,.45), 0 12px 32px rgba(0,0,0,.38); --halo: #12384f; --tint: #14303f; --ring: #8cc8e4; }
}
html { -webkit-text-size-adjust: 100%; }
body { font-size: 17px; line-height: 1.55; min-height: 100vh;
  background: radial-gradient(900px 420px at 50% -80px, var(--halo), transparent 72%) no-repeat, var(--bg); }
.wrap { max-width: 780px; padding: 0 16px; }
header { padding: 14px 0 8px; }
.home { display: inline-flex; align-items: center; gap: 8px; letter-spacing: .01em; }
.home::before { content: ""; width: 22px; height: 22px; background: currentColor; opacity: .9;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='5' r='2.5'/%3E%3Cpath d='M12 7.5V21M7 11h10M4 15a8 8 0 0 0 16 0'/%3E%3C/svg%3E") center/contain no-repeat;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='5' r='2.5'/%3E%3Cpath d='M12 7.5V21M7 11h10M4 15a8 8 0 0 0 16 0'/%3E%3C/svg%3E") center/contain no-repeat; }
.lang { min-height: 36px; padding: 4px 12px; border-radius: 999px; background: var(--surface); }
.lang:hover { border-color: var(--sea); }
.kicker { display: inline-block; font: 600 12px/1 var(--mono); letter-spacing: .08em; text-transform: uppercase;
  color: var(--sea); background: var(--tint); border-radius: 999px; padding: 6px 11px; margin: 10px 0 0; }
h1 { font-weight: 800; letter-spacing: -.015em; margin: 12px 0 8px; }
.lede { font-size: 17px; max-width: 62ch; }
.panel { border-radius: 16px; padding: 20px; box-shadow: var(--shadow); }
button { -webkit-tap-highlight-color: transparent; }
button:focus-visible, a:focus-visible, select:focus-visible, input:focus-visible, [tabindex]:focus-visible { outline: 3px solid var(--ring); outline-offset: 2px; }
.modes { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 14px 0 16px; }
.modes button { display: flex; flex-direction: column; gap: 2px; min-height: 92px; padding: 12px 14px; border-radius: var(--r);
  background: var(--surface); transition: transform .15s ease, border-color .15s ease, background-color .15s ease; }
.modes button:hover { border-color: var(--sea); }
.modes button .ic { width: 26px; height: 26px; margin-bottom: 4px; color: var(--sea); flex: none; }
.modes button b { font-size: 16px; }
.modes button span { font-size: 13px; line-height: 1.35; }
.modes button[aria-pressed="true"] { background: var(--tint); border-color: var(--sea); box-shadow: inset 0 0 0 2px var(--sea); }
.primary { min-height: 54px; border-radius: 12px; font-size: 17px; letter-spacing: .01em;
  box-shadow: 0 2px 0 rgba(0,0,0,.18), 0 8px 18px rgba(214,64,47,.22); transition: transform .12s ease, filter .15s ease; }
.primary:hover { filter: brightness(1.06); }
.primary:active { transform: translateY(1px) scale(.995); }
#best:not(:empty) { display: inline-flex; align-items: center; gap: 8px; margin: 14px 0 0 !important; padding: 7px 13px;
  font-size: 14px; color: var(--fg); background: var(--tint); border-radius: 999px; }
#best:not(:empty)::before { content: ""; width: 18px; height: 18px; flex: none; background: var(--sea);
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0zM17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3'/%3E%3C/svg%3E") center/contain no-repeat;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0zM17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3'/%3E%3C/svg%3E") center/contain no-repeat; }
.bar { align-items: center; gap: 10px; margin-bottom: 8px; font-size: 14px; }
.bar > span { background: var(--bg); border: 1px solid var(--line); border-radius: 999px; padding: 3px 12px; }
#clock { font-variant-numeric: tabular-nums; }
.pbar { height: 6px; border-radius: 999px; background: var(--line); overflow: hidden; margin: 0 0 14px; }
.pbar i { display: block; height: 100%; width: 0; border-radius: inherit; background: linear-gradient(90deg, var(--sea), var(--ok)); transition: width .4s ease; }
.scene { border-radius: var(--r-sm); }
.q { font-size: 18px; line-height: 1.45; margin: 16px 0 12px; }
.opts { gap: 10px; }
.opts button { min-height: 54px; padding: 12px 14px; border-radius: 12px; background: var(--surface); align-items: center; line-height: 1.4;
  overflow-wrap: anywhere; transition: border-color .15s ease, transform .12s ease, background-color .15s ease; }
.opts button:not(:disabled):hover { border-color: var(--sea); background: var(--tint); }
.opts button:not(:disabled):active { transform: scale(.992); }
.opts kbd { display: inline-grid; place-items: center; min-width: 26px; height: 26px; padding: 0; border-radius: 7px; background: var(--bg); flex: none; }
.opts button.right { background: color-mix(in srgb, var(--ok) 13%, var(--surface)); }
.opts button.wrong { background: color-mix(in srgb, var(--bad) 11%, var(--surface)); }
.opts button.right kbd { background: var(--ok); color: #fff; border-color: var(--ok); }
.opts button.wrong kbd { background: var(--bad); color: #fff; border-color: var(--bad); }
.explain { font-size: 16px; line-height: 1.6; padding: 14px 16px; border-radius: 0 var(--r-sm) var(--r-sm) 0; background: var(--tint); }
.next { margin-top: 14px; }
.result { text-align: left; }
.result h2 { font-size: 22px; margin: 0 0 4px; }
.scorebig { display: flex; align-items: baseline; gap: 10px; margin: 2px 0 6px; }
.scorebig b { font: 800 clamp(44px, 12vw, 64px)/1 var(--font); letter-spacing: -.03em; color: var(--sea); font-variant-numeric: tabular-nums; }
.scorebig span { font-size: 16px; color: var(--muted); }
.review { padding-left: 20px; }
.review li { margin-bottom: 10px; }
.share .row a, .share .row button { min-height: 44px; border-radius: 999px; }
.more a.card { border-radius: 12px; min-height: 56px; transition: border-color .15s ease, transform .12s ease; }
.more a.card:hover { transform: translateY(-1px); }
footer { border-top: 1px solid var(--line); margin-top: 28px; padding-top: 18px; line-height: 1.5; }
section:not([hidden]) { animation: ui-in .28s ease-out both; }
@keyframes ui-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
@keyframes ui-pop { 0% { transform: scale(1); } 45% { transform: scale(1.018); } 100% { transform: scale(1); } }
@keyframes ui-shake { 0%, 100% { transform: translateX(0); } 20% { transform: translateX(-5px); } 50% { transform: translateX(5px); } 80% { transform: translateX(-3px); } }
.opts button.right { animation: ui-pop .32s ease-out; }
.opts button.wrong { animation: ui-shake .32s ease-out; }
@media (max-width: 460px) {
  body { font-size: 16.5px; }
  .wrap { padding: 0 12px; }
  .panel { padding: 14px; border-radius: 14px; }
  .modes { grid-template-columns: 1fr; gap: 8px; }
  .modes button { display: grid; grid-template-columns: 34px 1fr; column-gap: 12px; min-height: 64px; align-items: center; }
  .modes button .ic { grid-row: 1 / span 2; margin: 0; }
  .q { font-size: 17px; }
  .bar { flex-wrap: wrap; }
  .explain { font-size: 15.5px; padding: 12px 14px; }
}
@media (prefers-reduced-motion: reduce) {
  section:not([hidden]), .opts button.right, .opts button.wrong { animation: none; }
  .pbar i, .modes button, .opts button, .primary, .more a.card { transition: none; }
}
/* UI-END */
</style>
"""

JS = r"""<script id="ui-js">
/* UI-BEGIN */
(function () {
  var d = document, root = d.documentElement;
  var P = {
    natt: 'M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z',
    dag: 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4',
    blandet: 'M16 3h5v5M4 20 21 3M21 16v5h-5M15 15l6 6M4 4l5 5',
    compass: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM15.5 8.5l-2 5-5 2 2-5z',
    ship: 'M3 17l2 3h14l2-3zM6 17v-6h12v6M12 11V5M9 8h6',
    list: 'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01',
    cloud: 'M7 18a4 4 0 0 1-.5-7.97A6 6 0 0 1 18 9a4.5 4.5 0 0 1 0 9z',
    book: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5zM6.5 17H20v4H6.5A2.5 2.5 0 0 1 4 19.5',
    speaker: 'M3 9v6h4l5 4V5L7 9zM16 8a5 5 0 0 1 0 8',
    blocks: 'M3 3h8v8H3zM13 13h8v8h-8zM13 3h8v4h-8zM3 13h8v8H3z',
    info: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 16v-5M12 8h.01',
    flag: 'M5 21V4M5 4h12l-2 4 2 4H5',
    alert: 'M12 3 2 21h20zM12 10v5M12 18h.01',
    eye: 'M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12zM12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z',
    turn: 'M9 14 4 9l5-5M4 9h10a6 6 0 0 1 6 6v5',
    hold: 'M8 5v14M16 5v14',
    bell: 'M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0',
    lanes: 'M4 4v16M12 4v16M20 4v16M8 8l2 2M16 14l-2 2',
    strait: 'M4 4c3 5 3 11 0 16M20 4c-3 5-3 11 0 16M10 8l2-2 2 2M12 6v12'
  };
  var MAP = { natt: 'natt', dag: 'dag', blandet: 'blandet', situasjon: 'compass', 'fartøy': 'ship', rangering: 'list',
    sikt: 'cloud', regler: 'book', signal: 'speaker', 'tåke': 'cloud', bygg: 'blocks', fakta: 'info', norge: 'flag',
    nod: 'alert', se: 'eye', vik: 'turn', hold: 'hold', sig: 'bell', utk: 'eye', anv: 'flag', def: 'book', fare: 'alert', trang: 'strait', tss: 'lanes' };
  function icon(mode) {
    var path = P[MAP[mode] || 'compass'];
    return '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + path + '"/></svg>';
  }
  d.querySelectorAll('.modes button[data-mode]').forEach(function (b) {
    if (!b.querySelector('.ic')) b.insertAdjacentHTML('afterbegin', icon(b.dataset.mode));
  });

  /* kicker: regelområde over tittelen, følger språkvalget */
  var K = { nb: d.body.dataset.kickerNb, en: d.body.dataset.kickerEn };
  var h1 = d.querySelector('#start h1');
  if (h1 && K.nb && !d.querySelector('.kicker')) {
    var kk = d.createElement('p'); kk.className = 'kicker'; h1.parentNode.insertBefore(kk, h1);
  }
  function setKicker() { var kk = d.querySelector('.kicker'); if (kk) kk.textContent = root.lang === 'en' ? K.en : K.nb; }
  setKicker();
  new MutationObserver(setKicker).observe(root, { attributes: true, attributeFilter: ['lang'] });

  /* fremdriftslinje fra «Spørsmål i/n» */
  var bar = d.querySelector('#play .bar'), count = d.getElementById('count');
  if (bar && count && !d.querySelector('.pbar')) {
    var pb = d.createElement('div'); pb.className = 'pbar'; pb.setAttribute('aria-hidden', 'true'); pb.innerHTML = '<i></i>';
    bar.parentNode.insertBefore(pb, bar.nextSibling);
    var fill = pb.firstChild;
    var upd = function () {
      var m = (count.textContent || '').match(/(\d+)\D+(\d+)/);
      fill.style.width = m ? Math.max(0, Math.min(100, (parseInt(m[1], 10) - 1) / parseInt(m[2], 10) * 100)) + '%' : '0%';
    };
    new MutationObserver(upd).observe(count, { childList: true, characterData: true, subtree: true });
    upd();
  }

  /* resultat: stor poengverdi med telling, aria-live, fokus */
  var res = d.getElementById('result'), resText = d.getElementById('resText'), resTitle = d.getElementById('resTitle');
  if (res && resText && resTitle) {
    resTitle.setAttribute('role', 'status'); resTitle.setAttribute('aria-live', 'polite'); resTitle.tabIndex = -1;
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var big = null, anim = 0, shown = '';
    var build = function () {
      var m = (resText.textContent || '').match(/(?:Poeng|Points):\s*(\d+)/i);
      if (!m) return;
      var pts = parseInt(m[1], 10), label = root.lang === 'en' ? 'points' : 'poeng';
      if (!big) {
        big = d.createElement('div'); big.className = 'scorebig'; big.innerHTML = '<b></b><span></span>';
        resText.parentNode.insertBefore(big, resText);
      }
      big.lastChild.textContent = label;
      var num = big.firstChild, key = pts + '|' + res.hidden;
      if (key === shown) return; shown = key;
      cancelAnimationFrame(anim);
      if (reduce || !window.requestAnimationFrame) { num.textContent = pts; return; }
      var t0 = null, dur = 900;
      var step = function (t) {
        if (t0 === null) t0 = t;
        var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        num.textContent = Math.round(pts * e);
        if (p < 1) anim = requestAnimationFrame(step);
      };
      num.textContent = 0; anim = requestAnimationFrame(step);
    };
    new MutationObserver(build).observe(resText, { childList: true, characterData: true, subtree: true });
    new MutationObserver(function () {
      if (!res.hidden) { shown = ''; build(); try { resTitle.focus({ preventScroll: true }); } catch (e) {} } else { shown = ''; }
    }).observe(res, { attributes: true, attributeFilter: ['hidden'] });
    build();
  }
})();
/* UI-END */
</script>
"""

STYLE_BLOCK = re.compile(r'\n?<style id="ui-css">.*?</style>\n?', re.S)
SCRIPT_BLOCK = re.compile(r'<script id="ui-js">.*?</script>\n', re.S)

for slug, (knb, ken) in GAMES.items():
    p = os.path.join(ROOT, slug, 'index.html')
    s = open(p, encoding='utf-8').read()
    s = STYLE_BLOCK.sub('', s)
    s = SCRIPT_BLOCK.sub('', s)
    # CSS rett etter siste </style> i <head>
    head_end = s.index('</head>')
    last_style = s.rfind('</style>', 0, head_end)
    assert last_style != -1, slug
    cut = last_style + len('</style>')
    s = s[:cut] + '\n' + CSS + s[cut:]
    # data-game / kicker på <body>
    s = re.sub(r'<body[^>]*>', '<body data-game="%s" data-kicker-nb="%s" data-kicker-en="%s">' % (slug, knb, ken), s, count=1)
    # theme-color
    if 'name="theme-color"' not in s:
        s = s.replace('</head>', '<meta name="theme-color" content="#f6f3ec" media="(prefers-color-scheme: light)">\n'
                                 '<meta name="theme-color" content="#0a1822" media="(prefers-color-scheme: dark)">\n</head>', 1)
    # JS rett før </body>
    s = s.replace('</body>', JS + '</body>', 1)
    assert s.count('id="ui-css"') == 1 and s.count('id="ui-js"') == 1, slug
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', slug)
