# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 03 - Analysis
#
# Compute the headline statistics for the Loveland et al. 2024 stat-level
# reproduction. This notebook:
#
# 1. Transcribes the paper's Tables 4, 5, 6, 7 verbatim into CSVs under
#    `data/published_baselines/` (these are the per-storm wall-clock times and
#    per-config average RMSE values).
# 2. Loads the cleaned observation files written by notebook 02 and computes
#    obs-only peaks per station + sigma_peak as an obs-side context for the
#    paper's percent-error-of-peak metric.
# 3. Assembles the comparison table `results/headline_comparison.csv` that the
#    figures notebook plots.
#
# **What this notebook does NOT do.** Because the DesignSafe deposit
# (DOI: 10.17603/DS2-7HBT-EF65) requires an authenticated account, this
# notebook cannot recompute RMSE between modelled and observed series - the
# model outputs are not openly downloadable. The RMSE numbers used in the
# trade-off plot are therefore the **paper's own**, transcribed verbatim.
# This limitation is recorded explicitly in the Outcome draft in Phase 3.

# %%
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

# %%
PROC_DIR = Path("../data/processed")
PUB_DIR = Path("../data/published_baselines")
RESULTS_DIR = Path("../results")
PUB_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## Table 4 - wall-clock times (verbatim from PDF p. 7)

# %%
table4 = pd.DataFrame(
    [
        {"config": "No SWAN", "ike_h": 1.094, "ike_ratio": np.nan, "ida_h": 0.647, "ida_ratio": np.nan},
        {"config": "Gen1",    "ike_h": 2.837, "ike_ratio": 2.593,  "ida_h": 1.881, "ida_ratio": 2.907},
        {"config": "Gen2",    "ike_h": 2.688, "ike_ratio": 2.457,  "ida_h": 1.818, "ida_ratio": 2.809},
        {"config": "Gen3",    "ike_h": 4.086, "ike_ratio": 3.735,  "ida_h": 3.206, "ida_ratio": 4.955},
    ]
)
table4.to_csv(PUB_DIR / "table4_runtimes.csv", index=False)
print("Table 4 - wall-clock times")
print(table4.to_string(index=False))

# %% [markdown]
# ## Tables 5 & 6 - average WSE / peak metrics at NOAA gauges
#
# Average RMSE of WSE across NOAA gauges and absolute average percent error of
# the peak value, per configuration. Reported in the paper's body text
# (Section 5.3 and Conclusions, pp. 7-11):
#
# - Ike: avg RMSE = 0.190 m (Gen1), 0.196 m (Gen2), 0.197 m (Gen3),
#   0.210 m (No SWAN). Peak rel err = 12% (Gen1), 10% (Gen2), 11% (Gen3),
#   13% (No SWAN).
# - Ida: avg RMSE = 0.282 m (Gen1), 0.281 m (Gen2), 0.282 m (Gen3),
#   0.285 m (No SWAN). Peak rel err = 20% (Gen1), 21% (Gen2), 22% (Gen3),
#   20% (No SWAN).

# %%
wse_summary = pd.DataFrame(
    [
        {"storm": "ike", "config": "No SWAN", "avg_RMSE_m": 0.210, "abs_avg_peak_pct_err": 13.0},
        {"storm": "ike", "config": "Gen1",    "avg_RMSE_m": 0.190, "abs_avg_peak_pct_err": 12.0},
        {"storm": "ike", "config": "Gen2",    "avg_RMSE_m": 0.196, "abs_avg_peak_pct_err": 10.0},
        {"storm": "ike", "config": "Gen3",    "avg_RMSE_m": 0.197, "abs_avg_peak_pct_err": 11.0},
        {"storm": "ida", "config": "No SWAN", "avg_RMSE_m": 0.285, "abs_avg_peak_pct_err": 20.0},
        {"storm": "ida", "config": "Gen1",    "avg_RMSE_m": 0.282, "abs_avg_peak_pct_err": 20.0},
        {"storm": "ida", "config": "Gen2",    "avg_RMSE_m": 0.281, "abs_avg_peak_pct_err": 21.0},
        {"storm": "ida", "config": "Gen3",    "avg_RMSE_m": 0.282, "abs_avg_peak_pct_err": 22.0},
    ]
)
wse_summary.to_csv(PUB_DIR / "wse_summary.csv", index=False)
print("\nWSE summary at NOAA gauges (transcribed from paper)")
print(wse_summary.to_string(index=False))

