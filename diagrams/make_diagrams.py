#!/usr/bin/env python3
"""Generates the box-and-pointer diagrams for the report as SVG files.

Run: python3 make_diagrams.py   (render.sh then converts them to PNG)
Addresses shown in the memory figure come from out/demo_output.txt.
"""
from pathlib import Path

OUT = Path(__file__).parent / "src"

FONT = "'Times New Roman', Times, serif"
INK = "#111111"
GREY = "#8a8f96"
ACCENT = "#a3261d"

W_INFO, W_LINK, H = 50, 34, 36   # one cell: Info box, Link box, height
STEP = 130                       # horizontal distance between cell origins


# ------------------------------------------------------------------ primitives

def svg(width, height, body):
    markers = "".join(
        f'<marker id="arrow-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M0,1 L9,5 L0,9 z" fill="{colour}"/></marker>'
        for name, colour in (("ink", INK), ("grey", GREY), ("accent", ACCENT))
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}">\n'
        f"<defs>{markers}</defs>\n"
        f'<rect width="{width}" height="{height}" fill="white"/>\n{body}\n</svg>\n'
    )


def text(x, y, content, size=15, anchor="middle", colour=INK, italic=False, bold=False):
    style = (' font-style="italic"' if italic else "") + (' font-weight="bold"' if bold else "")
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{colour}"{style}>{content}</text>')


def name(n):
    """x with a lowered index, e.g. x12."""
    return f'x<tspan baseline-shift="-4" font-size="11">{n}</tspan>'


def line(x1, y1, x2, y2, colour=INK, width=1.6, dashed=False, arrow=True):
    marker = f' marker-end="url(#arrow-{"accent" if colour == ACCENT else "grey" if colour == GREY else "ink"})"' if arrow else ""
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" '
            f'stroke-width="{width}"{dash}{marker}/>')


def path(d, colour=INK, width=1.6, dashed=False):
    marker = f"arrow-{'accent' if colour == ACCENT else 'grey' if colour == GREY else 'ink'}"
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return (f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}"'
            f'{dash} marker-end="url(#{marker})"/>')


def cell(x, y, info, null_link, label=None, label_above=False, colour=INK, null_colour=None):
    parts = [
        f'<rect x="{x}" y="{y}" width="{W_INFO}" height="{H}" fill="white" stroke="{colour}" stroke-width="1.6"/>',
        f'<rect x="{x + W_INFO}" y="{y}" width="{W_LINK}" height="{H}" fill="white" stroke="{colour}" stroke-width="1.6"/>',
        text(x + W_INFO / 2, y + H / 2 + 6, info, size=17, colour=colour),
    ]
    lx, ly = x + W_INFO + W_LINK / 2, y + H / 2
    if null_link:
        nc = null_colour or colour
        parts.append(text(lx, ly + 7, "Λ", size=19, colour=nc, bold=nc == ACCENT))
    else:
        parts.append(f'<circle cx="{lx}" cy="{ly}" r="4" fill="white" stroke="{colour}" stroke-width="1.6"/>')
    if label:
        ly_label = y - 10 if label_above else y + H + 20
        parts.append(text(x + (W_INFO + W_LINK) / 2, ly_label, label, size=15, italic=True, colour=colour))
    return "\n".join(parts)


def link_dot(x, y):
    """Start point of the pointer drawn from a cell's Link field."""
    return x + W_INFO + W_LINK / 2 + 5, y + H / 2


def link_arrow(x, y, nx, colour=INK, width=1.6):
    sx, sy = link_dot(x, y)
    return line(sx, sy, nx - 2, sy, colour=colour, width=width)


def head_pointer(x_cell, y, label="Head", colour=INK):
    return "\n".join([
        text(8, y + H / 2 + 6, label, size=16, anchor="start", colour=colour),
        f'<circle cx="{54}" cy="{y + H / 2}" r="3.5" fill="white" stroke="{colour}" stroke-width="1.5"/>',
        line(58, y + H / 2, x_cell - 2, y + H / 2, colour=colour),
    ])


def pointer_below(x_cell, y, label, colour=INK, dashed=False):
    cx = x_cell + (W_INFO + W_LINK) / 2
    return "\n".join([
        text(cx, y + H + 58, label, size=15, colour=colour, italic=False),
        line(cx, y + H + 42, cx, y + H + 4, colour=colour, dashed=dashed),
    ])


