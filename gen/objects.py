"""Composite bases: drawers (folders), documents, tiles."""
from lib import *


def folder(ic, c=DRAWER, emblem=None, opened=False):
    back = path('M7,13 Q7,10 10,10 H23 Q25,10 26.5,12 L28.5,15 H54 Q57,15 57,18 V52 H7 Z', ic.v(dk(c, .12), .25, .35))
    paper = (rect(11, 18, 42, 26, 1, ic.v(WHITE, .2, .12), OL, 1.1) +
             ''.join(rect(15, y, 30, 1.6, .5, '#b8c0d0', None) for y in (22, 26)))
    if opened:
        front = path('M2,30 Q1.5,28 4,28 H56 Q58.5,28 58,30 L55.5,54 Q55.2,56 53,56 H10 Q7.8,56 7.5,54 Z', ic.v(c, .45, .3))
        gl = gloss(ic, 'M5,30 H55 L54.3,38 Q31,41 7,38 Z', .55)
        ex, ey, es = 21.5, 31, .33
    else:
        front = path('M4.5,24 Q4,22 6.5,22 H57.5 Q60,22 59.5,24 L56.5,53.5 Q56.2,56 53.5,56 H10.5 Q7.8,56 7.5,53.5 Z',
                     ic.v(c, .45, .3))
        gl = gloss(ic, 'M7,24.5 H57 L56,35 Q32,39 8,35 Z', .55)
        ex, ey, es = 21, 28.5, .34
    lip = path('M7,24.2 H57' if not opened else 'M4.5,30.2 H55.5', 'none', lt(c, .6), 1, ' opacity=".8"')
    body = shadow(ic, 32, 58.5, 27, 3.6) + back + paper + front + gl + lip
    if emblem:
        body += place(emblem, ex, ey, es)
    return body


def document(ic, accent=BLUE, emblem=None, label=None, fold=True):
    page = path('M13,4 H40 L52,16 V58 Q52,60 50,60 H15 Q13,60 13,58 V6 Q13,4 15,4 Z',
                ic.lg([(0, WHITE), (1, '#dfe3ea')]))
    corner = path('M40,4 V14 Q40,16 42,16 H52 Z', ic.lg([(0, lt(accent, .55)), (1, accent)], 0, 0, 1, 1)) if fold else ''
    body = shadow(ic, 32.5, 60, 21, 2.8, .35) + page + corner
    body += path('M15,6 H39 V12 Q27,16 15,12 Z', ic.glossfill(.6), None)
    if label:
        body += (path('M13,45 H52 V58 Q52,60 50,60 H15 Q13,60 13,58 Z', ic.v(accent, .35, .3)) +
                 text(32.5, 56, label, 9.5 if len(label) <= 4 else 7.5, WHITE, stroke=dk(accent, .5), sw=1.4))
        if emblem:
            body += place(emblem, 19.5, 16, .41)
        else:
            body += ''.join(rect(19, y, 27 if i != 3 else 17, 2.6, 1, '#9aa6c0', None) for i, y in enumerate(range(20, 42, 6)))
    elif emblem:
        body += place(emblem, 17.5, 20, .46)
    return body


def tile(ic, c, inner):
    return (shadow(ic, 32, 59, 24, 3.5) + rect(5, 4, 54, 54, 12, ic.v(c, .4, .35)) + place(inner, 13, 12, .6) +
            path('M7,15 Q7,6 16,6 H48 Q57,6 57,15 V24 Q32,32 7,24 Z', ic.glossfill(.5), None))


def obj(ic, inner, sh=True, s=1.0):
    """A standalone object with a floor shadow."""
    out = shadow(ic) if sh else ''
    if s != 1.0:
        off = 32 * (1 - s)
        return out + place(inner, off, off - 1, s)
    return out + inner


def with_badge(ic, base, badge, pos='br', s=.45):
    x, y = {'br': (35, 33), 'tr': (35, 1), 'bl': (1, 33), 'tl': (1, 1)}[pos]
    return base + place(badge, x, y, s)
