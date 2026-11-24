"""News24 v3 - one-page newspaper summing up Tuesday 24 November 2026.

Draws a 1024x1024 PNG with a standard-library-only Python program.
No network, no randomness, no timestamps: two runs write identical bytes.

Layout: giant date masthead, promise line, UTC timeline, numbers rail,
region tabs, 10 feature cards, dotted world map with numbered pins,
20 ALSO ON briefs, DATE CHECK, footer.
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (250, 246, 235)
INK = (22, 22, 22)
RULE = (148, 136, 108)
FAINT = (203, 194, 170)
RED = (172, 32, 32)
DARKRED = (130, 24, 24)
BLUE = (38, 68, 110)
GREEN = (36, 102, 58)
AMBER = (146, 104, 16)
PURPLE = (96, 60, 140)
LANDDOT = (96, 90, 70)
GRAT = (214, 206, 184)

CHIP_STYLE = {
    "CONFIRMED": ((203, 232, 203), (24, 96, 44)),
    "OFFICIALS SAY": ((246, 226, 170), (120, 82, 0)),
    "REPORTED": ((206, 221, 240), (30, 60, 110)),
    "FORECAST": ((226, 210, 240), (90, 50, 130)),
}

# ---------------------------------------------------------------- font: 5x7
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "\u00b7": ("00000", "00000", "00000", "01100", "01100", "00000", "00000"),
}
BLANK = ("00000", "00000", "00000", "00000", "00000", "00000", "00000")


def text_width(s, scale, gap=0):
    return len(s) * (6 * scale + gap) - gap if s else 0


def wrap(text, max_chars):
    """Greedy word wrap; hard-splits words longer than the line."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        while len(word) > max_chars:
            if cur:
                lines.append(cur)
                cur = ""
            lines.append(word[:max_chars])
            word = word[max_chars:]
        if not word:
            continue
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= max_chars:
            cur = cur + " " + word
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self):
        self.px = bytearray([PAPER[0], PAPER[1], PAPER[2]] * (W * H))

    def set(self, x, y, color):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def hline(self, x, y, w, color):
        self.rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.rect(x, y, 1, h, color)

    def border(self, x, y, w, h, color, t=1):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def line(self, x0, y0, x1, y1, color):
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy), 1)
        for i in range(steps + 1):
            self.set(x0 + dx * i // steps, y0 + dy * i // steps, color)

    def glyph(self, ch, x, y, scale, color):
        rows = FONT.get(ch, BLANK)
        for r in range(7):
            row = rows[r]
            for c in range(5):
                if row[c] == "1":
                    self.rect(x + c * scale, y + r * scale, scale, scale, color)

    def text(self, s, x, y, scale, color, gap=0, align="left"):
        s = s.upper()
        if align == "center":
            x = x - text_width(s, scale, gap) // 2
        elif align == "right":
            x = x - text_width(s, scale, gap)
        cx = x
        for ch in s:
            self.glyph(ch, cx, y, scale, color)
            cx += 6 * scale + gap
        return cx

    def para(self, s, x, y, width, scale, color, gap=-1, lh=None):
        """Wrapped paragraph; returns y after the last line."""
        if lh is None:
            lh = 7 * scale + 1
        max_chars = max(1, width // (6 * scale + gap))
        lines = wrap(s, max_chars)
        for ln in lines:
            self.text(ln, x, y, scale, color, gap=gap)
            y += lh
        return y


# ---------------------------------------------------------------- content
# (n, region, place, headline, body, chip, lat, lon)  lat/lon None = no pin
STORIES = [
    (1, "MIDDLE EAST", "",
     "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "IDF STRIKE IN GAZA CITY KILLS NAIM ABU NAHAL, HAMAS SECURITY CHIEF.",
     "CONFIRMED", 31.50, 34.47),
    (2, "ASIA", "MARKETS",
     "HUANG RETURN SENDS ASIAN MARKETS LEAPING",
     "TAIEX +9.0%, KOSPI +6.3%, NIKKEI +3.9% AS ASIAN STOCKS SURGE ON TUESDAY.",
     "CONFIRMED", 25.03, 121.57),
    (3, "MIDDLE EAST", "",
     "RIAL PLUNGES AFTER NEW US SANCTIONS",
     "DOLLAR HITS ABOUT 2.82M RIALS AFTER US SANCTIONS 26+ 'SHADOW BANKING' EXCHANGES.",
     "CONFIRMED", 35.69, 51.39),
    (4, "ASIA", "HANOI",
     "GAS BLAST AT HANOI EATERY KILLS SIX",
     "6 DEAD, 10 HURT AS GAS BLAST HITS EATERY.",
     "OFFICIALS SAY", 21.03, 105.85),
    (5, "AFRICA", "",
     "GAVI SECURES 1.5M EBOLA VACCINE DOSES",
     "SERUM DEAL FOR CONGO OUTBREAK.",
     "CONFIRMED", 0.49, 29.47),
    (6, "OCEANIA", "",
     "SOLOMONS DITCH CHINA PACT",
     "WALE TELLS BEIJING IT ENDS; CANBERRA NEXT.",
     "REPORTED", -9.43, 159.95),
    (7, "EUROPE", "",
     "RUSSIAN STRIKES KILL 2",
     "2 DEAD IN ZAPORIZHZHIA; 96 DRONES DOWNED.",
     "REPORTED", 47.84, 35.14),
    (8, "ASIA", "TAPLEJUNG",
     "MAGNITUDE-5.6 QUAKE HITS NEPAL-TIBET BORDER",
     "07:02 IST QUAKE IN TAPLEJUNG; FELT IN SIKKIM, BENGAL, BIHAR. NO CASUALTIES.",
     "CONFIRMED", 27.35, 87.67),
    (9, "EUROPE", "VATICAN",
     "POPE FRANCIS DIARY: 'I SAW THE DEVIL THREE TIMES'",
     "DIARIES 1992-2024 OUT IN 94 COUNTRIES; THREE ENCOUNTERS, A 'GATE OF HELL'.",
     "CONFIRMED", 41.90, 12.45),
    (10, "AMERICAS", "DC",
     "TRUMP SAYS HE 'CONVINCED' NVIDIA BOARD",
     "TRUMP CLAIMS CREDIT FOR HUANG RETURN; DEMOCRATS VOW A PROBE.",
     "CONFIRMED", 38.90, -77.04),
]

BRIEFS = [
    (11, "KHAN YOUNIS 3 DEAD"),
    (12, "S LEBANON STRIKES"),
    (13, "IRAQ OIL TAKEOVER"),
    (14, "KOREA JETS"),
    (15, "KIM YO-JONG"),
    (16, "SHENZHOU CREW"),
    (17, "BJP-SAD PACT"),
    (18, "POLAND ALERT"),
    (19, "PATRIOTS SLOWED"),
    (20, "NORWAY DESNA"),
    (21, "EVS 30% IN EU"),
    (22, "BELGIAN ATC"),
    (23, "EU CLIMATE BID"),
    (24, "6,929 MINE DEATHS"),
    (25, "47,000 KILLED"),
    (26, "SOMALIA-UGANDA"),
    (27, "NIGERIA CLASH"),
    (28, "MEXICO CPI 3.43%"),
    (29, "SYDNEY VISA ROW"),
    (30, "HUCKABEE ON IRAN"),
]

NUMBERS = [
    ("+9.0%", "TAIEX"),
    ("+6.3%", "KOSPI"),
    ("2.82M", "RIAL PER $1"),
    ("1.5M", "EBOLA DOSES"),
    ("6,929", "MINE DEATHS"),
    ("47,000", "WOMEN KILLED"),
]

DATE_BEFORE = [
    "MON 23 HUANG RETURNS",
    "MON 23 EU SANCTIONS",
    "MON 23 CROWDSTRIKE",
    "MON 23 MERZ REGRET",
    "MON 23 BELGIUM STRIKE",
    "MON 23 INDIA-NEPAL",
    "MON 23 IRAN $290BN",
    "MON 23 SATELLITE ROW",
    "SUN 22 COP31 COLLAPSE",
    "MON 23 BALI FLOODS",
    "MON 23 ANDREW ROW",
    "MON 23 HORMUZ CYBER",
]
DATE_NEXT = [
    "WED 25 SHENZHOU LIFT",
    "WED 25 SOLOMON DEAL",
    "WED 25 PHALA PHALA",
    "WED 25 TRUMP-RUTTE",
    "WED 25 IOWA BLAST",
]

# (lon, lat) continent outlines, coarse, for the dotted map.
LAND = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-97, 26), (-105, 22), (-115, 30),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-32, 68), (-22, 70), (-30, 76), (-50, 76),
     (-58, 70)],
    [(-80, 10), (-75, 5), (-80, -5), (-80, -15), (-70, -20), (-65, -35),
     (-60, -45), (-55, -35), (-48, -25), (-40, -20), (-35, -8), (-40, -3),
     (-50, 0), (-60, 5), (-70, 10)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (13, -10), (9, 4), (-8, 5),
     (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (35, 66), (40, 68),
     (50, 69), (60, 70), (70, 72), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 67), (178, 66), (178, 64), (170, 60), (162, 56), (158, 52),
     (150, 59), (142, 55), (140, 50), (135, 45), (130, 42), (127, 40),
     (122, 38), (120, 32), (115, 23), (110, 20), (105, 10), (103, 8),
     (100, 7), (98, 10), (95, 16), (92, 21), (90, 22), (86, 20), (82, 17),
     (80, 13), (77, 8), (75, 12), (72, 20), (68, 23), (62, 25), (57, 26),
     (52, 26), (50, 29), (48, 30), (44, 29), (40, 30), (36, 36), (33, 36),
     (30, 36), (26, 38), (23, 36), (19, 40), (15, 44), (12, 44), (8, 44),
     (3, 43), (-2, 37), (-6, 36), (-9, 37)],
    [(95, 5), (105, 0), (110, -5), (115, -8), (120, -10), (125, -9),
     (130, -5), (135, -3), (140, -8), (140, -2), (135, 0), (130, 1),
     (125, 1), (120, 0), (115, 0), (110, 0), (105, 5), (100, 5)],
    [(114, -22), (114, -32), (120, -34), (130, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (150, -22),
     (146, -19), (142, -11), (137, -12), (132, -12), (126, -14),
     (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 53), (-1, 51)],
    [(130, 31), (132, 34), (135, 34), (138, 35), (140, 38), (141, 41),
     (143, 43), (145, 44), (142, 40), (140, 36), (137, 34), (133, 33)],
]