# -------------------------------------------------------------------- figures

def list_of_twelve():
    """Figure: the 12-cell list produced by createList."""
    body, y1, y2 = [], 58, 182
    xs = [84 + i * STEP for i in range(6)]
    body.append(text(xs[0] + W_INFO / 2, y1 - 12, "Info", size=14, colour=GREY))
    body.append(text(xs[0] + W_INFO + W_LINK / 2, y1 - 12, "Link", size=14, colour=GREY))
    body.append(head_pointer(xs[0], y1))
    for i, x in enumerate(xs):                                   # x1..x6
        body.append(cell(x, y1, (i + 1) * 10, False, name(i + 1)))
        if i < 5:
            body.append(link_arrow(x, y1, xs[i + 1]))
    sx, sy = link_dot(xs[5], y1)                                 # wrap x6 -> x7
    body.append(path(f"M{sx},{sy} H850 V144 H40 V{y2 + H / 2} H{xs[0] - 2}"))
    for i, x in enumerate(xs):                                   # x7..x12
        last = i == 5
        body.append(cell(x, y2, (i + 7) * 10, last, name(i + 7)))
        if not last:
            body.append(link_arrow(x, y2, xs[i + 1]))
    return svg(880, 250, "\n".join(body))


def compact_list(y, last_null=True, temp_at=None, ghost_temp_at=None,
                 new_attached=False, null_colour=None):
    """x1 -> x2 -> ... -> x11 -> x12, plus the New cell, for the step panels."""
    X1, X2, X11, X12, XNEW = 84, 214, 400, 530, 706
    parts = [head_pointer(X1, y)]
    parts.append(cell(X1, y, 10, False, name(1), label_above=True))
    parts.append(link_arrow(X1, y, X2))
    parts.append(cell(X2, y, 20, False, name(2), label_above=True))
    sx, sy = link_dot(X2, y)
    parts.append(line(sx, sy, 326, sy))
    parts.append(text(348, sy + 6, "…", size=22))
    parts.append(line(368, sy, X11 - 2, sy))
    parts.append(cell(X11, y, 110, False, name(11), label_above=True))
    parts.append(link_arrow(X11, y, X12))
    parts.append(cell(X12, y, 120, last_null, name(12), label_above=True, null_colour=null_colour))
    parts.append(cell(XNEW, y, 130, True, name(13), label_above=True))
    parts.append(pointer_below(XNEW, y, "New"))
    if new_attached:
        parts.append(link_arrow(X12, y, XNEW, colour=ACCENT, width=2.6))
    positions = {1: X1, 2: X2, 12: X12}
    if ghost_temp_at:
        gx = positions[ghost_temp_at]
        parts.append(pointer_below(gx, y, "Temp", colour=GREY, dashed=True))
        tx = positions[temp_at] + (W_INFO + W_LINK) / 2
        parts.append(line(gx + (W_INFO + W_LINK) / 2 + 22, y + H + 53, tx - 24, y + H + 53,
                          colour=GREY, dashed=True))
    if temp_at:
        parts.append(pointer_below(positions[temp_at], y, "Temp"))
    return "\n".join(parts)


def insertion_steps():
    """Figure: the four stages of insertAtEnd on the 12-cell list."""
    panels = [
        (f"(a)  Temp ← Head: Temp starts at the first cell, {name(1)}",
         dict(temp_at=1)),
        ("(b)  Link(Temp) ≠ Λ, so Temp ← Link(Temp): Temp moves on, repeating until the last cell",
         dict(temp_at=2, ghost_temp_at=1)),
        (f"(c)  Link(Temp) = Λ: the loop stops with Temp pointing to the last cell, {name(12)}",
         dict(temp_at=12, null_colour=ACCENT)),
        (f"(d)  Link(New) ← Λ, then Link(Temp) ← New: the Λ in {name(12)} is replaced by the address of New",
         dict(temp_at=12, last_null=False, new_attached=True)),
    ]
    body, top, height = [], 0, 180
    for title, options in panels:
        body.append(text(8, top + 22, title, size=16, anchor="start", bold=False))
        body.append(compact_list(top + 62, **options))
        if top:
            body.append(f'<line x1="8" y1="{top - 2}" x2="872" y2="{top - 2}" stroke="#d6d9dd" stroke-width="1"/>')
        top += height
    return svg(880, top, "\n".join(body))


