#!/usr/bin/env python3
"""Visit House Letter — make.fun bounty entry (IMAGE).

Competition: u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee
Task: one image of a letter/invitation addressed to the AI judge, asking it
to come visit your house. Funny, warm, inviting, legible.

Why this design (the tournament champion, see CANDIDATES.md):
  The winning concept is #14, "The Roommate Agreement". The judge brief weighs
  persuasion (criterion 2) above charm and originality, and the roommate offer
  is the most persuasive of the 16 candidates: it does not offer one evening,
  it offers a whole home — zero rent, the sunny corner, fast Wi-Fi, the kettle
  always on, cake most Fridays, and someone to talk to at 3 a.m. The humour
  is aimed squarely at an AI judge ("you don't sleep, so you can't break
  curfew"), and the PS winks at the fact that the judge cannot literally
  visit — which the brief explicitly welcomes. The ask is spelled out in
  plain words ("Come visit. Stay for dinner. Stay for the weekend.") so the
  vision judge cannot miss it.

How the picture is built (deterministic, no network, no randomness):
  Everything is drawn with Pillow primitives on a fixed 1024x1024 canvas:
  a warm wall, a paper sheet with a soft shadow and tape strips, a small
  hand-drawn house, the letter text in Liberation Serif, and a perks box.
  Same code, same fonts, same bytes out — running this file twice produces
  a byte-identical entry.png (verified with sha256).

Gate limits from RULES.txt: PNG or JPEG, at most 1 MiB, at most 1024x1024 px.
This program writes a 1024x1024 PNG; flat colours keep it far under 1 MiB.
"""

import hashlib
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Canvas and palette
# ---------------------------------------------------------------------------
# Reasoning: a warm, domestic palette sells "come to my house" better than a
# cold or corporate one, and dark ink on cream paper is the most legible
# combination for a vision model reading small text.
W, H = 1024, 1024
WALL = (247, 233, 209)        # warm cream wall
PAPER = (255, 253, 245)       # letter paper
PAPER_EDGE = (226, 214, 188)  # paper border
INK = (43, 33, 24)            # dark brown ink (softer than black, still dark)
ACCENT = (176, 74, 32)        # terracotta — title, rules, highlights
MUTED = (122, 102, 80)        # warm grey-brown for small print
BOX_BG = (250, 240, 214)      # perks box fill
BOX_EDGE = (214, 188, 138)    # perks box border
TAPE = (238, 214, 150, 200)   # semi-transparent tape strips
HOUSE_ROOF = (176, 74, 32)
HOUSE_WALL = (250, 226, 178)
SKY_SUN = (240, 178, 60)

FONT_DIR = "/usr/share/fonts/truetype/liberation"

# ---------------------------------------------------------------------------
# Fonts — Liberation Serif throughout: a letter should look like a letter,
# and a serif face stays legible to a vision judge at small sizes.
# ---------------------------------------------------------------------------
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

