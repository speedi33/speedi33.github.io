#!/usr/bin/env python3
"""
GIMP Python-Fu Script: Expedition Packraft Design
Ausführen in GIMP über: Filter > Script-Fu > Konsole
Dann: exec(open('/pfad/zu/expedition_packraft_design.py').read())

Oder über: Filter > Python-Fu > Konsole
Dann: exec(open('/pfad/zu/expedition_packraft_design.py').read())
"""

from gimpfu import *
import math

# ── Farben ──────────────────────────────────────────────────────────────────
GOLD        = (0xC8, 0x9F, 0x3C)   # #C89F3C  – Wellen, Paddel, Text "PACKRAFT"
PETROL      = (0x35, 0x7A, 0x8C)   # #357A8C  – Kompassring, N/S/E/W
BLUE_LIGHT  = (0x4A, 0x9B, 0xBA)   # #4A9BBA  – blauer Kompassstern (hell)
BLUE_DARK   = (0x2E, 0x6E, 0x85)   # #2E6E85  – blauer Kompassstern (dunkel)
WHITE       = (0xFF, 0xFF, 0xFF)   # Text "EXPEDITION"
BG          = (0x0A, 0x0A, 0x0E)   # #0A0A0E  – fast Schwarz

# ── Bildgröße ───────────────────────────────────────────────────────────────
W, H = 1000, 1200   # Pixel

def rgb(r, g, b):
    """Hilfsfunktion: setzt Vordergrundfarbe."""
    gimp.context_set_foreground((r, g, b))

def draw_filled_ellipse(drawable, cx, cy, rx, ry, color):
    rgb(*color)
    gimp.image_select_ellipse(
        drawable.image, CHANNEL_OP_REPLACE,
        cx - rx, cy - ry, 2 * rx, 2 * ry
    )
    gimp.edit_fill(drawable, FILL_FOREGROUND)
    gimp.selection_none(drawable.image)

def draw_circle_outline(drawable, cx, cy, r, lw, color):
    """Zeichnet einen Kreisring (durch zwei übereinanderliegende Ellipsen)."""
    outer = r + lw // 2
    inner = r - lw // 2
    rgb(*color)
    gimp.image_select_ellipse(
        drawable.image, CHANNEL_OP_REPLACE,
        cx - outer, cy - outer, 2 * outer, 2 * outer
    )
    gimp.image_select_ellipse(
        drawable.image, CHANNEL_OP_SUBTRACT,
        cx - inner, cy - inner, 2 * inner, 2 * inner
    )
    gimp.edit_fill(drawable, FILL_FOREGROUND)
    gimp.selection_none(drawable.image)

def draw_polygon(drawable, points, color):
    """Füllt ein Polygon anhand einer Liste von (x,y)-Punkten."""
    rgb(*color)
    vectors = gimp.vectors_new(drawable.image, "tmp")
    stroke_id = gimp.vectors_bezier_stroke_new(
        vectors,
        [coord for pt in points for coord in (pt[0], pt[1], pt[0], pt[1], pt[0], pt[1])],
        len(points) * 6,
        True
    )
    gimp.image_insert_vectors(drawable.image, vectors, None, -1)
    pdb.gimp_image_set_active_vectors(drawable.image, vectors)
    pdb.gimp_vectors_to_selection(vectors, CHANNEL_OP_REPLACE, True, False, 0, 0)
    gimp.edit_fill(drawable, FILL_FOREGROUND)
    gimp.selection_none(drawable.image)
    gimp.image_remove_vectors(drawable.image, vectors)

