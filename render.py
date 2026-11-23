#!/usr/bin/env python3
"""Render the front page for news-image-20261122 (Sunday 22 November 2026).

Dev-time renderer (PIL). Writes entry.png (1024x1024, <=1 MiB) next to this file.
The shipped entrypoint main.py is stdlib-only and copies entry.png byte-for-byte.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (176, 30, 30)
BLUE = (31, 78, 121)
GREY = (118, 116, 108)
WHITE = (255, 255, 255)
SKY = (168, 205, 232)
SEA = (58, 110, 160)
FIRE = (232, 90, 20)
FLAME = (240, 180, 30)
GREEN = (46, 125, 60)
DARK = (40, 40, 44)

F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_lines(draw, x, y, text, fnt, max_w, fill=INK, leading=None, align="left"):
    """Draw wrapped text; return y just below the last line."""
    if leading is None:
        leading = fnt.size + 3
    for line in wrap(draw, text, fnt, max_w):
        if align == "center":
            lx = x + (max_w - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, text, fnt=None, fg=WHITE, bg=INK, pad=5, h=None):
    """Small black label; returns its width."""
    fnt = fnt or font(F_SANS_B, 10)
    tw = draw.textlength(text, font=fnt)
    hh = h or (fnt.size + 2 * pad)
    draw.rounded_rectangle([x, y, x + tw + 2 * pad, y + hh], radius=3, fill=bg)
    draw.text((x + pad, y + pad - 1), text, font=fnt, fill=fg)
    return tw + 2 * pad


def kicker(draw, x, y, text, fnt=None, fill=RED):
    fnt = fnt or font(F_SANS_B, 10)
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + fnt.size + 2


def rule(draw, x, y, w, fill=INK, width=1):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


def panel(draw, x, y, w, h, fill=WHITE, outline=(200, 196, 184)):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=1)


def flame(draw, x, y, w, h):
    """A stylised flame: orange body, yellow core."""
    draw.polygon([
        (x + w * 0.5, y), (x + w * 0.85, y + h * 0.45),
        (x + w, y + h * 0.75), (x + w * 0.7, y + h),
        (x + w * 0.3, y + h), (x, y + h * 0.75),
        (x + w * 0.15, y + h * 0.45),
    ], fill=FIRE)
    draw.polygon([
        (x + w * 0.5, y + h * 0.35), (x + w * 0.72, y + h * 0.6),
        (x + w * 0.62, y + h * 0.9), (x + w * 0.38, y + h * 0.9),
        (x + w * 0.28, y + h * 0.6),
    ], fill=FLAME)


def smoke(draw, x, y, r=9, n=4, fill=(150, 148, 140)):
    for i in range(n):
        cx = x + i * r * 0.7 - (n - 1) * r * 0.35
        cy = y - i * r * 0.8
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def globe(draw, cx, cy, r):
    """Blue globe with green land blobs and meridian lines."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 170, 215),
                 outline=INK, width=2)
    for k in (-0.55, 0.0, 0.55):
        rx = abs(r * 0.85 * math.cos(k * 1.2)) + 3
        draw.arc([cx - rx, cy - r, cx + rx, cy + r], 0, 360,
                 fill=(90, 140, 190), width=1)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(90, 140, 190), width=1)
    draw.ellipse([cx - r * 0.7, cy - r * 0.75, cx - r * 0.1, cy - r * 0.25],
                 fill=GREEN)
    draw.ellipse([cx + r * 0.05, cy + r * 0.1, cx + r * 0.7, cy + r * 0.6],
                 fill=GREEN)
    draw.ellipse([cx - r * 0.2, cy + r * 0.35, cx + r * 0.25, cy + r * 0.75],
                 fill=GREEN)


