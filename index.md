# coastal-rom-replication

> **Efficacy of reduced order source terms for a coupled wave-circulation model in the Gulf of Mexico** — replication study.
>
> Reference paper: [10.1016/j.ocemod.2024.102387](https://doi.org/10.1016/j.ocemod.2024.102387)

This repository is a self-contained replication of the headline claim from the reference paper above. It produces:

- A reproducible computational pipeline (Snakefile + notebooks).
- A FORRT-tagged nanopublication chain on the [Science Live platform](https://platform.sciencelive4all.org), documenting the claim, the replication design, and the outcome with full provenance.
- A Zenodo-archived release (source + container image) with a citable DOI.

## Quick start

```bash
git clone https://github.com/annefou/coastal-rom-replication.git
cd coastal-rom-replication
pixi install
pixi run snakemake --cores 1
```

Or with Docker:

```bash
docker run --rm ghcr.io/annefou/coastal-rom-replication:latest
```

## Structure

- `paper/` — the source paper PDF (drop yours in there).
- `notebooks/` — jupytext `.py` notebooks that drive the pipeline.
- `data/` — downloaded by `notebooks/01_data_download.py`, never committed.
- `nanopubs/` — drafts of the FORRT chain field-by-field, plus the published-URI registry.
- `docs/` — operating manuals (FORRT form fields, chain decision tree, claim-type vocabulary).
- `figures/` — curated figures used in the Jupyter Book.

## Published chain

The six-step FORRT chain for this replication is live on the Science Live platform. Outcome: **Validated** (moderate confidence). The full registry, including link semantics, is at [`nanopubs/PUBLISHED.md`](nanopubs/PUBLISHED.md).

- [01 — Quote-with-comment](https://w3id.org/sciencelive/np/RA_tuuJYawQ_zY1L6R0puEuiDVSo7JoHNfYQ9ULXPERZk)
- [02 — AIDA Sentence](https://w3id.org/sciencelive/np/RAPii6l2XAPcge7KM59fmPqxtMKVMjTA8AYY6hqUS4w1k)
- [03 — FORRT Claim](https://w3id.org/sciencelive/np/RAnDNlZ87EvWIfh3BqqBf3b5BtZYyJ7z8QYZv-bXhbAF0)
- [04 — FORRT Replication Study](https://w3id.org/sciencelive/np/RAKYb38hHcOMN5D-X1o_1RKSmDUojUUTxcT4pjL_Pe24s)
- [05 — FORRT Replication Outcome](https://w3id.org/sciencelive/np/RAG8PjhjvPQFZo54BTaV_b7TryMonH--aDGzEXLhzvQ4w)
- [06 — CiTO Citation](https://w3id.org/sciencelive/np/RAuvGPQk_nxEcBWzADcLnyfqgjJ9Hr2aSWxwof2sDAung)

Embedded below is the Replication Outcome (step 05), which carries the verdict, the supporting numerical evidence, and the limitations. From it you can walk back through the chain to the Quote and forward to the CiTO Citation.

<iframe src="https://platform.sciencelive4all.org/np/?uri=https://w3id.org/sciencelive/np/RAG8PjhjvPQFZo54BTaV_b7TryMonH--aDGzEXLhzvQ4w" width="100%" height="900"></iframe>

## Citation

If you use this work, please cite both:

- This software: [`CITATION.cff`](CITATION.cff) → DOI [10.5281/zenodo.20348366](https://doi.org/10.5281/zenodo.20348366).
- The original paper: [10.1016/j.ocemod.2024.102387](https://doi.org/10.1016/j.ocemod.2024.102387).
