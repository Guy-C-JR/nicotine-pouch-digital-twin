"""Generate the illustrative data-style figures (Supplementary Figs. S2-S5).

All values below are SYNTHETIC PLACEHOLDERS chosen to demonstrate the structure of the
framework's outputs. They are not estimates and were not computed from real data.

Usage:
    python scripts/plot_illustrative.py [output_dir]

Writes Figure_S2..Figure_S5 as vector PDF and 600-dpi PNG (default: figures/output).
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import BoundaryNorm, ListedColormap  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "figures", "output")
os.makedirs(OUT, exist_ok=True)

DISCLAIMER = ("Illustrative / schematic output structure — values are hypothetical placeholders, "
              "not computed from real data.")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": "#444444",
    "axes.linewidth": 0.9,
    "pdf.fonttype": 42,   # embed TrueType fonts in PDFs
})

YEARS = np.arange(2025, 2061)
T = (YEARS - YEARS[0]) / (YEARS[-1] - YEARS[0])   # 0 at 2025, 1 at 2060
BASE = 11.0                                         # placeholder baseline incidence per 100,000 PY


def trajectory(end_value):
    """Smooth placeholder trajectory from BASE (2025) to end_value (2060)."""
    return BASE * (end_value / BASE) ** T


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def footnote(fig, text=DISCLAIMER, y=0.005):
    fig.text(0.5, y, text, ha="center", va="bottom", fontsize=8.5, style="italic", color="#666666")


def incidence_axes(ax):
    ax.set_xlim(2025, 2060)
    ax.set_ylim(4, 26)
    ax.set_xlabel("Calendar year")
    ax.grid(True, color="#e8e8e8", linewidth=0.8)
    ax.set_axisbelow(True)


# --- Fig. S2: counterfactual scenario fan chart -------------------------------------
# (label, 2060 central value, band half-width at 2060, color); half-width is 0.5 at 2025.
SCENARIOS = [
    ("A  No market expansion (baseline)", 11.0, 1.1, "#5b6770"),
    ("B  Complete switching benefit", 9.4, 2.3, "#2a9d8f"),
    ("G  Policy intervention", 11.5, 1.6, "#457b9d"),
    ("C  Dual-use expansion", 12.7, 2.6, "#e9c46a"),
    ("F  High-frequency pouch use", 13.6, 3.2, "#9d4edd"),
    ("D  Youth / never-smoker initiation", 14.6, 3.1, "#e76f51"),
]


def fig_s2():
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    for label, end, half, color in SCENARIOS:
        y = trajectory(end)
        h = 0.5 + (half - 0.5) * T
        ax.fill_between(YEARS, y - h, y + h, color=color, alpha=0.12, linewidth=0)
        ax.plot(YEARS, y, color=color, linewidth=2.4, label=label)
    incidence_axes(ax)
    ax.set_ylabel("Projected incidence per 100,000 person-years\n(oral cavity + oropharynx, illustrative)")
    ax.legend(loc="upper left", frameon=False, fontsize=9.5)
    footnote(fig)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "Figure_S2")


# --- Fig. S3: risk-envelope projection ---------------------------------------------
def fig_s3():
    upper, central, lower = trajectory(16.0), trajectory(12.5), trajectory(9.2)
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    ax.fill_between(YEARS, lower, upper, color="#dbe5ee", alpha=0.7, linewidth=0,
                    label="Plausible envelope (Scenario I → H)")
    ax.plot(YEARS, upper, "--", color="#e76f51", linewidth=2.2, label="Upper bound  (H: worst-case sensitivity)")
    ax.plot(YEARS, central, "-", color="#1d3557", linewidth=2.8, label="Central projection")
    ax.plot(YEARS, lower, "--", color="#2a9d8f", linewidth=2.2, label="Lower bound  (I: harm-reduction best case)")
    incidence_axes(ax)
    ax.set_ylabel("Projected incidence per 100,000 person-years\n(illustrative)")
    ax.legend(loc="upper left", frameon=False, fontsize=9.5)
    footnote(fig)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "Figure_S3")


# --- Fig. S4: one-way sensitivity (tornado) ------------------------------------------
# (parameter, swing that drives burden down, swing that drives burden up); sorted by total swing.
TORNADO = [
    ("Youth / never-smoker uptake rate", -6.0, 14.5),
    ("Tumor-promotion coefficient (nicotine)", -2.5, 11.0),
    ("Dual-use persistence", -3.5, 9.0),
    ("Exposure duration (years of use)", -3.0, 7.0),
    ("Smoking displacement magnitude", -6.5, 3.0),
    ("Complete-switching fraction", -7.5, 2.0),
    ("Mean systemic nicotine dose", -1.8, 6.5),
    ("Oral lesion progression rate", -2.2, 5.5),
    ("Cessation / quit rate", -4.5, 2.5),
]


def fig_s4():
    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    ypos = np.arange(len(TORNADO))[::-1]
    for y, (label, down, up) in zip(ypos, TORNADO):
        ax.barh(y, up, color="#e76f51", alpha=0.85, height=0.62)
        ax.barh(y, down, color="#2a9d8f", alpha=0.85, height=0.62)
    ax.set_yticks(ypos, [t[0] for t in TORNADO])
    ax.axvline(0, color="#222222", linewidth=1.0)
    ax.set_xlim(-7.6, 15.6)
    ax.grid(True, axis="x", color="#e8e8e8", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Change in projected attributable cancer cases\n"
                  "(arbitrary illustrative units, ± from central estimate)")
    handles = [Patch(color="#e76f51", alpha=0.85, label="Drives burden upward"),
               Patch(color="#2a9d8f", alpha=0.85, label="Drives burden downward")]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=10)
    footnote(fig)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "Figure_S4")


# --- Fig. S5: gene / pathway evidence map -------------------------------------------
GENES = ["CHRNA7", "CHRNA4", "CHRNB2", "CHRNA5", "CHRNA3", "CHRNB4", "CYP2A6", "IL6", "TNF",
         "NFKB1", "NFE2L2", "HMOX1", "VEGFA", "BCL2", "CASP3/9", "TP53 pathway", "AKT pathway"]
CONDITIONS = ["Acute\nnicotine", "Chronic\nnicotine", "High-dose\nnicotine", "Withdrawal", "Dual-use\nexposure"]
# Direction-agnostic evidence strength: 0 none/inferred, 1 weak, 2 moderate, 3 strong (placeholder synthesis).
EVIDENCE = np.array([
    [2, 3, 3, 1, 2], [2, 3, 2, 2, 2], [2, 3, 2, 2, 2], [1, 2, 2, 1, 2], [1, 2, 2, 1, 2],
    [1, 2, 2, 1, 2], [3, 3, 3, 1, 2], [1, 2, 2, 1, 2], [1, 2, 2, 1, 2], [1, 2, 2, 1, 2],
    [1, 1, 2, 0, 1], [1, 1, 2, 0, 1], [2, 2, 3, 0, 2], [1, 2, 2, 0, 1], [1, 1, 2, 0, 1],
    [1, 1, 2, 0, 1], [2, 2, 2, 0, 1],
])


def fig_s5():
    cmap = ListedColormap(["#f6f6f6", "#d1e9e1", "#80c7b5", "#2a9d8f"])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    fig, ax = plt.subplots(figsize=(7.8, 8.4))
    im = ax.imshow(EVIDENCE, cmap=cmap, norm=norm, aspect="auto")
    for (r, c), v in np.ndenumerate(EVIDENCE):
        ax.text(c, r, str(v), ha="center", va="center", fontsize=9, color="#333333")
    ax.set_xticks(range(len(CONDITIONS)), CONDITIONS)
    ax.set_yticks(range(len(GENES)), GENES)
    ax.set_xlabel("Exposure condition", fontsize=12)
    cb = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3], fraction=0.05, pad=0.04)
    cb.ax.set_yticklabels(["0 none/\ninferred", "1 weak", "2 moderate", "3 strong"], fontsize=9)
    footnote(fig, DISCLAIMER + "\nCells encode direction-agnostic evidence strength for a nicotine-attributable perturbation.")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "Figure_S5")


if __name__ == "__main__":
    fig_s2()
    fig_s3()
    fig_s4()
    fig_s5()