# Pin label offsets (dx, dy) in pixels for crowded spots.
PIN_OFF = {
    1: (-20, -14), 3: (14, -12), 4: (-12, -8), 7: (10, 12), 8: (12, 10),
    9: (-14, 12), 10: (-18, -12), 11: (20, -12), 12: (-20, 14), 13: (-14, 12),
    14: (16, -12), 15: (-16, 12), 17: (-12, -10), 18: (12, -8), 19: (18, 12),
    20: (-12, -12), 21: (-24, -16), 22: (24, -16), 23: (0, 18),
    24: (12, 10), 30: (20, 14),
}

MAP_X0, MAP_Y0, MAP_W, MAP_H = 760, 236, 236, 128
MAP_LAT_TOP, MAP_LAT_BOT = 83, -60


def inside_land(lon, lat):
    for poly in LAND:
        inside = False
        n = len(poly)
        j = n - 1
        for i in range(n):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if ((yi > lat) != (yj > lat)) and (
                lon < (xj - xi) * (lat - yi) / (yj - yi) + xi
            ):
                inside = not inside
            j = i
        if inside:
            return True
    return False


def project(lon, lat):
    x = MAP_X0 + (lon + 180) / 360.0 * MAP_W
    y = MAP_Y0 + (MAP_LAT_TOP - lat) / (MAP_LAT_TOP - MAP_LAT_BOT) * MAP_H
    return int(x), int(y)


