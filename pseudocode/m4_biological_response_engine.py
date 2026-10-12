"""Biological-response engine — tumor-promotion score (TPS)

Supplementary Methods M4 of the article. ILLUSTRATIVE PSEUDOCODE: it sketches the
structure and interfaces of the framework, calls helper functions that are not defined here,
is not runnable as-is, and contains no empirical parameters. No model was fitted to real data.
"""

def tumor_promotion_score(cne, biomarkers, beta):
    """TPS_i = σ(β0 + β1·CNE + β2·R + β3·I + β4·O + β5·IR + β6·E)  (Eq. 4).
    beta are EVIDENCE-GRADED PRIORS, not fitted. Scenario I -> beta≈0."""
    z = (beta[0] + beta[1]*z(cne) + beta[2]*biomarkers["receptor"]
            + beta[3]*biomarkers["inflammation"] + beta[4]*biomarkers["oxidative"]
            + beta[5]*biomarkers["insulin_resistance"] + beta[6]*biomarkers["epithelial_turnover"])
    return 1.0 / (1.0 + np.exp(-z))                    # bounded (0,1)
