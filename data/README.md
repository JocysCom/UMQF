# UMQF Human-Rendering Benchmark (`/data`)

**What this is — and is not.** UMQF itself is grounded only in survival (`ΔOS`) and is **not** calibrated from human law, markets, or tradition. This folder is a separate **benchmark**: a record of how *one species — humans —* currently renders survival-value into law and money (sentencing, compensation, value-of-statistical-life, QALYs). Its only legitimate roles are to (1) **sanity-check** UMQF's first-principles outputs against what humans actually do, and (2) let UMQF **judge** human institutions (e.g. it scores blood-money gender/religion multipliers as immoral). These figures must **never** be imported as the formula's constants — doing so would inject one species' bias into a formula meant to apply to any entity in the universe. The math below (medians, GCU normalization, reconciliation) is how this *human benchmark* is summarized, not how UMQF is defined.

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
come from different instruments they are *not* mutually consistent as measured (the cycle differs
from 1.0 — see `value_axis.json` → `measured_arbitrage_cycle` and `arbitrage_attribution`).
`convert.py` reconciles them onto one log "value axis" by least-squares, so all
conversions become invertible and arbitrage-free **by construction**; the leftover residual is the
data inconsistency. `test_conversions.py` asserts these properties (T1 round-trip, T2 no-arbitrage,
T3 monotonic/sign, T4 curve-invertible, T5 anchor). `SAMPLING.md` + `sampling_adequacy.py` define
how many data points and which world sources are needed to shrink the residual and tighten each CI.

## Normalization (each value type → a universal unit)

Conversions never use raw quantities; each value type is first normalized to a universal,
entity-relative unit, then converted between the normalized units:

- **Money → GCU** (`gcu.py`): USD ÷ local lifetime resource throughput (GDP/capita × life
  expectancy). Income-invariant — by this human benchmark a statistical life is ≈1.4 GCU in the US
  or India alike, though ~30× apart in absolute USD. GCU is the **money hub**: `usd → GCU → life | welfare`.
- **Life → fraction of remaining lifespan** (`ΔOS`/`Tc`): death = −1 for every entity.
- **Welfare → quality-adjusted life-year** (κ≈1): a disability weight is a fraction of a healthy year.

`convert.py` reconciles the normalized rates onto one log value-axis (money node = GCU), so
round-trip and no-arbitrage hold by construction. **Construct-discipline**: a money figure is also
tagged `construct` (wtp / compensation / budget); only same-construct figures are pooled or
converted (WTP-vs-compensation differ ~100×, so they are reported separately, never averaged).

## Phasing

- **Phase 1 (now):** curated structured tariffs + a web-verified research-agent seed → first `ratios.json`. KB-scale, high signal.
- **Phase 2:** USSC individual-offender datafiles (~70k cases/yr) for robust harm-spacing and `In`.
- **Phase 3 (optional):** CourtListener bulk opinions (10M+) NLP-mined for pain-and-suffering awards.

## How UMQF relates to this benchmark

UMQF is defined from first principles (survival), **not** from `ratios.json`. The relationship runs the other way: UMQF scores an act in `ΔOS`/GCU, and this benchmark records how humans *happen* to render comparable acts into jail-time, money, or QALYs. **Convergence** between the two is reassurance that UMQF's survival-grounded outputs are sane; **divergence** is a finding — usually human bias UMQF should flag (e.g. blood-money identity multipliers), occasionally a gap in our own estimation to investigate. Nothing here sets a UMQF constant.

## Ideas under exploration (NOT in UMQF.md — unverified)

Working hypotheses from discussion, captured for analysis. They are **not** part of the formula and must be analysed, tested, and explicitly approved before any could enter `UMQF.md`. They are guidance to explore, not settled spec.

