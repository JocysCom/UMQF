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
import re
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


def parse_years(s):
    """Best-effort freeform duration -> years (e.g. '6 months' -> 0.5)."""
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    t = str(s).lower()
    m = re.search(r"\d+(?:\.\d+)?", t)
    if not m:
        return None
    try:
        val = float(m.group(0))
    except ValueError:
        return None
    if "month" in t:
        return val / 12.0
    if "week" in t:
        return val * 7 / 365.0
    if "day" in t:
        return val / 365.0
    if "hour" in t:
        return val / (365.0 * 24)
    return val


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

    # --- L_to_M : GCU value of one life (income-normalized), SPLIT BY CONSTRUCT ---
    m = df[has_ratio(df, "L_to_M")].copy()
    m = m[numcol(m, "money_value_gcu").notna()]
    if len(m):
        m["gval"] = numcol(m, "money_value_gcu")
        m["uval"] = numcol(m, "money_value_usd2024")
        m["con"] = col(m, "construct").fillna("unspecified")
        by_con = {}
        for con, grp in m.groupby("con"):
            v = grp["gval"]
            trad = sorted(set(col(grp, "legal_tradition").dropna().tolist()))
            by_con[con] = {"median_gcu": round(float(v.median()), 3),
                           "range_gcu": [round(float(v.min()), 3), round(float(v.max()), 3)],
                           "median_usd": round(float(grp["uval"].median()), 0) if grp["uval"].notna().any() else None,
                           "n": int(len(v)), "traditions": trad}
        # primary anchor = willingness-to-pay (forward-looking, matches the survival-odds framing of dOS)
        prim_key = "wtp" if "wtp" in by_con else ("unspecified" if "unspecified" in by_con else next(iter(by_con)))
        primary = by_con[prim_key]
        cross = None
        if "wtp" in by_con and "compensation" in by_con and by_con["compensation"]["median_gcu"]:
            cross = round(by_con["wtp"]["median_gcu"] / by_con["compensation"]["median_gcu"], 1)
        ratios.append({
            "ratio": "L_to_M", "meaning": "GCU value of one life (anchors dOS=-1); income-normalized; split by construct",
            "unit": "GCU per life", "estimate": primary["median_gcu"], "primary_construct": prim_key,
            "by_construct": by_con, "cross_construct_ratio_wtp_over_compensation": cross,
            "n": int(len(m)), "form": "point",
            "confidence": "high" if primary["n"] >= 2 else "medium", "status": "estimated",
            "notes": "Income-normalized (money/GCU): VSL is ~constant in GCU though ~30x in USD. WTP anchors dOS=-1; compensation is a separate, lower construct (not averaged in). diyya identity multipliers are cultural, excluded by UMQF."})
    else:
        ratios.append(pending("L_to_M", "need money_value_gcu (run categorize_ai after the gcu backfill)"))

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
    qaly = m[is_anchor & is_per_year].copy()
    qaly = qaly[numcol(qaly, "money_value_gcu").notna()]
    if len(qaly):
        qaly["gval"] = numcol(qaly, "money_value_gcu")
        qaly["con"] = col(qaly, "construct").fillna("budget")
        by_con = {}
        for con, grp in qaly.groupby("con"):
            v = grp["gval"]
            by_con[con] = {"median_gcu": round(float(v.median()), 5),
                           "range_gcu": [round(float(v.min()), 5), round(float(v.max()), 5)], "n": int(len(v))}
        prim_key = "wtp" if "wtp" in by_con else next(iter(by_con))
        primary = by_con[prim_key]
        ratios.append({
            "ratio": "W_to_M", "meaning": "GCU value of one welfare-year (QALY), income-normalized, by construct",
            "unit": "GCU per welfare-yr", "estimate": primary["median_gcu"], "primary_construct": prim_key,
            "by_construct": by_con, "n": int(len(qaly)), "form": "point", "confidence": "medium", "status": "estimated",
            "notes": "budget=cost-effectiveness threshold; wtp=empirical willingness-to-pay per QALY. They are close (~0.01-0.02 GCU), so the cross-rate residual is the VSL-vs-QALY value-per-life-year gap, not a W_to_M construct artifact."})
    else:
        ratios.append(pending("W_to_M", "need QALY thresholds with money_value_gcu (per-year anchor rows)"))

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

    # --- In : intent multiplier, computed WITHIN each jurisdiction then averaged ---
    # (per-jurisdiction ratio cancels absolute sentence-scale differences, e.g. UK life-minimums vs German terms)
    d = df[(col(df, "harm_type") == "death") & numcol(df, "penalty_jail_years").notna()].copy()
    if len(d):
        d["j"] = numcol(d, "penalty_jail_years")
        d["jur"] = col(d, "jurisdiction").fillna("?")
        per = {"reckless": [], "negligent": [], "accidental": []}
        njur = 0
        for _, grp in d.groupby("jur"):
            gi = grp[grp["intent"] == "intentional"]["j"]
            base = gi.mean()
            if not (base and base > 0):
                continue
            used = False
            for k in per:
                gk = grp[grp["intent"] == k]["j"]
                if len(gk):
                    per[k].append(float(gk.mean() / base)); used = True
            if used:
                njur += 1
        mult = {k: round(float(np.mean(v)), 3) for k, v in per.items() if v}
        if mult:
            ratios.append({
                "ratio": "In", "meaning": "intent multiplier (jail vs intentional, harm=death), averaged within-jurisdiction",
                "unit": "x of intentional", "estimate": mult, "form": "point",
                "n": int(len(d)), "jurisdictions": njur, "confidence": "medium", "status": "estimated",
                "notes": "Per-jurisdiction ratio then averaged, so absolute sentence-scale differences cancel. Murder=life minimum-terms bias this downward."})
        else:
            ratios.append(pending("In", "need a jurisdiction with BOTH intentional and non-intentional death sentences"))
    else:
        ratios.append(pending("In", "need death sentencing rows with intent"))

    # --- money_concavity : fit penalty(jail) vs loss WITHIN a coherent schedule ---
    # Pooling structurally-different national schemes (continuous US loss table vs categorical bands /
    # caps) destroys the fit, so fit per schedule (jurisdiction, else source) and report corroboration.
    m = df[has_ratio(df, "money_concavity")]
    d2 = pd.DataFrame({"x": numcol(m, "money_value_usd2024"), "y": numcol(m, "penalty_jail_years"),
                       "src": col(m, "source"), "jur": col(m, "jurisdiction")}).dropna(subset=["x", "y"])
    d2 = d2[(d2.x > 0) & (d2.y > 0)]
    d2["key"] = d2["jur"].fillna(d2["src"])
    persrc = []
    for k, grp in d2.groupby("key"):
        if len(grp) >= 4:
            f = fit_best(grp.x.values, grp.y.values)
            if f:
                persrc.append({"schedule": str(k), "n": int(len(grp)), "form": f[0],
                               "params": {kk: round(v, 6) for kk, v in f[1].items()}, "r2": round(f[2], 3)})
    if persrc:
        persrc.sort(key=lambda r: -r["n"])  # primary = the schedule with the most points (cleanest, continuous)
        primary = persrc[0]
        concave = sum(1 for r in persrc if (r["form"] == "power" and r["params"].get("b", 1) < 1) or r["form"] == "log")
        ratios.append({
            "ratio": "money_concavity", "meaning": "how punishment scales with money loss (within one coherent schedule)",
            "unit": "jail-yr vs USD", "form": primary["form"], "params": primary["params"], "r2": primary["r2"],
            "primary_schedule": primary["schedule"], "n": primary["n"],
            "schedules_fitted": len(persrc), "corroborating_concave_schedules": concave,
            "per_schedule": persrc, "confidence": "medium", "status": "estimated",
            "notes": "Fit within one coherent loss->penalty schedule (US USSG 2B1.1 is the cleanest, continuous one); national schemes differ structurally (caps, categorical bands) so a pooled fit is invalid. power b<1 => diminishing/concave; %d of %d fitted schedules are concave." % (concave, len(persrc))})
    else:
        ratios.append(pending("money_concavity", "need >=4 (loss,penalty) points within one coherent schedule"))

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

    # --- liberty_time : custodial years imposed per year of liberty taken ---
    m = df[has_ratio(df, "liberty_time")].copy()
    if len(m):
        m["dur"] = col(m, "harm_duration").apply(parse_years)
        m["jy"] = numcol(m, "penalty_jail_years")
        pairs = m.dropna(subset=["dur", "jy"])
        pairs = pairs[(pairs["dur"] > 0) & (pairs["jy"] > 0)]
        if len(pairs) >= 2:
            rate = pairs["jy"] / pairs["dur"]
            ratios.append({
                "ratio": "liberty_time", "meaning": "custodial years imposed per year of liberty taken",
                "unit": "jail-yr per liberty-yr", "estimate": round(float(rate.median()), 2),
                "range": [round(float(rate.min()), 2), round(float(rate.max()), 2)],
                "n": int(len(pairs)), "form": "point", "confidence": "low", "status": "estimated",
                "notes": "Median custody-to-deprivation ratio (retributive multiplier > 1 expected). Durations parsed best-effort."})
        else:
            ratios.append(pending("liberty_time", f"have {len(m)} liberty rows but <2 with parseable durations; need explicit detention durations"))
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