# %% [markdown]
# ## Buoy wave statistics - average RMSE per configuration
#
# From paper Section 5.2 (pp. 7-8), for buoys covered in Table 3:
#
# - Hs RMSE: Ike - 0.900 m (Gen1), 1.033 m (Gen2), 0.802 m (Gen3); Ida -
#   0.813 m (Gen1), 0.883 m (Gen2), 0.834 m (Gen3).
# - Hs peak rel err (absolute average): Ike - 27% / 30% / 22%; Ida - 40% /
#   81% / 63%.
# - Tp RMSE: Ike - 2.822 s (Gen1), 2.541 s (Gen2), 2.413 s (Gen3); Ida -
#   4.865 s (Gen1), 5.068 s (Gen2), 9.960 s (Gen3).
# - Tp peak rel err (absolute average): Ike - 10% / 8% / 14%; Ida - 23% /
#   30% / 17%.
# - MWD RMSE: Ike - 43.238 deg (Gen1), 40.392 deg (Gen2), 37.076 deg (Gen3);
#   Ida - 62.380 deg (Gen1), 60.229 deg (Gen2), 67.730 deg (Gen3).

# %%
wave_summary = pd.DataFrame(
    [
        {"storm": "ike", "config": "Gen1", "Hs_RMSE_m": 0.900, "Hs_peak_pct_err": 27.0, "Tp_RMSE_s": 2.822, "Tp_peak_pct_err": 10.0, "MWD_RMSE_deg": 43.238},
        {"storm": "ike", "config": "Gen2", "Hs_RMSE_m": 1.033, "Hs_peak_pct_err": 30.0, "Tp_RMSE_s": 2.541, "Tp_peak_pct_err":  8.0, "MWD_RMSE_deg": 40.392},
        {"storm": "ike", "config": "Gen3", "Hs_RMSE_m": 0.802, "Hs_peak_pct_err": 22.0, "Tp_RMSE_s": 2.413, "Tp_peak_pct_err": 14.0, "MWD_RMSE_deg": 37.076},
        {"storm": "ida", "config": "Gen1", "Hs_RMSE_m": 0.813, "Hs_peak_pct_err": 40.0, "Tp_RMSE_s": 4.865, "Tp_peak_pct_err": 23.0, "MWD_RMSE_deg": 62.380},
        {"storm": "ida", "config": "Gen2", "Hs_RMSE_m": 0.883, "Hs_peak_pct_err": 81.0, "Tp_RMSE_s": 5.068, "Tp_peak_pct_err": 30.0, "MWD_RMSE_deg": 60.229},
        {"storm": "ida", "config": "Gen3", "Hs_RMSE_m": 0.834, "Hs_peak_pct_err": 63.0, "Tp_RMSE_s": 9.960, "Tp_peak_pct_err": 17.0, "MWD_RMSE_deg": 67.730},
    ]
)
wave_summary.to_csv(PUB_DIR / "wave_summary.csv", index=False)
print("\nWave statistics at NDBC buoys (transcribed from paper)")
print(wave_summary.to_string(index=False))

# %% [markdown]
# ## Observation-side context
#
# For each gauge / buoy we compute the obs peak in the wind-forcing window.
# This is the denominator of the paper's e_peak metric and is independent of
# any model output, so it can be used to sanity-check that the gauges we
# downloaded contain a storm signal in the expected window.

# %%
ds_wse_ike   = xr.open_dataset(PROC_DIR / "ike" / "wse.nc")
ds_wse_ida   = xr.open_dataset(PROC_DIR / "ida" / "wse.nc")
ds_waves_ike = xr.open_dataset(PROC_DIR / "ike" / "waves.nc")
ds_waves_ida = xr.open_dataset(PROC_DIR / "ida" / "waves.nc")


def obs_peaks_wse(ds: xr.Dataset, storm: str) -> pd.DataFrame:
    rows = []
    for i in range(ds.station.size):
        s = ds.isel(station=i)
        peak = float(s["wse_m"].max(skipna=True).values) if int(s["n_obs"]) > 0 else float("nan")
        rows.append({
            "storm": storm,
            "gauge_no": str(s["gauge_no"].values),
            "station": str(s["station"].values),
            "name": str(s["name"].values),
            "lat": float(s["lat"]),
            "lon": float(s["lon"]),
            "n_obs": int(s["n_obs"]),
            "obs_peak_m": peak,
        })
    return pd.DataFrame(rows)


