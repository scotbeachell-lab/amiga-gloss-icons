"""Pictograms and objects, each drawn in 64x64 space: f(ic, ...) -> svg body."""
from lib import *


# ================================================================ pictograms
def e_note(ic, c=MAGENTA):
    f = ic.v(c)
    return (path('M22,16 L54,8 V44 H49 V18 L27,24 V50 H22 Z', f) +
            ellipse(17, 50, 8.5, 6.5, f, extra=' transform="rotate(-22 17 50)"') +
            ellipse(44, 44, 8.5, 6.5, f, extra=' transform="rotate(-22 44 44)"') +
            gloss(ic, 'M24,17 L52,10 V14 L24,21 Z', .8))


def e_picture(ic):
    sky = ic.lg([(0, '#5fb6ff'), (1, '#d6f0ff')])
    return (rect(5, 9, 54, 46, 3, ic.v('#f4f4f4', .5, .15)) +
            rect(10, 14, 44, 32, 1, sky, OL, 1.2) +
            circle(43, 23, 5, ic.ball(YELLOW), None) +
            path('M10,46 L24,27 L33,38 L39,31 L54,46 Z', ic.v(GREEN), OL, 1.2) +
            gloss(ic, 'M7,11 H57 V22 Q32,27 7,22 Z', .45))


def e_film(ic):
    body = rect(12, 4, 40, 56, 3, ic.v('#3a3a48', .3, .3))
    holes = ''.join(rect(x, y, 4, 4, 1, '#f0f0f0', None) for x in (14.5, 45.5) for y in range(8, 58, 8))
    frames = (rect(21, 9, 22, 20, 1.5, ic.lg([(0, '#7cc8ff'), (1, '#2f6fdc')]), OL, 1) +
              rect(21, 35, 22, 20, 1.5, ic.lg([(0, '#ffcf6a'), (1, '#e2352f')]), OL, 1))
    return body + holes + frames + gloss_rect(ic, 13, 5, 38, 14, 3, .3)


def e_download(ic, c=GREEN):
    return (ostroke('M8,44 V54 H56 V44', SILVER, 6) +
            path('M24,6 H40 V26 H51 L32,46 L13,26 H24 Z', ic.v(c)) +
            gloss(ic, 'M26,8 H38 V24 H26 Z', .55))


def e_upload(ic, c=BLUE):
    return (ostroke('M8,44 V54 H56 V44', SILVER, 6) +
            path('M24,46 H40 V26 H51 L32,6 L13,26 H24 Z', ic.v(c)) +
            gloss(ic, 'M32,9 L47,25 H17 Z', .55))


def e_lines(ic):
    return (rect(10, 6, 44, 52, 3, ic.v('#ffffff', .5, .12)) +
            ''.join(rect(16, y, 32 if i % 3 != 2 else 20, 4, 2, '#5b6d8f', None) for i, y in enumerate(range(14, 52, 8))))


def e_monitor(ic, screen=None):
    screen = screen or ic.lg([(0, '#6fc2ff'), (1, '#2445a8')])
    return (path('M26,50 H38 L41,58 H23 Z', ic.v(SILVER)) +
            rect(4, 6, 56, 44, 4, ic.v('#e8e6de', .5, .25)) +
            rect(9, 11, 46, 33, 2, screen, OL, 1.2) +
            gloss(ic, 'M10,12 H54 V24 Q32,29 10,24 Z', .5))


def e_house(ic):
    return (rect(40, 10, 7, 14, 1, ic.v(RED)) +
            path('M12,32 V56 H52 V32', ic.v(BEIGE)) +
            rect(27, 38, 11, 18, 1.5, ic.v(BROWN)) +
            rect(42, 36, 7, 7, 1, ic.lg([(0, '#bfe6ff'), (1, '#4c93e0')]), OL, 1.2) +
            path('M4,34 L32,8 L60,34 L55,38 L32,17 L9,38 Z', ic.v(RED)) +
            gloss(ic, 'M8,33 L32,11 L56,33 L32,15 Z', .6))


def e_star(ic, c=YELLOW):
    return path(star_pts(32, 34, 28, 12), ic.v(c, .5, .25)) + gloss(ic, star_pts(32, 30, 18, 6), .45)


def e_globe(ic):
    land = ic.v(GREEN, .3, .3)
    return (circle(32, 32, 27, ic.ball(BLUE)) +
            path('M14,18 Q22,12 28,16 Q30,24 22,26 Q20,34 14,32 Q8,28 14,18 Z', land, OL, 1) +
            path('M34,30 Q44,26 50,32 Q52,42 44,50 Q38,54 36,44 Q30,38 34,30 Z', land, OL, 1) +
            path('M38,10 Q46,10 50,16 Q44,18 38,14 Z', land, OL, 1) +
            ellipse(32, 32, 12, 27, 'none', WHITE, .8, ' opacity=".45"') +
            path('M5,32 H59 M9,19 H55 M9,45 H55', 'none', WHITE, .8, ' opacity=".45"') +
            ellipse(25, 19, 14, 9, ic.glossfill(.55), None))


def e_code(ic, c=CYAN):
    return (ostroke('M20,16 L6,32 L20,48', c, 7) + ostroke('M44,16 L58,32 L44,48', c, 7) +
            ostroke('M37,10 L27,54', YELLOW, 6))


def e_gear(ic, c=SILVER, cx=32, cy=32, ro=28, ri=21, n=9):
    return (path(gear_path(cx, cy, ro, ri, n, ri * .42), ic.v(c, .55, .35), OL, SW, ' fill-rule="evenodd"') +
            circle(cx, cy, ri * .7, 'none', dk(c, .35), 1.2) +
            ellipse(cx - ro * .15, cy - ro * .4, ro * .55, ro * .28, ic.glossfill(.5), None))


def e_lock(ic, c=AMBER):
    return (ostroke('M20,30 V20 A12,12 0 0,1 44,20 V30', SILVER, 6) +
            rect(10, 28, 44, 30, 5, ic.v(c, .5, .3)) +
            path('M32,36 a5,5 0 0,1 3,9 l1.5,7 h-9 l1.5,-7 a5,5 0 0,1 3,-9 Z', DARK, None) +
            gloss_rect(ic, 12, 30, 40, 11, 4, .6))


def e_cloud(ic, c='#eaf4ff'):
    shapes = [(20, 40, 12), (34, 30, 15), (46, 40, 11)]
    o = ''.join(circle(x, y, r, 'none', OL, SW * 2) for x, y, r in shapes) + rect(12, 36, 40, 16, 8, 'none', OL, SW * 2)
    f = ic.lg([(0, WHITE), (1, '#9fc7ee')], user=True, y1=15, y2=52)
    i = ''.join(circle(x, y, r, f, None) for x, y, r in shapes) + rect(12, 36, 40, 16, 8, f, None)
    return o + i


def e_user(ic, c=BLUE, x=0, y=0, s=1):
    body = (path('M10,60 Q10,38 32,38 Q54,38 54,60 Z', ic.v(c)) +
            circle(32, 22, 13, ic.ball('#f2c49b')) +
            path('M19,20 Q20,8 32,8 Q45,8 45,20 Q40,13 32,14 Q24,13 19,20 Z', ic.v(BROWN), OL, 1.2))
    return place(body, x, y, s) if s != 1 or x or y else body


def e_people(ic):
    return e_user(ic, GREEN, 22, 0, .7) + e_user(ic, BLUE, 4, 14, .78)


