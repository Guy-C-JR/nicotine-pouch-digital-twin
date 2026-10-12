"""Render the schematic figures (Figs. 1-4, S1, S6) from their Graphviz sources.

For each figure: Graphviz -> vector PDF trimmed to the drawing's bounding box, then a PNG
rendered from that PDF (so the PDF and PNG are identical).

Usage:
    python scripts/render_graphviz.py [output_dir]

Requires Graphviz (https://graphviz.org; tested with 16.1) and PyMuPDF.
"""
import os
import shutil
import subprocess
import sys

import fitz  # PyMuPDF

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "figures", "graphviz")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "figures", "output")

# Figures 1 and 3 use fixed node positions (neato -n2); the rest use the dot layout engine.
ENGINE = {
    "Figure_1": ("neato", ["-n2"]),
    "Figure_2": ("dot", []),
    "Figure_3": ("neato", ["-n2"]),
    "Figure_4": ("dot", []),
    "Figure_S1": ("dot", []),
    "Figure_S6": ("dot", []),
}
PNG_DPI = 860    # >1000 dpi when printed at a 6.7-in (17-cm) full-page width
MARGIN_PT = 4


def find_engine(name):
    path = shutil.which(name)
    if path:
        return path
    candidate = os.path.join(r"C:\Program Files\Graphviz\bin", name + ".exe")
    if os.path.exists(candidate):
        return candidate
    sys.exit(f"Graphviz '{name}' not found; install Graphviz and put it on PATH.")


def content_bbox(page):
    """Bounding box (points) of non-white pixels, found at 1 px = 1 pt."""
    pix = page.get_pixmap(dpi=72, colorspace=fitz.csGRAY)
    w, h, s = pix.width, pix.height, pix.samples
    rows = [y for y in range(h) if min(s[y * w:(y + 1) * w]) < 250]
    cols = [x for x in range(w) if min(s[x::w][:h]) < 250]
    r = page.rect
    return fitz.Rect(max(r.x0, cols[0] - MARGIN_PT), max(r.y0, rows[0] - MARGIN_PT),
                     min(r.x1, cols[-1] + 1 + MARGIN_PT), min(r.y1, rows[-1] + 1 + MARGIN_PT))


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (engine, flags) in ENGINE.items():
        raw = os.path.join(OUT, name + "_untrimmed.pdf")
        subprocess.run([find_engine(engine), *flags, "-Tpdf", os.path.join(SRC, name + ".dot"), "-o", raw], check=True)
        doc = fitz.open(raw)
        doc[0].set_cropbox(content_bbox(doc[0]))
        pdf = os.path.join(OUT, name + ".pdf")
        doc.save(pdf, garbage=3, deflate=True)
        doc.close()
        os.remove(raw)
        doc = fitz.open(pdf)
        pix = doc[0].get_pixmap(dpi=PNG_DPI)
        pix.set_dpi(PNG_DPI, PNG_DPI)
        pix.save(os.path.join(OUT, name + ".png"))
        w_in = doc[0].rect.width / 72
        print(f"wrote {name}: {w_in:.2f} in wide; node text {12 * min(1, 6.5 / w_in):.1f} pt at 6.5-in width")
        doc.close()


if __name__ == "__main__":
    main()
