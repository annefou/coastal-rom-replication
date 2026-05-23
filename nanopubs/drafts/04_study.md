# 04 — FORRT Replication Study

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify code first:** read the actual reproduction script in `notebooks/03_analysis.py` before writing the methodology field. See `docs/verify-before-drafting.md`.

## Field-by-field draft

### Short URI suffix for study ID (text input, required)

Slug. Use kebab-case.

```
loveland-2024-rom-tradeoff-study
```

### Label/name of replication study (text input, required)

Human-readable title.

```
Stat-level reproduction of the Loveland et al. (2024) coupled ADCIRC+SWAN reduced-order source-term trade-off
```

### Study type (dropdown, required)

- [x] **Reproduction Study** — direct reproduction: same methodology, same tools.
- [ ] Replication Study — replication with different methodology or conditions.
- [ ] Reproduction/Replication Study — both.

(Per `00_paper_summary.md` § Replication design choice — same storms, same source-term taxonomy, same observational baseline.)

### Search for a FORRT claim (search/select, required)

URI of the Claim published in step 03. Pull from `nanopubs/PUBLISHED.md`.

> _If the Claim was published via Nanodash (`w3id.org/np/...` namespace), the platform's search may not find it — paste the URI manually._

```
_(step 03 Claim URI — paste here after publication; format https://w3id.org/sciencelive/np/RA… or https://w3id.org/np/RA… if published via Nanodash)_
```

### Describe what part of the claim is reproduced/replicated (textarea, required)

The **scope** of the claim being tested. Which aspect, what's in/out of scope. NOT methodology. NOT results. See `docs/pico-study-outcome-levels.md`.

```
In scope: the conditional trade-off claim from Loveland's §6 Conclusions as carried verbatim by the Quote — that reduced-order SWAN source terms (Gen1 first-generation, Gen2 second-generation) save computation relative to the third-generation ST6 Gen3 package without compromising water-surface-elevation (WSE) accuracy at NOAA gauges when WSE is of primary interest, with Loveland's own quantified caveat that large source-term sensitivities are observed in significant-wave-height fields near hurricane tracks. The two storm scenarios (Hurricane Ike 2008, Hurricane Ida 2021) and the four model configurations (No SWAN, Gen1, Gen2, Gen3) are tested in full.

Out of scope: (1) operational forecasting where wind-field uncertainty dominates the error budget — a second conditioning Loveland states in §6 ("if the meteorological forcing is not sufficiently accurate ... the additional computational cost associated with the detailed Gen3 source terms may not improve accuracy of the model") that the chosen Quote does not carry; the Outcome's Validated label therefore applies to the hindcasting regime only. (2) Model-level reproducibility of the ADCIRC+SWAN runs themselves — see Methodology field for what was and was not independently re-derived. (3) Generalisation beyond the Gulf of Mexico or beyond Loveland's two test storms.
```

### Describe how the claim is reproduced/replicated (textarea, required)

The **method** in plain prose. Read `notebooks/03_analysis.py` and any config files first. NOT exact numerical results.

