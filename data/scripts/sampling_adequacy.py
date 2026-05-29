#!/usr/bin/env python3
"""sampling_adequacy.py - how many data points / sources are needed per ratio.

Precision is set by the KIND of ratio, not a guess:
  - geomean ratios (L_to_M, W_to_M, W_to_L, liberty_time): a single quantity averaged across
    jurisdictions. Target a tight CI on the geometric mean:
        N >= (1.96 * sigma_log / ln F)^2     (F = target factor, e.g. 1.25 or 1.10)
  - curve ratios (money_concavity): the value-spread IS the signal (loss tiers span many
    decades), so raw-N is the wrong metric. Precision = CI on the fitted exponent; what matters
    is DOMAIN COVERAGE (points per decade) and JURISDICTION count.
  - group_ratio (In): a contrast of group means; precision = CI on the ratio -> JURISDICTION count.
  - ladder (severity_ladder): ordinal; needs the major guideline systems represented.

Writes data/sampling_status.json and prints a table. This is the STOPPING RULE: collect until
the geomean CI <= target AND a new jurisdiction no longer moves the estimate (and, globally,
until value_axis.json's measured_arbitrage_cycle is within tolerance of 1.0).
"""
import json
import math
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[1]
OBS = DATA / "observations"
OUT = DATA / "sampling_status.json"

JUR_TARGET = 8  # jurisdictions across >=3 legal traditions for curve/group/ladder ratios

SPEC = {  # ratio: (value_field, kind)
    "L_to_M": ("money_value_usd2024", "geomean"),
    "W_to_M": ("money_value_usd2024", "geomean"),
    "W_to_L": ("harm_magnitude", "geomean"),
    "liberty_time": ("penalty_jail_years", "geomean"),
    "In": ("penalty_jail_years", "group_ratio"),
    "money_concavity": ("money_value_usd2024", "curve"),
    "severity_ladder": ("penalty_jail_years", "ladder"),
}


def load():
    rows = []
    for f in sorted(OBS.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def n_needed(sigma_log, factor):
    if sigma_log <= 0:
        return 1
    return int(math.ceil((1.96 * sigma_log / math.log(factor)) ** 2))


def main():
    rows = load()
    out = {}
    for ratio, (field, kind) in SPEC.items():
        sel = [r for r in rows if ratio in (r.get("informs_ratio") or [])]
        vals = [float(r.get(field)) for r in sel if isinstance(r.get(field), (int, float)) and r.get(field) and r.get(field) > 0]
        jur = {r.get("jurisdiction") for r in sel if r.get("jurisdiction")}
        trad = {r.get("legal_tradition") for r in sel if r.get("legal_tradition")}
        rec = {"kind": kind, "n": len(vals), "jurisdictions": len(jur),
               "legal_traditions": len(trad), "traditions": sorted(t for t in trad if t)}
        if len(vals) >= 2:
            lv = np.log(vals)
            sigma = float(np.std(lv, ddof=1))
            rec["sigma_log"] = round(sigma, 3)
            rec["geo_mean"] = float(math.exp(np.mean(lv)))
            if kind == "geomean":
                rec["achieved_95ci_factor"] = round(math.exp(1.96 * sigma / math.sqrt(len(vals))), 2)
                rec["n_for_25pct"] = n_needed(sigma, 1.25)
                rec["n_for_10pct"] = n_needed(sigma, 1.10)
                rec["gap_to_25pct"] = max(0, rec["n_for_25pct"] - len(vals))
            elif kind == "curve":
                rec["decades_covered"] = round(float((np.max(lv) - np.min(lv)) / math.log(10)), 1)
                rec["jur_target"] = JUR_TARGET
                rec["jur_gap"] = max(0, JUR_TARGET - len(jur))
                rec["precision_note"] = "fit the exponent; bootstrap its CI. Need >=1 pt/decade and >=8 jurisdictions; raw-N target N/A."
            else:  # group_ratio / ladder
                rec["jur_target"] = JUR_TARGET
                rec["jur_gap"] = max(0, JUR_TARGET - len(jur))
                rec["precision_note"] = "precision = CI on the group contrast / ordinal coverage; driven by jurisdiction count, not raw-N."
        else:
            rec["status"] = "insufficient (need >=2)"
        out[ratio] = rec

    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"sampling_adequacy: wrote {OUT.relative_to(DATA)}")
    print(f"  {'ratio':16s} {'kind':11s} {'n':>3s} {'jur':>3s} {'trd':>3s} {'sig':>5s}  target")
    for k, v in out.items():
        tgt = ""
        if v.get("kind") == "geomean" and "n_for_25pct" in v:
            tgt = f"CI {v['achieved_95ci_factor']}x; need {v['n_for_25pct']} for +-25%, {v['n_for_10pct']} for +-10%"
        elif "jur_target" in v:
            extra = f", {v['decades_covered']} decades" if "decades_covered" in v else ""
            tgt = f">= {v['jur_target']} jurisdictions (have {v['jurisdictions']}, gap {v['jur_gap']}){extra}"
        else:
            tgt = v.get("status", "")
        sig = f"{v.get('sigma_log', float('nan')):5.2f}" if "sigma_log" in v else "  -  "
        print(f"  {k:16s} {v['kind']:11s} {v['n']:3d} {v['jurisdictions']:3d} {v.get('legal_traditions', 0):3d} {sig}  {tgt}")
    print("  (trd = independent legal traditions represented; universality wants this high, not just jur)")


if __name__ == "__main__":
    main()
