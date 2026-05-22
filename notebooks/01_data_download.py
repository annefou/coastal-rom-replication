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
# # 01 - Data download
#
# Reproduction of the observational side of Loveland et al. (2024),
# *Efficacy of reduced order source terms for a coupled wave-circulation model
# in the Gulf of Mexico*, Ocean Modelling 190: 102387,
# DOI: 10.1016/j.ocemod.2024.102387.
#
# ## Scope of this notebook
#
# This is a **stat-level (figure-and-table) reproduction**, not a full
# ADCIRC+SWAN model re-run. The original runs used 1064 Frontera cores on
# meshes of 3-6 million elements; reproducing that on a laptop / GitHub Actions
# is out of scope.
#
# Instead this notebook downloads:
#
# 1. NOAA CO-OPS water-level gauge data for the gauges in Tables 1 (Ike,
#    14 stations, 5-14 September 2008) and 2 (Ida, 13 stations,
#    26 August - 4 September 2021) of Loveland et al. 2024.
# 2. NOAA NDBC standard-meteorological buoy data for the 10 wave buoys in
#    Table 3 of the paper (shared between Ike and Ida).
#
# ## Authors' deposited data
#
# Loveland, M., Meixner, J., Valseth, E., Dawson, C. (2024).
# *ADCIRC+SWAN Runs for Hurricane Ike and Hurricane Ida Using Various Source
# Terms*. DesignSafe-CI, DOI: 10.17603/DS2-7HBT-EF65,
# https://www.designsafe-ci.org/data/browser/public/designsafe.storage.published/PRJ-4678/
#
# The DesignSafe DOI resolves, but the data files behind it require an
# authenticated DesignSafe account: the public API returns HTTP 401
# (`{"message": "Unauthenticated user"}`) for both
# `/api/projects/v2/PRJ-4678/` and
# `/api/datafiles/listing/public/designsafe.storage.published/PRJ-4678/`.
# DesignSafe-CI hosts the model outputs (fort.61 WSE time series, fort.63
# global WSE fields, fort.74 wind stresses, SWAN .mat files, fort.26 source-term
# configs, mesh files) but they cannot be fetched programmatically without
# credentials.
#
# Consequence: this replication compares the paper's transcribed Table 4-7
# baselines against the published observational record only. The
# observation-versus-model RMSE itself remains the authors' as transcribed
# from the PDF; we add the obs side as a verification surface and a
# context-plot for the headline trade-off.
#
# ## Public APIs used
#
# - **NOAA CO-OPS** (water levels): https://api.tidesandcurrents.noaa.gov - no
#   auth, returns JSON, 6-min interval. Datum NAVD88 (consistent with hurricane
#   storm-surge convention).
# - **NOAA NDBC** (wave buoys): https://www.ndbc.noaa.gov/data/historical/stdmet
#   - no auth, returns space-delimited .txt.gz files, ~50-min standard-met
#   interval. Columns: WVHT (significant wave height Hs, m), DPD (dominant
#   wave period Tp, s), MWD (mean wave direction, deg).

# %%
import gzip
import io
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests
from tqdm import tqdm