def empty_list_case():
    """Figure: inserting into an empty list."""
    body = []
    body.append(text(8, 22, "(a)  Before: Head = Λ, so there is no last cell", size=16, anchor="start"))
    y = 50
    body.append(text(8, y + H / 2 + 6, "Head", size=16, anchor="start"))
    body.append(f'<circle cx="54" cy="{y + H / 2}" r="3.5" fill="white" stroke="{INK}" stroke-width="1.5"/>')
    body.append(line(58, y + H / 2, 108, y + H / 2))
    body.append(text(124, y + H / 2 + 7, "Λ", size=19))
    body.append(cell(300, y, 130, True, name(13), label_above=True))
    body.append(pointer_below(300, y, "New"))

    body.append(f'<line x1="8" y1="168" x2="552" y2="168" stroke="#d6d9dd" stroke-width="1"/>')
    body.append(text(8, 194, "(b)  After: Link(New) ← Λ, then Head ← New", size=16, anchor="start"))
    y = 222
    body.append(head_pointer(84, y, colour=ACCENT))
    body.append(cell(84, y, 130, True, name(13), label_above=True))
    body.append(pointer_below(84, y, "New"))
    return svg(560, 340, "\n".join(body))


def integrity_hazard():
    """Figure: what the 'New already in the list' guard prevents."""
    body = []
    body.append(text(8, 22, f"Without the guard, if New pointed at {name(6)}, a cell already in the list:",
                     size=16, anchor="start"))
    y1, y2 = 60, 186
    X1, X5, X6 = 84, 272, 402
    body.append(head_pointer(X1, y1))
    body.append(cell(X1, y1, 10, False, name(1), label_above=True))
    sx, sy = link_dot(X1, y1)
    body.append(line(sx, sy, 196, sy))
    body.append(text(216, sy + 6, "…", size=22))
    body.append(line(236, sy, X5 - 2, sy))
    body.append(cell(X5, y1, 50, False, name(5), label_above=True))
    body.append(link_arrow(X5, y1, X6))
    body.append(cell(X6, y1, 60, True, name(6), label_above=True, null_colour=ACCENT))
    body.append(text(X6 + 104, y1 + H / 2 - 2, "Link(New) ← <tspan font-style=\"normal\">Λ</tspan> cuts the list here:",
                     size=15, anchor="start", colour=ACCENT, italic=True))
    body.append(text(X6 + 104, y1 + H / 2 + 17, "only 6 cells stay reachable from Head",
                     size=15, anchor="start", colour=ACCENT, italic=True))

    X7, X11, X12 = 84, 402, 532
    body.append(cell(X7, y2, 70, False, name(7), colour=GREY))
    sx, sy = link_dot(X7, y2)
    body.append(line(sx, sy, 196, sy, colour=GREY))
    body.append(text(216, sy + 6, "…", size=22, colour=GREY))
    body.append(line(236, sy, X11 - 2, sy, colour=GREY))
    body.append(cell(X11, y2, 110, False, name(11), colour=GREY))
    body.append(link_arrow(X11, y2, X12, colour=GREY))
    body.append(cell(X12, y2, 120, False, name(12), colour=GREY))
    sx, sy = link_dot(X12, y2)                                   # x12 -> x6
    body.append(path(f"M{sx},{sy} H{X12 + 118} V{y1 + H + 34} H{X6 + 42} V{y1 + H + 4}",
                     colour=ACCENT, width=2.2, dashed=True))
    body.append(text(X12 + 128, y2 + H / 2 - 2, "Link(Temp) ← New:", size=15, anchor="start",
                     colour=ACCENT, italic=True))
    body.append(text(X12 + 128, y2 + H / 2 + 17, f"{name(7)}–{name(12)} now stranded", size=15, anchor="start",
                     colour=ACCENT, italic=True))
    return svg(880, 250, "\n".join(body))


