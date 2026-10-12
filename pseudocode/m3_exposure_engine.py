"""Exposure engine — cumulative nicotine exposure (CNE)

Supplementary Methods M3 of the article. ILLUSTRATIVE PSEUDOCODE: it sketches the
structure and interfaces of the framework, calls helper functions that are not defined here,
is not runnable as-is, and contains no empirical parameters. No model was fitted to real data.
"""

def cumulative_nicotine_exposure(individual, schedule, product_db):
    """CNE_i = Σ_t  d * f * a * m * Δt  (Eq. 1). All factors are priors/inputs."""
    cne = 0.0
    m = METAB_MODIFIER[individual["cyp2a6"]]           # e.g., slow>normal>fast
    for t, use in schedule.items():                    # use: pouches, strength, dwell
        prod = product_db[use["product"]]
        d = absorbed_dose(prod["mg"], prod["pH"], use["dwell_min"])  # free-base dependent
        a = absorption_fraction(prod, use["dwell_min"])
        f = use["pouches_per_day"]
        cne += d * f * a * m * use["dt_years"]
    return cne
