# Sample data schema (Supplementary Methods M8)

Illustrative schema for a real implementation; no data are included in this repository.

| Table | Key fields | Source | Notes |
|---|---|---|---|
| `person` | person_id, age, sex, race_eth, ses, region | synthetic | disclosure-safe synthetic key |
| `product_use` | person_id, wave, product, strength_mg, pouches_day, dwell_min, dual_use_flag | PATH/NYTS-calibrated | longitudinal transitions |
| `biomarker` | person_id, wave, cotinine, nmr, il6, crp, homa_ir | NHANES/PATH-calibrated | exposure→biology |
| `product_db` | product, mg, pH, free_base_frac, abs_fraction | FDA/PK studies | dose computation |
| `transition_prior` | from_state, to_state, hazard_prior, source_grade | literature/SEER | evidence-graded |
| `outcome` | person_id, year, state, site, stage | SEER/registry (real impl.) | back-testing/calibration |
| `provenance` | source_id, funding_flag, industry_flag, weight | manual | down-weights industry data |