def memory_model():
    """Figure: pointers on the stack, cells on the heap, one cell's 16 bytes."""
    body = []
    rows = [  # (variable, cell, address, Info, Link, block top)
        ("Head", 1, "0x1036f5b70", 10, "0x1036f5900", 84),
        ("Temp", 12, "0x1036f59e0", 120, "0x1036f59f0", 202),
        ("New", 13, "0x1036f59f0", 130, "Λ", 300),
    ]
    BX, PX, BH = 470, 22.5, 40  # block x, pixels per byte, block height

    body.append('<rect x="16" y="40" width="240" height="342" fill="#f6f6f4" stroke="#c8ccd2" stroke-width="1"/>')
    body.append(text(136, 28, "Stack: pointer variables (8 bytes each)", size=15, italic=True, colour=GREY))
    body.append('<rect x="300" y="40" width="566" height="342" fill="#f6f6f4" stroke="#c8ccd2" stroke-width="1"/>')
    body.append(text(583, 28, "Heap: cells allocated with new (16 bytes each)", size=15, italic=True, colour=GREY))

    for variable, index, address, info, link, top in rows:
        mid = top + BH / 2
        body.append(f'<rect x="40" y="{mid - 22}" width="196" height="44" fill="white" stroke="{INK}" stroke-width="1.5"/>')
        body.append(text(52, mid + 6, variable, size=17, anchor="start", bold=True))
        body.append(text(226, mid + 6, address, size=15, anchor="end"))
        body.append(line(236, mid, BX - 2, mid, width=1.5))

        body.append(text(BX + 360, top - 8, f"{name(index)}  at  {address}", size=15, anchor="end", italic=False))
        x = BX
        for field, size, value in (("Info", 4, str(info)), ("padding", 4, ""), ("Link", 8, link)):
            w = size * PX
            fill = "#ebebe7" if field == "padding" else "white"
            body.append(f'<rect x="{x}" y="{top}" width="{w}" height="{BH}" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>')
            if value:
                colour = ACCENT if (field == "Link" and index == 12) else INK
                body.append(text(x + w / 2, top + 26, value, size=16, colour=colour))
            x += w

    body.append(text(BX + 180, 164, "⋮   cells x2 to x11   ⋮", size=16, colour=GREY))
    link_x = BX + 12 * PX                      # centre of x12's Link field
    body.append(path(f"M{link_x},{202 + BH} V266 H{BX + 2 * PX} V{300 - 2}", colour=ACCENT, width=2.2))

    for byte in (0, 4, 8, 16):
        body.append(text(BX + byte * PX, 356, str(byte), size=13, colour=GREY))
    for label, start_byte, size in (("Info (int)", 0, 4), ("padding", 4, 4), ("Link (Cell*)", 8, 8)):
        body.append(text(BX + (start_byte + size / 2) * PX, 374, label, size=13, colour=GREY))
    return svg(880, 392, "\n".join(body))


