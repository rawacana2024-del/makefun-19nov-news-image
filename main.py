#!/usr/bin/env python3
"""make.fun bounty entry — "Sum up 19 November's world news in one image".

Renders a newspaper front page (11 verified stories from the 19 Nov 2026
brief) to /output/entry.png (or a local path given as argv[1]).
Square 1024x1024 canvas, pure Pillow, no network, deterministic:
two runs produce byte-identical output.
Prepared for Irpan, 20 Nov 2026. Not submitted anywhere by this script.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 32  # margin
PAPER = (251, 247, 238)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (110, 110, 105)
RULE = (60, 60, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, width, fill=INK, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


# (number, title, summary, lon, lat)
STORIES = [
    (1, "Trump, Xi and Putin meet in Shenzhen",
     "First three-way meeting, on the APEC sidelines. Ukraine, nuclear "
     "arms control and the end of New START on the table.",
     114.06, 22.55),
    (2, "Ukraine hits the Crimea Bridge",
     "Third strike in a week; car traffic across the bridge halted.",
     34.0, 45.0),
    (3, "Iran strikes Gulf states",
     "After a US strike on Qeshm Island; the US sank five Iranian "
     "tankers on 18 November.", 56.0, 27.0),
    (4, "ICJ rules on the Rohingya genocide case",
     "Gambia v. Myanmar decided 19 Nov, over the 2017 crackdown that "
     "drove 730,000+ Rohingya to Bangladesh.", 4.3, 52.07),
    (5, "Bangladesh in turmoil",
     "Ancestral home of Muhammad Yunus torched; violence reported in "
     "28 districts.", 90.4, 23.8),
    (6, "COP31 talks in Antalya",
     "Ministers push to unblock negotiations and adopt a final text.",
     30.7, 36.9),
    (7, "Anthropic's record IPO",
     "$81.3 billion raised at a $1.5 trillion valuation.",
     -122.4, 37.8),
    (8, "Van Gogh sells for $190.4 million",
     "\u201cCh\u00e2taigniers en fleurs\u201d sets a record for the artist "
     "at Sotheby\u2019s New York.", -74.0, 40.7),
    (9, "North Korea expands uranium enrichment",
     "IAEA reports expansion at the Yongbyon site.", 126.0, 39.8),
    (10, "Cyclone Akvan nears India",
     "Landfall expected 20 Nov on the Andhra Pradesh\u2013Odisha coast.",
     80.0, 16.0),
    (11, "IEA warns on Hormuz",
     "Hormuz crisis called the biggest ever recorded threat to global "
     "energy security.", 2.35, 48.85),
]

LEAD = STORIES[0]
REST = STORIES[1:]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    f_mast = font(SERIF_B, 62)
    title = "THE WORLD"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 12), title, font=f_mast, fill=INK)
    d.line([(M, 88), (W - M, 88)], fill=INK, width=3)
    d.line([(M, 93), (W - M, 93)], fill=INK, width=1)
    f_date = font(SANS_B, 20)
    dateline = "Thursday, 19 November 2026  \u2022  11 stories  \u2022  3 continents"
    tw = d.textlength(dateline, font=f_date)
    d.text(((W - tw) / 2, 101), dateline, font=f_date, fill=INK)
    d.line([(M, 130), (W - M, 130)], fill=INK, width=1)

    # ---- Lead story ----
    y = 142
    f_kicker = font(SANS_B, 17)
    d.text((M, y), "LEAD  \u2022  SHENZHEN, CHINA", font=f_kicker, fill=RED)
    y += 26
    f_head = font(SERIF_B, 46)
    y = draw_wrapped(d, (M, y),
                     "Trump, Xi and Putin meet\nfor the first time",
                     f_head, W - 2 * M, leading=52)
    y += 8
    f_deck = font(SERIF, 21)
    y = draw_wrapped(d, (M, y),
                     "Three leaders, one table: Ukraine, nuclear arms "
                     "control and the end of New START dominate the "
                     "first-ever three-way summit on the APEC sidelines.",
                     f_deck, W - 2 * M, leading=28)
    y += 10
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 10

    # ---- Map panel: numbered dots on a graticule ----
    map_top = y
    map_h = 150
    map_left, map_right = M, W - M
    d.rectangle([map_left, map_top, map_right, map_top + map_h],
                outline=INK, width=2)
    f_map_t = font(SANS_B, 15)
    d.text((map_left + 12, map_top + 8), "WHERE IT HAPPENED",
           font=f_map_t, fill=INK)
    grid_top = map_top + 30
    grid_bot = map_top + map_h - 8
    for lon in range(-150, 181, 30):
        x = map_left + (lon + 180) / 360 * (map_right - map_left)
        d.line([(x, grid_top), (x, grid_bot)], fill=(200, 196, 186), width=1)
    for lat in (-30, 0, 30, 60):
        yy = grid_top + (85 - lat) / 145 * (grid_bot - grid_top)
        d.line([(map_left, yy), (map_right, yy)], fill=(200, 196, 186), width=1)
    f_dot = font(SANS_B, 13)
    # Small manual offsets so near-identical locations stay readable.
    offsets = {2: (0, -13), 4: (0, -13), 6: (0, 13), 10: (0, 13), 11: (0, 13)}
    for num, _t, _s, lon, lat in STORIES:
        dx, dy = offsets.get(num, (0, 0))
        x = map_left + (lon + 180) / 360 * (map_right - map_left) + dx
        yy = grid_top + (85 - lat) / 145 * (grid_bot - grid_top) + dy
        r = 11
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=RED, outline="white",
                  width=2)
        label = str(num)
        lw = d.textlength(label, font=f_dot)
        d.text((x - lw / 2, yy - 9), label, font=f_dot, fill="white")
    y = map_top + map_h + 12
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 12

    # ---- Story grid: 2 columns x 5 rows ----
    col_w = (W - 2 * M - 24) // 2
    grid_top_y = y
    grid_bot_y = H - 52
    row_h = (grid_bot_y - grid_top_y) // 5
    f_num = font(SERIF_B, 24)
    f_t = font(SERIF_B, 19)
    f_s = font(SERIF, 15)
    for i, (num, title, summ, _lon, _lat) in enumerate(REST):
        col, row = i % 2, i // 2
        x0 = M + col * (col_w + 24)
        y0 = grid_top_y + row * row_h
        d.text((x0, y0), f"{num}.", font=f_num, fill=RED)
        num_w = d.textlength(f"{num}.", font=f_num)
        tx = x0 + num_w + 10
        ty = draw_wrapped(d, (tx, y0 + 2), title, f_t, col_w - (tx - x0),
                          leading=23)
        draw_wrapped(d, (tx, ty + 4), summ, f_s, col_w - (tx - x0),
                     fill=(40, 40, 40), leading=19)
        if row < 4:
            d.line([(x0, y0 + row_h - 10), (x0 + col_w, y0 + row_h - 10)],
                   fill=(190, 186, 176), width=1)

    # ---- Footer ----
    d.line([(M, H - 40), (W - M, H - 40)], fill=INK, width=2)
    f_f = font(SANS, 16)
    foot = ("Sources: Open Chronicle \u2022 Horizon \u2022 OneTurn \u2022 "
            "Nexus Europa \u2022 RajGlobalStudies  \u2014  19 Nov 2026")
    d.text((M, H - 30), foot, font=f_f, fill=GREY)

    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    img.save(out)
    print(f"wrote {out} ({W}x{H})")


if __name__ == "__main__":
    main()
