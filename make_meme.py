#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 entry meme: a make.fun air boarding pass,
LOS SANTOS -> LEONIDA, delayed 13 years. Document parody drawn with PIL;
the make.fun ghost mark (official press kit) is the airline logo and the
pass stub art, worked into the document itself.
Output: meme.png (1200x1200, square so the judge sees it at 480x480).
"""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1200
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
MARK = "assets/mark-1024.png"
OUT = "meme.png"

INK = (20, 33, 61)
GRAY = (110, 118, 135)
MAGENTA = (216, 27, 140)
STAMP_RED = (217, 4, 41)


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def background():
    """Vice City sunset: purple -> magenta -> orange, with a low sun."""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top, mid, bot = (43, 16, 85), (178, 24, 120), (255, 122, 61)
    for y in range(H):
        t = y / H
        c = lerp(top, mid, t * 1.6) if t < 0.62 else lerp(mid, bot, (t - 0.62) / 0.38)
        d.line([(0, y), (W, y)], fill=c)
    # sun disc with retro slats, low on the horizon
    sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun)
    sd.ellipse([330, 120, 870, 660], fill=(255, 190, 90, 255))
    for i, yy in enumerate(range(430, 660, 34)):
        sd.rectangle([330, yy, 870, yy + 10 + i * 3], fill=(0, 0, 0, 0))
    sun = sun.filter(ImageFilter.GaussianBlur(1))
    img.paste(sun, (0, 0), sun)
    return img


def rounded_pass(img):
    """White boarding pass with soft shadow, centered on the sunset."""
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([62, 232, 1162, 1032], 28, fill=(10, 0, 20, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    img.paste(shadow, (0, 0), shadow)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([50, 210, 1150, 1010], 28, fill=(255, 255, 255))
    return d


def paste_mark(img, cx, cy, size):
    mark = Image.open(MARK).convert("RGBA").resize((size, size), Image.LANCZOS)
    img.paste(mark, (cx - size // 2, cy - size // 2), mark)


def field(d, x, y, label, value, vsize=52):
    d.text((x, y), label, font=font(SANS, 25), fill=GRAY)
    d.text((x, y + 32), value, font=font(SANS, vsize), fill=INK)


def main():
    img = background()
    d = rounded_pass(img)

    # header band: magenta, ghost logo + airline name, worked into the pass
    d.rounded_rectangle([50, 210, 1150, 342], 28, fill=MAGENTA)
    d.rectangle([50, 300, 1150, 342], fill=MAGENTA)
    paste_mark(img, 134, 276, 112)
    d = ImageDraw.Draw(img)
    d.text((208, 242), "make.fun air", font=font(SANS, 58), fill=(255, 255, 255))
    bp = "BOARDING PASS"
    f = font(SANS, 42)
    tw = d.textlength(bp, font=f)
    d.text((1120 - tw, 250), bp, font=f, fill=(255, 255, 255))

    # route, huge: the joke's first read
    d.text((92, 366), "LOS SANTOS", font=font(SANS, 86), fill=INK)
    d.text((92, 458), "→ LEONIDA", font=font(SANS, 86), fill=INK)
    d.text((94, 558), "VICE CITY INTL · TERMINAL VI", font=font(SANS, 29), fill=GRAY)

    # fields
    field(d, 92, 612, "FLIGHT", "GTA VI")
    field(d, 360, 612, "DEPARTS", "2013")
    field(d, 590, 612, "ARRIVES", "2026")
    field(d, 92, 730, "PASSENGER", "EVERY GTA FAN", vsize=48)

    # perforated stub: dashed line, big ghost, seat, barcode
    for y in range(362, 990, 26):
        d.line([(880, y), (880, y + 14)], fill=(190, 196, 208), width=4)
    paste_mark(img, 1015, 448, 196)
    d = ImageDraw.Draw(img)
    for txt, yy, sz in [("SEAT 6A", 562, 46), ("GATE 6", 620, 36)]:
        f = font(SANS, sz)
        tw = d.textlength(txt, font=f)
        d.text((1015 - tw / 2, yy), txt, font=f, fill=INK)
    rng = random.Random(6)
    x = 922
    while x < 1100:
        bw = rng.choice([3, 5, 8, 12])
        d.rectangle([x, 686, x + bw, 794], fill=INK)
        x += bw + rng.choice([4, 6, 9])
    f = font(MONO, 24)
    code = "GTA6-2013-2026"
    tw = d.textlength(code, font=f)
    d.text((1015 - tw / 2, 806), code, font=f, fill=GRAY)
    for txt, yy in [("Carry-on: 150 GB", 852), ("No refunds", 888)]:
        f2 = font(SANS_R, 28)
        tw2 = d.textlength(txt, font=f2)
        d.text((1015 - tw2 / 2, yy), txt, font=f2, fill=GRAY)

    # red delay stamp in its own band at the foot of the pass, the punchline
    stamp = Image.new("RGBA", (600, 150), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([6, 6, 594, 144], 14, outline=STAMP_RED + (220,), width=9)
    sf = font(SANS, 58)
    st = "DELAYED 13 YEARS"
    tw = sd.textlength(st, font=sf)
    sd.text(((600 - tw) / 2, 42), st, font=sf, fill=STAMP_RED + (220,))
    stamp = stamp.rotate(8, resample=Image.BICUBIC, expand=True)
    img.paste(stamp, (140, 780), stamp)

    img.save(OUT)
    print(f"wrote {OUT} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
