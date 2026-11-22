#!/usr/bin/env python3
"""News21 v6 — 'Saturday 21 November 2026' front page, drawn fresh with PIL.

Direction: v1 RESTORED + sharpened. v1's editorial backbone (40 stories,
7 regions, Riyadh lead, exact verified numbers) with a punchy but honest
DATE CHECK and rank-1's top bar. All art is original vector work drawn
here; no external images are used. Deterministic: no randomness, no time.
"""
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 244, 230)
INK = (24, 24, 24)
RED = (178, 34, 34)
GREY = (110, 105, 95)
NAVY = (14, 27, 46)
GREEN = (46, 125, 60)
AMBER = (176, 122, 42)
SLATE = (110, 110, 110)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


def serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return font("DejaVuSerif.ttf", s)


def sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def sans(s):
    return font("DejaVuSans.ttf", s)


# ---------------------------------------------------------------- data
# Region assignment: every story 1..40 exactly once; counts match v1.
REGIONS = [
    ("EUROPE", 15, (163, 51, 51),
     [3, 4, 5, 9, 10, 12, 16, 17, 21, 25, 26, 27, 28, 29, 34]),
    ("AMERICAS", 10, (46, 95, 163),
     [8, 13, 14, 15, 18, 20, 30, 32, 35, 39]),
    ("ASIA-PACIFIC", 5, (46, 125, 107), [11, 22, 31, 36, 38]),
    ("MIDEAST", 4, (176, 122, 42), [1, 6, 24, 40]),
    ("SPACE & SCIENCE", 3, (107, 79, 163), [2, 7, 19]),
    ("AFRICA", 2, (122, 106, 58), [23, 37]),
    ("OCEANIA", 1, (74, 122, 58), [33]),
]

HEROES = [
    dict(n=1, place="RIYADH, SAUDI ARABIA", tag="CONFLICT", label="CLAIMED",
         head="Coalition downs three Houthi missiles over Riyadh",
         deck="Air defences destroy three ballistic missiles fired at the "
              "capital early on Saturday.",
         source="Reuters, AFP", scene="city_missiles"),
    dict(n=2, place="MERCURY", tag="SPACE", label="CONFIRMED",
         head="BepiColombo reaches Mercury after eight years",
         deck="The ESA-JAXA craft fires its thrusters at 18:24 UTC to enter "
              "Mercury orbit — a first.",
         source="ESA", scene="mercury"),
    dict(n=3, place="ANTALYA, TÜRKIYE", tag="CLIMATE", label="CONFIRMED",
         head="COP31 runs into overtime with no deal",
         deck="A third draft is due on Saturday morning; fossil-fuel "
              "language is out, no deal yet.",
         source="Reuters, UN News", scene="cop"),
]

PICTURED = [
    dict(n=4, place="WARSAW, POLAND", tag="NATO", label="CONFIRMED",
         head="Rutte in Warsaw as Poland seeks more cover",
         deck="NATO chief visits on Saturday after Friday's missile landings.",
         scene="city"),
    dict(n=5, place="KRYVYI RIH, UKRAINE", tag="WAR", label="CONFIRMED",
         head="Overnight strike kills 2, injures 58",
         deck="Six children among the hurt, officials say.",
         scene="starburst"),
    dict(n=6, place="HODEIDAH, YEMEN", tag="AID", label="REPORTED",
         head="UN warns port strikes threaten aid lifeline",
         deck="Civilians told to leave the port area.",
         scene="port"),
    dict(n=7, place="BEIJING", tag="TECH", label="CONFIRMED",
         head="US clears 879,868 AI chips for China",
         deck="Washington approved the sale of the chips.",
         scene="chip"),
    dict(n=8, place="NEW YORK", tag="CYBER", label="REPORTED",
         head="Banks hit in cyberattack on outside vendors",
         deck="JPMorgan, Visa, Mastercard report incidents.",
         scene="chart"),
    dict(n=9, place="COPENHAGEN", tag="SECURITY", label="CONFIRMED",
         head="Denmark charges two over Russian murder plot",
         deck="Two Danes accused of a plot to kill a rapper.",
         scene="doc"),
    dict(n=10, place="BRUSSELS", tag="EUROPE", label="CONFIRMED",
         head="EU pays out nearly €7,9bn to Ukraine",
         deck="The bloc's largest-ever payment.",
         scene="euro"),
    dict(n=11, place="NEW DELHI", tag="CRICKET", label="CONFIRMED",
         head="India resume on 159/1 on day three",
         deck="New Zealand made 368. Nicholls 175 not out.",
         scene="cricket"),
    dict(n=12, place="TURIN", tag="TENNIS", label="CONFIRMED",
         head="Medvedev meets Zverev in tonight's semi",
         deck="Medvedev beat Tiafoe on Friday to set it up.",
         scene="tennis"),
    dict(n=13, place="LAS VEGAS", tag="FORMULA 1", label="CONFIRMED",
         head="Las Vegas GP qualifying today",
         deck="The grid is decided under the lights.",
         scene="race"),
]

