#!/usr/bin/env python3
"""compute_ratios.py - estimate UMQF conversion ratios from observations/*.jsonl.

Reads the open JSONL source of truth (no hidden DB). Equivalent SQL-over-files (optional):
    pip install duckdb
    duckdb -c "SELECT harm_type, avg(penalty_jail_years) FROM read_json_auto('data/observations/*.jsonl') GROUP BY 1"

Here we use pandas/numpy (+scipy if present). Each ratio degrades gracefully: when data is
thin it is emitted with status='pending' and a note on what is needed. Functional forms are
fitted and selected by R2 (power law nests linear at b=1) per universal_formulas.md.
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1]
OBS = DATA / "observations"
OUT = DATA / "ratios.json"
LE_REF = 40.0  # reference remaining life expectancy (years) for value-of-a-life-year


def load():
    rows = []
    for f in sorted(OBS.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return pd.DataFrame(rows)


def col(df, name):
    if name in df.columns:
        return df[name]
    return pd.Series([np.nan] * len(df), index=df.index)


def numcol(df, name):
    return pd.to_numeric(col(df, name), errors="coerce")


def has_ratio(df, name):
    if "informs_ratio" not in df.columns:
        return pd.Series([False] * len(df), index=df.index)
    return df["informs_ratio"].apply(lambda r: isinstance(r, list) and name in r)


def r2(y, yhat):
    y = np.asarray(y, float); yhat = np.asarray(yhat, float)
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def fit_best(x, y):
    """Fit linear / power / log; return (form, params, R2) of the best by R2."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    out = []
    try:
        a, b = np.polyfit(x, y, 1)
        out.append(("linear", {"a": float(a), "b": float(b)}, r2(y, a * x + b)))
    except Exception:
        pass
    if np.all(x > 0) and np.all(y > 0):
        try:
            b, la = np.polyfit(np.log(x), np.log(y), 1)
            a = math.exp(la)
            out.append(("power", {"a": float(a), "b": float(b)}, r2(y, a * np.power(x, b))))
        except Exception:
            pass
    if np.all(x > 0):
        try:
            a, b = np.polyfit(np.log(x), y, 1)
            out.append(("log", {"a": float(a), "b": float(b)}, r2(y, a * np.log(x) + b)))
        except Exception:
            pass
    out = [o for o in out if not math.isnan(o[2])]
    return max(out, key=lambda o: o[2]) if out else None


def pending(name, note):
    return {"ratio": name, "status": "pending", "notes": note}