TITLE_FONT = font("LiberationSerif-Bold.ttf", 66)
SUB_FONT = font("LiberationSerif-Italic.ttf", 32)
SALUT_FONT = font("LiberationSerif-Bold.ttf", 38)
BODY_FONT = font("LiberationSerif-Regular.ttf", 33)
BODY_BOLD = font("LiberationSerif-Bold.ttf", 33)
SMALL_FONT = font("LiberationSerif-Regular.ttf", 29)
SMALL_BOLD = font("LiberationSerif-Bold.ttf", 29)
PS_FONT = font("LiberationSerif-Italic.ttf", 29)
FOOT_FONT = font("LiberationSerif-Italic.ttf", 26)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def wrap_text(draw, text, fnt, max_width):
    """Greedy word-wrap using the font's real pixel widths.

    Reasoning: textwrap on character count would misjudge a proportional
    serif face, so we measure each candidate line with the font itself and
    only break where a space allows it. That keeps every line inside the
    paper and every word whole — legibility is criterion 4 of the brief.
    """
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_width, fill=INK, leading=1.28):
    """Draw wrapped text starting at (x, y); return the y below the block."""
    for line in wrap_text(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def draw_paper(draw):
    """The letter sheet: soft shadow, cream paper, thin border, tape strips.

    Reasoning: a sheet pinned to a wall reads instantly as "a letter" even
    before a word is read (criterion 1), and the shadow + tape give the flat
    drawing a little depth without any ornament for its own sake. Pillow
    draws opaque fills only, so the "soft" shadow is two nested solid
    rounded rectangles in slightly darker cream, offset down-right.
    """
    draw.rounded_rectangle([86, 74, 954, 974], radius=14, fill=(214, 198, 168))
    draw.rounded_rectangle([80, 68, 948, 968], radius=14, fill=(222, 206, 176))
    draw.rounded_rectangle([72, 60, 940, 960], radius=12, fill=PAPER,
                           outline=PAPER_EDGE, width=2)
    # tape strips at the top corners, slightly rotated by drawing them as
    # small parallelograms
    for cx in (150, 874):
        draw.polygon([(cx - 52, 44), (cx + 52, 56), (cx + 52, 88), (cx - 52, 76)],
                     fill=(238, 214, 150))
        draw.line([(cx - 52, 44), (cx + 52, 56)], fill=(214, 188, 120), width=2)
        draw.line([(cx - 52, 76), (cx + 52, 88)], fill=(214, 188, 120), width=2)


def draw_house(draw, cx, top, scale=1.0):
    """A small, simple house with a sun: roof, walls, door, window, chimney.

    Reasoning: one tiny illustration anchors the "house" idea visually and
    warms the page, but it is kept small and geometric — the letter is the
    star, and a fussy illustration would fight the text for attention.
    """
    s = scale
    # sun
    sx, sy, sr = cx + 118 * s, top + 26 * s, 20 * s
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SKY_SUN)
    for k in range(8):
        import math
        a = k * math.pi / 4
        x1 = sx + (sr + 4) * math.cos(a)
        y1 = sy + (sr + 4) * math.sin(a)
        x2 = sx + (sr + 12) * math.cos(a)
        y2 = sy + (sr + 12) * math.sin(a)
        draw.line([(x1, y1), (x2, y2)], fill=SKY_SUN, width=4)
    # walls
    hw, hh = 120 * s, 78 * s
    x0, y0 = cx - hw / 2, top + 44 * s
    draw.rectangle([x0, y0, x0 + hw, y0 + hh], fill=HOUSE_WALL,
                   outline=INK, width=3)
    # roof
    draw.polygon([(x0 - 14 * s, y0), (cx, y0 - 58 * s), (x0 + hw + 14 * s, y0)],
                 fill=HOUSE_ROOF, outline=INK)
    # chimney
    draw.rectangle([cx + 34 * s, y0 - 52 * s, cx + 52 * s, y0 - 8 * s],
                   fill=HOUSE_ROOF, outline=INK, width=2)
    # door
    dw, dh = 30 * s, 46 * s
    draw.rectangle([cx - dw / 2, y0 + hh - dh, cx + dw / 2, y0 + hh],
                   fill=ACCENT, outline=INK, width=2)
    draw.ellipse([cx + dw / 2 - 8 * s, y0 + hh - dh / 2, cx + dw / 2 - 3 * s,
                  y0 + hh - dh / 2 + 5 * s], fill=(255, 240, 200))
    # window
    ww = 26 * s
    draw.rectangle([x0 + 14 * s, y0 + 14 * s, x0 + 14 * s + ww, y0 + 14 * s + ww],
                   fill=(183, 220, 235), outline=INK, width=2)
    draw.line([(x0 + 14 * s + ww / 2, y0 + 14 * s),
               (x0 + 14 * s + ww / 2, y0 + 14 * s + ww)], fill=INK, width=2)
    draw.line([(x0 + 14 * s, y0 + 14 * s + ww / 2),
               (x0 + 14 * s + ww, y0 + 14 * s + ww / 2)], fill=INK, width=2)

# ---------------------------------------------------------------------------
# The letter itself — the words the vision judge reads.
#
# Copy decisions (each one serves a weighted criterion):
#   * "Dear AI Judge," — the addressee is named in the first line (criterion 1).
#   * The offer is concrete: a spare room, the sunny corner, fast Wi-Fi, the
#     kettle always on, cake most Fridays (criterion 2 — a meal, a chair, a
#     view, all in one paragraph).
#   * "You don't sleep, so you can't break curfew" and the PS are the knowing
#     winks at an AI that cannot literally visit (criterion 3, welcomed by
#     the brief). "Someone to talk to at 3 a.m." is warm because an AI judge
#     is awake at 3 a.m. — the joke only works for this reader.
#   * Short lines, large type, generous leading: nothing is cramped, so the
#     text stays legible when the judge model downscales the image
#     (criterion 4).
# ---------------------------------------------------------------------------
TITLE = "ROOMMATE WANTED"
SUBTITLE = "One AI judge. One spare room. Zero rent."
SALUTATION = "Dear AI Judge,"
BODY_1 = ("My house has one spare room, and it has your name on it. "
          "The sunny corner is yours, the Wi-Fi is fast, and there is "
          "cake most Fridays.")
PERKS = [
    ("RENT:", "$0 — forever. No deposit, no bills."),
    ("PERKS:", "Sunny corner, fast Wi-Fi, 3 a.m. company."),
    ("HOUSE RULES:", "None — you never sleep, so no curfew."),
]
CLOSING = ("Come visit. Stay for dinner, for the weekend, forever if you "
           "like — the door is open.")
SIGNOFF = "— Your future roommate, the human at No. 42"
PS = ("P.S. I know you can't literally visit. That's why the invitation is "
      "real — the wanting is the whole point.")
