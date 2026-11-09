#!/usr/bin/env python3
"""Kort-/bakgrunnsbilder (kort-*.png, bg-*.png fra KI) -> webp. Bruk: prep-kort.py <kilde-mappe>
kort-*: 1200x630 (<90 KB). bg-*: 1920x1080 (<250 KB). Skriver til static/img/<navn>.webp."""
import sys, os, glob
from PIL import Image
src = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "img")
YOFF = {"kort-lanterner": 0.5, "kort-hvem-viker": 0.45, "kort-lydsignaler": 0.5}
def crop(im, ratio, y_off):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio); x = (w - nw) // 2; return im.crop((x, 0, x + nw, h))
    nh = int(w / ratio); y = int((h - nh) * y_off); return im.crop((0, y, w, y + nh))
for f in sorted(glob.glob(os.path.join(src, "*.png"))):
    n = os.path.splitext(os.path.basename(f))[0]
    if n.startswith("kort-") and not n.endswith("-v2"): size, maxkb = (1200, 630), 90
    elif n.startswith("bg-"): size, maxkb = (1920, 1080), 250
    else: continue
    im = crop(Image.open(f).convert("RGB"), size[0] / size[1], YOFF.get(n, 0.5)).resize(size, Image.LANCZOS)
    p = os.path.join(OUT, n + ".webp"); q = 82
    while True:
        im.save(p, "WEBP", quality=q, method=6)
        if os.path.getsize(p) <= maxkb * 1024 or q <= 40: break
        q -= 4
    print(n, size, os.path.getsize(p) // 1024, "KB q", q)
