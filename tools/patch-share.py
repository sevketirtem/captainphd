#!/usr/bin/env python3
"""Legger til OG/Twitter-meta og delingsknapper i spillsidene (idempotent)."""
import re, os, html
ROOT = os.path.join(os.path.dirname(__file__), '..', 'static')
GAMES = {
 'lanterner':   ('Lanterner og dagsignaler', 'Lights and shapes'),
 'hvem-viker':  ('Hvem viker?', 'Who gives way?'),
 'lydsignaler': ('Lydsignaler', 'Sound signals'),
 'nodsignaler': ('Nødsignaler', 'Distress signals'),
 'manovrer':    ('Manøver', 'Manoeuvres'),
 'utkikk-fart': ('Utkikk, fart og farvann', 'Lookout, speed and channels'),
}
CSS = """.share { margin: 16px 0 4px; }
.share h3 { font-size: 15px; margin: 0 0 8px; }
.share .row { display: flex; flex-wrap: wrap; gap: 8px; }
.share a, .share button { font: inherit; font-size: 14px; padding: 8px 14px; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); color: var(--fg); text-decoration: none; cursor: pointer; }
.share .main { background: var(--sea); border-color: var(--sea); color: #fff; }
.share a:hover, .share button:hover { border-color: var(--sea); }
</style>"""
JS = r"""
  const SHARE_URL = 'https://captainphd.com/__G__/';
  function renderShare() {
    const box = $('share'); if (!box) return;
    const nb = lang !== 'en';
    const title = t('title');
    const url = SHARE_URL + (nb ? '' : '?lang=en');
    const text = nb ? `Jeg fikk ${round.pts} poeng i «${title}» på captainphd.com` : `I scored ${round.pts} points in “${title}” on captainphd.com`;
    const L = nb ? { h: 'Del resultatet', share: 'Del …', copy: 'Kopier lenke', copied: 'Kopiert!' } : { h: 'Share result', share: 'Share …', copy: 'Copy link', copied: 'Copied!' };
    const enc = encodeURIComponent;
    box.innerHTML = ''; box.className = 'share';
    const h = document.createElement('h3'); h.textContent = L.h; box.appendChild(h);
    const row = document.createElement('div'); row.className = 'row'; box.appendChild(row);
    if (typeof navigator !== 'undefined' && navigator.share) {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'main'; b.textContent = L.share;
      b.addEventListener('click', () => { navigator.share({ title, text, url }).catch(() => {}); });
      row.appendChild(b);
    } else {
      [['WhatsApp', 'https://wa.me/?text=' + enc(text + ' ' + url)],
       ['X', 'https://x.com/intent/post?text=' + enc(text) + '&url=' + enc(url)],
       ['Facebook', 'https://www.facebook.com/sharer/sharer.php?u=' + enc(url)]].forEach(([n, href]) => {
        const a = document.createElement('a'); a.href = href; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = n; row.appendChild(a);
      });
    }
    const c = document.createElement('button'); c.type = 'button'; c.textContent = L.copy;
    c.addEventListener('click', () => {
      const done = () => { c.textContent = L.copied; setTimeout(() => { c.textContent = L.copy; }, 2000); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, done);
      else { const ta = document.createElement('textarea'); ta.value = url; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) { /* ingen */ } document.body.removeChild(ta); done(); }
    });
    row.appendChild(c);
  }
"""
for g, (tnb, ten) in GAMES.items():
    p = os.path.join(ROOT, g, 'index.html')
    s = open(p, encoding='utf-8').read()
    if 'renderShare' in s:
        print('skip', g); continue
    m = re.search(r'<meta name="description" content="([^"]*)">', s)
    desc = m.group(1)
    url = f'https://captainphd.com/{g}/'
    img = f'https://captainphd.com/img/kart-{g}.png'
    metas = f'''
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="nb" href="{url}">
<link rel="alternate" hreflang="en" href="{url}?lang=en">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Captain PhD">
<meta property="og:title" content="{html.escape(tnb)} · Captain PhD">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(tnb)} – Captain PhD">
<meta property="og:locale" content="nb_NO">
<meta property="og:locale:alternate" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(tnb)} · Captain PhD">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">'''
    s = s.replace(m.group(0), m.group(0) + metas, 1)
    s = s.replace('</style>', CSS, 1)
    s = s.replace('<div id="resReview"></div>', '<div id="resReview"></div>\n        <div id="share"></div>', 1)
    s = s.replace('  function showResult() {', JS.replace('__G__', g) + '\n  function showResult() {', 1)
    s = s.replace("    showBest();\n    $('again').focus", "    showBest();\n    renderShare();\n    $('again').focus", 1)
    assert s.count('    renderShare();') == 1 and 'id="share"' in s, g
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', g)