def e_play(ic, c=GREEN):
    return path('M18,8 L54,32 L18,56 Z', ic.v(c)) + gloss(ic, 'M21,13 L46,30 H21 Z', .6)


def e_mail(ic):
    return (rect(4, 14, 56, 38, 3, ic.v('#fafafa', .5, .18)) +
            path('M5,16 L32,38 L59,16', 'none', OL, SW) +
            path('M5,50 L24,32 M59,50 L40,32', 'none', '#8a8fa0', 1.2) +
            rect(46, 18, 9, 10, 1, ic.v(RED), OL, 1))


def e_heart(ic, c=RED):
    return (path('M32,56 L9,32 Q2,24 8,15 Q16,6 26,12 Q30,15 32,19 Q34,15 38,12 Q48,6 56,15 Q62,24 55,32 Z', ic.v(c, .45, .25)) +
            ellipse(20, 20, 8, 5, ic.glossfill(.7), None, ' transform="rotate(-30 20 20)"'))


def e_magnifier(ic):
    return (ostroke('M40,40 L56,56', BROWN, 9) +
            circle(27, 27, 19, ic.lg([(0, '#e6f6ff', .9), (1, '#7ab8e8', .7)]), OL, SW) +
            circle(27, 27, 19, 'none', SILVER, 4) + circle(27, 27, 21.5, 'none', OL, SW) +
            circle(27, 27, 16.5, 'none', OL, 1) +
            ellipse(21, 20, 8, 5, ic.glossfill(.8), None, ' transform="rotate(-35 21 20)"'))


def e_terminal(ic):
    """A Shell window: blue title bar, dark body, prompt."""
    return (rect(4, 8, 56, 48, 3, ic.v('#1c2740', .2, .2)) +
            path('M4,18 V11 Q4,8 7,8 H57 Q60,8 60,11 V18 Z', ic.v(BLUE), OL, SW) +
            rect(51, 10.5, 6, 5, 1, ic.v(SILVER), OL, .8) +
            text(9, 33, '1&gt;', 12, '#6dff7a', family='DejaVu Sans Mono,Monospace', anchor='start') +
            rect(32, 24, 7, 10, 0, '#6dff7a', None, extra=' opacity=".85"') +
            rect(9, 40, 24, 3, 1, '#4fbf5a', None) + rect(9, 46, 36, 3, 1, '#4fbf5a', None) +
            gloss_rect(ic, 5, 9, 54, 6, 2, .5))


def e_window(ic, c=BLUE, content=None):
    return (rect(4, 8, 56, 48, 3, ic.v('#f2f2f2', .5, .2)) +
            path('M4,18 V11 Q4,8 7,8 H57 Q60,8 60,11 V18 Z', ic.v(c), OL, SW) +
            rect(51, 10.5, 6, 5, 1, ic.v(SILVER), OL, .8) +
            rect(7, 10.5, 5, 5, 1, ic.v(SILVER), OL, .8) +
            (content or '') + gloss_rect(ic, 5, 9, 54, 6, 2, .5))


def e_wrench(ic, c=SILVER):
    d = 'M44,6 A13,13 0 0,0 32,24 L8,48 A5,5 0 0,0 16,56 L40,32 A13,13 0 0,0 58,20 L50,26 L42,22 L40,14 Z'
    return path(d, ic.metal(c)) + gloss(ic, 'M42,10 Q36,14 36,22 L14,44 L12,42 L34,20 Q34,12 42,10 Z', .7)


def e_screwdriver(ic):
    return (ostroke('M30,34 L52,12', SILVER, 5) +
            path('M8,54 L24,38 L32,42 L22,52 Q14,60 8,54 Z', ic.v(RED)) +
            path('M24,38 L28,34 L34,40 L32,42 Z', ic.v(AMBER)))


def e_toolbox(ic):
    return (wrapped_handle() +
            rect(4, 24, 56, 32, 4, ic.v(RED)) + rect(4, 32, 56, 6, 0, ic.v(dk(RED, .25)), OL, 1.2) +
            rect(27, 30, 10, 10, 2, ic.v(SILVER)) + gloss_rect(ic, 6, 25, 52, 7, 3, .6))


def wrapped_handle():
    return ostroke('M22,25 V17 Q22,13 26,13 H38 Q42,13 42,17 V25', SILVER, 5)


def e_chip(ic):
    pins = ''.join(rect(x, 4, 4, 10, 1, ic.v(SILVER), OL, 1) + rect(x, 50, 4, 10, 1, ic.v(SILVER), OL, 1)
                   for x in range(14, 50, 8))
    pins += ''.join(rect(4, y, 10, 4, 1, ic.v(SILVER), OL, 1) + rect(50, y, 10, 4, 1, ic.v(SILVER), OL, 1)
                    for y in range(14, 50, 8))
    return (pins + rect(11, 11, 42, 42, 4, ic.v('#3a3d4c', .3, .3)) +
            rect(20, 20, 24, 24, 2, ic.v(AMBER, .5, .2), OL, 1.2) + gloss_rect(ic, 12, 12, 40, 12, 3, .35))


def e_brush(ic, c=RED):
    return (ostroke('M54,8 L32,32', BROWN, 7) +
            path('M24,34 L30,40 Q34,50 24,56 Q14,60 6,58 Q12,52 12,46 Q14,36 24,34 Z', ic.v(c)) +
            rect(26, 30, 8, 9, 1.5, ic.v(SILVER), OL, 1.2, ' transform="rotate(45 30 34.5)"'))


def e_pencil(ic, c=YELLOW):
    return (path('M42,8 L56,22 L22,56 L6,58 L8,42 Z', ic.v(c)) +
            path('M8,42 L22,56 L6,58 Z', BEIGE) + path('M7,51 L13,57 L6,58 Z', DARK, None) +
            path('M42,8 L50,0 L64,14 L56,22 Z', ic.v(PINK), OL, SW, ' transform="translate(-3 3)"') +
            path('M11,39 L39,11', 'none', WHITE, 2, ' opacity=".6"'))


def e_calendar(ic, day='14'):
    return (rect(6, 10, 52, 48, 4, ic.v('#fafafa', .5, .15)) +
            path('M6,26 V14 Q6,10 10,10 H54 Q58,10 58,14 V26 Z', ic.v(RED), OL, SW) +
            ostroke('M20,6 V16', SILVER, 4) + ostroke('M44,6 V16', SILVER, 4) +
            text(32, 52, day, 24, DARK) + gloss_rect(ic, 8, 12, 48, 6, 2, .5))


def e_clock(ic, c=BLUE):
    return (circle(32, 32, 27, ic.v(c)) + circle(32, 32, 21, ic.lg([(0, '#ffffff'), (1, '#dfe6f0')]), OL, 1.4) +
            ''.join(circle(32 + 17 * math.cos(math.radians(a)), 32 + 17 * math.sin(math.radians(a)), 1.4, DARK, None)
                    for a in range(0, 360, 30)) +
            ostroke('M32,32 V17', DARK, 3, 3) + ostroke('M32,32 L42,38', RED, 2.5, 2.5) + circle(32, 32, 2.5, DARK, None) +
            ellipse(25, 17, 12, 6, ic.glossfill(.6), None))