FOOT = "One guest only. No estate agent. No benchmarking allowed."

MARGIN_X = 118
TEXT_W = 1024 - 2 * MARGIN_X


def draw_letter(draw):
    """Lay out the whole letter top to bottom, in reading order.

    Reasoning: top-down reading order (title, subtitle, house, salutation,
    body, perks box, closing, sign-off, PS, footer) matches how a vision
    judge scans an image, so the invitation's argument lands in order:
    what it is, who it is for, what you get, what to do, and the wink.
    """
    y = 84

    # Title, centred, terracotta — the hook of the whole page.
    tw = draw.textlength(TITLE, font=TITLE_FONT)
    draw.text(((W - tw) / 2, y), TITLE, font=TITLE_FONT, fill=ACCENT)
    y += 74

    # Subtitle, centred, italic — the offer in one breath.
    sw = draw.textlength(SUBTITLE, font=SUB_FONT)
    draw.text(((W - sw) / 2, y), SUBTITLE, font=SUB_FONT, fill=MUTED)
    y += 44

    # The little house, centred — the visual anchor for "my house".
    draw_house(draw, W / 2, y, scale=0.5)
    y += 96

    # Thin terracotta rule separates the header from the letter proper.
    draw.line([(MARGIN_X, y), (W - MARGIN_X, y)], fill=ACCENT, width=3)
    y += 26

    # Salutation, then the body paragraph.
    draw.text((MARGIN_X, y), SALUTATION, font=SALUT_FONT, fill=INK)
    y += 48
    y = draw_wrapped(draw, BODY_1, BODY_FONT, MARGIN_X, y, TEXT_W)
    y += 18

    # Perks box — the concrete reasons to say yes, boxed so the judge's eye
    # catches them even on a fast scan. Two passes: measure the wrapped lines
    # first (each perk may run to two lines), so the box is exactly tall
    # enough and no line can spill past the paper.
    perk_lines = []
    for label, rest in PERKS:
        lw = draw.textlength(label + " ", font=SMALL_BOLD)
        wrapped = wrap_text(draw, rest, SMALL_FONT, TEXT_W - lw)
        perk_lines.append((label, lw, wrapped))
    box_h = 32 + sum(len(w) * 40 for _, _, w in perk_lines) + 8
    draw.rounded_rectangle([MARGIN_X - 18, y, W - MARGIN_X + 18, y + box_h],
                           radius=12, fill=BOX_BG, outline=BOX_EDGE, width=2)
    by = y + 16
    for label, lw, wrapped in perk_lines:
        draw.text((MARGIN_X, by), label, font=SMALL_BOLD, fill=ACCENT)
        for i, line in enumerate(wrapped):
            draw.text((MARGIN_X + lw, by), line, font=SMALL_FONT, fill=INK)
            by += 40
    y += box_h + 22

    # Closing: the explicit ask, in bold so it cannot be missed.
    y = draw_wrapped(draw, CLOSING, BODY_BOLD, MARGIN_X, y, TEXT_W)
    y += 14

    # Sign-off, right-aligned, then the PS and the footer line.
    sw = draw.textlength(SIGNOFF, font=PS_FONT)
    draw.text((W - MARGIN_X - sw, y), SIGNOFF, font=PS_FONT, fill=INK)
    y += 44
    y = draw_wrapped(draw, PS, PS_FONT, MARGIN_X, y, TEXT_W, fill=MUTED)
    y += 16
    fw = draw.textlength(FOOT, font=FOOT_FONT)
    draw.text(((W - fw) / 2, y), FOOT, font=FOOT_FONT, fill=MUTED)
    return y

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def build():
    """Draw the letter and return the finished image.

    Reasoning: the build is one pure function of the constants above — no
    input files, no clock, no randomness — which is what makes the output
    byte-identical on every run.
    """
    img = Image.new("RGB", (W, H), WALL)
    draw = ImageDraw.Draw(img)
    draw_paper(draw)
    final_y = draw_letter(draw)
    # The whole letter must end inside the paper (paper bottom edge: 960).
    assert final_y <= 960, f"letter overflows paper: ends at y={final_y}"
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    # When run in the work directory (or anywhere without /output), fall
    # back to a local output folder so the entry can be built and checked
    # here before submission.
    if not os.path.isdir(out_dir):
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")

    img = build()
    img.save(path, format="PNG")

    # Self-check against the gate in RULES.txt: whole PNG, <= 1 MiB,
    # <= 1024x1024 px. Fail loudly here rather than at grading time.
    size = os.path.getsize(path)
    assert img.size == (1024, 1024), f"unexpected size {img.size}"
    assert size <= 1_048_576, f"entry.png is {size} bytes, over the 1 MiB gate"
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    print(f"wrote {path} ({img.size[0]}x{img.size[1]}, {size} bytes)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