def obs_peaks_waves(ds: xr.Dataset, storm: str) -> pd.DataFrame:
    rows = []
    for i in range(ds.buoy.size):
        b = ds.isel(buoy=i)
        peak_hs = float(b["Hs"].max(skipna=True).values) if int(b["n_obs_Hs"]) > 0 else float("nan")
        peak_tp = float(b["Tp"].max(skipna=True).values) if int(b["n_obs_Hs"]) > 0 else float("nan")
        rows.append({
            "storm": storm,
            "buoy_no": str(b["buoy_no"].values),
            "buoy": str(b["buoy"].values),
            "name": str(b["name"].values),
            "lat": float(b["lat"]),
            "lon": float(b["lon"]),
            "n_obs_Hs": int(b["n_obs_Hs"]),
            "obs_peak_Hs_m": peak_hs,
            "obs_peak_Tp_s": peak_tp,
        })
    return pd.DataFrame(rows)


obs_wse = pd.concat([obs_peaks_wse(ds_wse_ike, "ike"), obs_peaks_wse(ds_wse_ida, "ida")], ignore_index=True)
obs_waves = pd.concat([obs_peaks_waves(ds_waves_ike, "ike"), obs_peaks_waves(ds_waves_ida, "ida")], ignore_index=True)
obs_wse.to_csv(RESULTS_DIR / "obs_wse_peaks.csv", index=False)
obs_waves.to_csv(RESULTS_DIR / "obs_wave_peaks.csv", index=False)
print("\nObservation peak summary (WSE):")
print(obs_wse.to_string(index=False))
print("\nObservation peak summary (waves):")
print(obs_waves.to_string(index=False))

# %% [markdown]
# ## Headline comparison
#
# Assemble the trade-off table: per (storm, config) row, the wall-clock cost
# from Table 4 and the average WSE RMSE from Tables 5/6 + average Hs RMSE from
# Table 7. This is what the main result figure plots in notebook 04.

# %%
headline = (
    wse_summary.rename(columns={"avg_RMSE_m": "WSE_RMSE_m", "abs_avg_peak_pct_err": "WSE_peak_pct_err"})
    .merge(
        wave_summary[["storm", "config", "Hs_RMSE_m", "Tp_RMSE_s", "MWD_RMSE_deg"]],
        on=["storm", "config"],
        how="left",
    )
    .merge(
        table4.melt(id_vars="config", value_vars=["ike_h", "ida_h"], var_name="storm_h", value_name="runtime_h")
        .assign(storm=lambda d: d["storm_h"].str.replace("_h", "", regex=False))
        .drop(columns="storm_h"),
        on=["storm", "config"],
        how="left",
    )
)
# Ratio column: divide each config's runtime by the storm's No-SWAN baseline.
baseline = headline[headline["config"] == "No SWAN"].set_index("storm")["runtime_h"].to_dict()
headline["runtime_ratio"] = headline.apply(
    lambda r: r["runtime_h"] / baseline[r["storm"]] if not np.isnan(r["runtime_h"]) else np.nan, axis=1
)
headline = headline[["storm", "config", "runtime_h", "runtime_ratio", "WSE_RMSE_m", "WSE_peak_pct_err",
                     "Hs_RMSE_m", "Tp_RMSE_s", "MWD_RMSE_deg"]]
headline.to_csv(RESULTS_DIR / "headline_comparison.csv", index=False)
print("\nHeadline comparison (runtime vs accuracy across configs)")
print(headline.to_string(index=False))

# %% [markdown]
# ## Trade-off check
#
# The paper's central claim is that Gen1/Gen2 (reduced order) deliver
# significant compute savings versus Gen3 with relatively low additional error
# at the gauges. We check the relative compute savings and the per-storm
# RMSE deltas explicitly.

# %%
def trade_off(storm: str) -> dict:
    sub = headline[headline["storm"] == storm].set_index("config")
    return {
        "storm": storm,
        "Gen3_over_Gen1_runtime": sub.loc["Gen3", "runtime_h"] / sub.loc["Gen1", "runtime_h"],
        "Gen3_over_Gen2_runtime": sub.loc["Gen3", "runtime_h"] / sub.loc["Gen2", "runtime_h"],
        "Gen3_minus_Gen1_RMSE_m": sub.loc["Gen3", "WSE_RMSE_m"] - sub.loc["Gen1", "WSE_RMSE_m"],
        "Gen3_minus_Gen2_RMSE_m": sub.loc["Gen3", "WSE_RMSE_m"] - sub.loc["Gen2", "WSE_RMSE_m"],
        "Gen3_minus_Gen1_Hs_RMSE_m": sub.loc["Gen3", "Hs_RMSE_m"] - sub.loc["Gen1", "Hs_RMSE_m"],
    }


tradeoffs = pd.DataFrame([trade_off("ike"), trade_off("ida")])
tradeoffs.to_csv(RESULTS_DIR / "tradeoffs.csv", index=False)
print("\nTrade-off summary")
print(tradeoffs.to_string(index=False))
