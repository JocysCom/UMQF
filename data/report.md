# UMQF Legal/Economic Calibration — Report

Source of truth: `data/observations/*.jsonl` — **111 observations** across **11 sources** (confidence: 97 high / 12 medium / 2 low). Currency: USD_2024.

> First-pass estimates from a curated seed + research-agent corpus. Treat as Phase-1 anchors, not final constants.

## Observations by source

- **day_fines**: 10
- **homicide_intent**: 17
- **liberty_duration**: 11
- **money_loss_curve**: 17
- **qaly**: 3
- **qaly_weights**: 21
- **tort_pain_suffering**: 18
- **uk_violence**: 2
- **vsl**: 2
- **vsl_wrongful_death**: 7
- **workers_comp**: 3

## Conversion ratios

### L_to_M — money value of one life (anchors dOS=-1)
- estimate: **13700000.0** USD_2024 per life
- range: [11500000.0, 890000000.0]
- n=9  confidence=high
- Median of VSL / wrongful-death figures. dOS=-1 maps to this USD amount.

### W_to_L — life-years lost per year at given suffering (disability weight)
- estimate: **0.402** life-yr per suffering-yr
- range: [0.03, 0.732]
- n=22  confidence=medium
- GBD-style disability weights. Supports kappa near 1 (one shared scale): worst sustained states ~0.5-0.7, not 60x.

### W_to_M — money value of one welfare-year (QALY)
- estimate: **65500.0** USD_2024 per welfare-yr
- range: [31000.0, 100000.0]
- n=2  confidence=medium
- Cost-effectiveness thresholds per QALY.

### suffering_severity_to_money — lump-sum money per unit suffering severity (permanent-state pain-and-suffering awards)
- form: **linear**  params={'a': 567658.462, 'b': -69791.467}  R2=0.6867
- n=18  confidence=medium
- Tort PSLA awards; exponent/curvature shows how suffering price scales with severity (lump-sum, not per-year).

### In — intent multiplier (jail vs intentional, harm=death)
- estimate: **{'reckless': 0.404, 'negligent': 0.27}** x of intentional
- n=15  confidence=medium
- Empirical In from murder vs manslaughter sentencing.

### money_concavity — how punishment scales with money loss
- form: **power**  params={'a': 0.06603, 'b': 0.283861}  R2=0.9041
- n=17  confidence=medium
- power exponent b<1 => diminishing (concave); b~1 => linear.

### severity_ladder — relative harm ordering by custodial sentence
  - Murder, 30-year minimum-term starting point: 30.0 yr (norm 1.0)
  - Murder, 25-year minimum-term starting point (weapon taken to scene): 25.0 yr (norm 0.833)
  - Second-degree murder, USSG level 38, 235-293 mo at CHC I: 22.0 yr (norm 0.733)
  - 18 U.S.C. §1201(g): mandatory minimum 20 years where victim is a minor and offender is not parent/close relative/legal custodian: 20.0 yr (norm 0.667)
  - Unlawful-act manslaughter tier A (start 18yr, range 11-24yr): 18.0 yr (norm 0.6)
  - USSG §2B1.1(b)(1)(P): >$550,000,000 → +30 levels (level 36) → 188–235 months, Category I: 17.625 yr (norm 0.588)
  - Kidnap/False Imprisonment definitive guideline; range community order to 16 years; max life: 16.0 yr (norm 0.533)
  - Murder, 15-year default minimum-term starting point: 15.0 yr (norm 0.5)
- n=43  confidence=medium
- Layer-A relative ladder; multiply by an absolute anchor (VSL) to make it cardinal.

### liberty_time — custodial response per duration of liberty taken
- n=12  confidence=low
- From false imprisonment / kidnapping; refine with explicit durations.

## Triangulation consistency check

- check: W_to_L =? W_to_M / value_of_a_life_year
- value_of_a_life_year_usd: 342500.0
- implied_W_to_L_from_money: 0.191
- measured_W_to_L: 0.402
- verdict: consistent (same order of magnitude)

## Status

- estimated: L_to_M, W_to_L, W_to_M, suffering_severity_to_money, In, money_concavity, severity_ladder, liberty_time
- pending (need more data): none
