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
# # 04 - Figures
#
# Figures for the Loveland et al. 2024 stat-level reproduction.
#
# Context plots (existing):
#
# - `figures/gauge_map.png` - cartopy map of all gauges and buoys for Ike+Ida.
# - `figures/wse_timeseries_example.png` - one well-located gauge per storm,
#   obs WSE time series with peak annotated.
# - `figures/main_result.png` - the trade-off plot that visualises the
#   headline claim: wall-clock cost (Table 4) versus accuracy across
#   Gen1 / Gen2 / Gen3 source-term packages at both gauges (WSE RMSE) and
#   buoys (Hs RMSE).
#
# Figure-level reproduction of Loveland's observational side (added in
# Phase 3 follow-up):
#
# - `figures/fig10_11_obs_equivalent.png` - observed peak WSE per gauge with
#   Loveland's storm-averaged RMSE bands (paper Figs 10 + 11 equivalent).
# - `figures/fig7_8_buoy_winds_equivalent.png` - NDBC buoy wind speed series
#   for the buoys plotted in Loveland's Figs 7 (Ike) and 8 (Ida).
# - `figures/fig5_6_obs_equivalent.png` - observed peak Hs and Tp per buoy
#   with Loveland's storm-averaged RMSE bands (paper Figs 5 + 6 equivalent).
#
# All three reproduction figures plot only the observational side; modelled
# bars / lines are deliberately omitted because the DesignSafe deposit (DOI
# 10.17603/DS2-7HBT-EF65) requires an authenticated account.

# %%
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

plt.style.use("seaborn-v0_8-whitegrid")  # per USER_PREFERENCES.md

# %%
PROC_DIR = Path("../data/processed")
RESULTS_DIR = Path("../results")
FIGURES_DIR = Path("../figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

ds_wse_ike   = xr.open_dataset(PROC_DIR / "ike" / "wse.nc")
ds_wse_ida   = xr.open_dataset(PROC_DIR / "ida" / "wse.nc")
ds_waves_ike = xr.open_dataset(PROC_DIR / "ike" / "waves.nc")
ds_waves_ida = xr.open_dataset(PROC_DIR / "ida" / "waves.nc")
headline = pd.read_csv(RESULTS_DIR / "headline_comparison.csv")
obs_wse = pd.read_csv(RESULTS_DIR / "obs_wse_peaks.csv")
obs_waves = pd.read_csv(RESULTS_DIR / "obs_wave_peaks.csv")

# Per USER_PREFERENCES.md (Phase 2 / 03_analysis.py): the config palette is
# shared across all trade-off plots and the new figure-level reproduction
# panels, so the eye keeps the same colour mapping across figures.
CONFIG_COLORS = {"Gen1": "#3498db", "Gen2": "#e67e22", "Gen3": "#27ae60"}

# %% [markdown]
# ## Figure 1 - gauge / buoy map

# %%
fig = plt.figure(figsize=(11, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-100, -84, 24, 32], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor="#f2efe9")
ax.add_feature(cfeature.OCEAN.with_scale("50m"), facecolor="#dceaf2")
ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.6)
ax.add_feature(cfeature.STATES.with_scale("50m"), linewidth=0.4, edgecolor="grey")

# WSE gauges
ax.scatter(ds_wse_ike["lon"].values, ds_wse_ike["lat"].values, marker="o",
           s=42, color="#c0392b", edgecolor="white", linewidth=0.6,
           transform=ccrs.PlateCarree(), label="Ike gauges (Table 1)", zorder=4)
ax.scatter(ds_wse_ida["lon"].values, ds_wse_ida["lat"].values, marker="s",
           s=42, color="#d4a017", edgecolor="white", linewidth=0.6,
           transform=ccrs.PlateCarree(), label="Ida gauges (Table 2)", zorder=4)
