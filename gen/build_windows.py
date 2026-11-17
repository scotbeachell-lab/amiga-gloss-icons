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
import struct
import sys

import resvg_py
from PIL import Image

from build import REG
from lib import Icon

SIZES = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]


def render(svg, px):
    png = resvg_py.svg_to_bytes(svg_string=svg, width=px, height=px)
    return Image.open(io.BytesIO(bytes(png))).convert('RGBA')


def dib(img):
    """One .ico frame as a classic 32-bit bitmap (BGRA rows bottom-up + 1-bit AND mask)."""
    w, h = img.size
    px = img.tobytes('raw', 'BGRA')
    row = w * 4
    xor = b''.join(px[y * row:(y + 1) * row] for y in range(h - 1, -1, -1))
    alpha = img.getchannel('A').tobytes()
    mrow = ((w + 31) // 32) * 4
    mask = bytearray()
    for y in range(h - 1, -1, -1):
        bits = bytearray(mrow)
        for x in range(w):
            if alpha[y * w + x] == 0:
                bits[x // 8] |= 0x80 >> (x % 8)
        mask += bits
    header = struct.pack('<IiiHHIIiiII', 40, w, h * 2, 1, 32, 0, len(xor) + len(mask), 0, 0, 0, 0)
    return header + xor + bytes(mask)


def write_ico(path, imgs):
    """Write an .ico the way Windows' own icons are laid out: bitmaps for the
    small sizes and PNG only at 256 px, which every Windows version and
    icon tool reads."""
    blobs = []
    for im in imgs:
        if im.width >= 256:
            b = io.BytesIO()
            im.save(b, format='PNG')
            blobs.append(b.getvalue())
        else:
            blobs.append(dib(im))
    out = struct.pack('<HHH', 0, 1, len(imgs))
    offset = 6 + 16 * len(imgs)
    for im, data in zip(imgs, blobs):
        d = 0 if im.width >= 256 else im.width
        out += struct.pack('<BBBBHHII', d, d, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
    with open(path, 'wb') as f:
        f.write(out + b''.join(blobs))


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
        write_ico(os.path.join(d, name + '.ico'), imgs)
        n += 1
    print('%d icons -> %s' % (n, out))


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', 'windows', 'ico'))
