# UMQF Calibration Data (`/data`)

**Goal:** estimate UMQF's conversion ratios and the *functional form* of each, empirically, from how the real world already prices harm — legal sentencing, compensation tariffs, and economic value-of-life/health figures. Calibrate for humans; a few constant tweaks then generalize to any entity.

This is the spec + the working pipeline. Everything here is **plain text** (JSON Lines / JSON / Markdown / Python) — open and readable to humans and AI, RAG-indexable, git-diffable. **No hidden binary database.**

## Design principles (governing)

1. **One formula, many resolutions ("zoom").** Model the largest correlation first as a simple top-level formula; every variable is a "particle" expandable into sub-variables that aggregate by a fixed operator — **sum** for independent parts, **duration-weighted average** for levels that vary over time, **product** for gates. Estimate fast at large scale, refine by going deeper. (Also written into the README `### UMQ Improvement Prompt`.)
2. **Prefer known natural laws.** Before inventing a curve, check `../universal_formulas.md`. Default every conversion to a **power law `y = a·xᵇ`** (nests linear at `b=1`); upgrade to **logistic** only for bounded survival-odds, **exponential** only for time-decay. Let the data pick the exponent.
3. **Two-layer calibration.** *Layer A* — sentencing gives the **relative harm ladder** (spacing/ordering) and the intent multiplier, in punishment units. *Layer B* — VSL / QALY / tort give **absolute anchors** that make one point of the ladder cardinal. One anchor turns millions of ordinal sentences into real units.
4. **Triangulate.** `W↔L` should ≈ `W↔M ÷ L↔M`; disagreement flags which instrument is biased.

## The currencies and the ratios

| Symbol | Currency | Unit | Anchor |
|---|---|---|---|
| **L** | Life / survival | life-years (death = −1 ΔOS) | VSL |
| **M** | Resources / money | normalized → 1 GCU | VSL / income |
| **W** | Welfare (suffering↔pleasure × time) | welfare-years (QALY-like) | QALY threshold |
| **J** | Liberty (jail time) | years incarcerated | *sentencing's own unit* |

Target ratios (and the "clean" offence that isolates each):

| Ratio | Meaning | Best source | Clean isolator |
|---|---|---|---|
| `L_to_M` | money per life | VSL, wrongful-death | regulatory VSL |
| `W_to_M` | money per welfare-year | tort pain-and-suffering, QALY $ | non-fatal injury awards |
| `W_to_L` | life-years per welfare-year | GBD disability weights, TTO | chronic health states |
| `In` | intent multiplier | sentencing tiers | murder vs manslaughter |
| `money_concavity` | how punishment scales with $ loss | theft/fraud loss tables | larceny by amount |
| `liberty_time` | custody per duration of liberty taken | kidnap/false imprisonment | false imprisonment |
| `severity_ladder` | relative harm ordering | sentencing guidelines | cross-offence grids |

## Storage layout

```text
/data/
  raw/                      # inputs, unmodified
    seed.jsonl              # curated, hand-verified anchors (source of truth seed)
    collected.json          # research-agent output (web-verified, cited)
    sources_manifest.json   # written by download.py
  observations/             # SOURCE OF TRUTH — readable, RAG-indexable
    vsl.jsonl  qaly.jsonl  uk_violence.jsonl  workers_comp.jsonl  ...
  ratios.json               # OUTPUT: conversion ratios + form + params + R²
  report.md                 # OUTPUT: human-readable calibration summary
  exports/                  # optional CSV mirrors
  scripts/
    config.json             # source registry, currency/year, conversion-form defaults
    schema.json             # the observation schema (JSON Schema)
    download.py             # register/refresh sources
    extract.py              # seed + collected -> observations/*.jsonl (idempotent, dedups by id)
    categorize_ai.py        # normalize/(re)categorize harm_type, intent, magnitude
    compute_ratios.py       # observations -> ratios.json (fits linear/power/log, selects by R²)
    report.py               # ratios.json -> report.md
```

### The one record type: an *observation*

Each line of `observations/*.jsonl` is one priced harm (a guideline cell, a tariff entry, an award, or an anchor figure). Schema: `scripts/schema.json`. Each row carries a natural-language `summary` (for RAG), the harm dimensions (`harm_type`, `harm_magnitude`, `harm_duration`, `intent`), the priced cost (`penalty_jail_years`, `penalty_fine_usd2024`, `compensation_usd2024`, `money_value_usd2024`), an optional nested `harm.components[]` (zoom-in), `informs_ratio`, `source_citation`, and `confidence`.

Query it in place with SQL (optional): `pip install duckdb` then
`duckdb -c "SELECT harm_type, avg(penalty_jail_years) FROM read_json_auto('data/observations/*.jsonl') GROUP BY 1"`.

## Pipeline

```bash
python data/scripts/download.py          # register sources
python data/scripts/extract.py           # seed + collected -> observations/*.jsonl
python data/scripts/categorize_ai.py     # normalize categories
python data/scripts/compute_ratios.py    # -> ratios.json
python data/scripts/report.py            # -> report.md
python data/scripts/convert.py           # reconcile rates onto one value axis -> value_axis.json
python data/scripts/test_conversions.py  # consistency gates (round-trip + no-arbitrage); exit 0 = pass
python data/scripts/sampling_adequacy.py # how many points/jurisdictions still needed -> sampling_status.json
```

Requires `numpy pandas` (and `scipy` for richer fits). Re-runnable; idempotent.

## Accuracy gates (must pass before a rate enters UMQF)

A rate is only usable once it is **invertible** and **arbitrage-free**: converting A→B→A returns A,
and no conversion cycle (life→money→welfare→life) multiplies to anything but 1. Because the rates
come from different instruments they are *not* mutually consistent as measured (currently the cycle
is ~2.1× off). `convert.py` reconciles them onto one log "value axis" by least-squares, so all
conversions become invertible and arbitrage-free **by construction**; the leftover residual is the
data inconsistency. `test_conversions.py` asserts these properties (T1 round-trip, T2 no-arbitrage,
T3 monotonic/sign, T4 curve-invertible, T5 anchor). `SAMPLING.md` + `sampling_adequacy.py` define
how many data points and which world sources are needed to shrink the residual and tighten each CI.

## Phasing

- **Phase 1 (now):** curated structured tariffs + a web-verified research-agent seed → first `ratios.json`. KB-scale, high signal.
- **Phase 2:** USSC individual-offender datafiles (~70k cases/yr) for robust harm-spacing and `In`.
- **Phase 3 (optional):** CourtListener bulk opinions (10M+) NLP-mined for pain-and-suffering awards.

## How it feeds UMQF

`ratios.json` proposes empirical values + forms for: the GCU↔ΔOS anchor (BLRR), the ΔOS severity ladder, the welfare scale κ, the `In` multiplier, the money-loss curve, and — via the **torture-murder premium** — whether suffering is priced *beyond* death (informs the welfare floor: clamp at −1 vs allow below). Each calibration pass re-checks the UMQF worked examples.
