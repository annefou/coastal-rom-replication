# 03 — FORRT Claim

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"FORRT Claim — Declare an original claim according to FORRT, linking it to an AIDA sentence with a specific FORRT type."*

## Documented field list (verbatim from `docs/forrt-form-fields.md` § FORRT Claim)

| Field label | Field type | Notes |
|---|---|---|
| Short URI suffix as claim ID | text input, **required** | Placeholder: "e.g. my-claim-01". Slug becomes part of nanopub URI. Use kebab-case. |
| Label of the claim (to find it later) | text input, **required** | Used for searches/discovery. A descriptive title, not a sentence. |
| Search for an AIDA sentence | search/select dropdown, **required** | Search by AIDA text → pick the published AIDA URI. **Caveat**: not yet confirmed whether this search finds AIDAs published via Nanodash (`w3id.org/np/...` namespace) versus only Science Live (`w3id.org/sciencelive/np/...`). If your AIDA was published via Nanodash, paste the URI manually rather than relying on search. |
| Type of FORRT claim | dropdown, **required** | Single-select from 7 options. See `docs/claim-type-vocabulary.md`. |
| Source URI (optional) | text input, **optional** | Placeholder: `https://doi.org/...` — **expects full URL form** (`https://doi.org/10.x/y`), unlike the Quote-with-comment "Cited DOI" field which expects bare `10.x/y`. |

There are no other substantive fields below "Source URI" — only a "publish as example" toggle.

## Field-by-field draft

### Short URI suffix as claim ID (text input, required)

Slug becomes part of the nanopub URI. Use kebab-case.

```
loveland-2024-rom-tradeoff-claim
```

### Label of the claim (text input, required)

A descriptive title (not a sentence). Used for searches/discovery.

```
Coastal-ROM trade-off in coupled ADCIRC+SWAN hindcasts (Loveland et al. 2024)
```

### Search for an AIDA sentence (search/select, required)

URI of the AIDA published in step 02. Pull from `nanopubs/PUBLISHED.md`.

> _If the AIDA was published via Nanodash (`w3id.org/np/...` namespace), the platform's search may not find it — paste the URI manually._

```
_(step 02 AIDA URI — paste here after publication; format https://w3id.org/sciencelive/np/RA… or https://w3id.org/np/RA… if published via Nanodash)_
```

### Type of FORRT claim (dropdown, required)

Pick one. See `docs/claim-type-vocabulary.md` for the seven options and how to choose.

- [x] **computational performance**
- [ ] scalability
- [ ] data quality
- [ ] data governance
- [ ] descriptive pattern
- [ ] model performance
- [ ] statistical significance

**Why `computational performance`:** Loveland et al. (2024) is foregrounded by its title — *"Efficacy of reduced order source terms for a coupled wave-circulation model in the Gulf of Mexico"*. The headline claim, as re-anchored in `00_paper_summary.md` to the §6 Conclusions sentence, asserts a **runtime-vs-fidelity trade-off**: that reduced-order (Gen1/Gen2) SWAN source-term packages save computational cost relative to the third-generation (ST6/Gen3) package without measurably degrading water-surface-elevation accuracy in coupled ADCIRC+SWAN hindcasts of Gulf-of-Mexico hurricanes. The runtime axis (the ~40 % wall-clock penalty for Gen3 over Gen1/Gen2, Table 4) is what makes this a *trade-off* claim rather than a pure-accuracy claim, and the runtime axis is what disqualifies the alternative classifications:

- Not `model performance`: the claim is not "Gen3 has accuracy X on a held-out set"; it is "Gen3's marginal accuracy gain on WSE does not justify its marginal compute cost".
- Not `scalability`: the claim is not about behaviour as mesh size or core count grows; runs are at fixed compute (1064 cores) and fixed meshes.
- Not `descriptive pattern`: there is no observed empirical relationship between variables in the world being asserted — the trade-off is between *implementation choices*, not between natural phenomena.
- Not `statistical significance`: no significance test is the claim.
- Not `data quality` / `data governance`: nothing about preserving fidelity through preprocessing or FAIR conformance.

### Source URI (text input, optional)

Full URL form: `https://doi.org/...` (NOT bare DOI).

```
https://doi.org/10.1016/j.ocemod.2024.102387
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 03.