# Wave buoys (shared)
ax.scatter(ds_waves_ike["lon"].values, ds_waves_ike["lat"].values, marker="^",
           s=60, color="#2980b9", edgecolor="white", linewidth=0.6,
           transform=ccrs.PlateCarree(), label="NDBC wave buoys (Table 3)", zorder=4)
gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="grey", alpha=0.5)
gl.top_labels = False
gl.right_labels = False
ax.set_title("Loveland et al. 2024 - NOAA gauges + NDBC buoys (Ike, Ida)")
ax.legend(loc="lower left", fontsize=9, framealpha=0.9)
fig.tight_layout()
fig.savefig(FIGURES_DIR / "gauge_map.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## Figure 2 - example WSE time series
#
# Two well-located gauges: Galveston Pier 21 (8a, NOAA 8771450) for Ike,
# the gauge closest to Galveston in Table 1, and Grand Isle (10b,
# NOAA 8761724) for Ida, on the Louisiana coast where Ida made landfall.

# %%
def select_gauge(ds: xr.Dataset, gauge_no: str) -> xr.Dataset:
    idx = list(ds["gauge_no"].values).index(gauge_no)
    return ds.isel(station=idx)


g_ike = select_gauge(ds_wse_ike, "8a")
g_ida = select_gauge(ds_wse_ida, "10b")

fig, axes = plt.subplots(2, 1, figsize=(10, 6.5), sharex=False)

for ax, ds_g, storm, color in zip(
    axes,
    (g_ike, g_ida),
    ("Hurricane Ike (8a Galveston Pier 21)", "Hurricane Ida (10b Grand Isle)"),
    ("#c0392b", "#d4a017"),
):
    t = pd.to_datetime(ds_g["time"].values)
    y = ds_g["wse_m"].values
    ax.plot(t, y, color=color, linewidth=1.0)
    finite = np.isfinite(y)
    if finite.any():
        peak_idx = int(np.nanargmax(y))
        ax.axvline(t[peak_idx], color="black", linewidth=0.6, linestyle=":")
        ax.scatter([t[peak_idx]], [y[peak_idx]], color="black", s=18, zorder=4)
        ax.annotate(
            f"peak {y[peak_idx]:.2f} m",
            xy=(t[peak_idx], y[peak_idx]),
            xytext=(8, 10),
            textcoords="offset points",
            fontsize=9,
        )
    ax.set_title(storm)
    ax.set_ylabel("WSE (m, NAVD88 where avail.)")
    ax.tick_params(axis="x", rotation=20)

fig.suptitle("Observed WSE during storm windows (NOAA CO-OPS)")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "wse_timeseries_example.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## Figure 3 - main result: compute vs accuracy trade-off
#
# Visualises the headline claim from the abstract: reduced-order source terms
# (Gen1, Gen2) save significant compute time, with relatively small added
# error at the WSE gauges. The buoy Hs RMSE panel shows the qualifier - Gen3
# is meaningfully better than Gen1/Gen2 for Hs during Ike but not during Ida.
#
# Bars are coloured by configuration; left axis runtime in hours, right axis
# RMSE.

# %%
df = headline[headline["config"].isin(["Gen1", "Gen2", "Gen3"])].copy()
configs = ["Gen1", "Gen2", "Gen3"]
storms = ["ike", "ida"]
config_colors = CONFIG_COLORS

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=False)

bar_width = 0.22
x = np.arange(len(storms))