ALSO = [
    "WASHINGTON — Trump wants Huang back.",
    "BRASÍLIA — Indigenous safeguards pass.",
    "MADRID — General strike hits Spain.",
    "ROME — Workers, students march vs budget.",
    "LOS ANGELES — Palisades arsonist guilty.",
    "HEALTH — Cancer pill breakthrough hailed.",
    "WASHINGTON — Trump in no rush on Iran.",
    "KYIV — Ukraine hit three launchers.",
    "NEW DELHI — US: India targets minorities.",
    "DAKAR — Youth Olympics medalists emerge.",
    "GAZA — Children appeal for food.",
    "KYIV — Ukraine sends food aid to nine nations.",
    "BERN — Swiss hail ICJ Myanmar ruling.",
    "LONDON — ICJ ruling may hit UK defence.",
    "EUROPE — Youth cost-of-living protests.",
    "ATLANTIC — Storm Xavier warnings narrow.",
    "LOS ANGELES — Hyundai unveils Elantra.",
    "ODISHA — Cyclone Akvan's rains lash Bengal.",
    "NEW YORK — UN: 44 of 96 climate signs up.",
    "MELBOURNE — Australia host England in T20.",
    "WOLVERHAMPTON — Darts quarters live.",
    "WASHINGTON — Pentagon: Iran cost $48.3bn.",
    "BEIJING — Trump 'too busy' for Kim Jong-un.",
    "GENEVA — WHO: Congo Ebola still emergency.",
    "TOKYO — Japan Tobacco faces $8.6bn loss.",
    "WASHINGTON — Contractor rule finalized.",
    "HORMUZ — Tanker fire; US sanctions hit.",
]

NUMSTRIP = [
    ("3", "missiles downed over Riyadh"),
    ("8 yrs", "BepiColombo's voyage to Mercury"),
    ("92,934", "people at COP31, the largest ever"),
    ("879,868", "AI chips cleared for China"),
    ("58", "hurt in the Kryvyi Rih strike"),
    ("€7,9bn", "EU payment to Ukraine"),
]

UTCSTRIP = [
    ("OVERNIGHT", "Kryvyi Rih kills 2"),
    ("EARLY SAT", "3 missiles over Riyadh"),
    ("SAT AM", "COP31 third draft due"),
    ("SAT AM", "Rutte visits Warsaw"),
    ("18:24", "BepiColombo in orbit"),
    ("EVENING", "Las Vegas GP qualifying"),
    ("TONIGHT", "Medvedev–Zverev semi"),
]

DATE_CHECK = (
    "DATE CHECK — Chip files hit the news Saturday: the 879,868-chip "
    "clearance is Saturday's story. Left out as Friday 20 Nov news: "
    "Russian missiles land in Poland · Kyiv bridges hit · UK-EU deals · "
    "Shenzhen summit · ICJ Myanmar ruling · Mongolia president quits · "
    "LA quake 4.2 · US-China AI pact · Pete Rose pardon · Wall Street "
    "sell-off. Sun 22 Nov, not shown: Verstappen wins Las Vegas GP · "
    "new COP31 draft · India declare at 720-9."
)