# %%
RAW_DIR = Path("../data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
(RAW_DIR / "wse_ike").mkdir(exist_ok=True)
(RAW_DIR / "wse_ida").mkdir(exist_ok=True)
(RAW_DIR / "waves").mkdir(exist_ok=True)

# %% [markdown]
# ## Station registries
#
# Transcribed verbatim from Tables 1, 2, 3 of Loveland et al. 2024.

# %%
# Table 1 - Water surface elevation stations for Hurricane Ike.
WSE_IKE_STATIONS = [
    {"gauge_no": "1a", "name": "Bob Hall Pier Corpus Christi", "id": "8775870", "lat": 27.5800, "lon": -97.2167},
    {"gauge_no": "2a", "name": "Port Aransas",                  "id": "8775237", "lat": 27.8404, "lon": -97.0730},
    {"gauge_no": "3a", "name": "Rockport",                      "id": "8774770", "lat": 28.0217, "lon": -97.0467},
    {"gauge_no": "4a", "name": "USCG Freeport",                 "id": "8772447", "lat": 28.9428, "lon": -95.3025},
    {"gauge_no": "5a", "name": "Manchester Houston",            "id": "8770777", "lat": 29.7247, "lon": -95.2656},
    {"gauge_no": "6a", "name": "Morgans Point",                 "id": "8770613", "lat": 29.6817, "lon": -94.9850},
    {"gauge_no": "7a", "name": "Eagle Point",                   "id": "8771013", "lat": 29.4813, "lon": -94.9172},
    {"gauge_no": "8a", "name": "Galveston Pier 21",             "id": "8771450", "lat": 29.3100, "lon": -94.7933},
    {"gauge_no": "9a", "name": "Galveston Pleasure Pier",       "id": "8771510", "lat": 29.2849, "lon": -94.7894},
    {"gauge_no": "10a", "name": "Galveston Bay Entrance North Jetty", "id": "8771341", "lat": 29.3576, "lon": -94.7260},
    {"gauge_no": "11a", "name": "Freshwater Canal Locks",       "id": "8766072", "lat": 29.5541, "lon": -92.3082},
    {"gauge_no": "12a", "name": "Port Fourchon",                "id": "8762075", "lat": 29.0848, "lon": -90.1985},
    {"gauge_no": "13a", "name": "New Canal Station",            "id": "8761927", "lat": 30.0272, "lon": -90.1134},
    {"gauge_no": "14a", "name": "Shell Beach",                  "id": "8761305", "lat": 29.8681, "lon": -89.6733},
]
IKE_DATE_RANGE = ("20080905", "20080914")  # 5-14 September 2008 - per paper Section 4.1

# Table 2 - Water surface elevation stations for Hurricane Ida.
WSE_IDA_STATIONS = [
    {"gauge_no": "1b", "name": "Calcasieu Pass",                "id": "8768094", "lat": 29.7683, "lon": -93.3433},
    {"gauge_no": "2b", "name": "Bulk Terminal",                 "id": "8767961", "lat": 30.1900, "lon": -93.3000},
    {"gauge_no": "3b", "name": "Freshwater Canal Locks",        "id": "8766072", "lat": 29.5541, "lon": -92.3082},
    {"gauge_no": "4b", "name": "Eugene Island",                 "id": "8764314", "lat": 29.3667, "lon": -91.3833},
    {"gauge_no": "5b", "name": "LAWMA Amerada Pass",            "id": "8764227", "lat": 29.4500, "lon": -91.3383},
    {"gauge_no": "6b", "name": "West Bank 1",                   "id": "8762482", "lat": 29.7838, "lon": -90.4200},
    {"gauge_no": "7b", "name": "Port Fourchon",                 "id": "8762075", "lat": 29.1142, "lon": -90.1993},
    {"gauge_no": "8b", "name": "Carrollton",                    "id": "8761955", "lat": 29.9333, "lon": -90.1350},
    {"gauge_no": "9b", "name": "New Canal Station",             "id": "8761927", "lat": 30.0272, "lon": -90.1133},
    {"gauge_no": "10b", "name": "Grand Isle",                   "id": "8761724", "lat": 29.2633, "lon": -89.9567},
    {"gauge_no": "11b", "name": "Pilots Station East",          "id": "8760922", "lat": 28.9316, "lon": -89.4067},
    {"gauge_no": "12b", "name": "Pilottown, LA",                "id": "8760721", "lat": 29.1793, "lon": -89.2588},
    {"gauge_no": "13b", "name": "Shell Beach",                  "id": "8761305", "lat": 30.1267, "lon": -89.2217},
]
IDA_DATE_RANGE = ("20210826", "20210904")  # 26 August - 4 September 2021 - per paper Section 4.1

# Table 3 - Wave-buoy stations used in both scenarios.
WAVE_BUOYS = [
    {"buoy_no": "1w",  "name": "NBDC 42020", "id": "42020", "lat": 26.9680, "lon": -96.6930},
    {"buoy_no": "2w",  "name": "NBDC 42019", "id": "42019", "lat": 27.9100, "lon": -95.3450},
    {"buoy_no": "3w",  "name": "NBDC 42035", "id": "42035", "lat": 29.2320, "lon": -94.4130},
    {"buoy_no": "4w",  "name": "NBDC 42055", "id": "42055", "lat": 22.1240, "lon": -93.9410},
    {"buoy_no": "5w",  "name": "NBDC 42002", "id": "42002", "lat": 26.0550, "lon": -93.6460},
    {"buoy_no": "6w",  "name": "NBDC 42001", "id": "42001", "lat": 25.9190, "lon": -89.6740},
    {"buoy_no": "7w",  "name": "NBDC 42007", "id": "42007", "lat": 30.0900, "lon": -88.7690},
    {"buoy_no": "8w",  "name": "NBDC 42040", "id": "42040", "lat": 29.2070, "lon": -88.2370},
    {"buoy_no": "9w",  "name": "NBDC 42039", "id": "42039", "lat": 28.7870, "lon": -86.0070},
    {"buoy_no": "10w", "name": "NBDC 42036", "id": "42036", "lat": 28.5010, "lon": -84.5080},
]


# %% [markdown]
# ## NOAA CO-OPS water-level downloader
#
# The CO-OPS API caps each request at 31 days; both storm windows are <31 days
# so a single call per station suffices. Datum: NAVD88 where available, fall
# back to MSL for stations that don't support NAVD88 in the requested window.

# %%
COOPS_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"


def fetch_coops_water_level(
    station_id: str,
    begin_date: str,
    end_date: str,
    datum: str = "NAVD",
) -> pd.DataFrame:
    """Fetch one CO-OPS water-level series. Returns empty DataFrame on missing data."""
    params = {
        "product": "water_level",
        "application": "coastal-rom-replication",
        "begin_date": begin_date,
        "end_date": end_date,
        "datum": datum,
        "station": station_id,
        "time_zone": "GMT",
        "units": "metric",
        "format": "json",
    }
    r = requests.get(COOPS_URL, params=params, timeout=120)
    r.raise_for_status()
    payload = r.json()
    if "data" not in payload:
        return pd.DataFrame(columns=["time", "wse_m", "sigma_m", "quality"])
    df = pd.DataFrame(payload["data"])
    df["time"] = pd.to_datetime(df["t"], utc=True)
    df["wse_m"] = pd.to_numeric(df["v"], errors="coerce")
    df["sigma_m"] = pd.to_numeric(df.get("s", pd.Series([], dtype="float")), errors="coerce")
    df["quality"] = df.get("q", pd.Series([], dtype="object"))
    return df[["time", "wse_m", "sigma_m", "quality"]]


def download_wse(stations: Iterable[dict], date_range: tuple, out_dir: Path) -> dict:
    """Fetch every station; cache as CSV; skip if file already present and non-empty."""
    begin, end = date_range
    log = {}
    for st in tqdm(list(stations), desc=f"WSE {out_dir.name}"):
        out = out_dir / f"{st['id']}.csv"
        if out.exists() and out.stat().st_size > 200:
            log[st["id"]] = {"status": "cached", "path": str(out)}
            continue
        df = pd.DataFrame()
        for datum in ("NAVD", "MSL"):
            try:
                df = fetch_coops_water_level(st["id"], begin, end, datum=datum)
            except requests.HTTPError:
                df = pd.DataFrame()
            if not df.empty:
                log[st["id"]] = {"status": "ok", "datum": datum, "n_obs": len(df)}
                break
        if df.empty:
            log[st["id"]] = {"status": "no_data"}
        df.to_csv(out, index=False)
    return log


# %% [markdown]
# ## NOAA NDBC wave-buoy downloader
#
# NDBC standard-meteorological files are at:
# `https://www.ndbc.noaa.gov/data/historical/stdmet/{ID}h{YYYY}.txt.gz`.
# Each file covers one calendar year. We need 2008 (Ike) and 2021 (Ida).

# %%
NDBC_URL_TMPL = "https://www.ndbc.noaa.gov/data/historical/stdmet/{id}h{year}.txt.gz"


def fetch_ndbc_stdmet(buoy_id: str, year: int) -> pd.DataFrame:
    """Fetch one buoy-year standard-met file. Returns empty DataFrame if absent."""
    url = NDBC_URL_TMPL.format(id=buoy_id, year=year)
    r = requests.get(url, timeout=120)
    if r.status_code != 200:
        return pd.DataFrame()
    with gzip.GzipFile(fileobj=io.BytesIO(r.content)) as gz:
        text = gz.read().decode("utf-8", errors="replace")
    lines = text.splitlines()
    # NDBC stdmet has two header lines: column names + units
    # then space-delimited numeric rows.
    header = lines[0].lstrip("#").split()
    data = [ln.split() for ln in lines[2:] if ln.strip()]
    df = pd.DataFrame(data, columns=header)
    # Combine YY MM DD hh mm into a single timestamp
    df["time"] = pd.to_datetime(
        df["YY"] + "-" + df["MM"] + "-" + df["DD"] + " " + df["hh"] + ":" + df["mm"],
        format="%Y-%m-%d %H:%M",
        utc=True,
        errors="coerce",
    )
    # Coerce wave fields to numeric; NDBC sentinel 99.0 / 999.0 -> NaN
    for col in ("WVHT", "DPD", "APD", "MWD", "WSPD", "WDIR"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df.loc[df[col] >= 99.0, col] = pd.NA
    return df


def download_waves(buoys: Iterable[dict], out_dir: Path) -> dict:
    """Fetch each buoy for both 2008 and 2021."""
    log = {}
    for st in tqdm(list(buoys), desc="waves"):
        for year in (2008, 2021):
            out = out_dir / f"{st['id']}_{year}.csv"
            if out.exists() and out.stat().st_size > 200:
                log[f"{st['id']}_{year}"] = {"status": "cached", "path": str(out)}
                continue
            df = fetch_ndbc_stdmet(st["id"], year)
            if df.empty:
                log[f"{st['id']}_{year}"] = {"status": "no_data"}
            else:
                log[f"{st['id']}_{year}"] = {"status": "ok", "n_obs": len(df)}
            df.to_csv(out, index=False)
    return log


# %% [markdown]
# ## Run downloads

# %%
print("Downloading WSE for Hurricane Ike (Sept 5-14, 2008)...")
log_ike = download_wse(WSE_IKE_STATIONS, IKE_DATE_RANGE, RAW_DIR / "wse_ike")

print("Downloading WSE for Hurricane Ida (Aug 26 - Sep 4, 2021)...")
log_ida = download_wse(WSE_IDA_STATIONS, IDA_DATE_RANGE, RAW_DIR / "wse_ida")

print("Downloading NDBC wave buoys for both 2008 and 2021...")
log_waves = download_waves(WAVE_BUOYS, RAW_DIR / "waves")

# %% [markdown]
# ## Persist source registry
#
# A JSON manifest of what was fetched, with timestamps, station counts and
# DOIs. Downstream notebooks audit this file.

# %%
manifest = {
    "paper_doi": "10.1016/j.ocemod.2024.102387",
    "designsafe_doi": "10.17603/DS2-7HBT-EF65",
    "designsafe_access": "auth-required; not fetched in this reproduction",
    "accessed_on": datetime.utcnow().date().isoformat(),
    "stations": {
        "wse_ike": WSE_IKE_STATIONS,
        "wse_ida": WSE_IDA_STATIONS,
        "waves": WAVE_BUOYS,
    },
    "date_ranges": {"ike": IKE_DATE_RANGE, "ida": IDA_DATE_RANGE},
    "download_log": {
        "wse_ike": log_ike,
        "wse_ida": log_ida,
        "waves": log_waves,
    },
    "sources": [
        {
            "name": "NOAA CO-OPS water-level gauges",
            "url": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter",
            "license": "U.S. Government Work (public domain)",
        },
        {
            "name": "NOAA NDBC standard-meteorological buoy data",
            "url": "https://www.ndbc.noaa.gov/data/historical/stdmet/",
            "license": "U.S. Government Work (public domain)",
        },
    ],
}
with open(RAW_DIR / "sources.json", "w") as f:
    json.dump(manifest, f, indent=2, default=str)
print(f"Wrote manifest to {RAW_DIR / 'sources.json'}")
print(f"WSE Ike stations OK: {sum(1 for v in log_ike.values() if v.get('status') in ('ok','cached'))}/{len(WSE_IKE_STATIONS)}")
print(f"WSE Ida stations OK: {sum(1 for v in log_ida.values() if v.get('status') in ('ok','cached'))}/{len(WSE_IDA_STATIONS)}")
print(f"Wave buoy-year files OK: {sum(1 for v in log_waves.values() if v.get('status') in ('ok','cached'))}/{2*len(WAVE_BUOYS)}")