def e_key(ic, c=AMBER):
    return (circle(20, 22, 15, ic.v(c, .5, .3)) + circle(16, 18, 4.5, DARK, None) +
            path('M30,30 L56,56 L50,60 L46,56 L43,59 L38,54 L41,51 L26,36 Z', ic.v(c, .5, .3)) +
            ellipse(15, 13, 7, 4, ic.glossfill(.7), None, ' transform="rotate(-30 15 13)"'))


def e_shield(ic, c=BLUE, check=True):
    d = 'M32,4 L56,12 V30 Q56,50 32,60 Q8,50 8,30 V12 Z'
    body = path(d, ic.v(c)) + path('M32,4 V60 Q8,50 8,30 V12 Z', WHITE, None, extra=' opacity=".18"')
    if check:
        body += ostroke('M20,32 L29,41 L45,23', WHITE, 6)
    return body + gloss(ic, 'M32,7 L53,14 V26 Q32,32 11,26 V14 Z', .45)


def e_bell(ic, c=AMBER):
    return (circle(32, 54, 6, ic.v(dk(c, .1))) +
            path('M32,6 Q46,6 47,24 Q48,40 56,48 H8 Q16,40 17,24 Q18,6 32,6 Z', ic.v(c, .5, .3)) +
            rect(6, 46, 52, 6, 3, ic.v(c, .3, .35)) + gloss(ic, 'M24,12 Q20,18 20,30 Q22,22 28,13 Z', .8))


def e_speaker(ic, waves=True, c=DARK):
    body = path('M6,24 H18 L34,10 V54 L18,40 H6 Z', ic.v(c, .45, .2)) + gloss(ic, 'M8,26 H18 L32,14 V28 H8 Z', .4)
    if waves:
        body += ostroke(arc_pts(34, 32, 10, -50, 50), BLUE, 4) + ostroke(arc_pts(34, 32, 20, -50, 50), BLUE, 4)
    return body


def e_power(ic, c=RED):
    return (circle(32, 32, 28, ic.ball(c)) +
            ostroke(arc_pts(32, 33, 14, -55, 235), WHITE, 5) + ostroke('M32,12 V30', WHITE, 5))


def e_badge(ic, c, glyph):
    """Round glossy badge with a white glyph path drawn with ostroke-like style."""
    return circle(32, 32, 28, ic.ball(c)) + glyph + ellipse(32, 17, 18, 9, ic.glossfill(.55), None)


def e_info(ic):
    return e_badge(ic, BLUE, circle(32, 18, 4.5, WHITE, None) + rect(27.5, 26, 9, 24, 3, WHITE, None))


def e_question(ic):
    return e_badge(ic, PURPLE, ostroke('M22,22 Q22,12 32,12 Q42,12 42,21 Q42,27 35,30 Q32,32 32,37', WHITE, 6, 6) +
                   circle(32, 47, 4.5, WHITE, None))


def e_error(ic):
    return e_badge(ic, RED, ostroke('M21,21 L43,43 M43,21 L21,43', WHITE, 7, 7))


def e_ok(ic):
    return e_badge(ic, GREEN, ostroke('M18,33 L28,43 L46,22', WHITE, 7, 7))


def e_warning(ic):
    return (path('M32,5 L60,54 Q61,58 57,58 H7 Q3,58 4,54 Z', ic.v(YELLOW, .5, .25)) +
            rect(28, 20, 8, 22, 3, DARK, None) + circle(32, 49, 4.2, DARK, None) +
            gloss(ic, 'M32,10 L50,42 Q32,38 14,42 Z', .45))


def e_plus(ic, c=GREEN):
    return path('M24,6 H40 V24 H58 V40 H40 V58 H24 V40 H6 V24 H24 Z', ic.v(c)) + gloss_rect(ic, 8, 26, 48, 6, 2, .6)


def e_minus(ic, c=RED):
    return rect(6, 24, 52, 16, 3, ic.v(c)) + gloss_rect(ic, 8, 26, 48, 6, 2, .6)


def e_cross(ic, c=RED):
    return ostroke('M14,14 L50,50 M50,14 L14,50', c, 12) + ostroke('M17,17 L30,30', lt(c, .5), 3, 0)


def e_check(ic, c=GREEN):
    return ostroke('M8,34 L24,50 L56,14', c, 12) + ostroke('M12,34 L24,46', lt(c, .5), 3, 0)


def e_arrow(ic, c=BLUE, rot=0):
    """Chunky arrow pointing right, rotated about centre."""
    body = path('M6,22 H32 V8 L58,32 L32,56 V42 H6 Z', ic.v(c, .5, .3)) + gloss(ic, 'M8,24 H34 V13 L52,30 H8 Z', .5)
    return g(body, 'rotate(%s 32 32)' % rot) if rot else body


def e_arrow_end(ic, c=BLUE, rot=0):
    body = (path('M4,22 H26 V8 L50,32 L26,56 V42 H4 Z', ic.v(c, .5, .3)) + rect(51, 8, 8, 48, 2, ic.v(c, .5, .3)) +
            gloss(ic, 'M6,24 H28 V13 L44,30 H6 Z', .5))
    return g(body, 'rotate(%s 32 32)' % rot) if rot else body


def e_refresh(ic, c=GREEN):
    return (ostroke(arc_pts(32, 32, 20, 200, 340), c, 8, cap='butt') +
            path('M45,10 L58,24 L40,28 Z', ic.v(c)) +
            ostroke(arc_pts(32, 32, 20, 20, 160), c, 8, cap='butt') +
            path('M19,54 L6,40 L24,36 Z', ic.v(c)))


def e_undo(ic, c=AMBER, flip=False):
    body = ostroke('M18,26 H40 Q54,26 54,40 Q54,54 40,54 H28', c, 8, cap='butt') + path('M22,10 L4,26 L22,42 Z', ic.v(c))
    return g(body, 'translate(64 0) scale(-1 1)') if flip else body


def e_camera(ic, c=DARK):
    return (path('M20,16 L24,8 H40 L44,16 Z', ic.v(SILVER)) +
            rect(4, 14, 56, 40, 6, ic.v(c, .45, .25)) +
            rect(8, 20, 9, 5, 1.5, ic.v(SILVER), OL, 1) +
            circle(36, 35, 15, ic.v(SILVER)) + circle(36, 35, 10, ic.ball('#2a4c9a')) +
            circle(32, 31, 3, WHITE, None, ' opacity=".8"') + gloss_rect(ic, 6, 16, 52, 10, 4, .3))


def e_printer(ic):
    return (rect(16, 4, 32, 20, 1, ic.v(WHITE, .5, .1)) +
            rect(4, 20, 56, 26, 5, ic.v('#e4e2da', .5, .3)) +
            rect(12, 38, 40, 22, 1, ic.v(WHITE, .5, .1)) +
            ''.join(rect(17, y, 30, 2.5, 1, '#8a94ab', None) for y in (44, 49, 54)) +
            circle(50, 28, 2.5, GREEN, OL, 1) + gloss_rect(ic, 6, 21, 52, 8, 4, .6))


def e_phone(ic, c=DARK, screen=None):
    screen = screen or ic.lg([(0, '#7ad0ff'), (1, '#3045b0')])
    return (rect(16, 3, 32, 58, 6, ic.v(c, .4, .2)) + rect(19, 9, 26, 44, 2, screen, OL, 1) +
            circle(32, 57, 2, SILVER, None) + gloss(ic, 'M20,10 H44 V22 L20,34 Z', .3))