def draw_compass(drawable, cx, cy, r):
    """Zeichnet den kompletten Kompass."""
    # ── Kreisring ──
    draw_circle_outline(drawable, cx, cy, r, 6, PETROL)

    # ── Kreuzlinien (N-S und E-W Hilfslinien) ──
    lw = 3
    rgb(*PETROL)
    pdb.gimp_image_select_rectangle(
        drawable.image, CHANNEL_OP_REPLACE,
        cx - lw//2, cy - r - 30, lw, 2*r + 60
    )
    gimp.edit_fill(drawable, FILL_FOREGROUND)
    pdb.gimp_image_select_rectangle(
        drawable.image, CHANNEL_OP_REPLACE,
        cx - r - 30, cy - lw//2, 2*r + 60, lw
    )
    gimp.edit_fill(drawable, FILL_FOREGROUND)
    gimp.selection_none(drawable.image)

    # ── 45°-Diagonallinien (kürzere Markierungen) ──
    diag = int(r * 0.55)
    for angle_deg in [45, 135, 225, 315]:
        ang = math.radians(angle_deg)
        x0 = int(cx + math.cos(ang) * (r - 20))
        y0 = int(cy + math.sin(ang) * (r - 20))
        x1 = int(cx + math.cos(ang) * (r + 20))
        y1 = int(cy + math.sin(ang) * (r + 20))
        pdb.gimp_pencil(drawable, 4, [x0, y0, x1, y1])

    # ── Blauer 4-Zacken-Stern (Hauptstern) ──
    tip   = int(r * 0.85)
    side  = int(r * 0.18)
    # Zacken: N, E, S, W  — spitze Vierecke
    for ang_deg in [270, 0, 90, 180]:
        a = math.radians(ang_deg)
        al = math.radians(ang_deg + 90)
        # Spitze
        tx = int(cx + math.cos(a) * tip)
        ty = int(cy + math.sin(a) * tip)
        # linke/rechte Flanke
        lx = int(cx + math.cos(al) * side)
        ly = int(cy + math.sin(al) * side)
        rx2 = int(cx - math.cos(al) * side)
        ry2 = int(cy - math.sin(al) * side)
        # Farbe: N-Zacke = GOLD, Rest = BLUE
        col = GOLD if ang_deg == 270 else BLUE_LIGHT
        draw_polygon(drawable, [(cx, cy), (lx, ly), (tx, ty), (rx2, ry2)], col)

    # ── 8-Zacken-Stern (kleiner, dunkleres Blau, überlagert) ──
    tip2  = int(r * 0.5)
    side2 = int(r * 0.12)
    for ang_deg in range(0, 360, 45):
        a  = math.radians(ang_deg)
        al = math.radians(ang_deg + 90)
        tx = int(cx + math.cos(a) * tip2)
        ty = int(cy + math.sin(a) * tip2)
        lx = int(cx + math.cos(al) * side2)
        ly = int(cy + math.sin(al) * side2)
        rx2 = int(cx - math.cos(al) * side2)
        ry2 = int(cy - math.sin(al) * side2)
        draw_polygon(drawable, [(cx, cy), (lx, ly), (tx, ty), (rx2, ry2)], BLUE_DARK)

    # ── Kleiner Mittelpunkt ──
    draw_filled_ellipse(drawable, cx, cy, 12, 12, GOLD)
    draw_filled_ellipse(drawable, cx, cy, 6, 6, BG)

def draw_compass_letters(image, drawable, cx, cy, r):
    """Beschriftet den Kompass mit N/S/E/W."""
    offset = r + 52
    labels = [
        ("N", cx,          cy - offset),
        ("S", cx,          cy + offset + 10),
        ("E", cx + offset, cy),
        ("W", cx - offset, cy),
    ]
    size = 54
    for letter, x, y in labels:
        text_layer = pdb.gimp_text_fontname(
            image, None, x - size//2, y - size//2,
            letter, 0, True, size, UNIT_PIXEL, "Sans Bold"
        )
        if text_layer:
            pdb.gimp_text_layer_set_color(text_layer, PETROL)
            pdb.gimp_item_transform_translate(text_layer, 0, 0)
            pdb.gimp_floating_sel_to_layer(text_layer) if pdb.gimp_item_is_valid(text_layer) else None
            image.flatten()   # vereinfacht: flatten & weiterarbeiten

def draw_wave(drawable, cx, y_center, width, amplitude, phase, color, line_width=6):
    """Zeichnet eine einzelne Wellenlinie via Pencil-Strokes."""
    rgb(*color)
    pdb.gimp_context_set_line_width(line_width)
    pdb.gimp_context_set_stroke_method(STROKE_LINE)
    pdb.gimp_context_set_antialias(True)

    steps = 200
    points = []
    x_start = cx - width // 2
    for i in range(steps + 1):
        t = i / steps
        x = x_start + t * width
        y = y_center + amplitude * math.sin(2 * math.pi * t * 2.5 + phase)
        points.append(int(x))
        points.append(int(y))

    pdb.gimp_pencil(drawable, len(points), points)

def draw_waves(drawable, cx, y_top, w=820, ampl=22, gap=44):
    """Zeichnet 3 Wellenlinien untereinander."""
    # obere Welle hat kleine Bögen (Luftblasen-Anmutung)
    for i in range(3):
        draw_wave(drawable, cx, y_top + i * gap, w, ampl, phase=i * 0.4,
                  color=GOLD, line_width=5 + i)

