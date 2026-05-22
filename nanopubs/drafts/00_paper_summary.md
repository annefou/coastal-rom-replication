# Paper summary

> This is a working scratchpad for the paper-analysis phase. The output of this file feeds the Quote / AIDA / Claim drafts. It is not itself a nanopub.

**Reference paper:** Efficacy of reduced order source terms for a coupled wave-circulation model in the Gulf of Mexico

**DOI:** 10.1016/j.ocemod.2024.102387

**Authors:** Mark Loveland (Oden Institute for Computational Engineering and Sciences, University of Texas at Austin, 201 E. 24th St., Austin, 78712, TX, USA); Jessica Meixner (NWS/NCEP Environmental Modeling Center, National Oceanic and Atmospheric Administration (NOAA), College Park, MD, USA); Eirik Valseth (Oden Institute, UT Austin; The Department of Data Science, Norwegian University of Life Sciences, Drøbakveien 31, Ås, 1433, Norway; Department of Scientific Computing and Numerical Analysis, Simula Research Laboratory, Kristian Augusts gate 23, Oslo, 0164, Norway); Clint Dawson (Oden Institute, UT Austin).

**Year:** 2024

**Journal:** Ocean Modelling 190 (2024) 102387

## Headline claim

The single sentence in the paper that this replication tests. Verbatim from the abstract.

> "The usage of the reduced order source terms yielded significant savings in computational cost. Additionally, relatively low amounts of additional error with respect to observations during the simulations with reduced order source terms are observed in our computational experiments."

Alternative candidate sentences considered:

- (Abstract, follow-on caveat): "However, large changes in global model outputs of the wave statistics were observed based on the choice of source terms particularly near the track of each hurricane." — Rejected as the headline because it expresses the *qualifier*, not the *trade-off* claim itself. We will preserve it as nuance in the Comment / Outcome.
- (Conclusions, §6): "Upgrading from Gen1 or Gen2 source terms to the ST6 Gen3 source terms resulted in about a 40% increase in run time. The effects of the choice of source terms (Gen1, Gen2 or Gen3) on average WSE at NOAA gauges only changed RMSE relative to the gauges by about 0.007 m." — Rejected because it is two sentences; the abstract headline is more compact and is the single sentence the abstract foreshadows.
- (Abstract, framing): "this study investigates the potential consequences of using simplified (reduced order) source terms within the wave model component of the coupled wave-circulation model." — Rejected as a *framing/motivation* sentence, not an empirical claim.

The selected headline pairs a savings claim with a low-error claim and is the most compact statement of the paper's central empirical finding. It is 309 characters as a two-sentence excerpt and fits the Quote-whole-text mode (< 500 chars).

## Methodology summary

- **Models:** ADCIRC (Advanced Circulation Model, finite-element shallow-water equations on unstructured triangular meshes) tightly coupled to SWAN (Simulating Waves Nearshore, spectral wave model solving the Wave Action Balance Equation). ADCIRC+SWAN v41.31 was used, with coupling interval 600 s. ADCIRC and SWAN run on the same unstructured mesh.
- **Source-term configurations compared:** four — (a) ADCIRC standalone "No SWAN" control, (b) Gen1 (1st generation, Holthuijsen et al. 1988 — neglects nonlinear S_nl), (c) Gen2 (2nd generation — differs from Gen1 only by one parameter in S_in), (d) Gen3 / ST6 (3rd generation, Rogers et al. 2012 — full DIA nonlinear interactions, semi-empirical, calibrated to extreme weather).
- **Storm scenarios (sample = 2 hurricanes):** Hurricane Ike (Category 4, made landfall near Galveston, TX on 13 September 2008; simulation 5–14 September 2008, 8 d 18 h) and Hurricane Ida (Category 4, made landfall near Port Fourchon, LA on 29 August 2021; simulation 26 August – 4 September 2021, 9 d 6 h). Each storm has its own unstructured mesh: Ike mesh 6,675,517 elements / 3,352,598 nodes; Ida mesh 3,102,441 elements / 1,593,485 nodes. Both meshes extend west of 60°W with resolution from km offshore down to ~20 m at the impact coastline.
- **Forcing:** Ike — Oceanweather Inc. (OWI) validated meteorological hindcasts; Ida — NHC HURDAT2 best-track winds expanded via the Generalized Asymmetric Holland Model (GAHM); open-ocean boundary tides from TPXO. 30-day tidal spin-up of ADCIRC (no winds) before coupling.
- **Compute setup:** 1064 cores of Intel Xeon Platinum 8280 ("Cascade Lake") nodes on Frontera at TACC.
- **Observational comparison data:** WSE compared against 14 NOAA gauges for Ike (Table 1) and 13 NOAA gauges for Ida (Table 2). Wave statistics (significant wave height Hs, peak period Tp, mean wave direction θ_mean) compared against 10 NOAA wave buoys (NBDC) shared between both scenarios (Table 3). Output recorded every 30 min; errors computed only during the wind-forcing period.
- **Statistics:** RMSE (eqn 7) of WSE/Hs/Tp/θ_mean averaged across stations, and percent error of the peak value (e_peak).

### Headline numerical results (baselines for the replication's comparison)