def e_book(ic, c=BLUE, page=True):
    body = (path('M8,12 Q8,6 14,6 H54 V52 H14 Q8,52 8,58 Z', ic.v(c)) +
            path('M8,58 Q8,52 14,52 H54 V60 H14 Q8,60 8,58 Z', ic.v('#fafafa', .2, .2)) +
            ostroke('M16,6 V52', dk(c, .3), 2, 2))
    return body + gloss_rect(ic, 18, 8, 34, 8, 2, .5)


def e_chart(ic):
    bars = [(10, 36, GREEN), (22, 24, YELLOW), (34, 30, ORANGE), (46, 12, RED)]
    return (rect(4, 6, 56, 52, 3, ic.v('#fafafa', .5, .15)) +
            ''.join(rect(x, y, 9, 52 - y, 1, ic.v(c), OL, 1.2) for x, y, c in bars) +
            ostroke('M9,34 L20,26 L32,30 L52,12', BLUE, 3, 5))


def e_palette(ic):
    return (path('M32,6 Q58,6 58,30 Q58,44 46,44 Q38,44 40,50 Q42,58 32,58 Q6,58 6,32 Q6,6 32,6 Z', ic.v(BEIGE)) +
            circle(22, 20, 5, ic.ball(RED), OL, 1) + circle(36, 16, 5, ic.ball(YELLOW), OL, 1) +
            circle(48, 25, 5, ic.ball(GREEN), OL, 1) + circle(16, 34, 5, ic.ball(BLUE), OL, 1) +
            circle(24, 47, 5, ic.ball(PURPLE), OL, 1))


def e_font(ic):
    return (text(26, 50, 'A', 48, ic.v(RED), 'bold', stroke=OL, sw=2, family='DejaVu Serif,Serif') +
            text(48, 54, 'a', 30, ic.v(BLUE), 'bold', stroke=OL, sw=2, family='DejaVu Serif,Serif'))


def e_box(ic, c='#c98d4e'):
    return (path('M4,20 L32,8 L60,20 L32,32 Z', ic.v(lt(c, .25))) +
            path('M4,20 L32,32 V60 L4,48 Z', ic.v(c)) + path('M60,20 L32,32 V60 L60,48 Z', ic.v(dk(c, .2))) +
            path('M18,14 L46,26 V36 L52,33 V24 L24,11 Z', ic.v(BEIGE, .3, .1), OL, 1))


def e_puzzle(ic, c=GREEN):
    d = ('M8,20 H22 Q20,8 29,8 Q38,8 36,20 H50 V34 Q62,32 62,41 Q62,50 50,48 V60 H36 Q38,50 29,50 Q20,50 22,60 H8 V46'
         ' Q18,48 18,40 Q18,32 8,34 Z')
    return path(d, ic.v(c)) + gloss(ic, 'M10,22 H24 Q22,11 29,11 Q35,11 34,22 H48 V30 Q30,34 10,30 Z', .5)


def e_ball(ic, cx=32, cy=32, R=28, tilt=-22, pitch=-8, spin=11.25):
    """Red/white checkered sphere, 3D-projected with tilt, curved bands and soft shading."""
    tz, tx = math.radians(tilt), math.radians(pitch)

    def proj(la, lo):
        la, lo = math.radians(la), math.radians(lo + spin)
        x, y, z = math.cos(la) * math.sin(lo), -math.sin(la), math.cos(la) * math.cos(lo)
        y, z = y * math.cos(tx) - z * math.sin(tx), y * math.sin(tx) + z * math.cos(tx)
        x, y = x * math.cos(tz) - y * math.sin(tz), x * math.sin(tz) + y * math.cos(tz)
        if z < 0:                       # behind: pin to the visible rim
            m = math.hypot(x, y) or 1
            x, y = x / m, y / m
        return '%.2f,%.2f' % (cx + R * x, cy + R * y), z

    tiles, nla, nlo, k = [], 8, 16, 6
    for i in range(nla):
        for j in range(nlo):
            if (i + j) % 2:
                continue
            la0, la1 = -90 + 180 * i / nla, -90 + 180 * (i + 1) / nla
            lo0, lo1 = 360 * j / nlo, 360 * (j + 1) / nlo
            edge = ([(la0, lo0 + (lo1 - lo0) * t / k) for t in range(k + 1)] +
                    [(la0 + (la1 - la0) * t / k, lo1) for t in range(1, k + 1)] +
                    [(la1, lo1 - (lo1 - lo0) * t / k) for t in range(1, k + 1)] +
                    [(la1 - (la1 - la0) * t / k, lo0) for t in range(1, k)])
            pts = [proj(*p) for p in edge]
            if max(z for _, z in pts) <= 0:
                continue
            tiles.append('M' + ' L'.join(p for p, _ in pts) + 'Z')
    red = ic.rg([(0, '#ff5a4a'), (.6, '#e0201c'), (1, '#9a0e10')], .38, .32, .75)
    white = ic.rg([(0, '#ffffff'), (.6, '#f2f0f4'), (1, '#b8b8c8')], .38, .32, .75)
    out = circle(cx, cy, R, white, None)
    out += path(' '.join(tiles), red, None)
    out += circle(cx, cy, R, ic.rg([(0, WHITE, 0), (.55, '#101030', 0), (.85, '#101030', .22), (1, '#101030', .55)],
                                   .4, .36, .72, .32, .26), OL, SW * .8)
    out += ellipse(cx - R * .33, cy - R * .42, R * .38, R * .2, ic.glossfill(.8), None,
                   ' transform="rotate(-30 %s %s)"' % (cx - R * .33, cy - R * .42))
    out += circle(cx - R * .42, cy - R * .5, R * .07, WHITE, None, ' opacity=".9"')
    return out


def e_gamepad(ic, c=DARK):
    return (path('M14,18 H50 Q60,18 61,32 Q63,52 54,54 Q48,55 42,44 H22 Q16,55 10,54 Q1,52 3,32 Q4,18 14,18 Z', ic.v(c, .45, .2)) +
            path('M15,26 h5 v5 h5 v5 h-5 v5 h-5 v-5 h-5 v-5 h5 Z', ic.v(SILVER), OL, 1) +
            circle(44, 28, 3.5, ic.ball(RED), OL, 1) + circle(51, 34, 3.5, ic.ball(YELLOW), OL, 1) +
            circle(44, 40, 3.5, ic.ball(GREEN), OL, 1) + circle(37, 34, 3.5, ic.ball(BLUE), OL, 1) +
            gloss(ic, 'M14,20 H50 Q57,20 58,28 H6 Q8,20 14,20 Z', .3))


def e_trash(ic, full=False):
    body = rect(10, 18, 44, 40, 3, ic.metal(SILVER))
    body = path('M10,18 H54 L50,58 Q50,60 47,60 H17 Q14,60 14,58 Z', ic.metal(SILVER))
    body += ''.join(path('M%s,24 V54' % x, 'none', dk(SILVER, .35), 2) for x in (22, 32, 42))
    if full:
        body += (path('M12,18 Q14,4 24,8 Q30,0 38,7 Q48,2 52,18 Z', ic.v('#f4f0e0', .4, .15)) +
                 path('M24,14 L34,6 L40,16', 'none', '#a08860', 1.2) + rect(36, 6, 12, 9, 1, ic.v(BLUE), OL, 1,
                                                                            ' transform="rotate(20 42 10)"'))
        lid = g(rect(6, 12, 52, 7, 3, ic.metal(SILVER)) + rect(26, 7, 12, 6, 2, ic.metal(SILVER)), 'rotate(-14 10 18)')
    else:
        lid = rect(6, 12, 52, 7, 3, ic.metal(SILVER)) + rect(26, 7, 12, 6, 2, ic.metal(SILVER))
    return body + lid


