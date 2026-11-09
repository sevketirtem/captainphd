#!/usr/bin/env python3
"""Legger til «Spill flere / Play more» på resultatskjermen i spillsidene.

Idempotent og oppdaterbar: blokken mellom markørene MORE-BEGIN/MORE-END (CSS og JS)
byttes ut på nytt hver gang, så nye spill legges bare til i GAMES under.
Må kjøres etter tools/patch-share.py (bruker #share og renderShare)."""
import re, os
ROOT = os.path.join(os.path.dirname(__file__), '..', 'static')
# slug: (tittel nb, tittel en, regelområde nb, regelområde en) i rekkefølge for «neste spill»
GAMES = [
 ('lanterner',   'Lanterner og dagsignaler', 'Lights and shapes',            'Regel 20–31', 'Rules 20–31'),
 ('hvem-viker',  'Hvem viker?',              'Who gives way?',               'Regel 11–19', 'Rules 11–19'),
 ('manovrer',    'Manøver',                  'Manoeuvres',                   'Regel 8, 15–17, 34', 'Rules 8, 15–17, 34'),
 ('lydsignaler', 'Lydsignaler',              'Sound signals',                'Regel 32–37', 'Rules 32–37'),
 ('nodsignaler', 'Nødsignaler',              'Distress signals',             'Regel 37, vedlegg IV', 'Rule 37, Annex IV'),
 ('utkikk-fart', 'Utkikk, fart og farvann',  'Lookout, speed and channels',  'Regel 5–7, 9–10', 'Rules 5–7, 9–10'),
]
CSS = """/* MORE-BEGIN */
.more { margin: 18px 0 4px; }
.more h3 { font-size: 15px; margin: 0 0 8px; }
.more .cards { display: grid; gap: 8px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
.more a.card { display: block; padding: 10px 12px; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); color: var(--fg); text-decoration: none; }
.more a.card:hover { border-color: var(--sea); }
.more a.card.next { border-color: var(--sea); }
.more .card b { display: block; font-size: 14px; }
.more .card span { font-size: 12px; color: var(--muted); }
.more .home { display: inline-block; margin-top: 10px; font-size: 14px; color: var(--sea); }
/* MORE-END */
"""
def js(slug):
    games = ',\n    '.join(
        "{ s: %r, nb: %r, en: %r, rnb: %r, ren: %r }" % g for g in GAMES)
    return f"""
  /* MORE-BEGIN */
  const MORE_SELF = {slug!r};
  const MORE_GAMES = [
    {games}
  ];
  function renderMore() {{
    const box = $('more'); if (!box) return;
    const nb = lang !== 'en';
    const i = MORE_GAMES.findIndex(g => g.s === MORE_SELF);
    const order = [];
    for (let k = 1; k < MORE_GAMES.length; k++) order.push(MORE_GAMES[(i + k) % MORE_GAMES.length]);
    box.innerHTML = ''; box.className = 'more';
    const h = document.createElement('h3'); h.textContent = nb ? 'Spill flere' : 'Play more'; box.appendChild(h);
    const cards = document.createElement('div'); cards.className = 'cards'; box.appendChild(cards);
    order.slice(0, 3).forEach((g, k) => {{
      const a = document.createElement('a'); a.className = 'card' + (k === 0 ? ' next' : '');
      a.href = '/' + g.s + '/' + (nb ? '' : '?lang=en');
      const b = document.createElement('b'); b.textContent = nb ? g.nb : g.en; a.appendChild(b);
      const sp = document.createElement('span'); sp.textContent = nb ? g.rnb : g.ren; a.appendChild(sp);
      cards.appendChild(a);
    }});
    const home = document.createElement('a'); home.className = 'home';
    home.href = nb ? '/' : '/en/'; home.textContent = nb ? 'Til forsiden' : 'Home';
    box.appendChild(home);
  }}
  /* MORE-END */
"""
BLOCK = re.compile(r'\n?[ ]*/\* MORE-BEGIN \*/.*?/\* MORE-END \*/\n?', re.S)
for g in GAMES:
    slug = g[0]
    p = os.path.join(ROOT, slug, 'index.html')
    s = open(p, encoding='utf-8').read()
    assert 'renderShare' in s, f'{slug}: kjør patch-share.py først'
    s = BLOCK.sub('\n', s)  # fjern gammel blokk (CSS og JS)
    s = s.replace('</style>', CSS + '</style>', 1)
    s = s.replace('  function renderShare() {', js(slug).lstrip('\n') + '\n  function renderShare() {', 1)
    if 'id="more"' not in s:
        s = s.replace('<div id="share"></div>', '<div id="share"></div>\n        <div id="more"></div>', 1)
    if 'renderMore();' not in s:
        s = s.replace('    renderShare();\n', '    renderShare();\n    renderMore();\n', 1)
    assert s.count('renderMore();') == 1 and s.count('MORE-BEGIN') == 2 and 'id="more"' in s, slug
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', slug)
