"""Glossy 'Workbench 4' style SVG primitives.

Everything is drawn on a 64x64 canvas. Kept to SVG features QtSvg renders
(no filters, masks or clip paths) so KDE shows them exactly as previewed.
"""
import colorsys
import math

OL = "#1c1a24"          # outline colour
SW = 1.6                # base outline width


# ---------------------------------------------------------------- colours
def _rgb(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(rgb):
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(v * 255))) for v in rgb)


def shade(c, l=0.0, s=0.0):
    h, L, S = colorsys.rgb_to_hls(*_rgb(c))
    L = L + (1 - L) * l if l > 0 else L * (1 + l)
    return _hex(colorsys.hls_to_rgb(h, L, max(0, min(1, S + s))))


def lt(c, a=0.35):
    return shade(c, a)


def dk(c, a=0.3):
    return shade(c, -a)


# palette
RED, ORANGE, AMBER, YELLOW = "#e2352f", "#f07a1a", "#f2a516", "#f7d32a"
GREEN, TEAL, CYAN, BLUE = "#3fae3a", "#1fa59a", "#22b4e6", "#2f6fdc"
NAVY, PURPLE, MAGENTA, PINK = "#22408f", "#7a45c8", "#c83aa8", "#ee5a8c"
BROWN, GREY, SILVER, BEIGE = "#9a6232", "#7c8290", "#c4cad4", "#e6dcc0"
WHITE, BLACK, DARK = "#ffffff", "#000000", "#2c2e3a"
DRAWER = "#f2a516"


# ---------------------------------------------------------------- icon
class Icon:
    def __init__(self):
        self.defs = []
        self.n = 0

    def _id(self):
        self.n += 1
        return 'g%d' % self.n

    @staticmethod
    def _stops(stops):
        out = []
        for s in stops:
            o, c = s[0], s[1]
            a = s[2] if len(s) > 2 else 1
            out.append('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>' % (o, c, a))
        return ''.join(out)

    def lg(self, stops, x1=0, y1=0, x2=0, y2=1, user=False):
        i = self._id()
        u = ' gradientUnits="userSpaceOnUse"' if user else ''
        self.defs.append('<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s"%s>%s</linearGradient>'
                         % (i, x1, y1, x2, y2, u, self._stops(stops)))
        return 'url(#%s)' % i

    def rg(self, stops, cx=.5, cy=.5, r=.5, fx=None, fy=None, user=False):
        i = self._id()
        u = ' gradientUnits="userSpaceOnUse"' if user else ''
        fx = cx if fx is None else fx
        fy = cy if fy is None else fy
        self.defs.append('<radialGradient id="%s" cx="%s" cy="%s" r="%s" fx="%s" fy="%s"%s>%s</radialGradient>'
                         % (i, cx, cy, r, fx, fy, u, self._stops(stops)))
        return 'url(#%s)' % i

    # standard glossy vertical fill
    def v(self, c, top=0.45, bot=0.3):
        return self.lg([(0, lt(c, top)), (0.5, c), (1, dk(c, bot))])

    # horizontal metal fill
    def metal(self, c=SILVER):
        return self.lg([(0, dk(c, .25)), (.2, lt(c, .5)), (.5, c), (.8, lt(c, .3)), (1, dk(c, .35))], 0, 0, 1, 0)

    def ball(self, c):
        return self.rg([(0, lt(c, .75)), (.35, lt(c, .2)), (.8, c), (1, dk(c, .35))], .38, .32, .7, .32, .25)

    def glossfill(self, a=0.75):
        return self.lg([(0, WHITE, a), (1, WHITE, 0.04)])

    def render(self, body, size=64):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 64 64">'
                '<defs>%s</defs>%s</svg>\n' % (size, size, ''.join(self.defs), body))


# ---------------------------------------------------------------- shapes
def path(d, fill='none', stroke=OL, sw=SW, extra=''):
    s = '' if stroke is None else ' stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"' % (stroke, sw)
    return '<path d="%s" fill="%s"%s%s/>' % (d, fill, s, extra)


def rect(x, y, w, h, r=0, fill='none', stroke=OL, sw=SW, extra=''):
    s = '' if stroke is None else ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (stroke, sw)
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s%s/>' % (x, y, w, h, r, fill, s, extra)


def circle(cx, cy, r, fill='none', stroke=OL, sw=SW, extra=''):
    s = '' if stroke is None else ' stroke="%s" stroke-width="%s"' % (stroke, sw)
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"%s%s/>' % (cx, cy, r, fill, s, extra)


def ellipse(cx, cy, rx, ry, fill='none', stroke=OL, sw=SW, extra=''):
    s = '' if stroke is None else ' stroke="%s" stroke-width="%s"' % (stroke, sw)
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"%s%s/>' % (cx, cy, rx, ry, fill, s, extra)


def text(x, y, s, size=10, fill=WHITE, weight='bold', anchor='middle', stroke=None, sw=1.2, family='DejaVu Sans,Sans'):
    st = '' if stroke is None else ' stroke="%s" stroke-width="%s" paint-order="stroke"' % (stroke, sw)
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s" font-weight="%s" text-anchor="%s" fill="%s"%s>%s</text>'
            % (x, y, family, size, weight, anchor, fill, st, s))


def g(body, tf=None, op=None):
    a = ''
    if tf:
        a += ' transform="%s"' % tf
    if op is not None:
        a += ' opacity="%s"' % op
    return '<g%s>%s</g>' % (a, body)


def place(body, x, y, s):
    """Place a 64-space drawing scaled by s with top-left at x,y."""
    return g(body, 'translate(%s %s) scale(%s)' % (x, y, s))


def ostroke(d, color, w=6, ow=None, cap='round'):
    """Outlined stroke: dark wide stroke under a coloured one."""
    ow = w + 2 * SW + .4 if ow is None else ow
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"/>'
            % (d, OL, ow, cap, d, color, w, cap))


def shadow(ic, cx=32, cy=58.5, rx=25, ry=4.2, a=0.42):
    f = ic.rg([(0, BLACK, a), (0.6, BLACK, a * .45), (1, BLACK, 0)])
    return ellipse(cx, cy, rx, ry, f, None)


def gloss(ic, d, a=0.7):
    return path(d, ic.glossfill(a), None)


def gloss_rect(ic, x, y, w, h, r=3, a=0.7):
    return rect(x, y, w, h, r, ic.glossfill(a), None)


def star_pts(cx, cy, ro, ri, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = math.radians(rot + i * 180 / n)
        pts.append('%.2f,%.2f' % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return 'M' + ' L'.join(pts) + ' Z'


def gear_path(cx, cy, ro, ri, n=8, hole=None):
    pts = []
    step = 2 * math.pi / n
    for i in range(n):
        a = i * step
        for da, r in ((-0.30, ri), (-0.18, ro), (0.18, ro), (0.30, ri)):
            pts.append('%.2f,%.2f' % (cx + r * math.cos(a + da * step * 1.6), cy + r * math.sin(a + da * step * 1.6)))
    d = 'M' + ' L'.join(pts) + ' Z'
    if hole:
        d += ' M%s,%s a%s,%s 0 1,0 %s,0 a%s,%s 0 1,0 %s,0 Z' % (cx - hole, cy, hole, hole, 2 * hole, hole, hole, -2 * hole)
    return d


def arc_pts(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return 'M%.2f,%.2f A%s,%s 0 %d,1 %.2f,%.2f' % (x0, y0, r, r, large, x1, y1)
