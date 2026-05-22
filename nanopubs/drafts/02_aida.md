# 02 — AIDA Sentence

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"AIDA Sentence — Make structured scientific claims following the AIDA model"*

## Documented field list (verbatim from `docs/forrt-form-fields.md` § AIDA sentence)

| Field label | Field type | Notes |
|---|---|---|
| Enter your AIDA sentence here (ending with a full stop) | textarea, **required** | The atomic, independent, declarative, absolute sentence. Must end with a full stop. |
| Select related topics/tags | dropdown, **optional** | Predefined topic vocabulary — open the dropdown and pick available labels. |
| Relates to this nanopublication | text input, **required** | URI of the nanopub the AIDA derives from. For paper-rooted chains this is the Quote-with-comment URI. |
| Supported by datasets | repeatable group ("+ Add Item"), **optional** | DOI/URL of datasets that ground the AIDA claim. |
| Supported by other publications | repeatable group ("+ Add Item"), **optional** | DOI/URL of publications that support the AIDA claim. |

## Pre-write checklist (CLAUDE.md § AIDA pre-write checklist)

| Check | Status |
|---|---|
| No numerical values | pass — no coefficients, intervals, percentages, or thresholds |
| No method names | pass — "ADCIRC", "SWAN", "ST6", "first-/second-/third-generation source-term package" are the paper's own domain vocabulary, not internal codebase identifiers; "root-mean-square error" is a discipline-level metric |
| No cryptic identifiers | pass — no variable names, no internal slugs |
| World-talk, not model-talk | pass — frames the finding as a property of the coupled modelling configuration in hurricane hindcasts, not as "the model finds" or "the test rejects" |
| One empirical finding | pass — the trade-off itself is the atomic empirical unit (no WSE accuracy gain *coupled with* higher cost). The wave-stats sensitivity caveat is deliberately excluded; it would be a separate AIDA on a separate Claim. |
| Ends with a full stop | pass |

## Field-by-field draft

### AIDA sentence (textarea, required)

Atomic, Independent, Declarative, Absolute. One empirical finding. Must end with a full stop.

```
In coupled ADCIRC+SWAN hindcasts of Gulf of Mexico hurricanes, the third-generation ST6 source-term package in SWAN yields no improvement in water-surface-elevation root-mean-square error at NOAA gauges over the first- or second-generation source-term packages, while increasing wall-clock run time.
```

Character count: 299. One sentence, declarative ("yields no improvement … while increasing"), absolute (no "may"/"could"/"tends to"). The wave-stats sensitivity in the Quote's second sentence is deliberately not linked here — it would be a second AIDA on a separate Claim, per the Atomic AIDA rule.

### Select related topics/tags (dropdown, optional)

Predefined topic vocabulary — open the dropdown on the platform and pick from these candidates (don't paste them as free text):

- storm surge
- hurricane
- coastal ocean modelling
- spectral wave model
- computational cost
- reproducibility

Pick the 2-4 that are actually offered in the dropdown. If none of these labels exist in the platform vocabulary, leave this field empty rather than inventing a label.

### Relates to this nanopublication (text input, required)

URI of the Quote-with-comment from step 01.

```
_(step 01 Quote URI — paste here after publication; format https://w3id.org/sciencelive/np/RA…)_
```

Pull the URI from `nanopubs/PUBLISHED.md` once step 01 has been published on `platform.sciencelive4all.org`.

### Supported by datasets (repeatable group, optional)

*(skip — optional)*

The empirical grounding (NOAA gauge water-surface elevations, NOAA NDBC buoy wave statistics, Frontera wall-clock run-times) is recorded against the FORRT Replication Study and Outcome downstream, not on the AIDA. Adding dataset DOIs here is also not advisable until the known platform bug (publishing fails when both *Supported by datasets* AND *Supported by other publications* are populated — `docs/forrt-form-fields.md`) is resolved.

### Supported by other publications (repeatable group, optional)

*(skip — optional)*

The source paper (Loveland, Meixner, Valseth, Dawson 2024, DOI `10.1016/j.ocemod.2024.102387`) is already cited via the step-01 Quote-with-comment, so re-citing it here would duplicate the link. Methods-paper citations (Rogers et al. 2012 for ST6; Holthuijsen et al. 1988 for Gen1) belong on the Replication Study's Methodology field, not on the AIDA.

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 02.