def draw_paddle(drawable, cx, y, total_w=820, blade_w=110, blade_h=44, shaft_lw=5):
    """Zeichnet ein Paddel (zwei Blätter + Schaft + kleiner Mittelpunkt)."""
    shaft_half = total_w // 2 - blade_w // 2

    # linkes Blatt (Ellipse)
    bx_l = cx - shaft_half - blade_w // 2
    draw_filled_ellipse(drawable, bx_l, y, blade_w // 2, blade_h // 2, GOLD)

    # rechtes Blatt
    bx_r = cx + shaft_half + blade_w // 2
    draw_filled_ellipse(drawable, bx_r, y, blade_w // 2, blade_h // 2, GOLD)

    # Schaft
    rgb(*GOLD)
    pdb.gimp_context_set_line_width(shaft_lw)
    pdb.gimp_pencil(drawable, 4, [cx - shaft_half, y, cx + shaft_half, y])

    # Mittelpunkt
    draw_filled_ellipse(drawable, cx, y, 10, 10, GOLD)
    draw_filled_ellipse(drawable, cx, y, 5, 5, BG)

def draw_text_block(image, cx, y, line1, line2):
    """Zeichnet EXPEDITION (weiß) und PACKRAFT (gold) mit Trennlinien."""
    # obere Trennlinie
    rgb(*WHITE)
    bar_w = 580
    pdb.gimp_image_select_rectangle(
        image, CHANNEL_OP_REPLACE,
        cx - bar_w//2, y, bar_w, 4
    )
    gimp.edit_fill(image.get_active_drawable(), FILL_FOREGROUND)
    gimp.selection_none(image)

    # "EXPEDITION"
    size1 = 110
    tl1 = pdb.gimp_text_fontname(
        image, None,
        cx - 300, y + 14,
        line1, 0, True, size1, UNIT_PIXEL, "Sans Bold"
    )
    if tl1:
        pdb.gimp_text_layer_set_color(tl1, WHITE)
        pdb.gimp_text_layer_set_justification(tl1, TEXT_JUSTIFY_CENTER)
        w = pdb.gimp_drawable_width(tl1)[0]
        pdb.gimp_layer_set_offsets(tl1, cx - w//2, y + 14)
        pdb.gimp_floating_sel_to_layer(tl1) if False else None
        image.flatten()

    # "PACKRAFT"
    size2 = 90
    tl2 = pdb.gimp_text_fontname(
        image, None,
        cx - 260, y + 14 + size1 + 10,
        line2, 0, True, size2, UNIT_PIXEL, "Sans Bold"
    )
    if tl2:
        pdb.gimp_text_layer_set_color(tl2, GOLD)
        pdb.gimp_text_layer_set_justification(tl2, TEXT_JUSTIFY_CENTER)
        w = pdb.gimp_drawable_width(tl2)[0]
        pdb.gimp_layer_set_offsets(tl2, cx - w//2, y + 14 + size1 + 10)
        image.flatten()

    # untere Trennlinie
    rgb(*WHITE)
    pdb.gimp_image_select_rectangle(
        image, CHANNEL_OP_REPLACE,
        cx - bar_w//2, y + 14 + size1 + 10 + size2 + 14, bar_w, 4
    )
    gimp.edit_fill(image.get_active_drawable(), FILL_FOREGROUND)
    gimp.selection_none(image)


# ════════════════════════════════════════════════════════════════════════════
#  HAUPTFUNKTION
# ════════════════════════════════════════════════════════════════════════════

def build_design():
    # Bild anlegen
    image    = gimp.image_new(W, H, RGB)
    layer    = gimp.layer_new(image, W, H, RGBA_IMAGE, "Design", 100, LAYER_MODE_NORMAL)
    image.insert_layer(layer, None, -1)

    # Hintergrund füllen
    rgb(*BG)
    gimp.edit_fill(layer, FILL_FOREGROUND)

    cx = W // 2   # 500

    # ── Kompass ──────────────────────────────────────────
    comp_cy = 290
    comp_r  = 190
    draw_compass(layer, cx, comp_cy, comp_r)
    # N/S/E/W – als einfache Text-Layer
    draw_compass_letters(image, layer, cx, comp_cy, comp_r)

    layer = image.get_active_drawable()  # nach flatten neu holen

    # ── Wellenlinien ─────────────────────────────────────
    wave_y = 590
    draw_waves(layer, cx, wave_y)

    # ── Paddel ───────────────────────────────────────────
    paddle_y = 760
    draw_paddle(layer, cx, paddle_y)

    # ── Textblock ────────────────────────────────────────
    text_y = 840
    draw_text_block(image, cx, text_y, "EXPEDITION", "PACKRAFT")

    layer = image.get_active_drawable()

    # ── Ergebnis anzeigen ────────────────────────────────
    gimp.display_new(image)
    gimp.displays_flush()
    print("✓ Expedition Packraft Design erstellt!")
    return image


build_design()