- **UMQF must apply to *any* entity in the universe** — microbe, fly, human, alien, immortal AI. Human law, culture, markets, and tradition are *distortions to measure against*, never the basis of the formula.
- **`ΔOS` (change in odds of survival) as the one universal currency** — the single thing all living entities share is the drive to stay alive, so survival is the only non-arbitrary common unit.
- **Life-value (hypothesis):** an entity's worth may scale with self-awareness (`VSA`) × remaining lifespan × its role in others' survival. *To analyse:* this conflicts with the current `Tc`-as-fraction (every death is `ΔOS = −1` regardless of absolute lifespan); reconciling cross-entity lifespan weighting with within-kind equal dignity is open.
- **Suffering as a modulator of survival-value (hypothesis):** higher suffering lowers how much an entity *seeks* its own survival; past a threshold survival becomes worthless, then negative — the entity seeks termination (a universal basis for consensual euthanasia). *To analyse:* differs from the current `Sc`, which only amplifies the harm of a negative `ΔOS`.
- **Punishment, universally (hypothesis):** the universal penalty is reduction of survival; everything else (liberty-time, money, suffering-time) is a *secondary* penalty that works by removing what a specific entity seeks. Compute the wrong in `ΔOS`/GCU, then render it in the entity's available medium — human jail-years, any currency, an alien's currency; for an immortal/suspendable AI: raised deletion risk, lost redundancy, capability/resource loss, enforced suspension, or agreed suffering-time.
- **Human law is one species' rendering** of survival-value into punishment — a benchmark to check and judge, never the formula's source.

Open tensions to resolve before anything is *proposed* for `UMQF.md`: absolute-lifespan vs `Tc`-fraction; suffering→negative-survival vs the `Sc` multiplier; how `VSA`, lifespan, and survival-role combine into one cross-entity life-value.

## Universal penalty framework (analysis — unverified, not in UMQF.md)

Goal: express moral conversions and penalties as **logical formulas in universal, objective, quantifiable units** that hold for any entity (human, alien, AI) — never fixed numbers or one species' currency. To validate against data and refine; not part of the formula.

**Universal units.** `ΔOS` (change in survival odds) is the master currency. The denominators that make everything comparable are the **entity's life-expectancy** (time) and **GCU** (resources = one lifetime's throughput). A penalty stated in these units renders into any entity's terms (human jail-years, alien currency, AI suspension) by plugging in that entity's lifespan/resources.

**Fair-penalty law.**

> `penalty = ( harm_restored + actor's_illicit_gain ) ÷ P(caught)`

computed in `ΔOS`, then rendered in the offender's units. The `÷ P(caught)` term makes the act non-profitable *in expectation*, so predation cannot pay for any rational entity. Fare-dodging is the clean case: `penalty = fare ÷ P(caught)` (caught every 5th ride ⇒ fare × 5) — no currency, fair on any planet. Murder ≈ 1 life-expectancy restored + additional damage + the gain-removal / `÷P` that strips the profit.

**Minimum penalty floor.**

> `penalty = max( floor , (harm + gain) ÷ P(caught) )`

Pure marginal-harm scoring leaves *cheap targets* undefended: by raw `ΔOS`, killing an entity at the very end of its life destroys little remaining survival, so it would carry a tiny penalty — an open season on the near-dead, the poor (small absolute loss), the low-`VSA`. A floor blocks that.
*First-principles grounding (so the floor is derived, not imposed):* the floor's value is itself measured in `ΔOS`, but at the level of the **society / web**, not the individual victim. A society that enforces a minimum behaves more fairly — even cheap targets (the near-dead, the poor, the low-`VSA`) stay protected — which raises trust and cooperation and therefore **increases the collective's survival odds**. Equivalently, cheaply violating "do not kill / steal" erodes the survival-security every entity relies on: killing the near-dead removes little of *their* survival but lowers *everyone's* security. The deficit the floor restores is real group-level `ΔOS`, and norms that raise group survival are evolutionarily selected — which is why such minimums recur across societies.
*Convergent evidence:* mandatory minimum sentences are near-universal across human legal traditions — consistent with a real attractor, to be tested in relative units, not copied as numbers.