```
This study is a stat-level (table-and-figure-level) reproduction, deliberately distinguishing what was independently re-derived from what was transcribed from the source paper. The downstream reader should not infer model-level verification.

INDEPENDENTLY RE-DERIVED (notebooks/01_data_download.py + 02_data_clean.py):
- Observational baseline. NOAA CO-OPS water-level gauge time series for the 14 Ike stations (Table 1 of the paper) over 5-14 September 2008 and the 13 Ida stations (Table 2) over 26 August - 4 September 2021, downloaded fresh from the public CO-OPS API. NDBC wave-buoy data (significant wave height, peak period, mean wave direction) for 10 buoys (Table 3), 9 of which were retrievable; buoy 42007 is absent from NDBC's 2021 historical archive at the URL pattern. Cleaned into tidy per-storm xarray Datasets per-variable, with per-variable resampling onto a common time grid (a naive nearest-reindex collapses NDBC's 10-min wind interleave into NaN-filled wave records; per-variable resampling avoids this).
- Storm-peak consistency check. Per-gauge peak water levels were extracted (Galveston Pier 21 = 3.20 m on 13 September 2008; Grand Isle = 1.65 m on 29 August 2021) and verified against NHC historical reports as a sanity check on the observational baseline Loveland modelled against.

TRANSCRIBED FROM THE SOURCE PAPER (notebooks/03_analysis.py, data/published_baselines/):
- All model-side outputs. Run times (Table 4) for each (storm, config) cell, WSE-RMSE per gauge (Tables 5-6 and the prose summaries in §5.3 of the paper), Hs / Tp / mean-wave-direction RMSE per buoy (Tables 5-7 transcribed from §5.2). These values come from Loveland's Frontera-scale ADCIRC+SWAN runs and were not re-computed.
- Source-term configuration files. The fort.26 files printed in the paper's Appendix (pp. 12-13) were inspected for documentation but not used to drive any new SWAN runs.
- Spatial figures. The paper's Fig. 9 (spatial Hs differences near hurricane tracks) and Fig. 12-13 (spatial WSE differences) were inspected for qualitative context but not regenerated.

What the comparison therefore tests: the internal consistency of Loveland's published model-vs-observation Δ values with the publicly retrievable observational baseline, and the per-storm trade-off ratios visible in Loveland's own Table 4. Not the reproducibility of the model runs themselves.

The headline statistic (Gen3 / (Gen1 or Gen2) wall-clock ratio per storm, and maximum WSE-RMSE Δ across source-term configurations per storm) is consolidated in results/headline_comparison.csv and visualised in figures/main_result.png. Orchestrated via Snakemake (pipeline rules in Snakefile); reproducible environment via pixi (pixi.toml + pixi.lock); container build via Dockerfile to ghcr.io/annefou/coastal-rom-replication.
```

### Describe any deviations from original methodology (textarea, optional)

What's different from the original method. Verify against the actual code, don't guess.

```
1. No ADCIRC+SWAN model re-runs. Loveland's runs were on 1064 Intel Xeon Platinum 8280 cores (19 nodes of TACC Frontera, "Cascade Lake"), with unstructured meshes of 6,675,517 elements / 3,352,598 nodes for Ike and 3,102,441 elements / 1,593,485 nodes for Ida. This compute scale is out of scope for a laptop / GitHub Actions / Docker reproduction. The replication therefore transcribes Loveland's published model-side outputs rather than regenerating them. The trade-off ratios reported in the Outcome's Evidence field are derived from Loveland's Table 4; the WSE-RMSE values are from Tables 5-6; the wave-statistics RMSE values are from Tables 5-7 and the §5.2 prose.

2. DesignSafe deposit not retrievable. Loveland deposited their model inputs (meshes, fort.26 source-term configs, OWI Ike winds, HURDAT2-derived Ida GAHM winds, NOAA gauge / buoy time series, model output files) at DOI 10.17603/DS2-7HBT-EF65 (DesignSafe-CI project PRJ-4678). Both /api/projects/v2/PRJ-4678/ and /api/datafiles/listing/public/designsafe.storage.published/PRJ-4678/ return HTTP 401 to anonymous requests, so the deposit cannot be re-fetched by an unauthenticated reproducer. The fort.26 files for the Ida run are reprinted in the paper's Appendix on pp. 12-13.

3. NDBC wave-buoy 42007 absent from the 2021 historical archive. Loveland's Table 3 lists 10 buoys; only 9 are retrievable for Ida from NDBC's URL pattern. The missing buoy is recorded in data/raw/sources.json.

4. Per-storm wall-clock-cost framing granularity. Loveland's §5.1 prose ("around 1.5 times longer") and §6 prose ("about a 40 percent increase") cover Hurricane Ike (Gen3/Gen1 = 1.44×, Gen3/Gen2 = 1.52×) but understate Hurricane Ida (Gen3/Gen1 = 1.70×, Gen3/Gen2 = 1.76×) by approximately 20 percentage points relative to Loveland's own Table 4. This is not a deviation from method — the replication uses the same per-storm cells from Table 4 — but is surfaced by the Outcome because Loveland's prose summary lacks this per-storm distinction. See Outcome Limitations item 5.
```

### Search keywords (Wikidata) (multi-select, optional)

Provide labels (not QIDs) — the Wikidata search picks up labels.

- storm surge
- Hurricane Ike
- Hurricane Ida
- ADCIRC

(Alternative candidates if any of the above fail to resolve in the Wikidata search box: `SWAN (wave model)`, `spectral wave model`, `coastal engineering`, `computational cost`.)

### Search discipline (Wikidata) (search, optional)

Provide labels.

- physical oceanography

(Alternative candidates if `physical oceanography` does not resolve: `coastal engineering`, `computational fluid dynamics`.)

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.
