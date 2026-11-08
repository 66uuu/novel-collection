# -*- coding: utf-8 -*-
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
OUT = r"<DESKTOP>/咒术：我的符咒上班摸鱼\发布素材\poster.png"

NAVY_TOP = (30, 44, 96); NAVY_BOT = (9, 13, 33)
GOLD = (201, 161, 74); GOLD_D = (150, 116, 46); CREAM = (242, 232, 204)
CRIM = (122, 31, 43); JEW_B = (70, 100, 190); JEW_R = (170, 46, 56); SHADOW = (5, 8, 20)

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ---- background vertical gradient ----
base = Image.new("RGB", (W, H), NAVY_BOT); px = base.load()
for y in range(H):
    c = lerp(NAVY_TOP, NAVY_BOT, min(1.0, y / H))
    for x in range(W): px[x, y] = c
base = base.convert("RGBA"); draw = ImageDraw.Draw(base)

# ---- radial glow behind emblem ----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
cx, cy = 540, 740
for i in range(90):
    r = 460 - i * 5
    if r <= 0: break
    a = int(42 * (1 - i / 90) ** 1.3)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(GOLD[0], GOLD[1], GOLD[2], a))
base = Image.alpha_composite(base, glow); draw = ImageDraw.Draw(base)

# ---- fonts (all legible) ----
FONT_EN = ImageFont.truetype(r"C:\Windows\Fonts\CALISTB.TTF", 100)      # Castellar, roman serif, for English
FONT_CN = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 88)        # bold sans, for main Chinese title
FONT_CN_M = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 42)     # bold, for ribbon motto
FONT_CN_S = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 36)     # bold, for imprint

def fit_font(text, maxw, base_sz, path, step=2):
    sz = base_sz
    while sz > 12:
        f = ImageFont.truetype(path, sz)
        w = draw.textbbox((0, 0), text, font=f)[2]
        if w <= maxw: return f
        sz -= step
    return ImageFont.truetype(path, sz)

def spaced_shadow(text, font, y, fill, shadow, cx=540, sp=4):
    widths = [draw.textbbox((0, 0), ch, font=font)[2] for ch in text]
    total = sum(widths) + sp * (len(text) - 1); x = cx - total / 2
    for ch, w in zip(text, widths):
        for dx, dy in [(-2, 1), (2, 1), (-2, -1), (2, -1), (0, 2), (2, 0), (-2, 0)]:
            draw.text((x + dx, y + dy), ch, font=font, fill=shadow)
        draw.text((x, y), ch, font=font, fill=fill); x += w + sp

def center_shadow(text, font, y, fill, shadow, cx=540):
    b = draw.textbbox((0, 0), text, font=font); tw = b[2] - b[0]
    x = cx - tw / 2
    for dx, dy in [(-2, 1), (2, 1), (-2, -1), (2, -1)]:
        draw.text((x + dx, y + dy), text, font=font, fill=shadow)
    draw.text((x, y), text, font=font, fill=fill)

# ---- ornate double frame ----
draw.rectangle([28, 28, W - 28, H - 28], outline=GOLD, width=4)
draw.rectangle([44, 44, W - 44, H - 44], outline=GOLD_D, width=2)

# corner flourishes (fixed: bbox always min/max so mirrored corners don't crash)
def corner(ox, oy, sx, sy):
    x0, x1 = min(ox, ox + 150 * sx), max(ox, ox + 150 * sx)
    y0, y1 = min(oy, oy + 150 * sy), max(oy, oy + 150 * sy)
    draw.arc([x0, y0, x1, y1], 0, 90, fill=GOLD, width=3)
    ex, ey = ox + 120 * sx, oy + 120 * sy
    draw.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=GOLD)
    ax0, ax1 = min(ox + 20, ox + 110 * sx), max(ox + 20, ox + 110 * sx)
    ay0, ay1 = min(oy + 20, oy + 110 * sy), max(oy + 20, oy + 110 * sy)
    draw.arc([ax0, ay0, ax1, ay1], 0, 90, fill=GOLD_D, width=2)
corner(44, 44, 1, 1); corner(W - 44, 44, -1, 1)
corner(44, H - 44, 1, -1); corner(W - 44, H - 44, -1, -1)