# Panel 1 - runtime
ax = axes[0]
for i, cfg in enumerate(configs):
    sub = df[df["config"] == cfg].set_index("storm").reindex(storms)
    ax.bar(x + (i - 1) * bar_width, sub["runtime_h"], width=bar_width,
           color=config_colors[cfg], label=cfg, edgecolor="white", linewidth=0.6)
    for j, val in enumerate(sub["runtime_h"]):
        ax.text(x[j] + (i - 1) * bar_width, val + 0.06, f"{val:.2f}h",
                ha="center", va="bottom", fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels([s.title() for s in storms])
ax.set_ylabel("Wall-clock run time (h, 1064 cores)")
ax.set_title("Compute cost (Table 4)")
ax.legend(title="SWAN source terms", loc="upper left", fontsize=9)
ax.set_ylim(0, max(df["runtime_h"]) * 1.18)

# Panel 2 - accuracy at gauges + buoys
ax = axes[1]
metrics = [("WSE_RMSE_m", "WSE RMSE (m)\nat gauges", "o"),
           ("Hs_RMSE_m", "Hs RMSE (m)\nat buoys",   "s")]
for k, (col, label, marker) in enumerate(metrics):
    for i, cfg in enumerate(configs):
        sub = df[df["config"] == cfg].set_index("storm").reindex(storms)
        x_off = x + (i - 1) * bar_width + k * 0.03
        ax.scatter(x_off, sub[col], s=110, marker=marker, color=config_colors[cfg],
                   edgecolor="black", linewidth=0.5, label=f"{cfg} {label}" if k == 1 else None)
ax.set_xticks(x)
ax.set_xticklabels([s.title() for s in storms])
ax.set_ylabel("RMSE")
ax.set_title("Accuracy vs observations (Tables 5-7)")
# Custom legend - markers for metric, colours already taken
from matplotlib.lines import Line2D  # noqa: E402

legend_elems = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="grey", markersize=10, label="WSE RMSE (m)"),
    Line2D([0], [0], marker="s", color="w", markerfacecolor="grey", markersize=10, label="Hs RMSE (m)"),
] + [
    Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=10, label=name)
    for name, c in config_colors.items()
]
ax.legend(handles=legend_elems, loc="upper left", fontsize=8, ncol=2)

