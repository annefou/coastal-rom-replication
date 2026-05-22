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
# # 02 - Data clean
#
# Convert the raw NOAA CO-OPS gauge CSVs and NDBC buoy CSVs from
# `data/raw/` into per-storm xarray Datasets aligned on a common time index,
# saved as NetCDF in `data/processed/{storm}/` (NetCDF preferred over .npz per
# DOMAIN.md).
#
# The two storm windows from Loveland et al. 2024 Section 4.1:
#
# - Hurricane Ike: 5-14 September 2008 (8 days 18 hours of wind forcing).
# - Hurricane Ida: 26 August - 4 September 2021 (9 days 6 hours of wind forcing).
#
# Per the paper, "errors are computed at each station while wind forcing is
# active to avoid biasing the results to when the contribution from wind
# waves is not active". We trim each observation series to the wind-forcing
# window so the QC view matches the paper's evaluation window.

# %%
import json
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

# %%
RAW_DIR = Path("../data/raw")
PROC_DIR = Path("../data/processed")
(PROC_DIR / "ike").mkdir(parents=True, exist_ok=True)
(PROC_DIR / "ida").mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## Load the source manifest written by notebook 01

# %%
with open(RAW_DIR / "sources.json") as f:
    manifest = json.load(f)

WSE_IKE_STATIONS = manifest["stations"]["wse_ike"]
WSE_IDA_STATIONS = manifest["stations"]["wse_ida"]
WAVE_BUOYS = manifest["stations"]["waves"]

# Wind-forcing windows (per Loveland et al. 2024 Section 4.1).
# Ike: 5 September 2008 12:00 GMT -> 14 September 2008 06:00 GMT.
# Ida: 26 August 2021 12:00 GMT -> 4 September 2021 18:00 GMT.
WINDOWS = {
    "ike": ("2008-09-05T12:00", "2008-09-14T06:00"),
    "ida": ("2021-08-26T12:00", "2021-09-04T18:00"),
}


# %% [markdown]
# ## Helpers

# %%
def load_gauge_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size < 200:
        return pd.DataFrame(columns=["time", "wse_m"])
    df = pd.read_csv(path, parse_dates=["time"])
    if "wse_m" not in df.columns:
        return pd.DataFrame(columns=["time", "wse_m"])
    # Drop rows where wse_m is null or duplicated timestamps
    df = df.dropna(subset=["wse_m"]).drop_duplicates(subset=["time"])
    return df


def build_wse_dataset(stations: list, storm: str) -> xr.Dataset:
    """Build a (time, station) xarray Dataset for the storm window."""
    t_start, t_end = WINDOWS[storm]
    raw_subdir = "wse_ike" if storm == "ike" else "wse_ida"
    # Common 6-min time index (CO-OPS native cadence).
    time_index = pd.date_range(t_start, t_end, freq="6min", tz="UTC")
    station_ids = [s["id"] for s in stations]
    wse = np.full((len(time_index), len(stations)), np.nan, dtype="float32")
    n_obs = np.zeros(len(stations), dtype="int32")
    for i, st in enumerate(stations):
        df = load_gauge_csv(RAW_DIR / raw_subdir / f"{st['id']}.csv")
        if df.empty:
            continue
        df = df.set_index("time")
        # Trim to wind window
        df = df[(df.index >= time_index[0]) & (df.index <= time_index[-1])]
        # Reindex to the common grid (no fill - keep NaN for gaps).
        df = df.reindex(time_index)
        wse[:, i] = df["wse_m"].to_numpy(dtype="float32")
        n_obs[i] = int(df["wse_m"].notna().sum())
    ds = xr.Dataset(
        data_vars={
            "wse_m": (("time", "station"), wse, {
                "long_name": "Water surface elevation",
                "units": "m",
                "standard_name": "sea_surface_height_above_geopotential_datum",
                "note": "NAVD88 where available, fall back to MSL per CO-OPS station support",
            }),
            "n_obs": (("station",), n_obs, {
                "long_name": "Number of valid observations in storm window",
            }),
        },
        coords={
            "time": ("time", time_index.tz_convert(None).to_pydatetime()),
            "station": ("station", station_ids),
            "gauge_no": ("station", [s["gauge_no"] for s in stations]),
            "name": ("station", [s["name"] for s in stations]),
            "lat": ("station", [s["lat"] for s in stations]),
            "lon": ("station", [s["lon"] for s in stations]),
        },
        attrs={
            "title": f"Cleaned NOAA CO-OPS WSE for Hurricane {storm.title()}",
            "source": manifest["sources"][0]["url"],
            "reference_paper": manifest["paper_doi"],
            "storm_window_utc": f"{t_start} / {t_end}",
        },
    )
    return ds


def load_buoy_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size < 200:
        return pd.DataFrame(columns=["time", "WVHT", "DPD", "MWD"])
    df = pd.read_csv(path, parse_dates=["time"])
    keep = [c for c in ("time", "WVHT", "DPD", "APD", "MWD") if c in df.columns]
    df = df[keep].dropna(subset=["time"]).drop_duplicates(subset=["time"])
    return df


