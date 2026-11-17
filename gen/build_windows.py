#!/usr/bin/env python3
"""Build AmigaGloss as Windows .ico files.

usage: build_windows.py [OUTDIR]     (default: ../windows/ico)

Writes OUTDIR/<context>/<name>.ico for every drawn icon (aliases are skipped).
Each .ico holds a separate render at every size Windows uses, so small sizes
stay crisp instead of being shrunk from the 256 px version.

Needs: pip install resvg-py pillow
"""
import io
import os
import shutil
import sys

import resvg_py
from PIL import Image

from build import REG
from lib import Icon

SIZES = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]


def render(svg, px):
    png = resvg_py.svg_to_bytes(svg_string=svg, width=px, height=px)
    return Image.open(io.BytesIO(bytes(png))).convert('RGBA')


def main(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    n = 0
    for (ctx, name), fn in sorted(REG.items()):
        ic = Icon()
        svg = ic.render(fn(ic))
        imgs = [render(svg, s) for s in SIZES]
        d = os.path.join(out, ctx)
        os.makedirs(d, exist_ok=True)
        big = imgs[-1]
        big.save(os.path.join(d, name + '.ico'), format='ICO',
                 sizes=[(s, s) for s in SIZES], append_images=imgs[:-1])
        n += 1
    print('%d icons -> %s' % (n, out))


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', 'windows', 'ico'))