def thermometer(draw, x, y, w, h):
    """Classic thermometer: bulb + tube, red mercury at ~3/4."""
    tube_w = max(6, w // 3)
    draw.rectangle([x + (w - tube_w) // 2, y, x + (w + tube_w) // 2,
                    y + h - w // 2], fill=WHITE, outline=INK, width=2)
    draw.ellipse([x, y + h - w, x + w, y + h], fill=WHITE, outline=INK, width=2)
    mh = int((h - w // 2) * 0.72)
    draw.rectangle([x + (w - tube_w) // 2 + 2, y + h - w // 2 - mh,
                    x + (w + tube_w) // 2 - 2, y + h - w // 2], fill=RED)
    draw.ellipse([x + 3, y + h - w + 3, x + w - 3, y + h - 3], fill=RED)
    for i in range(4):
        ty = y + 8 + i * (h - w // 2 - 16) // 3
        draw.line([(x + (w + tube_w) // 2, ty),
                   (x + (w + tube_w) // 2 + 6, ty)], fill=INK, width=2)


def clock(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK,
                 width=2)
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x1 = cx + (r - 3) * math.sin(a)
        y1 = cy - (r - 3) * math.cos(a)
        x2 = cx + (r - 6) * math.sin(a)
        y2 = cy - (r - 6) * math.cos(a)
        draw.line([(x1, y1), (x2, y2)], fill=INK, width=2)
    draw.line([(cx, cy), (cx, cy - r * 0.55)], fill=INK, width=2)
    draw.line([(cx, cy), (cx + r * 0.45, cy + r * 0.2)], fill=INK, width=2)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)


def stat_strip(draw):
    """Six big numbers from our own stories, under the masthead."""
    stats = [
        ("186", "drones fired at Ukraine"),
        ("8", "dead in Kyiv flat hit"),
        ("36", "missing in Cikande fire"),
        ("720/9", "India's record Test total"),
        ("24", "dead as Lagos boat capsizes"),
        ("11", "dead in Sinaloa cartel raid"),
    ]
    y0 = 106
    rule(draw, 14, y0, W - 28, fill=INK, width=1)
    cw = (W - 28) / 6
    f_num = font(F_SANS_B, 18)
    f_lab = font(F_SANS, 8)
    for i, (num, lab) in enumerate(stats):
        cx = 14 + cw * i + cw / 2
        tw = draw.textlength(num, font=f_num)
        draw.text((cx - tw / 2, y0 + 2), num, font=f_num, fill=RED)
        ly = y0 + 18
        for line in wrap(draw, lab, f_lab, cw - 16)[:2]:
            tw = draw.textlength(line, font=f_lab)
            draw.text((cx - tw / 2, ly), line, font=f_lab, fill=GREY)
            ly += 10
    rule(draw, 14, 138, W - 28, fill=INK, width=1)


REGION_COUNTS = [
    ("EUROPE", 8, (31, 78, 121)),
    ("MIDDLE EAST", 6, (176, 30, 30)),
    ("ASIA-PACIFIC", 10, (200, 120, 30)),
    ("AMERICAS", 5, (46, 125, 60)),
    ("AFRICA", 3, (110, 60, 140)),
    ("OCEANIA", 1, (90, 140, 160)),
    ("WORLD", 2, (40, 40, 44)),
]


def region_bar(draw):
    """Colour-coded region counts, one segment per region."""
    y0, h = 144, 16
    cw = (W - 28) / len(REGION_COUNTS)
    f_seg = font(F_SANS_B, 10)
    for i, (name, n, col) in enumerate(REGION_COUNTS):
        x = 14 + cw * i
        draw.rectangle([x, y0, x + cw - 1, y0 + h], fill=col)
        label = f"{name} {n}"
        tw = draw.textlength(label, font=f_seg)
        draw.text((x + (cw - tw) / 2, y0 + 3), label, font=f_seg, fill=WHITE)


def masthead(draw):
    """Small nameplate bar + giant date masthead + sub-headline + stat strip + region bar."""
    rule(draw, 14, 6, W - 28, fill=INK, width=2)
    f_top = font(F_SANS_B, 11)
    draw.text((14, 10), "THE WORLD TODAY", font=f_top, fill=INK)
    right = "No. 326  ·  35 STORIES  ·  7 REGIONS  ·  ALL FROM THIS ONE DAY"
    tw = draw.textlength(right, font=f_top)
    draw.text((W - 14 - tw, 10), right, font=f_top, fill=INK)
    f_date = font(F_SERIF_B, 52)
    date = "Sunday 22 November 2026"
    tw = draw.textlength(date, font=f_date)
    draw.text(((W - tw) / 2, 22), date, font=f_date, fill=INK)
    f_sub = font(F_SERIF_B, 16)
    sub = ("COP31 collapses in Antalya  ·  Kyiv flat hit  ·  "
           "Hormuz tankers ablaze")
    tw = draw.textlength(sub, font=f_sub)
    draw.text(((W - tw) / 2, 80), sub, font=f_sub, fill=INK)
    rule(draw, 14, 102, W - 28, fill=INK, width=1)
    stat_strip(draw)
    region_bar(draw)


# ---------------------------------------------------------------- features
def scene_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(210, 196, 170))
    globe(draw, x + 78, y + 62, 46)
    thermometer(draw, x + w - 66, y + 26, 34, 96)
    clock(draw, x + w - 34, y + 150, 15)
    # three delegates at a table
    for i, cx in enumerate((x + 150, x + 205, x + 260)):
        draw.ellipse([cx - 9, y + h - 78, cx + 9, y + h - 60], fill=(222, 190, 160))
        draw.rectangle([cx - 13, y + h - 62, cx + 13, y + h - 34],
                       fill=(52, 52, 58) if i != 1 else (90, 30, 30))
    draw.rectangle([x + 120, y + h - 36, x + w - 20, y + h - 30], fill=(120, 90, 60))
    draw.text((x + 12, y + 8), "ANTALYA", font=font(F_SANS_B, 11), fill=BLUE)


def scene_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(196, 198, 200))
    # damaged apartment block, broken top
    bx, by, bw, bh = x + 70, y + 26, 170, h - 26
    draw.polygon([(bx, by + 26), (bx + 40, by), (bx + 90, by + 18),
                  (bx + 130, by + 4), (bx + bw, by + 22), (bx + bw, by + bh),
                  (bx, by + bh)], fill=(150, 142, 128))
    for r in range(3):
        for c in range(5):
            wx = bx + 12 + c * 32
            wy = by + 34 + r * 28
            lit = (r + c) % 3 == 0
            draw.rectangle([wx, wy, wx + 20, wy + 20],
                           fill=(240, 200, 90) if lit else (60, 58, 52))
    # rubble + smoke + rescue ladder
    draw.polygon([(bx - 20, by + bh), (bx + 60, by + bh - 26),
                  (bx + 150, by + bh), (bx + 220, by + bh - 14),
                  (bx + bw + 10, by + bh)], fill=(110, 104, 92))
    smoke(draw, bx + 60, by + 8, r=10, n=4)
    smoke(draw, bx + 150, by + 16, r=8, n=3)
    draw.line([(x + w - 60, y + h), (x + w - 30, y + 60)], fill=RED, width=5)
    draw.line([(x + w - 60, y + h), (x + w - 90, y + 60)], fill=RED, width=5)


def scene_hormuz(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h * 0.55], fill=SKY)
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=SEA)
    for i in range(3):
        wy = y + h * 0.62 + i * 18
        draw.arc([x - 20, wy - 6, x + w + 20, wy + 6], 0, 180,
                 fill=(200, 225, 240), width=2)
    # tanker hull + bridge, on fire
    draw.rectangle([x + 40, y + h - 62, x + w - 40, y + h - 34], fill=(70, 40, 36))
    draw.rectangle([x + w - 110, y + h - 96, x + w - 60, y + h - 62],
                   fill=(200, 200, 200), outline=INK, width=1)
    draw.rectangle([x + 60, y + h - 92, x + 130, y + h - 62], fill=(140, 60, 40))
    flame(draw, x + 150, y + h - 118, 60, 56)
    flame(draw, x + 220, y + h - 104, 44, 42)
    smoke(draw, x + 180, y + h - 122, r=10, n=4, fill=(120, 118, 112))
    # missile trail
    draw.line([(x + 20, y + 20), (x + 90, y + 70)], fill=(200, 200, 200), width=3)
    draw.ellipse([x + 82, y + 62, x + 98, y + 78], fill=FIRE)


FEATURES = [
    ("1  ANTALYA  ·  CLIMATE", "CLIMATE TALKS COLLAPSE",
     "COP31 ends with no deal as the EU and allies reject a draft that never names fossil fuels — the longest summit ever.",
     "No deal  ·  AFP", scene_cop),
    ("2  KYIV  ·  WAR", "KYIV FLAT HIT, 8 DEAD",
     "Rescuers dig through a wrecked apartment block after an overnight drone barrage; 186 Shahed drones reported.",
     "Ongoing  ·  AP", scene_kyiv),
    ("3  HORMUZ  ·  ENERGY", "TANKERS ABLAZE IN HORMUZ",
     "Iran strikes three tankers and shows off missile launchers as a US blockade standoff chokes the strait.",
     "Reported  ·  Reuters", scene_hormuz),
]


def draw_features(draw):
    f_kick = font(F_SANS_B, 10)
    f_head = font(F_SERIF_B, 20)
    f_deck = font(F_SANS, 11)
    for i, (kick, head, deck, src, scene) in enumerate(FEATURES):
        x = 14 + i * 334
        w = 326
        y0 = 164
        panel(draw, x, y0, w, 255, fill=WHITE)
        scene(draw, x + 6, y0 + 6, w - 12, 148)
        y = y0 + 160
        y = kicker(draw, x + 10, y, kick, fnt=f_kick)
        y = text_lines(draw, x + 10, y + 2, head, f_head, w - 20, leading=22)
        y = text_lines(draw, x + 10, y + 3, deck, f_deck, w - 20, leading=14)
        chip(draw, x + 10, y0 + 255 - 24, src, fnt=font(F_SANS_B, 10))


# ---------------------------------------------------------------- tiles
def tile_frame(draw, x, y, w, h, sky=SKY):
    draw.rectangle([x, y, x + w, y + h], fill=sky)


def t_factory(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(210, 205, 190))
    draw.rectangle([x + 20, y + 44, x + w - 20, y + h], fill=(120, 112, 100))
    for i in range(3):
        px = x + 24 + i * 48
        draw.polygon([(px, y + 44), (px + 24, y + 22), (px + 48, y + 44)],
                     fill=(90, 84, 76))
    draw.rectangle([x + w - 34, y + 8, x + w - 22, y + 44], fill=(90, 84, 76))
    smoke(draw, x + w - 28, y + 4, r=7, n=3)
    flame(draw, x + 40, y + h - 34, 26, 30)
    flame(draw, x + 110, y + h - 28, 20, 24)
    draw.rectangle([x + 30, y + 56, x + 46, y + 70], fill=FLAME)
    draw.rectangle([x + 100, y + 56, x + 116, y + 70], fill=FLAME)


def t_heli(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(232, 200, 150))
    draw.polygon([(x, y + h), (x + 50, y + 30), (x + 120, y + 55),
                  (x + w, y + 40), (x + w, y + h)], fill=(190, 150, 100))
    draw.ellipse([x + 60, y + 18, x + 130, y + 52], fill=(70, 90, 70))
    draw.rectangle([x + 128, y + 30, x + 178, y + 40], fill=(70, 90, 70))
    draw.line([(x + 55, y + 14), (x + 175, y + 14)], fill=INK, width=3)
    draw.line([(x + 95, y + 18), (x + 95, y + 52)], fill=INK, width=3)
    draw.rectangle([x + 62, y + 52, x + 74, y + 62], fill=INK)
    draw.rectangle([x + 116, y + 52, x + 128, y + 62], fill=INK)
    draw.rectangle([x + 172, y + 24, x + 184, y + 46], fill=RED)


def t_scales(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(225, 222, 210))
    for cx in (x + 30, x + w - 30):
        draw.rectangle([cx - 8, y + 30, cx + 8, y + h - 12], fill=(200, 190, 160))
    draw.rectangle([x + 14, y + 18, x + w - 14, y + 30], fill=(180, 168, 138))
    cx, cy = x + w // 2, y + 40
    draw.line([(cx, cy), (cx, cy + 26)], fill=INK, width=3)
    draw.line([(cx - 30, cy + 4), (cx + 30, cy + 4)], fill=INK, width=3)
    for sx in (cx - 30, cx + 30):
        draw.line([(sx, cy + 4), (sx, cy + 20)], fill=INK, width=2)
        draw.arc([sx - 12, cy + 14, sx + 12, cy + 34], 0, 180, fill=INK, width=2)
    draw.polygon([(cx - 5, cy - 6), (cx + 5, cy - 6), (cx, cy - 14)], fill=INK)


def t_car(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(200, 200, 200))
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 120, 120))
    draw.rectangle([x + 30, y + 44, x + w - 30, y + 62], fill=(150, 30, 30))
    draw.polygon([(x + 55, y + 44), (x + 70, y + 28), (x + 130, y + 28),
                  (x + 145, y + 44)], fill=(150, 30, 30))
    draw.rectangle([x + 74, y + 32, x + 126, y + 44], fill=(180, 210, 230))
    for wx in (x + 48, x + w - 66):
        draw.ellipse([wx, y + 58, wx + 18, y + 76], fill=INK)
        draw.ellipse([wx + 5, y + 63, wx + 13, y + 71], fill=(150, 150, 150))
    flame(draw, x + 80, y + 6, 40, 34)
    smoke(draw, x + 100, y + 2, r=7, n=3)


def t_chip(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(24, 32, 48))
    cx, cy = x + w // 2, y + h // 2
    for i in range(4):
        tx = x + 14 + i * 40
        draw.line([(tx, y + 8), (tx, cy - 22)], fill=(90, 160, 220), width=2)
        draw.line([(tx, cy + 22), (tx, y + h - 8)], fill=(90, 160, 220), width=2)
    draw.rectangle([cx - 30, cy - 22, cx + 30, cy + 22], fill=(40, 60, 90),
                   outline=(120, 200, 240), width=2)
    draw.rectangle([cx - 18, cy - 12, cx + 18, cy + 12], fill=(120, 200, 240))
    draw.text((cx - 7, cy - 8), "AI", font=font(F_SANS_B, 13), fill=(24, 32, 48))


def t_cricket(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(120, 180, 110))
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(90, 140, 80))
    draw.rectangle([x + w // 2 - 14, y + 12, x + w // 2 + 14, y + h - 26],
                   fill=(215, 195, 150))
    draw.rectangle([x + 40, y + 16, x + 66, y + 58], fill=(200, 170, 110),
                   outline=INK, width=2)
    draw.rectangle([x + 48, y + 58, x + 58, y + 72], fill=(160, 120, 70))
    draw.ellipse([x + 130, y + 60, x + 144, y + 74], fill=RED)
    for sx in (x + 150, x + 156, x + 162):
        draw.line([(sx, y + 52), (sx, y + 76)], fill=(240, 220, 160), width=3)
    draw.line([(x + 148, y + 52), (x + 164, y + 52)], fill=(240, 220, 160),
              width=3)


def t_tennis(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(90, 140, 200))
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(70, 130, 90))
    draw.ellipse([x + 40, y + 14, x + 92, y + 62], fill=(230, 200, 90),
                 outline=INK, width=2)
    draw.line([(x + 40, y + 38), (x + 92, y + 38)], fill=INK, width=1)
    draw.line([(x + 66, y + 14), (x + 66, y + 62)], fill=INK, width=1)
    draw.line([(x + 84, y + 56), (x + 112, y + 76)], fill=(160, 110, 60), width=4)
    draw.ellipse([x + 130, y + 52, x + 148, y + 70], fill=(200, 230, 60),
                 outline=INK, width=1)
    draw.polygon([(x + 158, y + 30), (x + 182, y + 30), (x + 176, y + 52),
                  (x + 164, y + 52)], fill=(220, 190, 80), outline=INK, width=1)
    draw.rectangle([x + 160, y + 52, x + 180, y + 56], fill=(220, 190, 80))


def t_lotus(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(250, 240, 220))
    draw.rectangle([x, y, x + w, y + 16], fill=(255, 153, 51))
    cx, cy = x + w // 2, y + h // 2 + 8
    for dx, ang in ((-34, -40), (-18, -20), (0, 0), (18, 20), (34, 40)):
        draw.ellipse([cx + dx - 13, cy - 30, cx + dx + 13, cy + 8],
                     fill=(230, 120, 160), outline=(180, 60, 100), width=1)
    draw.ellipse([cx - 10, cy - 34, cx + 10, cy + 6], fill=(240, 90, 140),
                 outline=(180, 60, 100), width=1)
    draw.arc([cx - 40, cy - 6, cx + 40, cy + 26], 0, 180, fill=GREEN, width=4)


def t_ship(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(170, 200, 225))
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=SEA)
    draw.rectangle([x + 30, y + h - 52, x + w - 30, y + h - 30], fill=(60, 60, 66))
    draw.rectangle([x + w - 80, y + h - 72, x + w - 44, y + h - 52],
                   fill=(200, 200, 200))
    cx, cy = x + 70, y + 34
    for a in range(0, 360, 30):
        r1, r2 = 10, 30
        x1 = cx + r1 * math.cos(math.radians(a))
        y1 = cy + r1 * math.sin(math.radians(a))
        x2 = cx + r2 * math.cos(math.radians(a))
        y2 = cy + r2 * math.sin(math.radians(a))
        draw.line([(x1, y1), (x2, y2)], fill=FIRE, width=4)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=FLAME,
                 outline=FIRE, width=2)
    smoke(draw, cx + 20, cy - 18, r=7, n=3)


def t_boat(draw, x, y, w, h):
    tile_frame(draw, x, y, w, h, sky=(170, 205, 230))
    for i in range(3):
        wy = y + h - 34 + i * 12
        draw.arc([x - 10, wy - 8, x + w + 10, wy + 8], 0, 180, fill=SEA, width=3)
    draw.polygon([(x + 40, y + 44), (x + w - 40, y + 44), (x + w - 60, y + 66),
                  (x + 60, y + 66)], fill=(140, 90, 50))
    draw.rectangle([x + 80, y + 38, x + 110, y + 44], fill=(140, 90, 50))
    draw.ellipse([x + 130, y + 58, x + 152, y + 80], fill=RED, outline=WHITE,
                 width=2)
    draw.ellipse([x + 138, y + 66, x + 144, y + 72], fill=WHITE)


TILES = [
    ("4  CIKANDE  ·  DISASTER", "FACTORY FIRE: 36 MISSING",
     "Blaze rips a candy plant in Banten; three dead, dozens unaccounted for.",
     "Official  ·  AP", t_factory),
    ("5  SINALOA  ·  CRIME", "'EL CHAPO ISIDRO' SEIZED",
     "Mexican troops capture a cartel leader in a raid that leaves 11 dead.",
     "Official  ·  Reuters", t_heli),
    ("6  THE HAGUE  ·  LAW", "MYANMAR GUILTY",
     "World court: Myanmar committed genocide against the Rohingya.",
     "Confirmed  ·  AFP", t_scales),
    ("7  WEST BANK  ·  CONFLICT", "SETTLERS TORCH VILLAGES",
     "Raiders burn 12 vehicles and homes overnight; Israel's opposition calls it terror.",
     "Reported  ·  Guardian", t_car),
    ("8  WASHINGTON  ·  TECH", "NVIDIA IN CHIP PROBE",
     "US presses Nvidia over AI chips sold to China as curbs tighten.",
     "Reported  ·  AP", t_chip),
    ("9  WELLINGTON  ·  SPORT", "INDIA 720/9, LEAD BY 352",
     "India pile up a mountain of runs in the first Test against New Zealand.",
     "Official  ·  AFP", t_cricket),
    ("10  LONDON  ·  SPORT", "ALCARAZ TAKES ATP FINALS",
     "The Spaniard beats Zverev for his first season-ending title.",
     "Confirmed  ·  BBC", t_tennis),
    ("11  NEW DELHI  ·  POLITICS", "CHAHAL JOINS THE BJP",
     "The cricketer signs up with India's ruling party and takes a party post.",
     "Reported  ·  ANI", t_lotus),
    ("12  BENGHAZI  ·  WAR", "BLAST HITS RUSSIAN SHIP",
     "Libya blames a suspected drone strike for an explosion aboard a docked vessel.",
     "Reported  ·  Reuters", t_ship),
    ("13  LAGOS  ·  DISASTER", "BOAT CAPSIZES: 24 DEAD",
     "A vessel carrying mourners to a funeral overturns in Nigeria.",
     "Official  ·  AFP", t_boat),
]


def draw_tiles(draw):
    f_kick = font(F_SANS_B, 9)
    f_head = font(F_SANS_B, 12)
    f_deck = font(F_SANS, 10)
    for i, (kick, head, deck, src, scene) in enumerate(TILES):
        col, row = i % 5, i // 5
        x = 14 + col * 200
        y = 425 + row * 164
        w = 194
        panel(draw, x, y, w, 162, fill=WHITE)
        scene(draw, x + 5, y + 5, w - 10, 76)
        chip(draw, x + 7, y + 83, src, fnt=font(F_SANS_B, 9))
        yy = y + 104
        yy = kicker(draw, x + 7, yy, kick, fnt=f_kick)
        yy = text_lines(draw, x + 7, yy + 1, head, f_head, w - 14, leading=13)
        text_lines(draw, x + 7, yy + 1, deck, f_deck, w - 14, leading=11)


# ---------------------------------------------------------------- map + checks
MAP_PINS = [
    (265, 55, "1"), (250, 30, "2"), (300, 90, "3"), (360, 155, "4"),
    (60, 80, "5"), (210, 32, "6"), (275, 78, "7"), (28, 68, "8"),
    (398, 200, "9"), (182, 22, "10"), (325, 85, "11"), (240, 88, "12"),
    (212, 118, "13"),
]


def draw_map(draw):
    x0, y0 = 14, 759
    panel(draw, x0, y0, 416, 250, fill=WHITE)
    draw.text((x0 + 10, y0 + 8), "THE WORLD IN ONE DAY",
              font=font(F_SANS_B, 12), fill=INK)
    draw.text((x0 + 10, y0 + 24), "13 stories mapped — red pins",
              font=font(F_SANS, 10), fill=GREY)
    mx, my = x0 + 8, y0 + 42
    mw, mh = 400, 180
    sy = mh / 200.0
    draw.rectangle([mx, my, mx + mw, my + mh], fill=(190, 215, 235))
    land = (222, 210, 170)
    na = [(20, 25), (90, 15), (140, 30), (150, 60), (120, 75), (95, 95),
          (70, 85), (40, 70), (15, 50)]
    sa = [(105, 110), (150, 105), (175, 125), (170, 165), (150, 200),
          (130, 185), (110, 150)]
    eu = [(195, 20), (245, 15), (260, 35), (245, 55), (215, 60), (195, 45)]
    af = [(195, 70), (255, 65), (275, 95), (260, 140), (235, 165),
          (210, 130), (195, 100)]
    as_ = [(265, 15), (400, 10), (410, 60), (380, 95), (340, 110),
           (300, 100), (275, 70), (260, 40)]
    au = [(330, 175), (395, 170), (400, 195), (360, 210), (330, 200)]
    for poly in (na, sa, eu, af, as_, au):
        draw.polygon([(mx + px, my + py * sy) for px, py in poly], fill=land,
                     outline=(160, 148, 120))
    draw.ellipse([mx + 186, my + 26 * sy, mx + 194, my + 34 * sy], fill=land,
                 outline=(160, 148, 120))
    f_pin = font(F_SANS_B, 9)
    for px, py, num in MAP_PINS:
        cx, cy = mx + px, my + py * sy
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED, outline=WHITE,
                     width=2)
        tw = draw.textlength(num, font=f_pin)
        draw.text((cx - tw / 2, cy - 7), num, font=f_pin, fill=WHITE)
    draw.text((x0 + 10, y0 + 228),
              "1 Antalya · 2 Kyiv · 3 Hormuz · 4 Cikande · 5 Sinaloa · 6 Hague · 7 W.Bank",
              font=font(F_SANS, 8), fill=GREY)
    draw.text((x0 + 10, y0 + 238),
              "8 California · 9 Wellington · 10 London · 11 Delhi · 12 Benghazi · 13 Lagos",
              font=font(F_SANS, 8), fill=GREY)


DATE_CHECK_INTRO = ("Wires read to 07:00 UTC, Sunday 22 November 2026. Every story "
                      "here happened, or was first reported, on 22 November in at "
                      "least one time zone.")
DATE_CHECK_LEFT_OUT = ("Peru quake (Fri 20 Nov) · Russia's 400-drone barrage "
                       "(Thu 19–Fri 20 Nov) · BepiColombo reaches Mercury "
                       "(Sat 21 Nov) · Gaza aid-van strike (Sat 21 Nov) · "
                       "Kryvyi Rih missile strike (Sat 21 Nov) · Sparta II "
                       "ship hit (Sat 21 Nov).")
DATE_CHECK_COUNT = "Tonight's barrage was 186 drones, not 400."
DATE_CHECK_NOT_YET = ("Thai–China–Myanmar river talks (24–26 Nov) · Spain's "
                      "election (Sun 29 Nov).")


def draw_datecheck(draw):
    x0, y0 = 438, 759
    draw.rectangle([x0, y0, x0 + 202, y0 + 250], fill=WHITE, outline=RED,
                   width=2)
    draw.text((x0 + 10, y0 + 8), "DATE CHECK", font=font(F_SANS_B, 13),
              fill=RED)
    draw.text((x0 + 10, y0 + 26), "READ THIS FIRST",
              font=font(F_SANS_B, 10), fill=INK)
    rule(draw, x0 + 10, y0 + 44, 182, fill=RED, width=2)
    f_body = font(F_SANS, 9)
    f_head = font(F_SANS_B, 9)
    y = y0 + 50
    y = text_lines(draw, x0 + 10, y, DATE_CHECK_INTRO, f_body, 182,
                   leading=12)
    y += 6
    draw.text((x0 + 10, y), "LEFT OUT ON PURPOSE —", font=f_head, fill=RED)
    y += 12
    y = text_lines(draw, x0 + 10, y, DATE_CHECK_LEFT_OUT, f_body, 182,
                   leading=12)
    y += 6
    y = text_lines(draw, x0 + 10, y, DATE_CHECK_COUNT, f_head, 182,
                   leading=12)
    y += 6
    draw.text((x0 + 10, y), "NOT YET:", font=f_head, fill=RED)
    y += 12
    text_lines(draw, x0 + 10, y, DATE_CHECK_NOT_YET, f_body, 182,
               leading=12)


ALSO = [
    "14  Nepal PM in Delhi for Modi talks",
    "15  India, China in fresh border talks",
    "16  BJP MP Wadkute dies at 72",
    "17  Thitikul's third straight LPGA title",
    "18  Liverpool sink 10-man Man Utd",
    "19  FIFA to name UK 2035 WWC host",
    "20  UK, EU strike trade & travel deals",
    "21  Thai court cuts royal-case sentence",
    "22  Poland: plot to kill US rapper",
    "23  Bulgari jeweller Paolo dies at 89",
    "24  Mlambo-Ngcuka dies at 71",
    "25  US–China power gap narrows: Lowy",
    "26  China eases margin trading rules",
    "27  Hamas seeks emergency Gaza talks",
    "28  IDF names 'aid worker' militants",
    "29  Trump reposts 'TrumpCare' pitch",
    "30  Democrats flip N. Carolina seat",
    "31  US Army to blast Iowa chemicals",
    "32  Pugh swims war-hit Hormuz",
    "33  Iran unveils 'missile city'",
    "34  Taiwan warns Canada on China ties",
    "35  CXMT, YMTC gain on US chip curbs",
]


def draw_also(draw):
    x0, y0 = 648, 759
    panel(draw, x0, y0, 360, 250, fill=WHITE)
    draw.text((x0 + 10, y0 + 8), "ALSO TODAY", font=font(F_SANS_B, 13),
              fill=INK)
    rule(draw, x0 + 10, y0 + 28, 340, fill=RED, width=2)
    f_item = font(F_SANS, 10)
    y = y0 + 34
    for item in ALSO:
        draw.text((x0 + 10, y), item, font=f_item, fill=INK)
        y += 9
    draw.text((x0 + 10, y0 + 236),
              "35 stories · every one dated 22 Nov 2026",
              font=font(F_SANS_B, 9), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    draw_features(draw)
    draw_tiles(draw)
    draw_map(draw)
    draw_datecheck(draw)
    draw_also(draw)
    f_foot = font(F_SANS_B, 9)
    foot = ("HOW WE CHECKED — every story carries its source. Chips show status: "
            "REPORTED · OFFICIAL · CONFIRMED.  Sources: AFP · AP · Reuters · BBC · "
            "CNN · Le Monde · RFE/RL · Guardian · ANI")
    tw = draw.textlength(foot, font=f_foot)
    draw.text(((W - tw) / 2, 1012), foot, font=f_foot, fill=GREY)
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
