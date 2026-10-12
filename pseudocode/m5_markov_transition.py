"""Markov-state transition (pseudocode)

Supplementary Methods M5 of the article. ILLUSTRATIVE PSEUDOCODE: it sketches the
structure and interfaces of the framework, calls helper functions that are not defined here,
is not runnable as-is, and contains no empirical parameters. No model was fitted to real data.
"""

STATES = ["healthy","inflammatory","premalignant","cancer","cancer_death","other_death"]

def step_individual(state, age, sex, X, tps, params, dt, rng):
    """Continuous-time multistate step. TPS multiplies ONLY promotion stages."""
    h = baseline_hazards(age, sex, params)             # λ1, λ2, λ3, μ_ca, μ_other
    adj = np.exp(X @ params["gamma"])                  # confounder adjustment
    kappa = params["kappa"]                            # exposure→hazard scale (prior)
    rates = {
        ("healthy","inflammatory"):   h["l1"]*adj,
        ("inflammatory","premalignant"): h["l2"]*adj*(1 + kappa*tps),   # promotion
        ("premalignant","cancer"):    h["l3"]*adj*(1 + kappa*tps),      # promotion
        ("inflammatory","healthy"):   h["reg1"],       # regression
        ("premalignant","inflammatory"): h["reg2"],    # regression
        ("cancer","cancer_death"):    h["mu_ca"],
        ("*","other_death"):          h["mu_other"],   # competing risk from any state
    }
    return sample_next_state(state, rates, dt, rng)