**Descriptive vs prescriptive.** UMQF *measures* the moral weight of an act (`ΔOS`); the *penalty* that deters it adds the `÷P(caught)` and the floor on top. They can differ — and the gap (norm-erosion, detection probability) is itself real survival-cost, so a complete `ΔOS` accounting tends to reproduce the deterrent penalty from first principles.

**Why this is the superalignment endpoint.** When penalties make predation non-profitable for *every* entity (restoration + gain-removal ÷ detection + floor), cooperation/synergy is the only survival-stable strategy — UMQF's founding claim, mechanized.

**Open questions before proposing anything for `UMQF.md`:** how the floor is set in universal units (a minimum fraction-of-life? a minimum `ΔOS`?); whether to model norm-erosion as an explicit diffuse-`ΔOS` term or a flat floor; how `P(caught)` is estimated per act; how this reconciles with the existing `Sc`/`Vc`/`Tc`/Equivalent-Counter machinery.

## UMQF as a fair-penalty-book generator (analysis — unverified)

The end use and the validation test in one. Given (a) a list of crimes, (b) a civilization's survival parameters — life expectancy, resources per capita (→ GCU), intelligence (→ `VSA`) — and (c) the UMQF formulas, a script could generate that civilization's **fair penalty book**: the just sentence and fine for each crime, in its own units. Same formula every time; only the inputs change, so humans, aliens, and AI get justice from one computation.

**Rendering a UMQF score into a sentence (`÷ P`, not `× P`):**

> `jail-time ≈ |UMQF| × life-expectancy ÷ P(caught)`
> `fine ≈ |UMQF resource-harm| × (GCU → local currency) ÷ P(caught)`

bounded by a **floor** (collective-survival minimum, above) and a **cap at one life** — you cannot take more than the offender's whole remaining survival, which is why grave crimes converge on a life sentence rather than an arbitrarily larger number. The `÷ P(caught)` is the deterrence term from the fare-dodge logic (caught every 5th time ⇒ × 5 = ÷ (1/5)); lower detection ⇒ higher penalty. *Open:* the exact mapping from a UMQF score to a "fraction of a life" still needs pinning (UMQF carries `VSA` and the consent/suffering doublers).

**Falsifiability / how to validate.** Run the generator with Earth's parameters and it must regenerate human penalty books to the degree UMQF is correct. Strong correlation = strong evidence of accuracy; mismatches are either human bias (which UMQF then judges) or a flaw to fix. So **human secular law is the test set / answer key, never the source of the constants** — the numbers come from survival first principles; existing law is what an accurate UMQF should predict.

## Grounding the coefficients in survival (toward better numbers — unverified)

Replace intuition-set coefficient scales with survival-grounded definitions, so the numbers are universal and anchored.

- **`Sc` (suffering): define as the fraction of the entity's survival-drive / functional survival-capacity that the suffering destroys.** The top anchor is objective and species-independent: `Sc → 1` is where suffering makes survival *worthless* and the entity begins to seek its own termination. Levels then read as functioning / will-to-live lost: discomfort ≈ negligible, distress ≈ a fifth, agony ≈ half, torture ≈ most. Human disability-weight data measures exactly this (a year at weight `w` ≈ losing `w` healthy life-years) and puts moderate states ≈ 0.2–0.3, worst ≈ 0.7–0.9 — close to the intuited scale, now with a definition behind it.
  - *Structural fork (most consequential for accuracy):* `Sc` plays two roles that should be separated — (1) suffering *inflicted on a victim* amplifies a crime's harm (current use: torture-murder > clean murder); (2) an entity's *own* suffering lowers the value of *its* continued survival, which can go negative (the euthanasia case). Same scale, different application.
- **`In` (intent): ground in recurrence risk.** Intent matters because an intentional predator is a standing future survival-threat while an accident is not; the ~3–4× intentional-vs-negligent gap in sentencing is then a *prediction of repeat harm*, not a human preference.
- **`P(caught)`, floor, cap:** as in the penalty framework above (deterrence; collective-survival minimum; one-life ceiling).
