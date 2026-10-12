# Population–Molecular Cancer Digital Twin for oral nicotine pouches

**Figure-generation code and framework pseudocode** accompanying:

> Giordano GC Jr. Artificial intelligence–enabled digital twins for forecasting cancer burden from oral nicotine pouches: a review and expert opinion. *AI Biology & Medicine* (submitted).

<!-- After the first Zenodo release, add the DOI badge here, e.g.:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX) -->

## Read this first

The article proposes a **hypothesis-generating** framework. It reports **no fitted model and no empirical estimates**, and this repository contains **no real data**.

- The schematic figures (Figs. 1–4, S1, S6) are conceptual diagrams.
- The data-style figures (Figs. S2–S5) plot **synthetic placeholder values** that only show what the framework's outputs would look like.
- The pseudocode sketches interfaces and is not runnable as-is.

Nothing here is evidence that any oral nicotine pouch causes cancer.

## Contents

| Path | What it is |
|---|---|
| `figures/graphviz/*.dot` | Graphviz sources for Figs. 1–4 and Supplementary Figs. S1 and S6 |
| `scripts/render_graphviz.py` | Renders the `.dot` sources to trimmed vector PDFs and high-resolution PNGs |
| `scripts/plot_illustrative.py` | Generates Supplementary Figs. S2–S5 (matplotlib; all values are placeholders defined in the script) |
| `figures/output/` | Rendered figures, as PDF (vector) and PNG |
| `pseudocode/` | Framework pseudocode from Supplementary Methods M2–M7: synthetic cohort, exposure engine, biological-response engine, Markov transitions, Monte Carlo uncertainty, Bayesian model sketch |
| `docs/` | Sample data schema (M8), validation checklist (M9), and reproducibility checklist (M10) |

## Figure map

| File | Article figure |
|---|---|
| `Figure_1` | Fig. 1. Oral nicotine pouch exposure-to-cancer uncertainty map |
| `Figure_2` | Fig. 2. Architecture of the Population–Molecular Cancer Digital Twin |
| `Figure_3` | Fig. 3. Multistate cancer-transition model (Layer 3) |
| `Figure_4` | Fig. 4. Causal directed acyclic graph for pouch use and cancer incidence |
| `Figure_S1` | Fig. S1. Candidate nicotine tumor-promotion signaling pathways |
| `Figure_S2` | Fig. S2. Counterfactual scenario fan chart (illustrative) |
| `Figure_S3` | Fig. S3. Risk-envelope projection (illustrative) |
| `Figure_S4` | Fig. S4. One-way sensitivity (tornado) plot (illustrative) |
| `Figure_S5` | Fig. S5. Gene and pathway evidence map (illustrative) |
| `Figure_S6` | Fig. S6. Policy-impact simulation schematic |

## Reproducing the figures

Requirements:
- Python ≥ 3.9
- [Graphviz](https://graphviz.org/download/) ≥ 16 on your `PATH` (on Windows, the default install location is also detected)
- The Python packages in `requirements.txt`

```bash
pip install -r requirements.txt
python scripts/render_graphviz.py
python scripts/plot_illustrative.py
```

Both scripts write to `figures/output/` by default; pass a different directory as the first argument to change it.

The figures in `figures/output/` were produced with Graphviz 16.1.0, Python 3.9, matplotlib 3.9.4, NumPy 2.0.2 and PyMuPDF 1.26.5.

## How to cite

Please cite the article, and this repository through its Zenodo DOI (see `CITATION.cff`).

## License

- **Code** (scripts, Graphviz sources, pseudocode): MIT License (see `LICENSE`)
- **Rendered figures and documentation**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Author

Guy C. Giordano Jr., Independent Researcher, Brighton, Michigan, USA.
ORCID [0009-0002-6997-3567](https://orcid.org/0009-0002-6997-3567). Contact: guy.c.giordano@gmail.com
