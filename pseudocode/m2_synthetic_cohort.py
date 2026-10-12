"""Synthetic-cohort simulation (pseudocode)

Supplementary Methods M2 of the article. ILLUSTRATIVE PSEUDOCODE: it sketches the
structure and interfaces of the framework, calls helper functions that are not defined here,
is not runnable as-is, and contains no empirical parameters. No model was fitted to real data.
"""

import numpy as np

def generate_synthetic_cohort(n, marginals, joint_constraints, rng):
    """Draw a synthetic population calibrated to survey marginals.
    No real individuals; disclosure-safe."""
    cohort = []
    for _ in range(n):
        age  = sample_age(marginals["age"], rng)
        sex  = sample_cat(marginals["sex"], rng)
        ses  = sample_cat(marginals["ses"], rng)
        # smoking status is the master confounder; condition pouch use on it
        smk  = sample_smoking_status(age, ses, marginals["smoking"], rng)
        pouch = sample_pouch_state(age, smk, marginals["pouch"], rng)  # never/switch/dual/initiate
        covars = dict(
            cyp2a6 = sample_metabolizer(rng),         # fast/normal/slow -> dose modifier m
            alcohol= sample_cat(marginals["alcohol"], rng),
            hpv    = sample_cat(marginals["hpv"], rng),
            oral_hygiene = sample_ordinal(rng),
            diabetes = sample_cat(marginals["dm"], rng),
        )
        cohort.append(dict(age=age, sex=sex, ses=ses, smk=smk, pouch=pouch, **covars))
    cohort = enforce_joint_constraints(cohort, joint_constraints)  # IPF / copula calibration
    return cohort
