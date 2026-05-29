# UMQF Legal/Economic Calibration — Report

Source of truth: `data/observations/*.jsonl` — **327 observations** across **27 sources** (confidence: 238 high / 64 medium / 25 low). Currency: USD_2024.

> First-pass estimates from a curated seed + research-agent corpus. Treat as Phase-1 anchors, not final constants.

## Observations by source

- **day_fines**: 10
- **diyya_blood_money**: 21
- **historical_codes**: 17
- **homicide_diverse**: 19
- **homicide_intent**: 17
- **in_civillaw**: 15
- **in_commonlaw**: 16
- **liberty_dur**: 12
- **liberty_duration**: 11
- **liberty_durations_2**: 13
- **money_concavity_intl**: 16
- **money_loss_curve**: 17
- **qaly**: 3
- **qaly_intl**: 8
- **qaly_weights**: 21
- **qaly_wtp**: 3
- **tort_pain_suffering**: 18
- **uk_violence**: 2
- **vsl**: 2
- **vsl_diverse**: 11
- **vsl_income_paired**: 17
- **vsl_intl**: 8
- **vsl_wrongful_death**: 7
- **workers_comp**: 3
- **wtol_more**: 15
- **wtol_national**: 15
- **wtp_qaly_more**: 10

## Conversion ratios

### L_to_M — GCU value of one life (anchors dOS=-1); income-normalized; split by construct
- estimate: **1.447** GCU per life
- n=58  confidence=high
- Income-normalized (money/GCU): VSL is ~constant in GCU though ~30x in USD. WTP anchors dOS=-1; compensation is a separate, lower construct (not averaged in). diyya identity multipliers are cultural, excluded by UMQF.

### W_to_L — life-years lost per year at given suffering (disability weight)
- estimate: **0.5545** life-yr per suffering-yr
- range: [0.003, 0.923]
- n=52  confidence=medium
- GBD-style disability weights. Supports kappa near 1 (one shared scale): worst sustained states ~0.5-0.7, not 60x.

### W_to_M — GCU value of one welfare-year (QALY), income-normalized, by construct
- estimate: **0.01122** GCU per welfare-yr
- n=21  confidence=medium
- budget=cost-effectiveness threshold; wtp=empirical willingness-to-pay per QALY. They are close (~0.01-0.02 GCU), so the cross-rate residual is the VSL-vs-QALY value-per-life-year gap, not a W_to_M construct artifact.

### suffering_severity_to_money — lump-sum money per unit suffering severity (permanent-state pain-and-suffering awards)
- form: **linear**  params={'a': 567658.462, 'b': -69791.467}  R2=0.6867
- n=18  confidence=medium
- Tort PSLA awards; exponent/curvature shows how suffering price scales with severity (lump-sum, not per-year).

### In — intent multiplier (jail vs intentional, harm=death), averaged within-jurisdiction
- estimate: **{'reckless': 0.357, 'negligent': 0.24}** x of intentional
- n=54  confidence=medium
- Per-jurisdiction ratio then averaged, so absolute sentence-scale differences cancel. Murder=life minimum-terms bias this downward.

### money_concavity — how punishment scales with money loss (within one coherent schedule)
- form: **power**  params={'a': 0.030713, 'b': 0.322712}  R2=0.944
- n=12  confidence=medium
- Fit within one coherent loss->penalty schedule (US USSG 2B1.1 is the cleanest, continuous one); national schemes differ structurally (caps, categorical bands) so a pooled fit is invalid. power b<1 => diminishing/concave; 2 of 3 fitted schedules are concave.

### severity_ladder — relative harm ordering by custodial sentence
  - kidnapping and rape: 431.0 yr (norm 1.0)
  - USA (Ohio) — State v. William Mozingo Jr., Summit County (Akron): 31.5 yr (norm 0.073)
  - Moord (Art. 289 WvSr) – life or up to 30 years: 30.0 yr (norm 0.07)
  - Meurtre (Art. 221-1) – 30 years réclusion criminelle: 30.0 yr (norm 0.07)
  - Murder, 30-year minimum-term starting point: 30.0 yr (norm 0.07)
  - Satsujin (Art. 199) – death, life, or ≥ 5 years: 30.0 yr (norm 0.07)
  - Murder, actual sentences imposed (NSW Sentencing Council Homicide report): 25.6 yr (norm 0.059)
  - Murder, 25-year minimum-term starting point (weapon taken to scene): 25.0 yr (norm 0.058)
- n=117  confidence=medium
- Layer-A relative ladder; multiply by an absolute anchor (VSL) to make it cardinal.

### liberty_time — custodial years imposed per year of liberty taken
- estimate: **273.75** jail-yr per liberty-yr
- range: [0.65, 13140.0]
- n=17  confidence=low
- Median custody-to-deprivation ratio (retributive multiplier > 1 expected). Durations parsed best-effort.

## Triangulation consistency check

- check: W_to_L =? W_to_M / value_of_a_life_year
- value_of_a_life_year_usd: 0.0
- implied_W_to_L_from_money: 0.31
- measured_W_to_L: 0.554
- verdict: consistent (same order of magnitude)

## Status

- estimated: L_to_M, W_to_L, W_to_M, suffering_severity_to_money, In, money_concavity, severity_ladder, liberty_time
- pending (need more data): none
