# 01 — Quote-with-comment (paper-rooted chains)

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> If this is a question-rooted chain, use `01_pico.md` or `01_pcc.md` instead — see `docs/chain-decision-tree.md`.
>
> **After choosing the chain shape, delete the two step-1 alternates you aren't using.** Once you've decided this chain is paper-rooted and keep `01_quote.md`, run:
> ```bash
> rm nanopubs/drafts/01_pico.md nanopubs/drafts/01_pcc.md
> ```

**Form heading:** *"Annotate a paper quotation — Annotating a paper quotation with personal interpretation"*

## Field-by-field draft

### Cited DOI (text input)

Format: starts with `10.` — bare DOI, **NOT** `https://doi.org/...` form.

```
10.1016/j.ocemod.2024.102387
```

### Quote mode (radio button)

- [x] **Quote whole text (less than 500 characters)**
- [ ] Quote start/end *(use this if the quote exceeds 500 chars)*

### Quoted Text (textarea, required)

Verbatim from the paper PDF in `paper/`, §6 Conclusions (p. 12). Character-for-character. ≤ 500 chars in whole-text mode.

> _Read the PDF first. Don't paraphrase from memory. See `docs/verify-before-drafting.md`._
>
> **Re-anchor note (Phase 1 second pass):** This Quote was originally drawn from the abstract; that sentence was unconditional ("relatively low amounts of additional error with respect to observations"), whereas §6 Conclusions explicitly conditions the trade-off on (a) WSE-only-interest scope and (b) wind-field-accuracy assumption. Anchoring on the conclusion preserves Loveland's own conditioning so the downstream Validated verdict is internally consistent with the Quote. See `00_paper_summary.md` § Headline claim for the full rationale.

```
For instance, it may be worth the savings in computation if only water surface elevations are of primary interest as opposed to wave statistics. However, large sensitivities to the source term choice in global output of significant wave height near hurricane tracks were observed.
```

Character count: 280 / 500.

### Comment (textarea, required)

Subtitle: *"Our interpretation or explanation of why this quotation is relevant."*

Why this quote matters and what the replication tests. Connect the paper's claim to the work this repo does. Don't repeat the quote.

```

```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 01.