# Map pins (absolute x, y); story 2 is off-map (Mercury). Min spacing >= 18.
PINS = {
    1: (212, 830), 3: (185, 775), 4: (160, 720), 5: (200, 730),
    6: (228, 868), 7: (272, 730), 8: (82, 735), 9: (152, 745),
    10: (138, 765), 11: (245, 780), 12: (158, 790), 13: (48, 770),
}

LABEL_FILL = {"CONFIRMED": GREEN, "CLAIMED": AMBER, "REPORTED": SLATE}


# ---------------------------------------------------------------- helpers
def wrap(d, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def pill(d, x, y, text, fill, fnt, pad=5, h=14):
    w = int(d.textlength(text, font=fnt)) + pad * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill)
    d.text((x + pad, y + (h - fnt.size) // 2 - 1), text, font=fnt,
           fill=(255, 255, 255))
    return w


def label_pill(d, x_right, y, label, fnt=None):
    """Right-aligned label pill; returns its left x."""
    fnt = fnt or sans_b(9)
    w = int(d.textlength(label, font=fnt)) + 10
    x = x_right - w
    d.rounded_rectangle([x, y, x_right, y + 14], radius=7,
                        fill=LABEL_FILL[label])
    d.text((x + 5, y + 2), label, font=fnt, fill=(255, 255, 255))
    return x


# ---------------------------------------------------------------- scenes
def scene_city_missiles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(13, 22, 38))
    for i in range(14):
        d.ellipse([x + 12 + i * 23, y + 8 + (i * 7) % 14, x + 14 + i * 23,
                   y + 10 + (i * 7) % 14], fill=(255, 255, 255))
    blds = [(0, 46, 52), (58, 62, 40), (104, 38, 58), (150, 66, 44),
            (204, 52, 60), (252, 40, 46)]
    for bx, bw, bh in blds:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(30, 58, 95))
        for wy in range(y + h - bh + 6, y + h - 4, 12):
            for wx in range(x + bx + 6, x + bx + bw - 4, 12):
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(245, 197, 66))
    for mx, my in [(70, 22), (170, 14), (260, 26)]:
        d.line([x + mx - 26, y + my + 16, x + mx, y + my], fill=(255, 140, 40),
               width=3)
        for dx, dy in [(0, -9), (7, -6), (9, 0), (7, 6), (0, 9), (-7, 6),
                       (-9, 0), (-7, -6)]:
            d.line([x + mx, y + my, x + mx + dx, y + my + dy],
                   fill=(255, 190, 60), width=2)


def scene_city(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(13, 22, 38))
    for i in range(8):
        d.ellipse([x + 10 + i * 24, y + 6 + (i * 5) % 10, x + 12 + i * 24,
                   y + 8 + (i * 5) % 10], fill=(255, 255, 255))
    blds = [(0, 40, 30), (46, 34, 38), (86, 44, 28), (136, 36, 34)]
    for bx, bw, bh in blds:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(30, 58, 95))
        for wy in range(y + h - bh + 5, y + h - 4, 11):
            for wx in range(x + bx + 5, x + bx + bw - 4, 11):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(245, 197, 66))


def scene_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 10, 20))
    for i in range(20):
        d.ellipse([x + 8 + (i * 37) % (w - 12), y + 6 + (i * 23) % (h - 12),
                   x + 10 + (i * 37) % (w - 12), y + 8 + (i * 23) % (h - 12)],
                  fill=(255, 255, 255))
    cx, cy, r = x + 92, y + h // 2, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(154, 154, 154))
    for ox, oy, orad in [(-18, -12, 9), (12, 8, 12), (-6, 20, 7), (22, -18, 6)]:
        d.ellipse([cx + ox - orad, cy + oy - orad, cx + ox + orad,
                   cy + oy + orad], fill=(120, 120, 120))
    d.rectangle([x + 215, y + 30, x + 265, y + 44], fill=(200, 200, 210))
    d.rectangle([x + 235, y + 44, x + 250, y + 56], fill=(240, 240, 240))
    d.polygon([(x + 238, y + 56), (x + 247, y + 56), (x + 242, y + 68)],
              fill=(255, 140, 40))