# ---- crown ----
def crown(cx, ty):
    bw = 150; base_y = ty + 62
    draw.rectangle([cx - bw, base_y, cx + bw, base_y + 30], fill=GOLD, outline=GOLD_D, width=2)
    peaks = [(cx - 120, ty + 58), (cx - 60, ty), (cx, ty - 26), (cx + 60, ty), (cx + 120, ty + 58)]
    for i in range(4):
        draw.polygon([peaks[i], peaks[i + 1], ((peaks[i][0] + peaks[i + 1][0]) / 2, base_y)], fill=GOLD, outline=GOLD_D)
    for pxx, pyy in peaks:
        draw.ellipse([pxx - 9, pyy - 9, pxx + 9, pyy + 9], fill=JEW_R if pyy < ty + 10 else JEW_B)
crown(540, 150)

# ---- royal sun-medallion (emblem) ----
R = 232
draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=GOLD, width=12)
draw.ellipse([cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10], outline=GOLD_D, width=3)
for i in range(24):
    ang = math.radians(i * 15); r1 = R + 14; r2 = R + 54
    draw.line([cx + r1 * math.cos(ang), cy + r1 * math.sin(ang),
               cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)],
              fill=GOLD if i % 2 == 0 else GOLD_D, width=5)
draw.ellipse([cx - R + 60, cy - R + 60, cx + R - 60, cy + R - 60], outline=GOLD, width=6)
for i in range(12):
    ang = math.radians(-90 + i * 30); r = R - 30
    gx = cx + r * math.cos(ang); gy = cy + r * math.sin(ang)
    draw.ellipse([gx - 11, gy - 11, gx + 11, gy + 11], fill=GOLD, outline=GOLD_D, width=2)
draw.ellipse([cx - 78, cy - 78, cx + 78, cy + 78], fill=(14, 20, 48), outline=GOLD, width=4)
for i in range(8):
    ang = math.radians(i * 45); r1 = 14; r2 = 66 if i % 2 == 0 else 40
    draw.line([cx + r1 * math.cos(ang), cy + r1 * math.sin(ang),
               cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)], fill=GOLD, width=3)
draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=GOLD)

# ---- side flourishes (scrolling horns) ----
def flourish(ccx, ccy):
    bx = [ccx - 180, ccy - 180, ccx + 180, ccy + 180]
    draw.arc(bx, 200, 320, fill=GOLD, width=4)
    for k in range(7):
        a = math.radians(200 + 120 * k / 6)
        lx = ccx + 180 * math.cos(a); ly = ccy + 180 * math.sin(a)
        draw.ellipse([lx - 11, ly - 6, lx + 11, ly + 6], fill=GOLD_D)
flourish(cx - 300, cy); flourish(cx + 300, cy)

# ---- titles: English on two lines at a generous size, safe from overflow ----
spaced_shadow("THE TWELVE", FONT_EN, 1006, CREAM, SHADOW, sp=2)
spaced_shadow("TALISMANS", FONT_EN, 1094, CREAM, SHADOW, sp=2)
draw.line([cx - 150, 1170, cx + 150, 1170], fill=GOLD, width=2)
draw.ellipse([cx - 160, 1166, cx - 150, 1174], fill=GOLD)
draw.ellipse([cx + 150, 1166, cx + 160, 1174], fill=GOLD)
spaced_shadow("咒术：我的符咒", FONT_CN, 1230, CREAM, SHADOW, sp=8)
spaced_shadow("上 班 摸 鱼", FONT_CN, 1350, GOLD, SHADOW, sp=10)

# ---- ribbon motto (Chinese must use a CJK font) ----
ry, rh, rw = 1460, 84, 560
draw.polygon([(cx - rw / 2, ry), (cx - rw / 2 - 40, ry + rh / 2), (cx - rw / 2, ry + rh)], fill=CRIM)
draw.polygon([(cx + rw / 2, ry), (cx + rw / 2 + 40, ry + rh / 2), (cx + rw / 2, ry + rh)], fill=CRIM)
draw.rectangle([cx - rw / 2, ry, cx + rw / 2, ry + rh], fill=CRIM, outline=GOLD, width=2)
center_shadow("符 咒 十 二 · 镇 于 苍 冥", FONT_CN_M, ry + rh / 2 - 18, CREAM, SHADOW)

# ---- bottom imprint (Chinese uses CJK font) ----
center_shadow("长篇异能 · 番茄小说首发", FONT_CN_S, 1720, GOLD_D, SHADOW)
draw.ellipse([cx - 26, 1800, cx + 26, 1852], outline=GOLD, width=3)
draw.line([cx, 1812, cx, 1840], fill=GOLD, width=3)
draw.line([cx - 14, 1826, cx + 14, 1826], fill=GOLD, width=3)

# ---- vignette ----
draw.rectangle([0, 0, W, H], outline=(0, 0, 0, 120), width=120)

base = base.convert("RGB"); base.save(OUT); print("SAVED", OUT, base.size)
