#!/usr/bin/env python3
"""KI-kildebilder (1376x768 PNG) -> nettklare webp. Bruk: prep-gorsel.py <kilde-mappe>
Kort: 1200x630 (kort-<navn>.webp). Bakgrunn: 1920x1080 (bg-<navn>.webp, <250 KB). Bånd: 1600x500 (bandet-<navn>.webp)."""
import sys, os
from PIL import Image
src = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), "..", "static", "img")
def crop(im, ratio, y_off=0.5):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio); x = (w - nw) // 2; return im.crop((x, 0, x + nw, h))
    nh = int(w / ratio); y = int((h - nh) * y_off); return im.crop((0, y, w, y + nh))
def save(im, name, size, ratio, q, y_off=0.5, maxkb=None):
    im = crop(im.convert("RGB"), ratio, y_off).resize(size, Image.LANCZOS)
    p = os.path.join(OUT, name)
    while True:
        im.save(p, "WEBP", quality=q, method=6)
        if not maxkb or os.path.getsize(p) <= maxkb * 1024 or q <= 40: break
        q -= 5
    print(name, size, os.path.getsize(p) // 1024, "KB q", q)
JOBS = {  # kildefil: [(utfil, størrelse, forhold, kvalitet, y_off, maxkb)]
 "natt":  [("bg-natt.webp",(1920,1080),16/9,80,0.5,240),("kort-lanterner.webp",(1200,630),1200/630,80,0.35,90)],
 "dag":   [("bg-dag.webp",(1920,1080),16/9,78,0.5,240)],
 "hvem":  [("kort-hvem-viker.webp",(1200,630),1200/630,80,0.55,90)],
 "tåke":  [("kort-lydsignaler.webp",(1200,630),1200/630,80,0.5,90)],
 "storm": [("kort-nodsignaler.webp",(1200,630),1200/630,80,0.5,90)],
 "luft":  [("kort-manovrer.webp",(1200,630),1200/630,80,0.5,90)],
 "bro":   [("kort-utkikk-fart.webp",(1200,630),1200/630,80,0.5,90)],
 "band1": [("bandet-skole.webp",(1600,500),1600/500,78,0.5,140)],
 "band2": [("bandet-forside.webp",(1600,500),1600/500,78,0.5,140)],
}
for k, outs in JOBS.items():
    f = os.path.join(src, k + ".png")
    if not os.path.exists(f): print("mangler", k); continue
    im = Image.open(f)
    for o in outs: save(im, *o[:5], maxkb=o[5])