def chip_pill(cv, x, y, chip):
    bg, fg = CHIP_STYLE[chip]
    w = text_width(chip, 2, gap=-1) + 12
    cv.rect(x, y, w, 18, bg)
    cv.border(x, y, w, 18, fg, 1)
    cv.text(chip, x + 6, y + 2, 2, fg, gap=-1)
    return w


def draw_card(cv, x, y, w, h, story):
    n, region, place, headline, body, chip, _lat, _lon = story
    cv.border(x, y, w, h, INK, 2)
    cv.rect(x + 2, y + 2, w - 4, 3, RED)
    pad = 8
    cx = x + pad
    cw = w - 2 * pad
    # number disc + kicker (single line by construction)
    cv.disc(cx + 9, y + 14, 9, RED)
    cv.text(str(n), cx + 9, y + 10, 1, PAPER, align="center")
    kx = cx + 22
    kicker = region if not place else region + " - " + place
    ky = y + 8
    ky = cv.para(kicker, kx, ky, cw - 22, 2, DARKRED, gap=-1, lh=15)
    # headline
    hy = ky + 2
    hy = cv.para(headline, cx, hy, cw, 2, INK, gap=-1, lh=16)
    # body, clamped so it never collides with the chip pill
    by = hy + 3
    max_body_lines = max(0, (y + h - 30 - by) // 15)
    max_chars = max(1, cw // 11)
    body_lines = wrap(body, max_chars)[:max_body_lines]
    for ln in body_lines:
        cv.text(ln, cx, by, 2, (52, 52, 52), gap=-1)
        by += 15
    # chip pill bottom-left
    chip_pill(cv, cx, y + h - 26, chip)


def draw_map(cv):
    cv.text("WHERE IT HAPPENED", 878, 218, 2, INK, gap=-1, align="center")
    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, 0)
        cv.vline(gx, MAP_Y0, MAP_H, GRAT)
    for lat in (60, 30, 0, -30):
        _, gy = project(0, lat)
        cv.hline(MAP_X0, gy, MAP_W, GRAT)
    # dotted land
    lat = 80
    while lat >= -58:
        lon = -180
        while lon < 180:
            if inside_land(lon, lat):
                px, py = project(lon, lat)
                cv.rect(px, py, 2, 2, LANDDOT)
            lon += 3
        lat -= 3
    cv.border(MAP_X0 - 2, MAP_Y0 - 2, MAP_W + 4, MAP_H + 4, RULE, 1)
    # pins for feature stories
    for story in STORIES:
        n, _r, _p, _h, _b, _c, lat, lon = story
        if lat is None:
            continue
        px, py = project(lon, lat)
        dx, dy = PIN_OFF.get(n, (0, 0))
        tx, ty = px + dx, py + dy
        if (dx, dy) != (0, 0):
            cv.line(px, py, tx, ty, RED)
        cv.disc(tx, ty, 7, PAPER)
        cv.disc(tx, ty, 5, RED)
        cv.text(str(n), tx, ty - 3, 1, PAPER, align="center")
    # pins for briefs (lat/lon table below)
    for n, lat, lon in BRIEF_PINS:
        px, py = project(lon, lat)
        dx, dy = PIN_OFF.get(n, (0, 0))
        tx, ty = px + dx, py + dy
        if (dx, dy) != (0, 0):
            cv.line(px, py, tx, ty, RED)
        cv.disc(tx, ty, 7, PAPER)
        cv.disc(tx, ty, 5, RED)
        cv.text(str(n), tx, ty - 3, 1, PAPER, align="center")


BRIEF_PINS = [
    (11, 31.35, 34.30), (12, 33.20, 35.20), (13, 33.31, 44.36),
    (14, 37.50, 130.90), (15, 39.15, 127.44), (16, 40.96, 100.29),
    (17, 30.74, 76.79), (18, 52.23, 21.01), (19, 38.87, -77.05),
    (20, 59.91, 10.75), (21, 50.85, 4.35), (22, 50.85, 4.35),
    (23, 50.85, 4.35), (24, 16.84, 96.17), (26, 2.05, 45.32),
    (27, 6.73, 6.73), (28, 19.43, -99.13), (29, -33.87, 151.21),
    (30, 32.08, 34.78),
]


def brief_region(n):
    return {
        11: "MIDDLE EAST", 12: "MIDDLE EAST", 13: "MIDDLE EAST",
        14: "ASIA", 15: "ASIA", 16: "ASIA", 17: "ASIA", 18: "EUROPE",
        19: "EUROPE", 20: "EUROPE", 21: "EUROPE", 22: "EUROPE",
        23: "EUROPE", 24: "GLOBAL", 25: "GLOBAL", 26: "AFRICA",
        27: "AFRICA", 28: "AMERICAS", 29: "OCEANIA", 30: "MIDDLE EAST",
    }[n]


def draw(cv):
    # ---- strap
    cv.text("THE WORLD TODAY", 24, 6, 3, INK, gap=-1)
    cv.text("VOL. 1 - NO. 328", 1000, 6, 3, INK, gap=-1, align="right")
    cv.hline(24, 28, 976, RULE)
    # ---- masthead: giant date, one line
    cv.text("TUESDAY 24 NOVEMBER 2026", 512, 34, 7, INK, gap=-2,
            align="center")
    cv.hline(24, 88, 976, INK)
    cv.hline(24, 91, 976, INK)
    # ---- promise line
    cv.text("30 STORIES - 7 REGIONS - 8 FIELDS - ALL FROM TUESDAY 24 NOVEMBER 2026",
            512, 97, 2, DARKRED, gap=-1, align="center")
    # ---- UTC rail: two plain text lines (a graphic timeline collided)
    cv.text("THE DAY IN UTC  01:00 HANOI BLAST - 01:30 NEPAL QUAKE - 05:30 ASIA CLOSE",
            24, 116, 2, INK, gap=-1)
    cv.text("07:29 96 DRONES - 10:39 MAGYAR TALKS - 10:55 GAZA STRIKE - 11:35 KYIV RAIL",
            24, 132, 2, INK, gap=-1)
    # ---- numbers rail
    box_w = (976 - 5 * 8) // 6
    for i, (val, label) in enumerate(NUMBERS):
        bx = 24 + i * (box_w + 8)
        cv.border(bx, 152, box_w, 38, RULE, 1)
        cv.text(val, bx + box_w // 2, 156, 3, RED, gap=-1, align="center")
        cv.text(label, bx + box_w // 2, 176, 2, INK, gap=-1, align="center")
    # ---- region tabs (counts computed from data)
    counts = {}
    for story in STORIES:
        counts[story[1]] = counts.get(story[1], 0) + 1
    for n, _t in BRIEFS:
        r = brief_region(n)
        counts[r] = counts.get(r, 0) + 1
    tab_order = ["AMERICAS", "EUROPE", "ASIA", "MIDDLE EAST", "AFRICA",
                 "OCEANIA", "GLOBAL"]
    tab_labels = ["%s %d" % (r, counts.get(r, 0)) for r in tab_order]
    total_w = sum(text_width(t, 2, gap=-1) + 20 for t in tab_labels) + 6 * 8
    tx = (1024 - total_w) // 2
    for label in tab_labels:
        w = text_width(label, 2, gap=-1) + 20
        cv.rect(tx, 194, w, 18, INK)
        cv.text(label, tx + 10, 197, 2, PAPER, gap=-1)
        tx += w + 8
    cv.hline(24, 216, 976, INK)
    # ---- feature grid
    # row A: stories 1-3, row B: 4-7, row C: 8-10
    row_a_y, row_a_h = 222, 170
    row_b_y, row_b_h = 400, 152
    row_c_y, row_c_h = 560, 192
    for i, story in enumerate(STORIES[0:3]):
        x = 24 + i * (232 + 10)
        draw_card(cv, x, row_a_y, 232, row_a_h, story)
    for i, story in enumerate(STORIES[3:7]):
        x = 24 + i * (172 + 10)
        draw_card(cv, x, row_b_y, 172, row_b_h, story)
    for i, story in enumerate(STORIES[7:10]):
        x = 24 + i * (232 + 10)
        draw_card(cv, x, row_c_y, 232, row_c_h, story)
    # ---- right rail
    draw_map(cv)
    # region legend
    cv.text("MAP KEY", 756, 372, 2, INK, gap=-1)
    leg = [("AMERICAS", 2), ("EUROPE", 8), ("ASIA", 7), ("MIDEAST", 6),
           ("AFRICA", 3), ("OCEANIA", 2), ("GLOBAL", 2)]
    ly = 390
    for j in range(0, 7, 2):
        cv.text("%s %d" % leg[j], 756, ly, 2, INK, gap=-1)
        if j + 1 < 7:
            cv.text("%s %d" % leg[j + 1], 880, ly, 2, INK, gap=-1)
        ly += 15
    # chip legend
    cy = 452
    cv.text("CHIPS", 756, cy, 2, INK, gap=-1)
    cy += 18
    for chip, meaning in (("CONFIRMED", "FACT"),
                          ("OFFICIALS SAY", "SOURCE"),
                          ("REPORTED", "PRESS"),
                          ("FORECAST", "PLAN")):
        bg, fg = CHIP_STYLE[chip]
        cv.rect(756, cy, 12, 12, bg)
        cv.border(756, cy, 12, 12, fg, 1)
        cv.text(chip + " - " + meaning, 774, cy, 2, INK, gap=-1)
        cy += 20
    # how to read
    hy = 556
    cv.text("HOW TO READ", 756, hy, 2, INK, gap=-1)
    hy += 18
    howto = [
        "NUMBERS 1-30 RUN",
        "THROUGH CARDS, MAP",
        "AND ALSO ON.",
        "CHIPS SHOW HOW",
        "SOLID EACH STORY",
        "IS. DATE CHECK",
        "LISTS EVENTS FROM",
        "OTHER DAYS. EVERY",
        "NUMBERED STORY",
        "HAPPENED ON TUE 24.",
    ]
    for ln in howto:
        cv.text(ln, 756, hy, 2, (52, 52, 52), gap=-1)
        hy += 15
    # ---- bottom bar
    cv.hline(24, 758, 976, INK)
    cv.text("ALSO ON - TUESDAY 24 NOVEMBER", 24, 766, 2, INK, gap=-1)
    # 2 columns x 10 briefs
    for i, (n, text) in enumerate(BRIEFS):
        col = i // 10
        row = i % 10
        bx = 24 + col * 250
        by = 786 + row * 16
        cv.text("%d %s" % (n, text), bx, by, 2, INK, gap=-1)
    # date check
    cv.text("DATE CHECK - NOT TUESDAY 24", 516, 766, 2, DARKRED, gap=-1)
    cv.text("BEFORE TUE 24:", 516, 786, 2, INK, gap=-1)
    dy = 802
    for j in range(0, len(DATE_BEFORE), 2):
        cv.text(DATE_BEFORE[j], 516, dy, 2, (52, 52, 52), gap=-1)
        if j + 1 < len(DATE_BEFORE):
            cv.text(DATE_BEFORE[j + 1], 770, dy, 2, (52, 52, 52), gap=-1)
        dy += 15
    cv.text("NOT YET:", 516, dy + 2, 2, INK, gap=-1)
    dy += 18
    for j in range(0, len(DATE_NEXT), 2):
        cv.text(DATE_NEXT[j], 516, dy, 2, (52, 52, 52), gap=-1)
        if j + 1 < len(DATE_NEXT):
            cv.text(DATE_NEXT[j + 1], 770, dy, 2, (52, 52, 52), gap=-1)
        dy += 15
    # ---- footer
    cv.hline(24, 956, 976, INK)
    cv.text("SOURCES: REUTERS, AP, AFP, YONHAP, XINHUA, KOREA HERALD, TIMES OF ISRAEL,",
            24, 964, 2, (52, 52, 52), gap=-1)
    cv.text("ASHARQ AL-AWSAT, GAVI, KONGSBERG, ACEA, INEGI, UN NEWS, ICBL, NORWEGIAN MOD,",
            24, 980, 2, (52, 52, 52), gap=-1)
    cv.text("POLISH ARMED FORCES, BRUSSELS TIMES, THE TRAVELER, PREMIUM TIMES, VANGUARD.",
            24, 996, 2, (52, 52, 52), gap=-1)


def encode_png(rgb):
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)
        raw += rgb[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        out = struct.pack(">I", len(data)) + typ + data
        out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def main():
    # consistency checks: 30 stories, numbers 1..30, tabs sum to 30
    assert len(STORIES) == 10 and len(BRIEFS) == 20
    nums = [s[0] for s in STORIES] + [b[0] for b in BRIEFS]
    assert sorted(nums) == list(range(1, 31)), "story numbers must be 1..30"
    counts = {}
    for s in STORIES:
        counts[s[1]] = counts.get(s[1], 0) + 1
    for n, _t in BRIEFS:
        r = brief_region(n)
        counts[r] = counts.get(r, 0) + 1
    assert sum(counts.values()) == 30, counts
    assert len(BRIEF_PINS) == 19, "19 brief pins (25 is global, no pin)"
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not outdir:
        outdir = "/output" if os.path.isdir("/output") else "./out"
    os.makedirs(outdir, exist_ok=True)
    cv = Canvas()
    draw(cv)
    data = encode_png(cv.px)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s %d bytes" % (path, len(data)))
    assert len(data) <= 1048576, "entry.png over 1 MiB"


if __name__ == "__main__":
    main()
