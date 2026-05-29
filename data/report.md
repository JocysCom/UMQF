# UMQF Legal/Economic Calibration — Report

Source of truth: `data/observations/*.jsonl` — **253 observations** across **21 sources** (confidence: 201 high / 37 medium / 15 low). Currency: USD_2024.

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
- **money_loss_curve**: 17
- **qaly**: 3
- **qaly_intl**: 8
- **qaly_weights**: 21
- **tort_pain_suffering**: 18
- **uk_violence**: 2
- **vsl**: 2
- **vsl_diverse**: 11
- **vsl_intl**: 8
- **vsl_wrongful_death**: 7
- **workers_comp**: 3
- **wtol_national**: 15

## Conversion ratios

### L_to_M — GCU value of one life (anchors dOS=-1); income-normalized; split by construct
- estimate: **1.683** GCU per life
- n=42  confidence=high
- Income-normalized (money/GCU): VSL is ~constant in GCU though ~30x in USD. WTP anchors dOS=-1; compensation is a separate, lower construct (not averaged in). diyya identity multipliers are cultural, excluded by UMQF.

### W_to_L — life-years lost per year at given suffering (disability weight)
- estimate: **0.402** life-yr per suffering-yr
- range: [0.03, 0.732]
- n=22  confidence=medium
- GBD-style disability weights. Supports kappa near 1 (one shared scale): worst sustained states ~0.5-0.7, not 60x.

### W_to_M — GCU value of one welfare-year (QALY threshold), income-normalized
- estimate: **0.01196** GCU per welfare-yr
- range: [0.006, 0.04368]
- n=8  confidence=medium
- Cost-effectiveness thresholds per QALY, normalized to GCU.

### suffering_severity_to_money — lump-sum money per unit suffering severity (permanent-state pain-and-suffering awards)
- form: **linear**  params={'a': 567658.462, 'b': -69791.467}  R2=0.6867
- n=18  confidence=medium
- Tort PSLA awards; exponent/curvature shows how suffering price scales with severity (lump-sum, not per-year).

### In — intent multiplier (jail vs intentional, harm=death), averaged within-jurisdiction
- estimate: **{'reckless': 0.357, 'negligent': 0.24}** x of intentional
- n=54  confidence=medium
- Per-jurisdiction ratio then averaged, so absolute sentence-scale differences cancel. Murder=life minimum-terms bias this downward.

### money_concavity — how punishment scales with money loss
- form: **power**  params={'a': 0.06603, 'b': 0.283861}  R2=0.9041
- n=17  confidence=medium
- power exponent b<1 => diminishing (concave); b~1 => linear.

### severity_ladder — relative harm ordering by custodial sentence
  - USA (Ohio) — State v. William Mozingo Jr., Summit County (Akron): 31.5 yr (norm 1.0)
  - Murder, 30-year minimum-term starting point: 30.0 yr (norm 0.952)
  - Satsujin (Art. 199) – death, life, or ≥ 5 years: 30.0 yr (norm 0.952)
  - Moord (Art. 289 WvSr) – life or up to 30 years: 30.0 yr (norm 0.952)
  - Meurtre (Art. 221-1) – 30 years réclusion criminelle: 30.0 yr (norm 0.952)
  - Murder, actual sentences imposed (NSW Sentencing Council Homicide report): 25.6 yr (norm 0.813)
  - Doodslag (Art. 287 WvSr) – up to 25 years: 25.0 yr (norm 0.794)
  - First-degree murder (Criminal Code s. 235 / s. 745(a)): 25.0 yr (norm 0.794)
- n=92  confidence=medium
- Layer-A relative ladder; multiply by an absolute anchor (VSL) to make it cardinal.

### liberty_time — custodial years imposed per year of liberty taken
- estimate: **521.43** jail-yr per liberty-yr
- range: [0.65, 3406.67]
- n=9  confidence=low
- Median custody-to-deprivation ratio (retributive multiplier > 1 expected). Durations parsed best-effort.

## Triangulation consistency check

- check: W_to_L =? W_to_M / value_of_a_life_year
- value_of_a_life_year_usd: 0.0
- implied_W_to_L_from_money: 0.284
- measured_W_to_L: 0.402
- verdict: consistent (same order of magnitude)

## Status

- estimated: L_to_M, W_to_L, W_to_M, suffering_severity_to_money, In, money_concavity, severity_ladder, liberty_time
- pending (need more data): none
