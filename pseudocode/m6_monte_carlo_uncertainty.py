"""Monte Carlo uncertainty propagation (pseudocode)

Supplementary Methods M6 of the article. ILLUSTRATIVE PSEUDOCODE: it sketches the
structure and interfaces of the framework, calls helper functions that are not defined here,
is not runnable as-is, and contains no empirical parameters. No model was fitted to real data.
"""

def run_scenario(scenario, n_draws, n_agents, priors, rng):
    """Propagate parameter uncertainty end-to-end; return trajectory distribution."""
    traj = []
    for _ in range(n_draws):
        params = sample_priors(priors, scenario, rng)  # incl. beta, kappa, transition rates
        cohort = generate_synthetic_cohort(n_agents, scenario["marginals"], scenario["joint"], rng)
        incidence = np.zeros(N_YEARS)
        for ind in cohort:
            cne = cumulative_nicotine_exposure(ind, scenario["schedule"](ind), PRODUCTS)
            tps = tumor_promotion_score(cne, biomarker_model(cne, ind, params), params["beta"])
            state = "healthy"
            for y in range(N_YEARS):
                state = step_individual(state, ind["age"]+y, ind["sex"],
                                        design_matrix(ind), tps, params, dt=1.0, rng=rng)
                if state == "cancer": incidence[y] += 1
        traj.append(incidence / n_agents * 1e5)         # per 100k
    traj = np.array(traj)
    return dict(median=np.median(traj,0),
                lo=np.percentile(traj,2.5,0), hi=np.percentile(traj,97.5,0))

def attributable_vs_baseline(scn, base):
    return scn["median"] - base["median"]               # report WITH intervals, never alone