def scene_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 166, 35))
    d.text((x + 10, y + 8), "1.5°C LIMIT PASSED", font=sans_b(13), fill=INK)
    d.rectangle([x + 10, y + 32, x + w - 52, y + 58], fill=(30, 80, 160))
    d.text((x + 18, y + 39), "3RD DRAFT DUE SAT AM", font=sans_b(12),
           fill=(255, 255, 255))
    d.text((x + 10, y + 66), "OVERTIME", font=sans_b(13), fill=INK)
    d.rectangle([x + w - 30, y + 10, x + w - 22, y + h - 22], fill=(255, 255, 255))
    d.ellipse([x + w - 36, y + h - 28, x + w - 16, y + h - 8], fill=RED)


def scene_starburst(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 16, 12))
    cx, cy = x + w // 2, y + h // 2 - 4
    for dx, dy in [(0, -20), (14, -14), (20, 0), (14, 14), (0, 20),
                   (-14, 14), (-20, 0), (-14, -14)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 150, 50), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 210, 90))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(40, 40, 48))


def scene_port(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(191, 227, 240))
    d.polygon([(x + 20, y + 12), (x + 90, y + 8), (x + 150, y + 22),
               (x + 170, y + h - 8), (x + 30, y + h - 6)],
              fill=(46, 125, 80))
    d.ellipse([x + 120 - 5, y + 30 - 5, x + 120 + 5, y + 30 + 5], fill=RED)
    for wy in (h - 14, h - 8):
        for wx in range(8, w - 8, 18):
            d.line([x + wx, y + wy, x + wx + 10, y + wy], fill=(255, 255, 255),
                   width=2)


def scene_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 95, 163))
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 34, cy - 20, cx + 34, cy + 20], fill=(30, 30, 40))
    d.rectangle([cx - 18, cy - 10, cx + 18, cy + 10], fill=(90, 160, 220))
    for px in range(cx - 30, cx + 31, 10):
        d.rectangle([px - 2, cy - 28, px + 2, cy - 20], fill=(220, 190, 90))
        d.rectangle([px - 2, cy + 20, px + 2, cy + 28], fill=(220, 190, 90))
    for py in range(cy - 12, cy + 13, 8):
        d.rectangle([cx - 42, py - 2, cx - 34, py + 2], fill=(220, 190, 90))
        d.rectangle([cx + 34, py - 2, cx + 42, py + 2], fill=(220, 190, 90))


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(243, 237, 226))
    for gy in range(10, h - 6, 12):
        d.line([x + 8, y + gy, x + w - 8, y + gy], fill=(220, 214, 200), width=1)
    pts = [(x + 12, y + 12), (x + 55, y + 18), (x + 95, y + 16),
           (x + 135, y + 30), (x + 175, y + 38)]
    d.line(pts, fill=RED, width=4)