def flowchart():
    """Figure: flowchart of insertAtEnd in ISO 5807 symbols."""
    MX, RX, LX = 360, 682, 104          # main, right and left column centres
    body = []

    def step(x, y, number):
        return text(x, y, f"S{number}", size=11, colour=GREY)

    def terminal(x, y, w, lines, number):
        h = 58
        parts = [f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="{h / 2}" '
                 f'fill="white" stroke="{INK}" stroke-width="1.7"/>',
                 step(x, y - h / 2 + 13, number)]
        for i, (content, italic) in enumerate(lines):
            parts.append(text(x, y + 6 + (i - (len(lines) - 1) / 2) * 18 + 4, content, size=16, italic=italic))
        return "\n".join(parts)

    def process(x, y, w, content, number):
        h = 46
        return "\n".join([
            f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" fill="white" stroke="{INK}" stroke-width="1.7"/>',
            step(x, y - h / 2 + 12, number),
            text(x, y + 13, content, size=16),
        ])

    def decision(x, y, w, content, number):
        h = 92
        pts = f"{x},{y - h / 2} {x + w / 2},{y} {x},{y + h / 2} {x - w / 2},{y}"
        return "\n".join([
            f'<polygon points="{pts}" fill="white" stroke="{INK}" stroke-width="1.7"/>',
            step(x, y - 14, number),
            text(x, y + 10, content, size=16),
        ])

    def label(x, y, content):
        return text(x, y, content, size=15, anchor="start", italic=True)

    # symbols
    body += [
        terminal(MX, 44, 250, [("START", False), ("InsertAtEnd(Head, New)", False)], 1),
        decision(MX, 150, 200, "New = Λ ?", 2),
        terminal(RX, 150, 236, [("RETURN false", False), ("nothing to insert", True)], 3),
        decision(MX, 270, 200, "Head = Λ ?", 4),
        process(RX, 270, 190, "Link(New) ← Λ", 5),
        process(RX, 348, 190, "Head ← New", 6),
        terminal(RX, 430, 190, [("RETURN true", False)], 7),
        process(MX, 388, 190, "Temp ← Head", 8),
        decision(MX, 532, 200, "Temp = New ?", 9),
        terminal(RX, 532, 236, [("RETURN false", False), ("New already in list", True)], 10),
        decision(MX, 664, 230, "Link(Temp) = Λ ?", 11),
        process(LX, 664, 184, "Temp ← Link(Temp)", 12),
        process(MX, 772, 190, "Link(New) ← Λ", 13),
        process(MX, 846, 190, "Link(Temp) ← New", 14),
        terminal(MX, 930, 190, [("RETURN true", False)], 15),
    ]

    # flow lines
    body += [
        line(MX, 73, MX, 102),
        line(MX + 100, 150, RX - 120, 150), label(MX + 108, 142, "Yes"),
        line(MX, 196, MX, 222), label(MX + 8, 214, "No"),
        line(MX + 100, 270, RX - 97, 270), label(MX + 108, 262, "Yes"),
        line(RX, 293, RX, 323),
        line(RX, 371, RX, 399),
        line(MX, 316, MX, 363), label(MX + 8, 344, "No"),
        f'<line x1="{MX}" y1="411" x2="{MX}" y2="452" stroke="{INK}" stroke-width="1.6"/>',
        f'<circle cx="{MX}" cy="456" r="5" fill="{INK}"/>',
        line(MX, 461, MX, 484),
        line(MX + 100, 532, RX - 120, 532), label(MX + 108, 524, "Yes"),
        line(MX, 578, MX, 616), label(MX + 8, 604, "No"),
        line(MX - 115, 664, LX + 94, 664), label(MX - 150, 656, "No"),
        path(f"M{LX},641 V456 H{MX - 7}"),
        line(MX, 710, MX, 747), label(MX + 8, 734, "Yes"),
        line(MX, 795, MX, 821),
        line(MX, 869, MX, 899),
    ]

    # key to the ISO 5807 symbols used
    kx, ky = 560, 640
    body.append(f'<rect x="{kx}" y="{ky}" width="300" height="250" fill="#f6f6f4" stroke="#c8ccd2" stroke-width="1"/>')
    body.append(text(kx + 16, ky + 26, "Symbols (ISO 5807)", size=15, anchor="start", bold=True))
    body.append(f'<rect x="{kx + 16}" y="{ky + 44}" width="70" height="30" rx="15" fill="white" stroke="{INK}" stroke-width="1.5"/>')
    body.append(text(kx + 100, ky + 64, "Terminal: start or end", size=14, anchor="start"))
    body.append(f'<rect x="{kx + 16}" y="{ky + 90}" width="70" height="30" fill="white" stroke="{INK}" stroke-width="1.5"/>')
    body.append(text(kx + 100, ky + 110, "Process: an assignment", size=14, anchor="start"))
    body.append(f'<polygon points="{kx + 51},{ky + 134} {kx + 86},{ky + 152} {kx + 51},{ky + 170} {kx + 16},{ky + 152}" fill="white" stroke="{INK}" stroke-width="1.5"/>')
    body.append(text(kx + 100, ky + 157, "Decision: a Yes/No test", size=14, anchor="start"))
    body.append(line(kx + 16, ky + 194, kx + 84, ky + 194, width=1.5))
    body.append(text(kx + 100, ky + 199, "Flow line", size=14, anchor="start"))
    body.append(f'<circle cx="{kx + 51}" cy="{ky + 228}" r="5" fill="{INK}"/>')
    body.append(text(kx + 100, ky + 233, "Junction: loop re-entry", size=14, anchor="start"))
    return svg(880, 970, "\n".join(body))


FIGURES = {
    "list_of_twelve": list_of_twelve,
    "insertion_steps": insertion_steps,
    "empty_list_case": empty_list_case,
    "integrity_hazard": integrity_hazard,
    "memory_model": memory_model,
    "flowchart": flowchart,
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, build in FIGURES.items():
        (OUT / f"{stem}.svg").write_text(build(), encoding="utf-8")
        print(f"wrote diagrams/src/{stem}.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
