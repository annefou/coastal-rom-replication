# 05 — FORRT Replication Outcome

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify the actual numerical results first** by reading `results/` and `notebooks/03_analysis.py`. Don't quote numbers from memory. See `docs/verify-before-drafting.md`.

## Field-by-field draft

### Short URI suffix for outcome ID (text input, required)

Slug. Use kebab-case.

```
loveland-2024-rom-tradeoff-outcome
```

### Plain-text label for the outcome (text input, required)

Descriptive title.

```
Coastal-ROM trade-off reproduction outcome (Loveland et al. 2024)
```

### Search for a FORRT replication study (search/select, required)

URI of the Replication Study published in step 04. Pull from `nanopubs/PUBLISHED.md`.

```
_To be filled in Phase 5 once step 04 Replication Study is published._
```

### Repository URL (text input, required)

```
https://github.com/annefou/coastal-rom-replication
```

### Completion date (date picker, required)

```
2026-05-22
```

### Validation status (dropdown, required)

- [x] **Validated**
- [ ] PartiallySupported
- [ ] Contradicted

This dropdown maps to the CiTO intention in step 06: Validated → `confirms`, PartiallySupported → `qualifies`, Contradicted → `disputes`.

Rationale: the Quote (step 01) was deliberately re-anchored from the abstract to §6 Conclusions in Phase 1 second pass to carry Loveland's own WSE-only-interest conditioning. Under that conditioning, the replication confirms both halves of the Quote — the WSE-only trade-off AND the wave-statistics sensitivity caveat — from the public data. CiTO downstream: `confirms`.

### Confidence level (dropdown, required)

_Vocabulary not yet captured — set during Phase 5 field-by-field drafting via the nanopub-drafter agent._

```

```

### Describe the overall conclusion about the original claim (textarea, required)

Substantive interpretation. Headline comparison: replication's number vs the paper's number, sign + significance.

```
Loveland et al.'s (2024) conditional trade-off claim — that reduced-order SWAN source terms (Gen1, Gen2) yield significant computational savings without compromising water-surface-elevation accuracy when WSE is of primary interest, while large source-term sensitivities in significant-wave-height fields are observed near hurricane tracks — is supported by a stat-level reproduction. The Gen3 / (Gen1 or Gen2) wall-clock ratio of approximately 40 percent reproduces from Table 4 (Ike 1.44×, Ida 1.71×). WSE RMSE invariance across all source-term configurations reproduces from Tables 5-6 (maximum difference 0.007 m for Ike, 0.001 m for Ida — well within observational noise). Independent download of NOAA CO-OPS gauge data confirms storm peaks (Galveston Pier 21 3.20 m on 13 September 2008; Grand Isle 1.65 m on 29 August 2021) are consistent with the modelled ranges. The wave-statistics sensitivity caveat in the Quote — large global Hs sensitivities near tracks — is reflected in Loveland's own Tables 5-7 (Tp RMSE Ida Gen3 9.96 s versus Gen1 4.87 s, a factor-of-2 divergence) and Fig. 9 (several-metre spatial differences). Verdict: Validated, under the WSE-only-interest conditioning the Quote carries.
```

### Describe the evidence that supports your conclusion (textarea, required)

Numerical results, test statistics, model coefficients. Read directly from `results/`.

```
Source files: results/headline_comparison.csv, results/tradeoffs.csv, results/obs_wse_peaks.csv, results/obs_wave_peaks.csv, figures/main_result.png. Paper baselines transcribed verbatim from Loveland Tables 4-7.

Run-time (1064 Frontera cores):
- Ike: No SWAN 1.094 h; Gen1 2.837 h; Gen2 2.688 h; Gen3 4.086 h. Gen3/Gen1 = 1.44.
- Ida: No SWAN 0.647 h; Gen1 1.881 h; Gen2 1.818 h; Gen3 3.206 h. Gen3/Gen1 = 1.70.

WSE RMSE at NOAA gauges (m):
- Ike: No SWAN 0.210; Gen1 0.190; Gen2 0.196; Gen3 0.197. Max with-wave Δ = 0.007 m.
- Ida: No SWAN 0.285; Gen1 0.282; Gen2 0.281; Gen3 0.282. Max with-wave Δ = 0.001 m.

Hs RMSE at NDBC buoys (m):
- Ike: Gen1 0.900; Gen2 1.033; Gen3 0.802 — Gen3 best.
- Ida: Gen1 0.813; Gen2 0.883; Gen3 0.834 — Gen1 best.

Tp RMSE at NDBC buoys (s):
- Ike: Gen1 2.822; Gen2 2.541; Gen3 2.413.
- Ida: Gen1 4.865; Gen2 5.068; Gen3 9.960 — Gen3 a factor of 2 worse than Gen1.

Mean wave direction RMSE at NDBC buoys (degrees):
- Ike: Gen1 43.238; Gen2 40.392; Gen3 37.076.
- Ida: Gen1 62.380; Gen2 60.229; Gen3 67.730.

Independent observational download: 14/14 NOAA CO-OPS gauges for Ike (5-14 September 2008); 13/13 for Ida (26 August - 4 September 2021); 9/10 NDBC buoys (42007 absent from NDBC historical archive for 2021). Storm peaks confirmed at Galveston Pier 21 (3.20 m, 13 September 2008) and Grand Isle (1.65 m, 29 August 2021).
```

### Describe what limits the conclusions of the study (textarea, optional)

Honest caveats. If the result is partial or contradicted, say so plainly. Don't overclaim.

```
Three caveats limit how this Outcome should be cited:

1. Stat-level reproduction, not model re-run. This replication does not independently re-run ADCIRC+SWAN at the paper's compute scale (1064 Frontera cores, 3-6 million-element meshes for Ike and Ida respectively). The model output side of the comparison is transcribed verbatim from Loveland et al.'s Tables 4-7; the observational side is independently downloaded from NOAA CO-OPS and NDBC. The Validated verdict therefore confirms consistency of Loveland's published numbers with the public observational baseline, not the reproducibility of the model run itself. Loveland's DesignSafe deposit (DOI 10.17603/DS2-7HBT-EF65) is access-restricted (HTTP 401 on the public listing API) and was not retrievable during this study.

2. Wind-field-accuracy conditioning, dropped by the Quote. Loveland's §6 Conclusions adds a second conditioning that the chosen Quote does not carry: 'if the meteorological forcing is not sufficiently accurate, which is common in forecasting scenarios, then the additional computational cost associated with the detailed Gen3 source terms may not improve accuracy of the model.' The Validated verdict therefore covers the hindcasting regime (Loveland used Oceanweather Inc. validated hindcasts for Ike and HURDAT2-derived GAHM winds for Ida) and should not be cited as supporting reduced-order source terms in operational forecasting where wind-field uncertainty dominates the error budget. This condition lives in the Replication Study's Methodology / Scope field as well.

3. Wave-statistics sensitivity is context, not independent corroboration. The second sentence of the Quote (large Hs sensitivities near hurricane tracks) is Loveland's own quantified finding — Tables 5-7 and Fig. 9, including the Tp RMSE Ida factor-of-2 divergence noted above. The replication confirms these published numbers from the independent NOAA buoy download but does not surface new wave-statistics evidence. Outcome-level citers should not use this chain as independent corroboration of the wave-statistics caveat; that caveat traces to Loveland's own data.

The replication's main figure (figures/main_result.png) summarises the trade-off as 'save 30-40 percent wall-clock at less than 5 percent added WSE-RMSE cost', and that summary is faithful to the WSE-only-conditioned Quote.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.
