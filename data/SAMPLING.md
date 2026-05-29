# Sampling Plan — how many data points, from which world sources

Before an exchange rate enters UMQF it must (a) pass the consistency gates in
`scripts/test_conversions.py` (round-trip + no-arbitrage), and (b) be estimated from enough
independent world sources that its confidence interval is tight and stable. This file defines
the target sample sizes and the source matrix. `scripts/sampling_adequacy.py` reports the
achieved CI and the remaining gap per ratio, so collection is **variance-driven**, not arbitrary.

## Universality through diverse, independent sources

The formula seeks rates that are **universal** — survival-grounded invariants, not one culture's
quirks. So prefer **maximally independent** value systems: geographically, culturally, and
temporally distant, drawn from different legal traditions (common law, civil law, Islamic/Sharia,
Chinese-socialist, customary, and historical codes). Six Anglophone common-law jurisdictions are
*not* six independent samples — they share heritage and count as roughly one. `sampling_adequacy.py`
therefore reports **independent legal traditions** (`trd`) alongside jurisdiction count; target
≥3–4 distinct traditions per ratio.

**Convergence is the universality test.** When distant, independent systems agree on a ratio, that
is strong evidence it is a real invariant. When they diverge, either the ratio is culture-dependent
or the instruments measure different *constructs* — which must then be separated, not averaged.

- **Independent life↔money anchors:** Islamic **diyya** (blood money, ~1,400 years, many cultures)
  and historical **wergild** / Code of Hammurabi / Roman law give life and injury prices from systems
  with no shared lineage. Expect diyya (~$50–100k *compensation*) to diverge ~100× from Western
  **VSL** (~$13.7M *willingness-to-pay*): that gap is not noise but a construct difference
  (backward-looking compensation vs forward-looking WTP vs healthcare budget). Reconcile *within* a
  construct; treat cross-construct gaps as informative.
- **Effective independent N:** down-weight correlated jurisdictions (shared legal family / colonial
  origin). A ratio confirmed by common law **and** civil law **and** Islamic law **and** a historical
  code is far more "universal" than one confirmed by 20 EU states.
- **Non-human entities (aspiration):** universality ultimately spans life forms. The schema carries
  `entity_type` (human/ai/alien); only `human` data exists today, but AI-derived or hypothetically
  non-human valuations would slot in as further independent systems — agreement *across life forms*
  would be the ultimate universality proof.

## How target N is set (precision, not a guess)

Values span orders of magnitude, so we work in log space. For a geometric-mean estimate to fall
within a factor **F** at 95% confidence:

```
N  >=  ( 1.96 * sigma_log / ln F )^2
```

`sigma_log` is measured from the collected data per ratio. Example: with cross-jurisdiction
`sigma_log ≈ 0.5`, ±25% (F=1.25) needs **~20** points; ±10% (F=1.10) needs **~106**.
`sampling_adequacy.py` prints, per ratio: current `n`, `sigma_log`, achieved CI factor, and
`N@25%` / `N@10%` (so you see exactly how many more to collect).

**Tiers**
- **First pass (now):** ≥6 points spanning ≥2 legal traditions → order-of-magnitude anchor.
- **Working (target ±25%):** ~15–25 independent points, ≥3 legal traditions.
- **Publishable (target ±10%):** ~100 points for the load-bearing ratios (`L_to_M`, the
  `money_concavity` exponent, `In`).
- **Curve fits** (`money_concavity`): coverage matters more than count — ≥5 points per order of
  magnitude across the domain, from ≥3 jurisdictions.

## Stopping rule

Stop collecting a ratio when **both**: (1) achieved 95% CI ≤ target factor, and (2) adding a new
jurisdiction shifts the geometric mean by less than the target factor (convergence). Also stop
when the **no-arbitrage residual** (`value_axis.json` → `measured_arbitrage_cycle`) is within
tolerance of 1.0 — that means the independently-measured rates have become mutually consistent.

## World-source matrix

Stratify across legal traditions to average out cultural bias (which UMQF excludes by design);
normalize money to 2024 USD and, where incomes differ, against local VSL/income.

| Ratio | Instruments | Jurisdictions to sample (≥ target) |
|---|---|---|
| `L_to_M` | regulatory VSL; wrongful-death awards; life-insurance norms | US (EPA/DOT/HHS), UK, EU, Canada, Australia, Japan — VSL ≥6; + 10–20 wrongful-death awards |
| `W_to_M` | HTA cost-per-QALY thresholds; tort pain-and-suffering tariffs | NICE (UK), ICER (US), Canada CADTH, Australia PBAC, Netherlands, Sweden, WHO-CHOICE ≥6 |
| `W_to_L` | GBD/IHME disability weights; EQ-5D/TTO worse-than-death | GBD global + national EQ-5D value sets (UK, US, EU, Japan, Korea) ≥15 states |
| `In` | homicide sentencing by intent (murder vs manslaughter) | Common law: US (USSG), UK (E&W, Scotland), Canada, Australia, Ireland, NZ, India; Civil law: Germany, France — ≥8 jurisdictions |
| `money_concavity` | theft/fraud loss→penalty tables; day-fine unit schedules | US §2B1.1; UK theft/fraud bands; Germany/Finland/Sweden day-fines; Canada, Australia — ≥5 jurisdictions × full loss range |
| `liberty_time` | false-imprisonment & kidnapping guidelines (penalty vs duration) | US, UK, Canada, Australia, Germany, France — ≥6, **with explicit detention durations** |
| `severity_ladder` | cross-offence guideline grids (the relative ordering) | the major guideline systems: US (USSG), UK, Canada, Australia, + civil-law statutory ranges |

### Sentencing depth: guideline points vs microdata

- **Guideline starting points** (one per offence-category per jurisdiction) give the *intended*
  ladder cheaply — best for `severity_ladder` and `In`.
- **Microdata distributions** give the *realized* ladder and proper variance: the US Sentencing
  Commission individual-offender datafiles are ~70,000 cases/year (Phase 2); CourtListener bulk
  (10M+ opinions) is Phase 3. For these, sample the full distribution per offence, not just the
  mean, and record `sigma_log` from the realized spread.

## Caveats that bound accuracy (not just N)

- A sentence bundles harm + culpability + deterrence + retribution; isolate the **harm** axis via
  the guidelines' explicit harm/culpability split, and prefer **civil compensation** (make-whole)
  for the cleanest harm price.
- Instruments measure different things (workers-comp = wage replacement « tort « VSL = willingness
  -to-pay). Keep them separate; for `L_to_M`/`W_to_M` prefer VSL/QALY, treat workers-comp as a floor.
- Mandatory minimums, caps, and life sentences are censored data — fit with that in mind (a murder
  "minimum term" is not the full punishment, which biases `In` downward).