def build_waves_dataset(buoys: list, storm: str) -> xr.Dataset:
    """Build a (time, buoy) xarray Dataset for Hs/Tp/MWD in the storm window."""
    year = 2008 if storm == "ike" else 2021
    t_start, t_end = WINDOWS[storm]
    # NDBC standard-met cadence is 50 min - resample to a regular 1-h index for both storms.
    time_index = pd.date_range(t_start, t_end, freq="1h", tz="UTC")
    buoy_ids = [b["id"] for b in buoys]
    hs = np.full((len(time_index), len(buoys)), np.nan, dtype="float32")
    tp = np.full((len(time_index), len(buoys)), np.nan, dtype="float32")
    mwd = np.full((len(time_index), len(buoys)), np.nan, dtype="float32")
    n_obs = np.zeros(len(buoys), dtype="int32")
    for i, b in enumerate(buoys):
        df = load_buoy_csv(RAW_DIR / "waves" / f"{b['id']}_{year}.csv")
        if df.empty:
            continue
        df = df.set_index("time")
        df = df[(df.index >= time_index[0]) & (df.index <= time_index[-1])]
        # NDBC files mix high-cadence (10-min) wind rows with hourly wave rows;
        # the hourly wave rows often sit at :40 or :50 past the hour while the
        # wind rows sit at :00, :10, :20. Nearest-match would prefer the :00 row
        # (NaN WVHT) over the :40 valid Hs row. Resample each variable on its
        # own valid rows to the regular hourly grid.
        for col, arr in (("WVHT", hs), ("DPD", tp), ("MWD", mwd)):
            if col not in df.columns:
                continue
            valid = df[col].dropna()
            if valid.empty:
                continue
            r = valid.reindex(time_index, method="nearest", tolerance=pd.Timedelta("1h"))
            arr[:, i] = r.to_numpy(dtype="float32")
        if "WVHT" in df.columns:
            n_obs[i] = int(np.isfinite(hs[:, i]).sum())
    ds = xr.Dataset(
        data_vars={
            "Hs": (("time", "buoy"), hs, {"long_name": "Significant wave height", "units": "m"}),
            "Tp": (("time", "buoy"), tp, {"long_name": "Dominant wave period", "units": "s"}),
            "MWD": (("time", "buoy"), mwd, {"long_name": "Mean wave direction", "units": "degree"}),
            "n_obs_Hs": (("buoy",), n_obs, {"long_name": "Valid Hs observations in window"}),
        },
        coords={
            "time": ("time", time_index.tz_convert(None).to_pydatetime()),
            "buoy": ("buoy", buoy_ids),
            "buoy_no": ("buoy", [b["buoy_no"] for b in buoys]),
            "name": ("buoy", [b["name"] for b in buoys]),
            "lat": ("buoy", [b["lat"] for b in buoys]),
            "lon": ("buoy", [b["lon"] for b in buoys]),
        },
        attrs={
            "title": f"Cleaned NOAA NDBC wave statistics for Hurricane {storm.title()}",
            "source": manifest["sources"][1]["url"],
            "reference_paper": manifest["paper_doi"],
            "storm_window_utc": f"{t_start} / {t_end}",
        },
    )
    return ds


# %% [markdown]
# ## Build and save

# %%
ds_wse_ike = build_wse_dataset(WSE_IKE_STATIONS, "ike")
ds_wse_ida = build_wse_dataset(WSE_IDA_STATIONS, "ida")
ds_waves_ike = build_waves_dataset(WAVE_BUOYS, "ike")
ds_waves_ida = build_waves_dataset(WAVE_BUOYS, "ida")

ds_wse_ike.to_netcdf(PROC_DIR / "ike" / "wse.nc")
ds_wse_ida.to_netcdf(PROC_DIR / "ida" / "wse.nc")
ds_waves_ike.to_netcdf(PROC_DIR / "ike" / "waves.nc")
ds_waves_ida.to_netcdf(PROC_DIR / "ida" / "waves.nc")

# %% [markdown]
# ## QC summary

# %%
qc = pd.DataFrame({
    "dataset":    ["wse_ike", "wse_ida", "waves_ike", "waves_ida"],
    "n_stations": [ds_wse_ike.station.size, ds_wse_ida.station.size, ds_waves_ike.buoy.size, ds_waves_ida.buoy.size],
    "n_times":    [ds_wse_ike.time.size,    ds_wse_ida.time.size,    ds_waves_ike.time.size, ds_waves_ida.time.size],
    "stations_with_data": [
        int((ds_wse_ike["n_obs"] > 0).sum()),
        int((ds_wse_ida["n_obs"] > 0).sum()),
        int((ds_waves_ike["n_obs_Hs"] > 0).sum()),
        int((ds_waves_ida["n_obs_Hs"] > 0).sum()),
    ],
})
qc.to_csv(PROC_DIR / "qc_summary.csv", index=False)
print(qc.to_string(index=False))
