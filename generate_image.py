#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026 with Pillow.

All headlines are real news first reported on 23 November 2026,
cross-checked against Reuters, AP/Xinhua reporting and same-day
news roundups. The drawing is fully deterministic: no randomness,
no network, no timestamps inside the image bytes beyond the date
printed on the masthead.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
MUTED = (84, 78, 66)
RED = (178, 28, 28)
BLUE = (30, 58, 95)
TEAL = (13, 110, 99)
GOLD = (196, 138, 18)
LIGHT = (238, 230, 214)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
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


def text_block(draw, x, y, text, fnt, fill, max_w, leading=4):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def panel(draw, x, y, w, h, color, kicker, headline, body, stat=None,
          headline_size=27):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=(205, 198, 180), width=2)
    draw.rectangle([x, y, x + w, y + 26], fill=color)
    draw.text((x + 10, y + 5), kicker, font=font(SANS_B, 14), fill=WHITE)
    yy = text_block(draw, x + 12, y + 36, headline, font(SERIF_B, headline_size),
                    INK, w - 24, leading=2)
    yy += 4
    yy = text_block(draw, x + 12, yy, body, font(SANS, 16), (45, 42, 36),
                    w - 24, leading=3)
    if stat:
        draw.line([x + 12, y + h - 44, x + w - 12, y + h - 44],
                  fill=(205, 198, 180), width=1)
        draw.text((x + 12, y + h - 34), stat, font=font(SANS_B, 17), fill=color)
    return y + h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 8], fill=RED)
    centered(d, W / 2, 18, "THE  WORLD  TODAY", font(SERIF_B, 62), INK)
    centered(d, W / 2, 88, "All the day's world news on one page", font(SERIF_I, 19), MUTED)
    d.line([28, 122, W - 28, 122], fill=INK, width=3)
    d.line([28, 128, W - 28, 128], fill=INK, width=1)
    centered(d, W / 2, 134, "MONDAY  23  NOVEMBER  2026", font(SANS_B, 21), RED)
    d.text((28, 134), "No. 23-11", font=font(SANS, 14), fill=MUTED)
    r = "ONE IMAGE  •  SIX STORIES"
    d.text((W - 28 - d.textlength(r, font=font(SANS, 14)), 134), r,
           font=font(SANS, 14), fill=MUTED)

    # ---- Lead story: COP31 ---------------------------------------------
    ly = 168
    d.rectangle([28, ly, W - 28, ly + 200], fill=(24, 34, 48))
    d.rectangle([28, ly, W - 28, ly + 30], fill=RED)
    d.text((44, ly + 6), "CLIMATE  •  ANTALYA, TURKIYE  •  LEAD STORY",
           font=font(SANS_B, 15), fill=WHITE)
    centered(d, W / 2, ly + 42, "COP31 ENDS WITHOUT A DEAL", font(SERIF_B, 47), WHITE)
    text_block(d, 150, ly + 102,
               "After two days of overtime, the UN climate summit closed with no "
               "agreement. The EU and about 130 parties rejected a draft that "
               "left out fossil fuels — the longest COP on record ends in deadlock.",
               font(SANS, 18), (232, 226, 210), W - 300, leading=4)
    # simple globe
    cx, cy, rr = 92, ly + 128, 42
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(140, 190, 220), width=3)
    d.ellipse([cx - 16, cy - rr, cx + 16, cy + rr], outline=(140, 190, 220), width=2)
    d.line([cx - rr, cy, cx + rr, cy], fill=(140, 190, 220), width=2)
    d.line([cx - rr + 8, cy - 24, cx + rr - 8, cy - 24], fill=(140, 190, 220), width=2)
    d.line([cx - rr + 8, cy + 24, cx + rr - 8, cy + 24], fill=(140, 190, 220), width=2)
    centered(d, W / 2, ly + 168, "NO SHARED PLAN TO PHASE OUT COAL, OIL AND GAS",
             font(SANS_B, 15), (250, 205, 90))

    # ---- Middle grid: four panels --------------------------------------
    gy = 384
    pw, ph, gap = 474, 190, 20
    panel(d, 28, gy, pw, ph, BLUE, "WAR  •  DYMER, KYIV REGION, UKRAINE",
          "Russian strike kills 11 in Dymer",
          "A Russian attack flattened homes in Dymer, north of Kyiv. "
          "Rescuers pulled a boy of 7 alive from the rubble as the toll "
          "rose to 11, the regional governor said on Monday.",
          stat="11 DEAD  •  BOY, 7, RESCUED ALIVE")
    panel(d, 28 + pw + gap, gy, pw, ph, RED, "MARKETS  •  TOKYO / NEW YORK / SEOUL",
          "AI sell-off rattles world markets",
          "Fears that AI shares are overpriced spread across Asia. "
          "Gold jumped as investors ran for safety, and Seoul pledged "
          "to stabilise markets after the KOSPI slid about 5%.",
          stat="NIKKEI -5.06%  •  S&P 500 -3.7%  •  GOLD +2.72%")
    gy2 = gy + ph + 14
    panel(d, 28, gy2, pw, ph, TEAL, "POLITICS  •  WASHINGTON, UNITED STATES",
          "Democrats clinch 258 House seats",
          "Democrats secured at least 258 seats in the US House of "
          "Representatives — the largest majority for either party "
          "since 1992, the Associated Press reported.",
          stat="258 SEATS  •  BIGGEST MAJORITY SINCE 1992")
    panel(d, 28 + pw + gap, gy2, pw, ph, GOLD, "DISASTER  •  BANTEN, INDONESIA",
          "Factory fire: 24 dead, dozens missing",
          "At least 24 bodies were recovered after a fire tore through a "
          "candy factory in Banten, with about 30 people still "
          "unaccounted for and the blaze not yet fully out.",
          stat="24 DEAD  •  ABOUT 30 STILL MISSING")

    # ---- Bottom wide panel: Iran / Hormuz -------------------------------
    by = gy2 + ph + 14
    d.rectangle([28, by, W - 28, by + 100], fill=WHITE, outline=(205, 198, 180), width=2)
    d.rectangle([28, by, W - 28, by + 26], fill=(92, 42, 110))
    d.text((38, by + 5), "MIDDLE EAST  •  STRAIT OF HORMUZ", font=font(SANS_B, 14), fill=WHITE)
    d.text((38, by + 32), "Iran vows to defy US naval blockade at Hormuz",
           font=font(SERIF_B, 27), fill=INK)
    text_block(d, 38, by + 64,
               "Tehran said it will use all available tools against the blockade. Trump said he is "
               "inclined to resume strikes if no deal is reached by the New Year. Oil held near $90.",
               font(SANS, 14), (45, 42, 36), W - 76, leading=2)

    # ---- Footer: three briefs -------------------------------------------
    fy = by + 110
    d.rectangle([0, fy, W, H], fill=INK)
    d.text((28, fy + 10), "ALSO TODAY", font=font(SANS_B, 14), fill=(250, 205, 90))
    briefs = [
        ("SINALOA, MEXICO", "FBI most-wanted fugitive 'El Chapo Isidro' captured"),
        ("MANCHESTER, ENGLAND", "Arena evacuated: unknown substance, 50+ treated"),
        ("BUNIA, DR CONGO", "Reuters: hidden graves reveal far higher Ebola toll"),
    ]
    bx = 28
    for place, head in briefs:
        d.text((bx, fy + 32), place, font=font(SANS_B, 12), fill=(160, 200, 235))
        text_block(d, bx, fy + 50, head, font(SANS_B, 15), WHITE, 296, leading=2)
        if bx > 28:
            d.line([bx - 16, fy + 30, bx - 16, fy + 96], fill=(90, 86, 76), width=1)
        bx += 330
    d.line([28, H - 24, W - 28, H - 24], fill=(90, 86, 76), width=1)
    centered(d, W / 2, H - 19, "Drawn from the day's reporting  •  Monday 23 November 2026",
             font(SANS, 11), (170, 164, 150))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