- **Wall-clock run times (Table 4):** Ike — No SWAN 1.094 h; Gen1 2.837 h (ratio 2.593); Gen2 2.688 h (ratio 2.457); Gen3 4.086 h (ratio 3.735). Ida — No SWAN 0.647 h; Gen1 1.881 h (ratio 2.907); Gen2 1.818 h (ratio 2.809); Gen3 3.206 h (ratio 4.955). Upgrading to Gen3 costs roughly 40 % more wall-clock time than Gen1/Gen2.
- **WSE at NOAA gauges (Ike, with-waves):** average RMSE 0.190 m (Gen1), 0.196 m (Gen2), 0.197 m (Gen3); excluding waves 0.210 m. Maximum RMSE difference between any two with-wave configs ≈ 0.007 m (< 5 % difference). Peak relative error 12 % (Gen1), 10 % (Gen2), 11 % (Gen3); 13 % without waves.
- **WSE at NOAA gauges (Ida):** average RMSE 0.282 m (Gen1), 0.281 m (Gen2), 0.282 m (Gen3); excluding waves 0.285 m. Differences in RMSE < 1.5 %. Peak relative error 20 % (Gen1), 21 % (Gen2), 22 % (Gen3); 20 % without waves.
- **Significant wave height Hs RMSE at NOAA buoys:** Ike — 0.900 m (Gen1), 1.033 m (Gen2), 0.802 m (Gen3); Gen3 is ~10 % better than Gen1 and ~20 % better than Gen2. Ida — 0.813 m (Gen1), 0.883 m (Gen2), 0.834 m (Gen3); Gen1 has the lowest mean RMSE; all packages within 0.07 m. Peak Hs relative-error average: Ike 27 % / 30 % / 22 %; Ida 40 % / 81 % / 63 %.
- **Peak period Tp RMSE across buoys:** Ike — 2.822 s (Gen1), 2.541 s (Gen2), 2.413 s (Gen3) — 15 % improvement Gen1→Gen3. Ida — 4.865 s (Gen1), 5.068 s (Gen2), 9.960 s (Gen3) — Gen3 substantially worse.
- **Mean wave direction θ_mean RMSE across buoys:** Ike — 43.238° (Gen1), 40.392° (Gen2), 37.076° (Gen3) — 14 % improvement Gen1→Gen3. Ida — 62.380° (Gen1), 60.229° (Gen2), 67.730° (Gen3).
- **Spatial wave-height differences:** near the hurricane track, maximum Hs differences between Gen3 and the reduced-order configs reach >1 m for Ike and several metres for Ida (Fig. 9), confirming the abstract's caveat that global outputs are highly sensitive to source-term choice in the storm-track corridor.

## Replication design choice

Which of the three FORRT Study Types fits this replication?

- [x] **Reproduction Study** — direct reproduction: same methodology, same tools.
- [ ] **Replication Study** — replication with different methodology or conditions.
- [ ] **Reproduction/Replication Study** — both.

### Justification

A Reproduction Study is the right shape here. The paper's headline is a *computational-cost-versus-accuracy trade-off* claim that is most credibly validated by re-running the identical ADCIRC+SWAN v41.31 configurations on the identical Ike and Ida meshes, with the same fort.26 source-term files (which the authors print in the Appendix). The published numerical baselines (Table 4 wall-clock times, the per-gauge / per-buoy RMSE values, and the spatial Hs differences in Figs. 9–13) provide a dense, quantitative comparison surface that a same-tools reproduction can address one-for-one. Switching solvers or storms first would conflate methodological variance with the original claim and dilute what we're testing.

**Data-availability flag (important):** The paper's "Data availability" statement reads "Data will be made available on request." The full input set (meshes, fort.26 spectral configs, OWI winds for Ike, GAHM-from-HURDAT2 winds for Ida, NOAA gauge/buoy time series) is referenced through the DesignSafe DOI in Loveland et al. (2024) and partially printed in the Appendix, but is not guaranteed to be openly archived end-to-end. If a subset of the inputs turns out to be access-restricted or missing from the DesignSafe deposit, fall back to a Reproduction-with-substitutions design (e.g. regenerate Ida winds from HURDAT2 via an open GAHM implementation) and document each substitution explicitly in the Replication Study's "Deviations" field — this still reads as a Reproduction Study, not a Replication Study, provided the model code and storm scenarios are unchanged.

## Notes for downstream drafts

- The selected headline quote is **two sentences** treated as a single quotation. Together they are 309 characters — within the < 500-character Quote-whole-text limit. If reviewers want only one sentence, prefer the first ("The usage of the reduced order source terms yielded significant savings in computational cost.") because it is the single empirical assertion the abstract foregrounds; the second sentence is the matched accuracy claim.
- **AIDA splitting:** the abstract bundles two empirical findings — (1) reduced-order source terms save computation, (2) they add little error vs. observations. These are independent enough that the FORRT chain may need two AIDA nanopubs, each anchoring its own Claim, per the "Atomic AIDA" rule in `CLAUDE.md`. Decide during Phase 5 drafting whether the chain carries one combined Claim or splits.
- **CiTO relation** when published: most likely `extends` if our reproduction confirms both the savings and the low-error result, or `qualifies` if we reproduce the savings but find the additional error in the storm-track corridor is larger than the abstract's framing implies. `disputes` should be reserved for an outright contradiction.
- **ADCIRC + SWAN are heavy:** Frontera-scale compute (1064 cores) is not in scope for an academic reproduction. Plan for a smaller-mesh or smaller-domain validation and label clearly in the Replication Study form.
- **Source-term configs printed in the Appendix:** the exact fort.26 files for Gen1, Gen2, and Gen3 (for Hurricane Ida) are reproduced on pp. 12–13 of the PDF and can be transcribed directly into the replication's input files. This is unusually generous for reproducibility and should be acknowledged.
