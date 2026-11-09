#!/usr/bin/env python3
"""Lager 1200x630 delingsbilder (egne SVG-tegninger, ingen KI). Bruk: python3 tools/lag-kort.py"""
import subprocess, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'static', 'img')
W, H = 1200, 630
BG = '#0b2233'; SEA = '#123a55'; SEA2 = '#0e2d44'

def frame(title, sub, art, accent='#d6402f'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Arial, sans-serif">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071622"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#g)"/>
<rect x="0" y="0" width="12" height="{H}" fill="{accent}"/>
{art}
<g>
<text x="64" y="118" font-size="30" fill="#9fb6c6" letter-spacing="3">CAPTAIN PHD</text>
<text x="64" y="205" font-size="76" font-weight="bold" fill="#ffffff">{title}</text>
<text x="64" y="262" font-size="32" fill="#cfe0ea">{sub}</text>
</g>
<rect x="0" y="{H-78}" width="{W}" height="78" fill="#071622"/>
<text x="64" y="{H-30}" font-size="30" fill="#ffffff" font-weight="bold">captainphd.com</text>
<text x="{W-64}" y="{H-30}" font-size="22" fill="#9fb6c6" text-anchor="end">Gratis læringsspill · Free learning game · CC BY-SA · Marfag K52</text>
</svg>'''

def ship(x, y, s=1.0, col='#cfd8dc', flip=False):
    sx = -s if flip else s
    return f'<g transform="translate({x},{y}) scale({sx},{s})"><path d="M-110 0 L110 0 L84 34 L-96 34 Z" fill="{col}"/><rect x="-30" y="-34" width="62" height="34" fill="{col}"/><rect x="-14" y="-62" width="30" height="28" fill="{col}"/></g>'

def waves(y0=420):
    out = []
    for i, y in enumerate(range(y0, H-78, 28)):
        out.append(f'<rect x="0" y="{y}" width="{W}" height="14" fill="{SEA if i%2==0 else SEA2}" opacity="0.8"/>')
    return ''.join(out)

def light(x, y, col, r=11, glow=34):
    return f'<circle cx="{x}" cy="{y}" r="{glow}" fill="{col}" opacity="0.18"/><circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>'

cards = {}

# 1 Lanterner: skip om natten sett forfra med topplanterner og sidelanterner
art = waves(430) + f'''<g transform="translate(860,330)">
<path d="M-170 70 L170 70 L130 130 L-130 130 Z" fill="#1b2f3f"/><rect x="-90" y="10" width="180" height="60" fill="#1b2f3f"/><rect x="-40" y="-40" width="80" height="50" fill="#1b2f3f"/>
{light(0,-110,'#fff8e1',12)}{light(0,-60,'#fff8e1',12)}
{light(-110,40,'#e53935',11)}{light(110,40,'#43a047',11)}
<line x1="0" y1="-110" x2="0" y2="-40" stroke="#1b2f3f" stroke-width="6"/></g>'''
cards['lanterner'] = frame('Lanterner og', 'dagsignaler · Regel 20–31', art)

# 2 Hvem viker
art = waves(430) + ship(760, 330, 1.2) + ship(1010, 360, 1.0, '#9fb6c6', True) + '''
<path d="M600 300 C 700 250, 820 250, 900 300" stroke="#43a047" stroke-width="8" fill="none" stroke-dasharray="14 10"/>
<polygon points="905,300 880,284 884,312" fill="#43a047"/>
<text x="860" y="205" font-size="40" fill="#43a047" font-weight="bold">?</text>'''
cards['hvem-viker'] = frame('Hvem viker?', 'Who gives way? · Regel 11–19', art, '#43a047')

# 3 Lydsignaler: lydbølger / kort-lang
bars = ''
x = 600
pat = [('s',1),('s',1),('l',3),('s',1),('l',3),('l',3),('s',1)]
for p, n in pat:
    w = 30*n
    bars += f'<rect x="{x}" y="300" width="{w}" height="46" rx="23" fill="{"#ffc107" if p=="l" else "#fff8e1"}"/>'
    x += w + 18
arcs = ''.join(f'<path d="M 940 {170+i*0} m 0 0" />' for i in range(0))
art = waves(450) + bars + '''<g stroke="#9fb6c6" stroke-width="6" fill="none" stroke-linecap="round">
<path d="M880 200 q40 30 0 60"/><path d="M910 180 q64 50 0 100"/><path d="M940 160 q88 70 0 140"/></g>
<text x="600" y="410" font-size="26" fill="#9fb6c6">kort · kort · lang · kort · lang · lang · kort</text>'''
cards['lydsignaler'] = frame('Lydsignaler', 'Sound signals · Regel 32–37', art, '#ffc107')

# 4 Nødsignaler: rød rakett + SOS i morse
dots = ''
x = 650
for n in [1,1,1,3,3,3,1,1,1]:
    if n == 1:
        dots += f'<circle cx="{x+14}" cy="330" r="14" fill="#fff"/>'; x += 56
    else:
        dots += f'<rect x="{x}" y="316" width="64" height="28" rx="14" fill="#fff"/>'; x += 90
art = waves(460) + f'''<g transform="translate(980,170)">{light(0,0,'#ff5252',20,80)}
<g stroke="#ff8a80" stroke-width="5" stroke-linecap="round"><line x1="0" y1="-60" x2="0" y2="-95"/><line x1="0" y1="60" x2="0" y2="95"/><line x1="-60" y1="0" x2="-95" y2="0"/><line x1="60" y1="0" x2="95" y2="0"/><line x1="42" y1="42" x2="66" y2="66"/><line x1="-42" y1="-42" x2="-66" y2="-66"/><line x1="42" y1="-42" x2="66" y2="-66"/><line x1="-42" y1="42" x2="-66" y2="66"/></g></g>{dots}'''
cards['nodsignaler'] = frame('Nødsignaler', 'Distress signals · Regel 37 · Vedlegg IV', art, '#ff5252')

# 5 Manøver: kurs og unnamanøver
art = waves(430) + ship(720, 400, 1.0) + ship(1000, 330, 1.0, '#9fb6c6', True) + '''
<path d="M560 395 L700 395 C 760 395, 790 480, 860 480 L1020 480" stroke="#43a047" stroke-width="7" fill="none"/>
<polygon points="1030,480 1005,466 1005,494" fill="#43a047"/>
<path d="M1150 330 L900 330" stroke="#cfd8dc" stroke-width="5" stroke-dasharray="10 10"/>'''
cards['manovrer'] = frame('Manøver', 'Avoiding collision · Regel 8, 15–17, 34', art, '#1d9bf0')

# 6 Utkikk, fart og farvann: TSS
art = waves(430) + '''<g transform="translate(0,60)"><g stroke="#cfd8dc" stroke-width="6">
<line x1="560" y1="300" x2="1140" y2="300" stroke-dasharray="26 16"/>
<line x1="560" y1="420" x2="1140" y2="420" stroke-dasharray="26 16"/></g>
<rect x="560" y="330" width="580" height="60" fill="#8e2d86" opacity="0.55"/>
<g fill="#fff"><polygon points="1100,270 1130,285 1100,300" transform="translate(0,-20)"/>
<polygon points="620,440 590,455 620,470" transform="translate(0,0)"/></g>
<path d="M600 262 L1090 262" stroke="#fff" stroke-width="5"/>
<path d="M1100 450 L620 450" stroke="#fff" stroke-width="5"/></g>'''
cards['utkikk-fart'] = frame('Utkikk, fart', 'og farvann · Regel 5–10', art, '#8e2d86')

for k, svg in cards.items():
    p = os.path.join(OUT, f'kart-{k}')
    open(p + '.svg', 'w').write(svg)
    subprocess.run(['rsvg-convert', '-w', str(W), '-h', str(H), p + '.svg', '-o', p + '.png'], check=True)
    os.remove(p + '.svg')
    print('ok', k, os.path.getsize(p + '.png'))
