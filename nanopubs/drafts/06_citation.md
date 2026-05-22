# 06 — CiTO Citation

> Pre-flight checklist (`docs/forrt-form-fields.md` § Pre-flight checklist) — RUN. Section "Citation with CiTO" is documented. Field list pasted verbatim below for alignment.

**Description:** *"Declare citations between papers or other works, using Citation Typing Ontology"*

## Documented field list (verbatim from `docs/forrt-form-fields.md` § Citation with CiTO)

| Field label | Field type | Notes |
|---|---|---|
| Identifier for the citing creative work | text input, **required** | URL or DOI of the citing work — for FORRT chains this is the Outcome's nanopub URI. |
| List citations | repeatable group, **required** ≥1 | One or more citation entries, each with type + URL. |
| ↳ Citation Type | dropdown | CiTO intention from the controlled list. Available: `confirms`, `qualifies`, `disputes`, `extends`, `usesMethodIn`, `citesAsAuthority`, `obtainsBackgroundFrom`, `discusses`, `citesAsDataSource`, `containsAssertionFrom`, `includesQuotationFrom`, `reviews`, `critiques`, `credits`. **NOT available**: `replicates`. |
| ↳ DOI or other URL of the cited work | text input | DOI URL form `https://doi.org/10.x/y` or other URL. |

Mapping rule applied here: Outcome's Validation status is **Validated** → CiTO intention **`confirms`**.

## Field-by-field draft

### Identifier for the citing creative work (text input, required)

URI of the Outcome published in step 05. Pull from `nanopubs/PUBLISHED.md` after publishing step 05, then paste here before publishing this Citation nanopub.

```
_(step 05 Outcome URI — paste here after publication; format https://w3id.org/sciencelive/np/RA…)_
```

### List citations (repeatable group, required ≥1)

#### Citation 1 — back to the original paper

##### Citation Type (dropdown)

Outcome Validation status = **Validated** → use **`confirms`**.

```
confirms
```

##### DOI or other URL of the cited work (text input)

Loveland, Meixner, Valseth, Dawson (2024), "Efficacy of reduced order source terms for a coupled wave-circulation model in the Gulf of Mexico", *Ocean Modelling* 190: 102387.

```
https://doi.org/10.1016/j.ocemod.2024.102387
```

#### Additional citations (optional)

*(skip — optional)*

Single-citation Outcome-confirms-paper is the canonical Phase 5 closing shape. The FORRT chain itself is captured through provenance links between Outcome → Study → Claim → AIDA → Quote, not through additional CiTO citations here.

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 06. This completes the six-step FORRT chain.

Optional next layers:

- **Research Software** (`drafts/07_research_software.md`) — only if the repo *produces* a reusable software artefact (per `CLAUDE.md` § Layered architecture). A reproduction repo is normally not in scope.
- **Research Synthesis** (`drafts/08_synthesis.md`) — only if this chain is one of several testing facets of a shared property.