def e_disc(ic, cx=32, cy=32, r=28):
    rainbow = ic.lg([(0, '#c9f1ff'), (.25, '#f3c9ff'), (.5, '#fff6c0'), (.75, '#c4ffd8'), (1, '#c9d9ff')], 0, 0, 1, 1)
    return (circle(cx, cy, r, rainbow) + circle(cx, cy, r, ic.rg([(0, WHITE, 0), (.6, WHITE, .1), (1, '#6070a0', .5)]), None) +
            path(sector(cx, cy, r - 1, -60, -25), WHITE, None, ' opacity=".5"') +
            path(sector(cx, cy, r - 1, 120, 155), WHITE, None, ' opacity=".5"') +
            circle(cx, cy, r * .32, ic.v(SILVER), OL, 1.2) + circle(cx, cy, r * .13, '#f0f0f0', OL, 1.2))


def sector(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return 'M%s,%s L%.2f,%.2f A%s,%s 0 0,1 %.2f,%.2f Z' % (cx, cy, x0, y0, r, r, x1, y1)


def e_floppy(ic, c=NAVY, label=None):
    body = (path('M6,10 Q6,6 10,6 H52 L58,12 V54 Q58,58 54,58 H10 Q6,58 6,54 Z', ic.v(c, .35, .35)) +
            rect(18, 6, 28, 18, 1, ic.metal(SILVER), OL, 1.2) + rect(36, 9, 6, 12, 1, ic.v(dk(c, .2), .1, .1), None) +
            rect(12, 32, 40, 26, 2, ic.v(WHITE, .4, .1), OL, 1.2) +
            ''.join(rect(16, y, 32, 1.5, 0, '#9aa6c0', None) for y in (40, 46, 52)) +
            rect(8, 51, 3, 4, .5, DARK, None))
    if label:
        body += text(32, 46, label, 9, DARK)
    return body + gloss(ic, 'M8,10 Q8,8 10,8 H17 V26 H8 Z', .35)


def e_hdd(ic):
    return (path('M4,26 L14,14 H50 L60,26 Z', ic.v('#d0d4dc', .5, .2)) +
            rect(4, 26, 56, 24, 4, ic.v('#a8aeba', .45, .35)) +
            rect(9, 31, 28, 14, 2, ic.lg([(0, '#4a4e5c'), (1, '#262833')]), OL, 1) +
            ''.join(rect(x, 33, 2, 10, 1, '#5c6070', None) for x in (12, 16, 20, 24, 28, 32)) +
            circle(51, 38, 3.5, ic.ball(GREEN), OL, 1) + gloss_rect(ic, 6, 27, 52, 7, 3, .55))


def e_ssd(ic):
    return (rect(6, 14, 52, 36, 4, ic.v('#3a3d4c', .35, .3)) +
            rect(12, 20, 40, 18, 2, ic.v(BLUE, .4, .2), OL, 1) + text(32, 33, 'SSD', 10, WHITE) +
            circle(50, 44, 2.5, ic.ball(GREEN), OL, 1) + gloss_rect(ic, 8, 15, 48, 8, 3, .35))


def e_usb(ic, c=BLUE):
    return (rect(22, 2, 20, 16, 1, ic.metal(SILVER)) + rect(26, 7, 4, 4, 0, DARK, None) + rect(34, 7, 4, 4, 0, DARK, None) +
            rect(16, 16, 32, 44, 7, ic.v(c, .45, .3)) +
            path('M32,26 V48 M32,30 L25,36 V40 M32,34 L39,38 V42', 'none', WHITE, 2.2) + circle(32, 50, 3, WHITE, None) +
            gloss_rect(ic, 18, 18, 28, 12, 5, .5))


def e_sdcard(ic, c=BLUE):
    return (path('M14,4 H44 L52,12 V58 Q52,60 50,60 H14 Q12,60 12,58 V6 Q12,4 14,4 Z', ic.v(c, .45, .3)) +
            ''.join(rect(x, 6, 4, 9, 1, ic.v(AMBER), OL, .8) for x in (18, 24, 30, 36)) +
            rect(16, 28, 32, 24, 2, ic.v(WHITE, .3, .1), OL, 1) + text(32, 44, 'SD', 11, DARK))


def e_computer(ic):
    """Wedge home computer with a matching monitor."""
    return (path('M26,40 H38 L40,46 H24 Z', ic.v('#d8d0b4')) +
            rect(10, 2, 44, 38, 5, ic.v(BEIGE, .5, .25)) +
            rect(15, 7, 34, 26, 2, ic.lg([(0, '#73b7ff'), (1, '#1f3d9c')]), OL, 1.2) +
            rect(18, 10, 18, 3, 0, WHITE, None, ' opacity=".8"') + rect(18, 15, 10, 8, 1, DRAWER, OL, .6) +
            rect(31, 15, 10, 8, 1, DRAWER, OL, .6) +
            path('M2,52 L8,44 H56 L62,52 V58 Q62,61 58,61 H6 Q2,61 2,58 Z', ic.v(BEIGE, .5, .3)) +
            ''.join(rect(x, 47, 4, 2.5, .5, '#9c957e', None) for x in range(12, 52, 5)) +
            rect(14, 51, 36, 3, 1, '#9c957e', None) +
            rect(46, 56, 10, 1.6, .5, DARK, None) + circle(8, 57, 1.3, RED, None) +
            gloss(ic, 'M16,8 H48 V18 Q32,22 16,18 Z', .45))


def e_amiga(ic):
    """A1200-ish wedge keyboard computer (generic)."""
    return (path('M2,40 L10,22 H54 L62,40 V50 Q62,54 58,54 H6 Q2,54 2,50 Z', ic.v(BEIGE, .5, .3)) +
            ''.join(rect(x, y, 4.5, 3, .6, '#f3eedf', OL, .6) for y in (26, 31) for x in range(13 + (y - 26) // 2, 50, 6)) +
            rect(15, 36, 32, 3.2, .6, '#f3eedf', OL, .6) +
            path('M2,44 H62', 'none', dk(BEIGE, .3), 1) + rect(44, 47, 13, 2, .5, DARK, None) +
            path('M6,48 l4,0 M6,48 l1.5,-3 l1.5,3', 'none', RED, 1) +
            rect(7, 47, 3, 2, .5, RED, None) + rect(11, 47, 3, 2, .5, GREEN, None) +
            gloss(ic, 'M10,23 H54 L57,29 H7 Z', .5))


def e_laptop(ic):
    return (rect(10, 8, 44, 34, 3, ic.v('#3a3d4c', .3, .3)) +
            rect(14, 12, 36, 26, 1, ic.lg([(0, '#73b7ff'), (1, '#1f3d9c')]), OL, 1) +
            path('M2,46 L8,42 H56 L62,46 V50 Q62,52 60,52 H4 Q2,52 2,50 Z', ic.v(SILVER, .5, .3)) +
            gloss(ic, 'M15,13 H49 V22 L15,30 Z', .3))


def e_keyboard(ic):
    keys = ''.join(rect(x, y, 5, 5, 1, ic.v('#fbfaf4', .3, .15), OL, .7) for y in (22, 29) for x in range(8, 56, 6))
    return (rect(2, 16, 60, 32, 4, ic.v('#d6d2c4', .4, .3)) + keys +
            rect(14, 36, 36, 5, 1, ic.v('#fbfaf4', .3, .15), OL, .7) + gloss_rect(ic, 4, 17, 56, 4, 2, .5))


def e_mouse(ic):
    return (ostroke('M32,8 Q32,2 40,2 Q48,2 46,8', DARK, 2, 3.5) +
            rect(14, 8, 36, 52, 18, ic.v('#f2f0ea', .5, .25)) +
            path('M32,8 V28 M14,28 H50', 'none', OL, 1.2) + rect(29, 13, 6, 10, 3, ic.v(DARK), OL, 1) +
            gloss(ic, 'M18,24 Q18,12 30,10 V26 Z', .6))


def e_tablet(ic):
    return (rect(6, 10, 52, 42, 5, ic.v(DARK, .35, .2)) + rect(12, 16, 40, 30, 2, ic.lg([(0, '#cfe9ff'), (1, '#6aa6e0')]), OL, 1) +
            ostroke('M30,56 L50,24', SILVER, 3) + path('M30,56 L28,60 L32,58 Z', DARK, None))


def e_touchpad(ic):
    return (rect(6, 10, 52, 44, 5, ic.v(SILVER, .4, .35)) + rect(10, 14, 44, 28, 3, ic.v('#5a5e6c', .2, .2), OL, 1) +
            rect(10, 44, 21, 6, 2, ic.v(DARK), OL, 1) + rect(33, 44, 21, 6, 2, ic.v(DARK), OL, 1))


def e_scanner(ic):
    return (path('M4,30 L10,20 H54 L60,30 Z', ic.lg([(0, '#cfeaff', .9), (1, '#5f8fc0', .9)])) +
            rect(4, 30, 56, 20, 4, ic.v('#e4e2da', .5, .3)) + rect(10, 36, 30, 3, 1, GREEN, None) +
            circle(52, 40, 2.5, GREEN, OL, 1) + gloss_rect(ic, 6, 31, 52, 6, 3, .55))


def e_headphones(ic, c=DARK):
    return (ostroke('M10,42 V32 Q10,8 32,8 Q54,8 54,32 V42', SILVER, 5) +
            rect(4, 34, 14, 24, 5, ic.v(c, .45, .2)) + rect(46, 34, 14, 24, 5, ic.v(c, .45, .2)) +
            rect(7, 37, 6, 10, 3, ic.glossfill(.4), None) + rect(49, 37, 6, 10, 3, ic.glossfill(.4), None))


def e_mic(ic):
    return (ostroke('M18,30 Q18,46 32,46 Q46,46 46,30', SILVER, 4) + ostroke('M32,46 V58 M22,58 H42', SILVER, 4) +
            rect(22, 4, 20, 34, 10, ic.v(DARK, .45, .2)) +
            ''.join(path('M24,%s H40' % y, 'none', '#6a6e80', 1) for y in (12, 16, 20)) + gloss_rect(ic, 24, 6, 7, 26, 3, .4))


def e_speakerbox(ic):
    return (rect(12, 4, 40, 56, 4, ic.v('#5a4430', .35, .3)) +
            circle(32, 20, 9, ic.rg([(0, '#555a6a'), (1, '#16171e')]), OL, 1.2) + circle(32, 20, 3, SILVER, None) +
            circle(32, 43, 12, ic.rg([(0, '#555a6a'), (1, '#16171e')]), OL, 1.2) + circle(32, 43, 4, SILVER, None) +
            gloss_rect(ic, 14, 6, 36, 8, 3, .3))


def e_soundcard(ic):
    return (rect(4, 14, 56, 30, 3, ic.v(GREEN, .3, .35)) + rect(4, 44, 34, 6, 0, ic.v(AMBER), OL, 1) +
            rect(10, 20, 16, 16, 2, ic.v(DARK), OL, 1) +
            ''.join(circle(x, 28, 4, ic.v(c), OL, 1) for x, c in ((36, GREEN), (46, PINK), (55, BLUE))))


def e_network(ic):
    """Ethernet plug with cable."""
    return (ostroke('M32,44 V60', BLUE, 6) +
            rect(14, 8, 36, 38, 4, ic.v('#e0e8f0', .5, .3)) + rect(20, 4, 24, 8, 2, ic.v('#e0e8f0', .4, .3)) +
            ''.join(rect(x, 6, 2, 6, 0, AMBER, None) for x in range(23, 42, 4)) +
            gloss_rect(ic, 16, 10, 32, 12, 3, .5))


def e_wifi(ic, c=BLUE):
    return (ostroke(arc_pts(32, 52, 40, 225, 315), c, 6) + ostroke(arc_pts(32, 52, 27, 225, 315), c, 6) +
            ostroke(arc_pts(32, 52, 14, 225, 315), c, 6) + circle(32, 52, 5, ic.ball(c)))


def e_bluetooth(ic):
    return (rect(12, 2, 40, 60, 20, ic.v(BLUE)) +
            ostroke('M22,22 L42,40 L32,50 V14 L42,24 L22,42', WHITE, 4, 4) +
            gloss_rect(ic, 16, 5, 32, 16, 12, .5))


def e_battery(ic, level=.8, c=GREEN):
    return (rect(24, 2, 16, 6, 2, ic.v(SILVER)) + rect(12, 7, 40, 54, 5, ic.v(SILVER, .4, .3)) +
            rect(16, 11 + 46 * (1 - level), 32, 46 * level, 2, ic.v(c, .45, .25), OL, 1) +
            gloss_rect(ic, 14, 9, 10, 48, 3, .5))


def e_server(ic):
    return (rect(14, 2, 36, 58, 4, ic.v('#3a3d4c', .3, .3)) +
            ''.join(rect(18, y, 28, 10, 1.5, ic.v('#5a5e70', .3, .3), OL, 1) + circle(42, y + 5, 1.8, ic.ball(GREEN), None) +
                    rect(21, y + 4, 14, 2, 0, '#22232c', None) for y in (7, 20, 33)) +
            gloss_rect(ic, 16, 4, 32, 10, 3, .3))


def e_tv(ic):
    return (rect(2, 8, 60, 42, 4, ic.v(DARK, .3, .2)) + rect(6, 12, 52, 34, 2, ic.lg([(0, '#73b7ff'), (1, '#1f3d9c')]), OL, 1) +
            path('M22,50 H42 L46,58 H18 Z', ic.v(SILVER)) + gloss(ic, 'M7,13 H57 V24 Q32,30 7,24 Z', .4))


def e_tape(ic):
    return (rect(2, 12, 60, 40, 4, ic.v(DARK, .35, .2)) + rect(8, 16, 48, 20, 3, ic.v(BEIGE, .3, .1), OL, 1) +
            circle(20, 26, 6, ic.v(WHITE), OL, 1) + circle(44, 26, 6, ic.v(WHITE), OL, 1) +
            path('M14,52 L18,42 H46 L50,52 Z', ic.v('#5a5e70'), OL, 1))


def e_modem(ic):
    return (path('M4,40 L10,22 H54 L60,40 Z', ic.v('#d8d4c8')) + rect(4, 40, 56, 12, 3, ic.v('#b8b4a8', .3, .3)) +
            ''.join(circle(x, 46, 2, ic.ball(c), None) for x, c in ((14, GREEN), (22, GREEN), (30, AMBER), (38, RED))))


def e_pda(ic):
    return e_phone(ic, '#5a5e70')


def e_ups(ic):
    return (rect(14, 4, 36, 56, 4, ic.v(DARK, .35, .2)) +
            path('M34,12 L24,32 H32 L28,50 L42,26 H34 Z', ic.v(YELLOW), OL, 1.2) + gloss_rect(ic, 16, 6, 32, 10, 3, .3))


def e_calculator(ic):
    keys = ''
    cols = [GREY, GREY, GREY, ORANGE]
    for r in range(4):
        for c in range(4):
            keys += rect(13 + c * 10, 26 + r * 8, 8, 6, 1.5, ic.v(cols[c]), OL, .8)
    return (rect(8, 4, 48, 56, 5, ic.v('#3a3d4c', .3, .3)) +
            rect(13, 9, 38, 13, 2, ic.lg([(0, '#cfe8c0'), (1, '#8fb07c')]), OL, 1) + text(48, 20, '42', 10, DARK, anchor='end') +
            keys + gloss_rect(ic, 10, 6, 44, 6, 3, .3))


def e_clipboard(ic):
    return (rect(10, 8, 44, 52, 4, ic.v(BROWN, .35, .3)) + rect(15, 14, 34, 42, 1, ic.v(WHITE, .3, .1), OL, 1) +
            ''.join(rect(19, y, 26, 2.5, 1, '#8a94ab', None) for y in (26, 32, 38, 44)) +
            rect(22, 4, 20, 10, 3, ic.metal(SILVER)))


def e_pages(ic):
    def page(x, y):
        return (rect(x, y, 30, 38, 2, ic.v(WHITE, .3, .12)) +
                ''.join(rect(x + 5, y + yy, 20, 2.5, 1, '#8a94ab', None) for yy in (8, 14, 20, 26)))
    return page(8, 6) + page(26, 20)


def e_scissors(ic):
    return (ostroke('M20,40 L46,6', SILVER, 5) + ostroke('M44,40 L18,6', SILVER, 5) +
            circle(18, 48, 9, 'none', OL, 7.4) + circle(18, 48, 9, 'none', RED, 4) +
            circle(46, 48, 9, 'none', OL, 7.4) + circle(46, 48, 9, 'none', RED, 4) + circle(32, 24, 2, DARK, None))


def e_eye(ic):
    return (path('M2,32 Q32,4 62,32 Q32,60 2,32 Z', ic.v(WHITE, .3, .15)) + circle(32, 32, 13, ic.ball(TEAL)) +
            circle(32, 32, 6, DARK, None) + circle(28, 28, 2.5, WHITE, None))


def e_wine(ic):
    return (ostroke('M32,40 V56 M22,58 H42', '#d8e8f0', 4) +
            path('M16,6 H48 Q50,22 46,32 Q42,42 32,42 Q22,42 18,32 Q14,22 16,6 Z', ic.lg([(0, WHITE, .5), (1, '#c8e0f0', .6)])) +
            path('M17,20 H47 Q47,30 44,34 Q40,40 32,40 Q24,40 20,34 Q17,30 17,20 Z', ic.v('#9a1838', .3, .3), None) +
            gloss(ic, 'M20,8 H26 Q22,22 24,34 Q18,26 20,8 Z', .7))


def e_steam(ic):
    return e_badge(ic, '#1b3a5c', ostroke('M14,40 L30,46', WHITE, 4, 4) + circle(42, 24, 9, 'none', WHITE, 4) +
                   circle(42, 24, 3.5, WHITE, None) + circle(28, 44, 6, 'none', WHITE, 3))


def e_cards(ic):
    def card(tf, suit, col):
        return g(rect(14, 6, 30, 44, 3, ic.v(WHITE, .3, .12)) + text(29, 36, suit, 22, col), tf)
    return card('rotate(-14 32 40)', '&#9824;', DARK) + card('rotate(12 32 40) translate(6 4)', '&#9829;', RED)


def e_mine(ic):
    return (ostroke('M32,4 V60 M4,32 H60 M12,12 L52,52 M52,12 L12,52', DARK, 4, 6) +
            circle(32, 32, 18, ic.ball('#4a4e5c')) + circle(26, 26, 4, WHITE, None, ' opacity=".8"'))


def e_tile(ic):
    return (rect(14, 8, 38, 50, 5, ic.v('#e8dcc0', .4, .35)) + rect(10, 4, 38, 50, 5, ic.v('#fbf6e8', .4, .15)) +
            text(29, 42, '&#26481;', 26, RED, family='Noto Sans CJK JP,Sans'))


def e_app_tile(ic, c, inner):
    """Rounded glossy tile holding a pictogram (for apps without an object)."""
    return (rect(4, 4, 56, 56, 12, ic.v(c, .4, .35)) + place(inner, 12, 12, .625) +
            path('M6,16 Q6,6 16,6 H48 Q58,6 58,16 V26 Q32,34 6,26 Z', ic.glossfill(.55), None))


def e_chat(ic, c=GREEN):
    return (path('M8,8 H48 Q54,8 54,14 V34 Q54,40 48,40 H26 L14,52 V40 H8 Q2,40 2,34 V14 Q2,8 8,8 Z', ic.v(c)) +
            path('M34,24 H56 Q62,24 62,30 V46 Q62,52 56,52 H54 V60 L46,52 H34 Q28,52 28,46 V30 Q28,24 34,24 Z', ic.v(BLUE)) +
            gloss_rect(ic, 5, 10, 46, 8, 4, .5))


def e_contact(ic):
    return (rect(6, 8, 52, 48, 4, ic.v(BEIGE, .5, .2)) + e_user(ic, BLUE, 8, 16, .45) +
            ''.join(rect(36, y, 16, 3, 1, '#8a7a5a', None) for y in (24, 31, 38)))


def e_globe_plus(ic, badge):
    return e_globe(ic) + place(badge, 34, 34, .45)


def e_lightning(ic, c=YELLOW):
    return path('M38,2 L12,36 H28 L22,62 L52,24 H36 Z', ic.v(c, .5, .25)) + gloss(ic, 'M36,6 L16,33 H24 Z', .6)


def e_moon(ic):
    return path('M40,4 A28,28 0 1,0 60,40 A22,22 0 1,1 40,4 Z', ic.v(YELLOW, .5, .25))


def e_sun(ic):
    rays = ''.join(path('M32,32 L%.1f,%.1f' % (32 + 29 * math.cos(math.radians(a)), 32 + 29 * math.sin(math.radians(a))),
                        'none', ORANGE, 4) for a in range(0, 360, 45))
    return rays + circle(32, 32, 16, ic.ball(YELLOW))


def e_bug(ic):
    legs = ''.join(ostroke(d, DARK, 2.5, 3) for d in ('M18,30 L6,26', 'M18,40 L6,42', 'M20,50 L10,58',
                                                     'M46,30 L58,26', 'M46,40 L58,42', 'M44,50 L54,58'))
    return (legs + ellipse(32, 40, 16, 20, ic.v(RED)) + circle(32, 16, 9, ic.v(DARK)) +
            path('M32,22 V60', 'none', OL, 1.5) + circle(25, 36, 3, DARK, None) + circle(39, 44, 3, DARK, None) +
            ostroke('M28,10 L22,2 M36,10 L42,2', DARK, 2, 3))


def e_rocket(ic):
    return (path('M32,2 Q48,16 46,42 H18 Q16,16 32,2 Z', ic.v(SILVER, .5, .3)) +
            path('M18,32 L8,48 L18,46 Z', ic.v(RED)) + path('M46,32 L56,48 L46,46 Z', ic.v(RED)) +
            circle(32, 22, 6, ic.ball(BLUE)) + path('M24,44 L32,62 L40,44 Z', ic.v(ORANGE)))


def e_qr(ic):
    sq = lambda x, y: rect(x, y, 16, 16, 1, 'none', DARK, 4) + rect(x + 5, y + 5, 6, 6, 0, DARK, None)
    dots = ''.join(rect(x, y, 5, 5, 0, DARK, None) for x, y in ((32, 8), (38, 14), (32, 32), (40, 40), (50, 34), (34, 48), (48, 50), (8, 32), (18, 38)))
    return rect(2, 2, 60, 60, 5, ic.v(WHITE, .3, .1)) + sq(8, 8) + sq(40, 8) + sq(8, 40) + dots


def e_hourglass(ic):
    return (rect(12, 4, 40, 6, 2, ic.v(BROWN)) + rect(12, 54, 40, 6, 2, ic.v(BROWN)) +
            path('M16,10 H48 Q48,26 34,32 Q48,38 48,54 H16 Q16,38 30,32 Q16,26 16,10 Z', ic.lg([(0, '#e6f4ff', .9), (1, '#a8c8e8', .9)])) +
            path('M22,18 H42 Q40,26 32,30 Q24,26 22,18 Z M20,52 Q24,42 32,40 Q40,42 44,52 Z', ic.v(AMBER), None))


def e_dice(ic):
    pip = lambda x, y: circle(x, y, 3.2, DARK, None)
    return rect(8, 8, 48, 48, 9, ic.v(WHITE, .3, .2)) + pip(20, 20) + pip(44, 20) + pip(32, 32) + pip(20, 44) + pip(44, 44)


def e_layers(ic):
    out = ''
    for i, c in enumerate((BLUE, GREEN, AMBER)):
        y = 34 - i * 12
        out += path('M32,%s L60,%s L32,%s L4,%s Z' % (y, y + 12, y + 24, y + 12), ic.v(c))
    return out


def e_film_clapper(ic):
    return (rect(6, 24, 52, 34, 3, ic.v(DARK, .3, .2)) +
            g(rect(6, 12, 52, 10, 2, WHITE) +
              ''.join(path('M%s,12 L%s,12 L%s,22 L%s,22 Z' % (x, x + 7, x + 3, x - 4), DARK, None) for x in (12, 26, 40)),
              'rotate(-12 6 22)') + rect(6, 24, 52, 8, 0, WHITE, OL, SW) +
            ''.join(path('M%s,24 L%s,24 L%s,32 L%s,32 Z' % (x, x + 7, x + 3, x - 4), DARK, None) for x in (16, 30, 44)))


def e_vm(ic):
    return (place(rect(4, 4, 44, 30, 3, ic.v('#3a3d4c', .3, .3)) + rect(8, 8, 36, 22, 1, ic.v(GREEN, .2, .2), OL, 1), 14, 2, .9) +
            place(e_monitor(ic), 0, 16, .72))


def e_slides(ic):
    return (rect(4, 6, 56, 40, 3, ic.v(WHITE, .3, .1)) + ostroke('M32,46 V58 M22,58 L32,50 L42,58', SILVER, 3) +
            path('M14,38 V26 H22 V38 M26,38 V16 H34 V38 M38,38 V22 H46 V38', ic.v(ORANGE), OL, 1.2) +
            rect(2, 4, 60, 4, 1.5, ic.v(SILVER), OL, 1))


def e_sheet(ic):
    cells = ''.join(rect(8 + c * 12, 14 + r * 9, 12, 9, 0, '#ffffff' if (r + c) % 2 else '#e6f4e0', '#7a9a70', .8)
                    for r in range(5) for c in range(4))
    return rect(4, 6, 56, 52, 3, ic.v(GREEN, .3, .3)) + cells


def e_sigma(ic):
    return text(32, 52, '&#931;', 50, ic.v(BLUE), 'bold', stroke=OL, sw=2)


def e_draw(ic):
    return (rect(6, 22, 26, 26, 2, ic.v(YELLOW)) + circle(40, 22, 16, ic.ball(BLUE)) +
            path('M30,60 L44,34 L58,60 Z', ic.v(RED)))


def e_writer_doc(ic):
    return (e_lines(ic))


def e_fsuae(ic):
    return e_amiga(ic)


def e_monitor_graph(ic):
    graph = (rect(9, 11, 46, 33, 2, ic.lg([(0, '#0e2a18'), (1, '#062010')]), OL, 1.2) +
             path('M10,36 L18,30 L24,34 L30,20 L36,28 L42,16 L54,24', 'none', '#5cff7a', 2.5) +
             path('M10,40 L20,38 L28,40 L38,36 L54,38', 'none', '#ffd84a', 1.8))
    return e_monitor(ic) + graph


def e_bars(ic):
    return ''.join(rect(6 + i * 13, 56 - h, 10, h, 2, ic.v(c)) for i, (h, c) in enumerate(((20, GREEN), (32, YELLOW), (44, ORANGE), (52, RED))))


def e_pie(ic):
    return (circle(32, 32, 26, ic.ball(BLUE)) + path('M32,32 V6 A26,26 0 0,1 57,40 Z', ic.ball(AMBER)) +
            path('M32,32 L57,40 A26,26 0 0,1 40,57 Z', ic.ball(GREEN)))


def e_redshift(ic):
    return place(e_sun(ic), 0, 0, .7) + place(e_moon(ic), 24, 24, .6)


def e_wallpaper(ic):
    return e_picture(ic)


def e_cursor(ic):
    return path('M14,4 V50 L25,40 L33,58 L41,54 L33,37 H48 Z', ic.v(WHITE, .3, .15)) + gloss(ic, 'M16,9 V30 L30,24 Z', .2)


def e_grid(ic):
    return ''.join(rect(6 + c * 18, 6 + r * 18, 15, 15, 3, ic.v(col)) for r, row in enumerate(
        ((RED, AMBER, YELLOW), (GREEN, TEAL, BLUE), (PURPLE, MAGENTA, PINK))) for c, col in enumerate(row))


def e_flag(ic):
    return (ostroke('M10,6 V60', SILVER, 4) +
            path('M12,8 Q24,2 34,8 Q44,14 56,8 V34 Q44,40 34,34 Q24,28 12,34 Z', ic.v(RED)) +
            gloss(ic, 'M14,10 Q24,5 34,11 Q44,16 54,11 V18 Q32,22 14,18 Z', .4))


def e_accessibility(ic):
    return e_badge(ic, BLUE, circle(32, 14, 4.5, WHITE, None) +
                   ostroke('M16,22 L32,25 L48,22 M32,25 V37 L24,50 M32,37 L40,50', WHITE, 4.5, 4.5))


def e_location(ic):
    return path('M32,60 Q12,36 12,24 A20,20 0 0,1 52,24 Q52,36 32,60 Z', ic.v(RED)) + circle(32, 24, 8, WHITE)


def e_bookmark(ic, c=RED):
    return path('M14,4 H50 V60 L32,46 L14,60 Z', ic.v(c)) + gloss_rect(ic, 16, 6, 32, 14, 2, .5)


def e_folder_icon(ic, c=DRAWER):
    from objects import folder
    return folder(ic, c)