def scene_doc(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 205, 184))
    d.rectangle([x + w // 2 - 42, y + 6, x + w // 2 + 42, y + h - 6],
                fill=(250, 248, 242))
    for i, ly in enumerate(range(y + 14, y + h - 12, 9)):
        ln = 64 if i % 3 else 48
        d.line([x + w // 2 - 34, ly, x + w // 2 - 34 + ln, ly],
               fill=(120, 115, 105), width=2)
    d.ellipse([x + w // 2 + 22, y + h - 20, x + w // 2 + 36, y + h - 6],
              fill=RED)


def scene_euro(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 110))
    cx, cy, r = x + w // 2, y + h // 2, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 197, 66))
    d.text((cx - 9, cy - 15), "€", font=serif_b(26), fill=(30, 58, 110))


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
    d.ellipse([x + 10, y + 8, x + w - 10, y + h - 8], fill=(90, 170, 80))
    d.rectangle([x + w // 2 - 8, y + 6, x + w // 2 + 8, y + h - 6],
                fill=(230, 220, 190))
    d.ellipse([x + w - 34, y + 10, x + w - 24, y + 20], fill=RED)


def scene_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 95, 163))
    d.rectangle([x + 14, y + 8, x + w - 14, y + h - 8], outline=(255, 255, 255),
                width=2)
    d.line([x + 14, y + h // 2, x + w - 14, y + h // 2], fill=(255, 255, 255),
           width=2)
    d.ellipse([x + w // 2 - 7, y + h // 2 - 7, x + w // 2 + 7, y + h // 2 + 7],
              fill=(220, 230, 60))


def scene_race(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 28))
    for wy in (12, 24, 36):
        d.line([x + 10, y + wy, x + 90, y + wy], fill=(70, 70, 90), width=2)
    d.rounded_rectangle([x + 52, y + 18, x + 168, y + 34], radius=6,
                        fill=(200, 40, 40))
    d.rounded_rectangle([x + 92, y + 8, x + 132, y + 20], radius=4,
                        fill=(200, 40, 40))
    d.ellipse([x + 66, y + 32, x + 84, y + 50], fill=(10, 10, 10))
    d.ellipse([x + 136, y + 32, x + 154, y + 50], fill=(10, 10, 10))


SCENES = {
    "city_missiles": scene_city_missiles, "city": scene_city,
    "mercury": scene_mercury, "cop": scene_cop,
    "starburst": scene_starburst, "port": scene_port, "chip": scene_chip,
    "chart": scene_chart, "doc": scene_doc, "euro": scene_euro,
    "cricket": scene_cricket, "tennis": scene_tennis, "race": scene_race,
}


# ---------------------------------------------------------------- render
def main():
    # ---- structural checks (before drawing) ----
    all_nums = sorted(n for _, _, _, lst in REGIONS for n in lst)
    assert all_nums == list(range(1, 41)), "region coverage must be 1..40"
    assert sum(c for _, c, _, _ in REGIONS) == 40, "region counts must sum 40"
    for name, count, _, lst in REGIONS:
        assert len(lst) == count, f"{name} count mismatch"
    assert len(ALSO) == 27, "ALSO must be 27 stories"
    assert len(HEROES) == 3 and len(PICTURED) == 10, "3 heroes + 10 pictured"
    pin_items = sorted(PINS)
    assert pin_items == [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "12 pins"
    for a in pin_items:
        for b in pin_items:
            if a < b:
                ax, ay = PINS[a]
                bx, by = PINS[b]
                dist = ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
                assert dist >= 18, f"pins {a} and {b} too close ({dist:.1f})"

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top bar ----
    d.text((8, 2), "THE WORLD IN ONE DAY", font=sans_b(11), fill=RED)
    mid = "DAY 325 OF 2026"
    d.text(((W - d.textlength(mid, font=sans_b(11))) / 2, 2), mid,
           font=sans_b(11), fill=RED)
    right = "ALL TIMES UTC · RANKED BY CONSEQUENCE"
    d.text((W - 8 - d.textlength(right, font=sans_b(11)), 2), right,
           font=sans_b(11), fill=INK)
    d.line([8, 16, W - 8, 16], fill=INK, width=1)

    # ---- masthead ----
    mast = "Saturday 21 November 2026"
    d.text(((W - d.textlength(mast, font=serif_b(58))) / 2, 18), mast,
           font=serif_b(58), fill=INK)
    sub = "40 STORIES, 7 REGIONS, EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text(((W - d.textlength(sub, font=sans_b(13))) / 2, 80), sub,
           font=sans_b(13), fill=INK)
    red = "Missiles over Riyadh · COP31 into overtime · BepiColombo reaches Mercury"
    d.text(((W - d.textlength(red, font=serif_b(15))) / 2, 94), red,
           font=serif_b(15), fill=RED)

    # ---- region chips ----
    chips = [(f"{name} {count}", color) for name, count, color, _ in REGIONS]
    widths = [int(d.textlength(t, font=sans_b(11))) + 16 for t, _ in chips]
    total = sum(widths) + 6 * (len(chips) - 1)
    cx = (W - total) // 2
    for (text, color), wdt in zip(chips, widths):
        d.rounded_rectangle([cx, 117, cx + wdt, 135], radius=9, fill=color)
        d.text((cx + 8, 121), text, font=sans_b(11), fill=(255, 255, 255))
        cx += wdt + 6

    # ---- number strip ----
    cell_w = (W - 16) // 6
    for i, (big, cap) in enumerate(NUMSTRIP):
        x0 = 8 + i * cell_w
        if i:
            d.line([x0, 141, x0, 179], fill=(200, 192, 178), width=1)
        d.text((x0 + 8, 139), big, font=serif_b(26), fill=(30, 58, 110))
        lines = wrap(d, cap, sans(10), cell_w - 16)
        assert len(lines) <= 2, f"numstrip caption too long: {cap}"
        for j, ln in enumerate(lines):
            d.text((x0 + 8, 167 + j * 11), ln, font=sans(10), fill=GREY)
    d.line([8, 185, W - 8, 185], fill=(200, 192, 178), width=1)

    # ---- UTC strip ----
    d.rectangle([8, 189, 108, 211], fill=INK)
    d.text((14, 195), "THE DAY IN UTC", font=sans_b(10), fill=(255, 255, 255))
    utc_w = (W - 8 - 112) // 7
    for i, (tm, tx) in enumerate(UTCSTRIP):
        x0 = 112 + i * utc_w
        d.text((x0 + 4, 191), tm, font=sans_b(10), fill=RED)
        lines = wrap(d, tx, sans(10), utc_w - 8)
        assert len(lines) == 1, f"utc text must fit 1 line: {tx}"
        for j, ln in enumerate(lines):
            d.text((x0 + 4, 202 + j * 11), ln, font=sans(10), fill=INK)

    # ---- heroes ----
    hero_w, hero_gap = 330, 8
    for i, s in enumerate(HEROES):
        x0 = 8 + i * (hero_w + hero_gap)
        SCENES[s["scene"]](d, x0, 215, hero_w, 92)
        kick = f"{s['n']} · {s['place']} · {s['tag']}"
        d.text((x0, 311), kick, font=sans_b(11), fill=RED)
        label_pill(d, x0 + hero_w, 310, s["label"])
        lines = wrap(d, s["head"], serif_b(20), hero_w)
        assert len(lines) <= 2, f"hero {s['n']} headline too long"
        for j, ln in enumerate(lines):
            d.text((x0, 325 + j * 19), ln, font=serif_b(20), fill=INK)
        dlines = wrap(d, s["deck"], sans(11), hero_w)
        assert len(dlines) <= 2, f"hero {s['n']} deck too long"
        for j, ln in enumerate(dlines):
            d.text((x0, 365 + j * 13), ln, font=sans(11), fill=(60, 58, 54))
        d.text((x0, 391), s["source"], font=sans(9), fill=GREY)

    # ---- pictured (2 rows x 5); label pill overlays scene top-right ----
    pic_w, pic_gap = 196, 6
    for row in range(2):
        y0 = 407 + row * 136
        for col in range(5):
            s = PICTURED[row * 5 + col]
            x0 = 8 + col * (pic_w + pic_gap)
            SCENES[s["scene"]](d, x0, y0, pic_w, 54)
            label_pill(d, x0 + pic_w - 3, y0 + 3, s["label"], fnt=sans_b(8))
            kick = f"{s['n']} · {s['place']} · {s['tag']}"
            d.text((x0, y0 + 58), kick, font=sans_b(9), fill=RED)
            lines = wrap(d, s["head"], serif_b(13), pic_w)
            assert len(lines) <= 2, f"pictured {s['n']} headline too long"
            for j, ln in enumerate(lines):
                d.text((x0, y0 + 72 + j * 15), ln, font=serif_b(13), fill=INK)
            dlines = wrap(d, s["deck"], sans(10), pic_w)
            assert len(dlines) <= 2, f"pictured {s['n']} deck too long"
            for j, ln in enumerate(dlines):
                d.text((x0, y0 + 104 + j * 12), ln, font=sans(10),
                       fill=(60, 58, 54))

    # ---- map + ALSO ----
    map_x0, map_y0, map_w, map_h = 8, 677, 292, 262
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h], fill=NAVY)
    d.text((map_x0 + 10, map_y0 + 8), "WHERE IT HAPPENED", font=sans_b(13),
           fill=(255, 255, 255))
    d.text((map_x0 + 10, map_y0 + 26), "2 MERCURY — off this map",
           font=sans(10), fill=(200, 200, 210))
    blobs = [
        [(30, 720), (95, 710), (125, 730), (115, 765), (60, 785), (28, 755)],
        [(140, 710), (215, 700), (255, 720), (245, 765), (180, 785),
         (145, 755)],
        [(60, 815), (115, 805), (135, 840), (105, 890), (55, 870)],
        [(200, 810), (270, 800), (285, 845), (240, 895), (195, 865)],
    ]
    for b in blobs:
        d.polygon([(map_x0 + px - 8, py) for px, py in b],
                  fill=(232, 222, 200))
    for n, (px, py) in sorted(PINS.items()):
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        d.text((px - d.textlength(t, font=sans_b(10)) / 2, py - 7), t,
               font=sans_b(10), fill=(255, 255, 255))
    d.text((map_x0 + 10, map_y0 + map_h - 26),
           "Red numbers mark stories 1–13.", font=sans(9),
           fill=(200, 200, 210))
    d.text((map_x0 + 10, map_y0 + map_h - 14),
           "No. 2 is in space: Mercury.", font=sans(9),
           fill=(200, 200, 210))

    ax0 = 312
    d.text((ax0, 677), "ALSO ON SATURDAY 21 NOVEMBER 2026 — 27 MORE STORIES",
           font=sans_b(13), fill=RED)
    col_w = (W - 8 - ax0 - 20) // 3
    f_also = sans(9)
    for idx, text in enumerate(ALSO):
        n = 14 + idx
        col, row = divmod(idx, 9)
        x = ax0 + col * (col_w + 10)
        y = 703 + row * 26
        line = f"{n} {text}"
        wdt = d.textlength(line, font=f_also)
        assert wdt <= col_w, f"ALSO {n} too wide ({wdt:.0f} > {col_w})"
        d.text((x, y), line, font=f_also, fill=INK)

    # ---- DATE CHECK ----
    d.rounded_rectangle([8, 942, W - 8, 984], radius=4,
                        outline=RED, width=2)
    dc_lines = wrap(d, DATE_CHECK, sans(10), W - 8 - 8 - 24)
    assert len(dc_lines) <= 3, f"DATE CHECK too long: {len(dc_lines)} lines"
    for j, ln in enumerate(dc_lines):
        d.text((20, 947 + j * 12), ln, font=sans(10), fill=INK)

    # ---- footer ----
    fx = 8
    d.text((fx, 990), "HOW SURE", font=sans_b(10), fill=INK)
    fx += int(d.textlength("HOW SURE", font=sans_b(10))) + 8
    for label, cap in [("CONFIRMED", "2+ major outlets"),
                       ("CLAIMED", "as stated by the source"),
                       ("REPORTED", "one major outlet")]:
        wdt = pill(d, fx, 989, label, LABEL_FILL[label], sans_b(9), h=13)
        fx += wdt + 4
        d.text((fx, 991), cap, font=sans(9), fill=GREY)
        fx += int(d.textlength(cap, font=sans(9))) + 14
    foot = ("Every story here happened or was first reported on Saturday "
            "21 November 2026 (UTC), told as the named outlets reported it. "
            "All maps and drawings are original vector work.")
    d.text(((W - d.textlength(foot, font=sans(9))) / 2, 1006), foot,
           font=sans(9), fill=GREY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out)
    data = out.read_bytes()
    print(f"wrote {out} {len(data)} bytes, final y=1015, "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
