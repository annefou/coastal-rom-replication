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
# Three figures for the Loveland et al. 2024 stat-level reproduction:
#
# - `figures/gauge_map.png` - cartopy map of all gauges and buoys for Ike+Ida.
# - `figures/wse_timeseries_example.png` - one well-located gauge per storm,
#   obs WSE time series with peak annotated.
# - `figures/main_result.png` - the trade-off plot that visualises the
#   headline claim: wall-clock cost (Table 4) versus accuracy across
#   Gen1 / Gen2 / Gen3 source-term packages at both gauges (WSE RMSE) and
#   buoys (Hs RMSE).

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
headline = pd.read_csv(RESULTS_DIR / "headline_comparison.csv")
obs_wse = pd.read_csv(RESULTS_DIR / "obs_wse_peaks.csv")

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
config_colors = {"Gen1": "#3498db", "Gen2": "#e67e22", "Gen3": "#27ae60"}

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
