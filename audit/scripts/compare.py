"""Pixel comparison of two screenshot directories.

Usage: python -I compare.py <before_dir> <after_dir> <diff_dir> [threshold]

For every PNG present in both directories, prints the image size, the percentage of
pixels whose max channel delta exceeds `threshold` (default 16/255), and writes a
diff image (changed pixels in red over a faded copy of the "after" capture).
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops

before, after, diffs = (Path(p) for p in sys.argv[1:4])
threshold = int(sys.argv[4]) if len(sys.argv) > 4 else 16
diffs.mkdir(parents=True, exist_ok=True)

rows = []
for a in sorted(after.glob("*.png")):
    b = before / a.name
    if not b.exists():
        rows.append((a.name, "missing in before", "", ""))
        continue
    ib, ia = Image.open(b).convert("RGB"), Image.open(a).convert("RGB")
    if ib.size != ia.size:
        rows.append((a.name, f"SIZE {ib.size} -> {ia.size}", "", ""))
        # Compare the common area anyway so the row stays informative.
        w, h = min(ib.width, ia.width), min(ib.height, ia.height)
        ib, ia = ib.crop((0, 0, w, h)), ia.crop((0, 0, w, h))
    delta = ImageChops.difference(ib, ia).convert("L")
    mask = delta.point(lambda v: 255 if v > threshold else 0)
    changed = sum(mask.histogram()[255:]) if False else mask.histogram()[255]
    total = mask.width * mask.height
    pct = 100 * changed / total
    bbox = mask.getbbox()
    if changed:
        faded = Image.blend(ia, Image.new("RGB", ia.size, (255, 255, 255)), 0.6)
        red = Image.new("RGB", ia.size, (255, 0, 0))
        faded.paste(red, mask=mask)
        faded.save(diffs / a.name)
    rows.append((a.name, f"{ia.size[0]}x{ia.size[1]}", f"{pct:.3f}%", str(bbox) if bbox else "-"))

for name, size, pct, bbox in rows:
    print(f"{name:45s} {size:22s} {pct:>9s} {bbox}")