def main():
    df = load()
    n = len(df)
    ratios = []

    # --- L_to_M : money value of one statistical life (anchors dOS = -1) ---
    m = df[has_ratio(df, "L_to_M")]
    vals = numcol(m, "money_value_usd2024").dropna()
    if len(vals) >= 1:
        ratios.append({
            "ratio": "L_to_M", "meaning": "money value of one life (anchors dOS=-1)",
            "unit": "USD_2024 per life", "estimate": float(vals.median()),
            "range": [float(vals.min()), float(vals.max())], "n": int(len(vals)),
            "form": "point", "confidence": "high" if len(vals) >= 2 else "medium",
            "sources": m[numcol(m, "money_value_usd2024").notna()]["id"].tolist(), "status": "estimated",
            "notes": "Median of VSL / wrongful-death figures. dOS=-1 maps to this USD amount."})
    else:
        ratios.append(pending("L_to_M", "need VSL or wrongful-death money figures"))

    # --- W_to_L : life-years lost per welfare-year (GBD disability weights only) ---
    # Filter by SOURCE: the QALY sources carry genuine DALY weights (any harm_type); tort severity-proxies are NOT weights.
    m = df[has_ratio(df, "W_to_L") & col(df, "source").isin(["qaly", "qaly_weights"])]
    dw = numcol(m, "harm_magnitude").dropna()
    if len(dw) >= 1:
        ratios.append({
            "ratio": "W_to_L", "meaning": "life-years lost per year at given suffering (disability weight)",
            "unit": "life-yr per suffering-yr", "estimate": float(dw.median()),
            "range": [float(dw.min()), float(dw.max())], "n": int(len(dw)),
            "form": "point", "confidence": "medium", "sources": m["id"].tolist(), "status": "estimated",
            "notes": "GBD-style disability weights. Supports kappa near 1 (one shared scale): worst sustained states ~0.5-0.7, not 60x."})
    else:
        ratios.append(pending("W_to_L", "need GBD disability weights"))

    # --- W_to_M : money value of one welfare-YEAR (QALY cost-effectiveness thresholds) ---
    # Per-year rate only: anchor rows whose duration is a year. Excludes permanent-state lump-sum tariffs.
    m = df[has_ratio(df, "W_to_M")]
    is_anchor = col(m, "harm_type") == "anchor"
    is_per_year = col(m, "harm_duration").astype(str).str.contains("year", case=False, na=False)
    qaly = m[is_anchor & is_per_year]
    wm = numcol(qaly, "money_value_usd2024").dropna()
    if len(wm) >= 1:
        ratios.append({
            "ratio": "W_to_M", "meaning": "money value of one welfare-year (QALY)",
            "unit": "USD_2024 per welfare-yr", "estimate": float(wm.median()),
            "range": [float(wm.min()), float(wm.max())], "n": int(len(wm)),
            "form": "point", "confidence": "medium", "sources": qaly["id"].tolist(), "status": "estimated",
            "notes": "Cost-effectiveness thresholds per QALY."})
    else:
        ratios.append(pending("W_to_M", "need QALY money thresholds (per-year anchor rows)"))

    # --- suffering_severity_to_money : lump-sum money vs suffering severity (tort/CICS PSLA) ---
    sm = df[col(df, "source") == "tort_pain_suffering"]
    smd = pd.DataFrame({"x": numcol(sm, "harm_magnitude"), "y": numcol(sm, "money_value_usd2024")}).dropna()
    smd = smd[(smd.x > 0) & (smd.y > 0)]
    if len(smd) >= 3:
        fit = fit_best(smd.x.values, smd.y.values)
        if fit:
            form, params, score = fit
            ratios.append({
                "ratio": "suffering_severity_to_money",
                "meaning": "lump-sum money per unit suffering severity (permanent-state pain-and-suffering awards)",
                "unit": "USD_2024 vs severity(0-1)", "form": form,
                "params": {k: round(v, 3) for k, v in params.items()}, "r2": round(score, 4),
                "n": int(len(smd)), "confidence": "medium", "status": "estimated",
                "notes": "Tort PSLA awards; exponent/curvature shows how suffering price scales with severity (lump-sum, not per-year)."})
        else:
            ratios.append(pending("suffering_severity_to_money", "fit failed on tort severity/money pairs"))
    else:
        ratios.append(pending("suffering_severity_to_money", "need >=3 tort severity/money pairs"))

    # --- In : intent multiplier from same-harm (death) sentencing at different intent ---
    d = df[(col(df, "harm_type") == "death") & numcol(df, "penalty_jail_years").notna()] if n else df
    if len(d):
        g = d.assign(j=numcol(d, "penalty_jail_years")).groupby("intent")["j"].mean()
        base = g.get("intentional", float("nan"))
        if base and not math.isnan(base) and base > 0:
            mult = {}
            for k in ["reckless", "negligent", "accidental"]:
                if k in g and not math.isnan(g[k]):
                    mult[k] = round(float(g[k] / base), 3)
            if mult:
                ratios.append({
                    "ratio": "In", "meaning": "intent multiplier (jail vs intentional, harm=death)",
                    "unit": "x of intentional", "estimate": mult, "form": "point",
                    "n": int(len(d)), "confidence": "medium", "status": "estimated",
                    "notes": "Empirical In from murder vs manslaughter sentencing."})
            else:
                ratios.append(pending("In", "have intentional-death baseline; need manslaughter (reckless/negligent) deaths"))
        else:
            ratios.append(pending("In", "need intentional-death (murder) baseline sentence"))
    else:
        ratios.append(pending("In", "need death sentencing rows with intent"))

    # --- money_concavity : fit penalty(jail) vs money loss ---
    m = df[has_ratio(df, "money_concavity")]
    d2 = pd.DataFrame({"x": numcol(m, "money_value_usd2024"), "y": numcol(m, "penalty_jail_years")}).dropna()
    d2 = d2[(d2.x > 0) & (d2.y > 0)]
    if len(d2) >= 3:
        fit = fit_best(d2.x.values, d2.y.values)
        if fit:
            form, params, score = fit
            ratios.append({
                "ratio": "money_concavity", "meaning": "how punishment scales with money loss",
                "unit": "jail-yr vs USD", "form": form,
                "params": {k: round(v, 6) for k, v in params.items()}, "r2": round(score, 4),
                "n": int(len(d2)), "confidence": "medium", "status": "estimated",
                "notes": "power exponent b<1 => diminishing (concave); b~1 => linear."})
        else:
            ratios.append(pending("money_concavity", "fit failed on available loss/penalty pairs"))
    else:
        ratios.append(pending("money_concavity", "need >=3 theft/fraud loss->penalty tiers"))

    # --- severity_ladder : relative ordering by custodial sentence ---
    s = df.copy()
    s["cost"] = numcol(s, "penalty_jail_years")
    ladder = s.dropna(subset=["cost"]).sort_values("cost", ascending=False)
    if len(ladder):
        mx = float(ladder["cost"].max())
        recs = ladder[["id", "label_raw", "cost"]].to_dict("records") if "label_raw" in ladder.columns else ladder[["id", "cost"]].to_dict("records")
        entries = [{"id": e["id"], "label": e.get("label_raw"), "jail_years": float(e["cost"]),
                    "norm": round(float(e["cost"] / mx), 3)} for e in recs][:12]
        ratios.append({
            "ratio": "severity_ladder", "meaning": "relative harm ordering by custodial sentence",
            "unit": "jail-yr (norm to max)", "entries": entries, "n": int(len(ladder)),
            "form": "ordinal", "confidence": "medium", "status": "estimated",
            "notes": "Layer-A relative ladder; multiply by an absolute anchor (VSL) to make it cardinal."})
    else:
        ratios.append(pending("severity_ladder", "need custodial sentences"))

    # --- liberty_time : custodial response per duration of liberty taken ---
    m = df[has_ratio(df, "liberty_time")]
    if len(m) >= 2:
        ratios.append({
            "ratio": "liberty_time", "meaning": "custodial response per duration of liberty taken",
            "unit": "jail-yr per yr liberty lost", "n": int(len(m)), "form": "point",
            "confidence": "low", "status": "estimated", "sources": m["id"].tolist(),
            "notes": "From false imprisonment / kidnapping; refine with explicit durations."})
    else:
        ratios.append(pending("liberty_time", "need false-imprisonment/kidnap sentences with durations"))

    # --- triangulation: W_to_L should ~ W_to_M / value_of_a_life_year ---
    tri = {"check": "W_to_L =? W_to_M / value_of_a_life_year"}
    def est(name):
        for r in ratios:
            if r["ratio"] == name and r.get("status") == "estimated":
                return r.get("estimate")
        return None
    lm, wm_e, wl_e = est("L_to_M"), est("W_to_M"), est("W_to_L")
    if isinstance(lm, (int, float)) and isinstance(wm_e, (int, float)) and isinstance(wl_e, (int, float)) and wl_e:
        vly = lm / LE_REF
        implied = wm_e / vly  # money-per-welfare-yr / money-per-life-yr = life-yr per welfare-yr
        ratio = implied / wl_e if wl_e else float("inf")
        tri.update({
            "value_of_a_life_year_usd": round(vly, 0),
            "implied_W_to_L_from_money": round(implied, 3),
            "measured_W_to_L": round(wl_e, 3),
            "verdict": "consistent (same order of magnitude)" if 0.2 <= ratio <= 5 else "DISCREPANCY - instruments disagree (expected; different instruments measure different things)"})
    else:
        tri["verdict"] = "pending (need L_to_M, W_to_M, W_to_L all estimated)"

    result = {
        "generated_from": f"{n} observations in data/observations/*.jsonl",
        "currency": "USD_2024",
        "method": "pandas/numpy fits; forms linear/power/log selected by R2 (see universal_formulas.md)",
        "ratios": ratios,
        "triangulation": tri,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"compute_ratios: wrote {OUT.relative_to(DATA)} from {n} observations")
    for r in ratios:
        tag = r.get("status", "")
        extra = ""
        if tag == "estimated":
            extra = f"  {r.get('form','')} est={r.get('estimate', r.get('entries') and '(ladder)')}"
        print(f"  - {r['ratio']:16s} {tag}{extra}")
    print(f"  triangulation: {tri.get('verdict')}")


if __name__ == "__main__":
    main()