fig.suptitle(
    "Loveland et al. 2024 (Gulf of Mexico): reduced-order source terms\n"
    "save 30-40% wall-clock at < 5% added WSE-RMSE cost",
    fontsize=12,
)
fig.tight_layout()
fig.savefig(FIGURES_DIR / "main_result.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## Figure A - observed peak WSE per gauge (Loveland Figs 10 + 11 equivalent)
#
# Two panels (Ike top, Ida bottom). For each panel, the bars are the observed
# peak WSE per gauge (NOAA CO-OPS, NAVD88 where available) over the
# wind-forcing window. Horizontal reference lines are the storm-averaged
# Gen1 / Gen2 / Gen3 WSE RMSE values transcribed verbatim from the paper's
# body text (notebook 03). The modelled bars from Loveland's Fig 10/11 cannot
# be reproduced here because the ADCIRC+SWAN outputs sit behind a DesignSafe
# authentication gate.
#
# The bands span across all gauge bars; their tight clustering is the
# WSE-invariance finding (delta RMSE across configs <= 0.007 m for Ike,
# <= 0.001 m for Ida) that conditions the headline trade-off.

# %%
# Storm-averaged WSE RMSE values for each Gen1/2/3 config, looked up from the
# transcribed-baseline table written by notebook 03.
def storm_rmse(storm: str, cfg: str, col: str) -> float:
    sub = headline[(headline["storm"] == storm) & (headline["config"] == cfg)]
    if sub.empty:
        return float("nan")
    return float(sub.iloc[0][col])


def gauge_order(storm: str) -> list:
    """Loveland's gauge order: by gauge_no index (1a, 2a, ... or 1b, 2b, ...)."""
    sub = obs_wse[obs_wse["storm"] == storm].copy()
    sub["order"] = sub["gauge_no"].str.extract(r"(\d+)").astype(int)
    return sub.sort_values("order")["gauge_no"].tolist()


fig, axes = plt.subplots(2, 1, figsize=(11.5, 8), sharex=False)

for ax, storm, panel_color, gauge_color in zip(
    axes,
    ("ike", "ida"),
    ("Hurricane Ike (Sept 5-14, 2008)", "Hurricane Ida (Aug 26 - Sep 4, 2021)"),
    ("#c0392b", "#d4a017"),
):
    order = gauge_order(storm)
    sub = (
        obs_wse[obs_wse["storm"] == storm]
        .set_index("gauge_no")
        .reindex(order)
        .reset_index()
    )
    x_pos = np.arange(len(sub))
    ax.bar(
        x_pos,
        sub["obs_peak_m"],
        color=gauge_color,
        edgecolor="white",
        linewidth=0.6,
        label="Observed peak WSE",
    )
    # Annotate bar heights so the eye can sanity-check against Loveland's
    # peak-error percentages.
    for j, val in enumerate(sub["obs_peak_m"]):
        if np.isfinite(val):
            ax.text(j, val + 0.05, f"{val:.2f}", ha="center", va="bottom", fontsize=7.5)
    # Reference bands at storm-averaged RMSE per config.
    for cfg in ("Gen1", "Gen2", "Gen3"):
        rmse_val = storm_rmse(storm, cfg, "WSE_RMSE_m")
        ax.axhline(
            rmse_val,
            color=CONFIG_COLORS[cfg],
            linewidth=1.4,
            linestyle="--",
            label=f"{cfg} avg RMSE = {rmse_val:.3f} m",
        )
    ax.set_xticks(x_pos)
    ax.set_xticklabels(sub["gauge_no"], rotation=0, fontsize=9)
    ax.set_ylabel("Peak WSE (m)")
    ax.set_title(panel_color)
    ax.set_ylim(0, max(sub["obs_peak_m"].max() * 1.18, 0.5))
    ax.legend(loc="upper right", fontsize=8, ncol=2, framealpha=0.92)
    # In-panel annotation summarising the WSE-invariance finding for the
    # storm. Loveland's three configs' avg RMSE differ by <=0.007 m for Ike
    # and <=0.001 m for Ida - smaller than typical CO-OPS observational
    # uncertainty (~0.02 m).
    if storm == "ike":
        delta = (
            storm_rmse("ike", "Gen3", "WSE_RMSE_m")
            - storm_rmse("ike", "Gen1", "WSE_RMSE_m")
        )
        msg = f"Delta RMSE across configs = {delta:+.3f} m (within observational noise)"
    else:
        delta = (
            storm_rmse("ida", "Gen3", "WSE_RMSE_m")
            - storm_rmse("ida", "Gen1", "WSE_RMSE_m")
        )
        msg = f"Delta RMSE across configs = {delta:+.3f} m (within observational noise)"
    ax.text(
        0.01,
        0.97,
        msg,
        transform=ax.transAxes,
        fontsize=8.5,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85, edgecolor="grey"),
    )

