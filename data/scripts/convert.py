#!/usr/bin/env python3
"""convert.py - reconcile the calibration rates onto ONE common value axis so every conversion
is invertible AND arbitrage-free (round-trips exactly), and expose convert().

The money node is GCU (income-normalized), not raw currency: money passes through GCU before any
conversion, which removes income dependence and is what lets the life<->money rate be universal.

The rates come from different instruments, so the raw cross-rates are not mutually consistent.
We place each currency on a single log "value axis" by least-squares; the fitted cross-rates then
satisfy no-arbitrage (any cycle multiplies to 1) BY CONSTRUCTION, and the leftover residual is the
data inconsistency to be reduced by more/cleaner sampling. Writes data/value_axis.json.
"""
import json
import math
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[1]
RATIOS = DATA / "ratios.json"
CONFIG = Path(__file__).resolve().parent / "config.json"
OUT = DATA / "value_axis.json"


def _ratios():
    r = json.loads(RATIOS.read_text(encoding="utf-8"))
    return {x["ratio"]: x for x in r.get("ratios", [])}


def build_axis():
    R = _ratios()
    LE = json.loads(CONFIG.read_text(encoding="utf-8")).get("life_expectancy_years_ref", 40)

    def est(n):
        x = R.get(n, {})
        return x.get("estimate") if x.get("status") == "estimated" else None

    L_to_M, W_to_M, W_to_L = est("L_to_M"), est("W_to_M"), est("W_to_L")  # money now in GCU
    # nodes: gcu (reference, v=0), life_year, welfare_year. rate(a->b)=exp(v_a-v_b) = units of b per a
    A, b, used = [], [], []
    if L_to_M:
        A.append([1, 0]); b.append(math.log(L_to_M / LE)); used.append("life_year->gcu (VLY)")
    if W_to_M:
        A.append([0, 1]); b.append(math.log(W_to_M)); used.append("welfare_year->gcu")
    if W_to_L:
        A.append([-1, 1]); b.append(math.log(W_to_L)); used.append("welfare_year->life_year")

    if not A:
        raise RuntimeError("no anchor rates estimated yet; run compute_ratios.py first")
    A = np.array(A, float); b = np.array(b, float)
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    v = {"gcu": 0.0, "life_year": float(x[0]), "welfare_year": float(x[1])}
    resid = (A @ x - b).tolist()

    arb = None
    if L_to_M and W_to_M and W_to_L:
        VLY = L_to_M / LE
        arb = VLY * (1.0 / W_to_M) * W_to_L  # life_year->gcu->welfare_year->life_year; ==1 iff consistent

    axis = {
        "money_unit": "GCU", "nodes_log_value": v, "LE_years": LE,
        "reconciled_rates": {
            "life_to_gcu": math.exp(v["life_year"] - v["gcu"]) * LE,
            "life_year_to_gcu": math.exp(v["life_year"] - v["gcu"]),
            "welfare_year_to_gcu": math.exp(v["welfare_year"] - v["gcu"]),
            "welfare_year_to_life_year": math.exp(v["welfare_year"] - v["life_year"]),
        },
        "measured_arbitrage_cycle": arb,
        "reconciliation_residuals_log": dict(zip(used, [round(r, 4) for r in resid])),
        "money_concavity": R.get("money_concavity", {}),
        "In": R.get("In", {}),
        "note": "Money is GCU (income-normalized). convert(x,a,b)=x*exp(v[a]-v[b]); invertible & arbitrage-free by construction. measured_arbitrage_cycle is the raw-data inconsistency (target 1.0).",
    }
    return axis


def convert(value, frm, to, axis=None):
    if axis is None:
        axis = json.loads(OUT.read_text(encoding="utf-8"))
    v = axis["nodes_log_value"]
    if frm not in v or to not in v:
        raise KeyError(f"unknown node(s): {frm}->{to}; have {list(v)}")
    return value * math.exp(v[frm] - v[to])


def money_to_harm(loss_usd, axis=None):
    """Punishment-severity proxy (jail-years) for a money loss, from the fitted concave law (USD loss)."""
    if axis is None:
        axis = json.loads(OUT.read_text(encoding="utf-8"))
    p = axis.get("money_concavity", {})
    if p.get("form") != "power":
        return None
    a, bx = p["params"]["a"], p["params"]["b"]
    return a * (loss_usd ** bx)


def harm_to_money(jail_years, axis=None):
    if axis is None:
        axis = json.loads(OUT.read_text(encoding="utf-8"))
    p = axis.get("money_concavity", {})
    if p.get("form") != "power":
        return None
    a, bx = p["params"]["a"], p["params"]["b"]
    return (jail_years / a) ** (1.0 / bx)


def main():
    axis = build_axis()
    OUT.write_text(json.dumps(axis, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"convert: wrote {OUT.relative_to(DATA)}")
    print(f"  nodes (log value): {axis['nodes_log_value']}")
    arb = axis["measured_arbitrage_cycle"]
    if arb:
        print(f"  measured arbitrage cycle = {arb:.3f}  (target 1.0; {max(arb, 1 / arb):.2f}x raw inconsistency)")
    print(f"  reconciled life value = {axis['reconciled_rates']['life_to_gcu']:.2f} GCU")
    print(f"  reconciliation residuals (log): {axis['reconciliation_residuals_log']}")


if __name__ == "__main__":
    main()
