# Snakefile - orchestrates the Loveland et al. 2024 stat-level reproduction.
#
# Each rule wraps one of the four jupytext-paired notebooks. The .py files are
# the source of truth; jupytext converts each to .ipynb at execution time and
# the .ipynb form is what runs.
#
# Usage:
#   pixi run snakemake --cores 1                  # run everything
#   pixi run snakemake --cores 1 -n               # dry run

NOTEBOOKS = "notebooks"
DATA = "data"
RESULTS = "results"
FIGURES = "figures"


rule all:
    input:
        f"{FIGURES}/gauge_map.png",
        f"{FIGURES}/wse_timeseries_example.png",
        f"{FIGURES}/main_result.png",


# ---------- 01: Data download ----------
# Self-contained: fetches NOAA CO-OPS water-level and NDBC wave-buoy series for
# both Hurricane Ike (2008) and Hurricane Ida (2021). No credentials needed.
rule data_download:
    output:
        f"{DATA}/raw/sources.json",
    shell:
        "cd {NOTEBOOKS} && jupytext --to notebook --execute 01_data_download.py"


# ---------- 02: Data clean ----------
rule data_clean:
    input:
        f"{DATA}/raw/sources.json",
    output:
        f"{DATA}/processed/ike/wse.nc",
        f"{DATA}/processed/ida/wse.nc",
        f"{DATA}/processed/ike/waves.nc",
        f"{DATA}/processed/ida/waves.nc",
        f"{DATA}/processed/qc_summary.csv",
    shell:
        "cd {NOTEBOOKS} && jupytext --to notebook --execute 02_data_clean.py"


# ---------- 03: Analysis ----------
# Transcribes the paper's Tables 4-7 and computes obs-side peak statistics.
# Writes the headline_comparison table that the figures notebook plots.
rule analysis:
    input:
        f"{DATA}/processed/ike/wse.nc",
        f"{DATA}/processed/ida/wse.nc",
        f"{DATA}/processed/ike/waves.nc",
        f"{DATA}/processed/ida/waves.nc",
    output:
        f"{DATA}/published_baselines/table4_runtimes.csv",
        f"{DATA}/published_baselines/wse_summary.csv",
        f"{DATA}/published_baselines/wave_summary.csv",
        f"{RESULTS}/obs_wse_peaks.csv",
        f"{RESULTS}/obs_wave_peaks.csv",
        f"{RESULTS}/headline_comparison.csv",
        f"{RESULTS}/tradeoffs.csv",
    shell:
        "cd {NOTEBOOKS} && jupytext --to notebook --execute 03_analysis.py"


# ---------- 04: Figures ----------
rule figures:
    input:
        f"{RESULTS}/headline_comparison.csv",
        f"{DATA}/processed/ike/wse.nc",
        f"{DATA}/processed/ida/wse.nc",
    output:
        f"{FIGURES}/gauge_map.png",
        f"{FIGURES}/wse_timeseries_example.png",
        f"{FIGURES}/main_result.png",
    shell:
        "cd {NOTEBOOKS} && jupytext --to notebook --execute 04_figures.py"