fig.suptitle(
    "Observed peak WSE per gauge with Loveland (2024) storm-averaged RMSE bands",
    fontsize=12,
)
# Caption beneath the panels - explains why no modelled bars are shown.
fig.text(
    0.5,
    -0.01,
    "Loveland Fig 10 / 11 equivalent - model bars not reproduced "
    "(DesignSafe deposit DOI 10.17603/DS2-7HBT-EF65 access-restricted).",
    ha="center",
    fontsize=9,
    style="italic",
)
fig.tight_layout()
fig.savefig(FIGURES_DIR / "fig10_11_obs_equivalent.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## Figure B - NDBC buoy wind speed (Loveland Figs 7 + 8 equivalent)
#
# Two-column layout (Ike left, Ida right) by four-row (one buoy per row).
# Plots only the NDBC standard-met wind-speed series; the ADCIRC wind-input
# trace is omitted because the model output is access-restricted.
#
# Buoy selections per Loveland Section 5.1:
# - Ike Fig 7: 42001, 42002, 42019, 42035.
# - Ida Fig 8: 42001, 42007, 42039, 42040. Loveland's Fig 8 shows ADCIRC's
#   Ida winds visibly diverging from the buoys near landfall, which is the
#   wind-field-accuracy caveat that conditions the headline Outcome.
#
# Axis convention follows Loveland: x = days since first wind-forcing time
# stamp, y = wind speed in m/s. Buoys missing in the 2021 NDBC archive
# (42001 retired July 2021; 42007 dropped from stdmet 2021) are flagged in
# the panel.

# %%
IKE_WIND_BUOYS = ["42001", "42002", "42019", "42035"]
IDA_WIND_BUOYS = ["42001", "42007", "42039", "42040"]


def wind_series(ds_waves: xr.Dataset, buoy_id: str):
    """Return (days_since_t0, wspd_m_per_s) for the given buoy."""
    ids = list(ds_waves["buoy"].values.astype(str))
    if buoy_id not in ids:
        return None, None
    idx = ids.index(buoy_id)
    times = pd.to_datetime(ds_waves["time"].values)
    t0 = times[0]
    days = (times - t0).total_seconds() / 86400.0
    wspd = ds_waves["WSPD"].isel(buoy=idx).values
    return days, wspd


fig, axes = plt.subplots(4, 2, figsize=(12, 11), sharex="col")

storm_specs = [
    ("ike", "Hurricane Ike", IKE_WIND_BUOYS, ds_waves_ike, 0),
    ("ida", "Hurricane Ida", IDA_WIND_BUOYS, ds_waves_ida, 1),
]

for storm, storm_label, buoys, ds_waves_storm, col in storm_specs:
    for row, buoy_id in enumerate(buoys):
        ax = axes[row, col]
        days, wspd = wind_series(ds_waves_storm, buoy_id)
        if days is None or wspd is None or not np.isfinite(wspd).any():
            ax.text(
                0.5,
                0.5,
                f"NDBC {buoy_id}: not available in archive\n({storm_label} window)",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=10,
                color="#7f8c8d",
            )
            ax.set_ylim(0, 30)
        else:
            ax.plot(
                days,
                wspd,
                color="#2c3e50",
                linewidth=0.9,
                marker=".",
                markersize=2.5,
                label="NDBC observed",
            )
            peak = np.nanmax(wspd) if np.isfinite(wspd).any() else float("nan")
            if np.isfinite(peak):
                ax.set_ylim(0, max(peak * 1.18, 15))
        ax.set_ylabel(f"NDBC {buoy_id}\nwind speed (m/s)", fontsize=9)
        if row == 0:
            ax.set_title(f"{storm_label} buoys", fontsize=11)
        if row == 3:
            ax.set_xlabel("Days since first wind-forcing timestamp")

fig.suptitle("NDBC buoy wind speed during storm windows", fontsize=12)
fig.text(
    0.5,
    -0.005,
    "Loveland Fig 7 / 8 equivalent - buoy data only; ADCIRC wind line not "
    "reproduced (model output access-restricted).\n"
    "Loveland's Fig 8 visibly shows ADCIRC's Ida winds diverging from the "
    "buoys near landfall - this wind-field accuracy caveat conditions the "
    "headline Outcome.",
    ha="center",
    fontsize=8.5,
    style="italic",
)
fig.tight_layout()
fig.savefig(FIGURES_DIR / "fig7_8_buoy_winds_equivalent.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## Figure C - observed peak Hs and Tp per buoy (Loveland Figs 5 + 6 equivalent)
#
# Two rows (Ike top, Ida bottom) x two columns (Hs left, Tp right). Bars are
# observed peaks at each Table 3 buoy in the wind-forcing window. Reference
# bands are storm-averaged Hs / Tp RMSE per Gen config (transcribed from the
# paper).
#
# Notable feature: Loveland's Ida Tp Gen3 = 9.960 s is about a factor of two
# worse than Gen1 (4.865 s) - this divergence is the wave-stats sensitivity
# carved out by the chain's Quote.

# %%
def buoy_order(storm: str) -> list:
    sub = obs_waves[obs_waves["storm"] == storm].copy()
    sub["order"] = sub["buoy_no"].str.extract(r"(\d+)").astype(int)
    return sub.sort_values("order")["buoy_no"].tolist()


fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=False)

panel_specs = [
    ("ike", "Hs", "obs_peak_Hs_m", "Hs_RMSE_m", "Peak Hs (m)",
     "Hurricane Ike", 0, 0, "#2980b9"),
    ("ike", "Tp", "obs_peak_Tp_s", "Tp_RMSE_s", "Peak Tp (s)",
     "Hurricane Ike", 0, 1, "#16a085"),
    ("ida", "Hs", "obs_peak_Hs_m", "Hs_RMSE_m", "Peak Hs (m)",
     "Hurricane Ida", 1, 0, "#2980b9"),
    ("ida", "Tp", "obs_peak_Tp_s", "Tp_RMSE_s", "Peak Tp (s)",
     "Hurricane Ida", 1, 1, "#16a085"),
]

for storm, metric, obs_col, rmse_col, ylabel, storm_label, r, c, bar_color in panel_specs:
    ax = axes[r, c]
    order = buoy_order(storm)
    sub = (
        obs_waves[obs_waves["storm"] == storm]
        .set_index("buoy_no")
        .reindex(order)
        .reset_index()
    )
    x_pos = np.arange(len(sub))
    bar_vals = sub[obs_col].to_numpy(dtype="float64")
    ax.bar(
        x_pos,
        np.where(np.isfinite(bar_vals), bar_vals, 0.0),
        color=bar_color,
        edgecolor="white",
        linewidth=0.6,
        label=f"Observed peak {metric}",
    )
    # Annotate any buoy where data is missing.
    for j, val in enumerate(bar_vals):
        if not np.isfinite(val):
            ax.text(
                j,
                0.15,
                "n/a",
                ha="center",
                va="bottom",
                fontsize=8,
                color="#7f8c8d",
            )
        else:
            ax.text(
                j,
                val + (0.04 if metric == "Hs" else 0.25),
                f"{val:.1f}",
                ha="center",
                va="bottom",
                fontsize=7.5,
            )
    # Reference bands per config.
    for cfg in ("Gen1", "Gen2", "Gen3"):
        rmse_val = storm_rmse(storm, cfg, rmse_col)
        ax.axhline(
            rmse_val,
            color=CONFIG_COLORS[cfg],
            linewidth=1.4,
            linestyle="--",
            label=f"{cfg} avg RMSE = {rmse_val:.3f}",
        )
    ax.set_xticks(x_pos)
    ax.set_xticklabels(sub["buoy_no"], rotation=0, fontsize=9)
    ax.set_ylabel(ylabel)
    finite_peak = np.nanmax(bar_vals) if np.isfinite(bar_vals).any() else 1.0
    rmse_max = max(
        storm_rmse(storm, "Gen1", rmse_col),
        storm_rmse(storm, "Gen2", rmse_col),
        storm_rmse(storm, "Gen3", rmse_col),
    )
    ax.set_ylim(0, max(finite_peak, rmse_max) * 1.22)
    ax.set_title(f"{storm_label} - {metric}", fontsize=10)
    ax.legend(loc="upper right", fontsize=7.5, ncol=1, framealpha=0.92)

fig.suptitle(
    "Observed peak Hs and Tp per buoy with Loveland (2024) "
    "storm-averaged RMSE bands",
    fontsize=12,
)
fig.text(
    0.5,
    -0.01,
    "Loveland Fig 5 / 6 partial equivalent - model bars not reproduced. "
    "Ida Tp Gen3 = 9.96 s is approximately twice the Gen1 value (4.87 s); "
    "this divergence is Loveland's quantification of the wave-stats "
    "sensitivity carried in the chain's Quote.",
    ha="center",
    fontsize=8.5,
    style="italic",
)
fig.tight_layout()
fig.savefig(FIGURES_DIR / "fig5_6_obs_equivalent.png", dpi=150, bbox_inches="tight")
plt.show()
