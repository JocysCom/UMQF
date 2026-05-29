#!/usr/bin/env python3
"""report.py - human-readable Markdown summary of the calibration (data/report.md)."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1]
OBS = DATA / "observations"
RATIOS = DATA / "ratios.json"
OUT = DATA / "report.md"


def load_obs():
    rows = []
    for f in sorted(OBS.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main():
    obs = load_obs()
    r = json.loads(RATIOS.read_text(encoding="utf-8")) if RATIOS.exists() else {"ratios": [], "triangulation": {}}
    by_src = {}
    conf = {"high": 0, "medium": 0, "low": 0}
    for o in obs:
        by_src[o["source"]] = by_src.get(o["source"], 0) + 1
        conf[o.get("confidence", "low")] = conf.get(o.get("confidence", "low"), 0) + 1

    L = []
    L.append("# UMQF Legal/Economic Calibration — Report")
    L.append("")
    L.append(f"Source of truth: `data/observations/*.jsonl` — **{len(obs)} observations** across "
             f"**{len(by_src)} sources** (confidence: {conf.get('high',0)} high / {conf.get('medium',0)} medium / {conf.get('low',0)} low). "
             f"Currency: {r.get('currency','USD_2024')}.")
    L.append("")
    L.append("> First-pass estimates from a curated seed + research-agent corpus. Treat as Phase-1 anchors, not final constants.")
    L.append("")
    L.append("## Observations by source")
    L.append("")
    for s, c in sorted(by_src.items()):
        L.append(f"- **{s}**: {c}")
    L.append("")
    L.append("## Conversion ratios")
    L.append("")
    for rat in r.get("ratios", []):
        name = rat.get("ratio")
        if rat.get("status") == "estimated":
            L.append(f"### {name} — {rat.get('meaning','')}")
            if "estimate" in rat:
                L.append(f"- estimate: **{rat['estimate']}** {rat.get('unit','')}")
            if "range" in rat:
                L.append(f"- range: {rat['range']}")
            if rat.get("form") and rat["form"] not in ("point", "ordinal"):
                L.append(f"- form: **{rat['form']}**  params={rat.get('params')}  R2={rat.get('r2')}")
            for e in rat.get("entries", [])[:8]:
                L.append(f"  - {e.get('label') or e.get('id')}: {e.get('jail_years')} yr (norm {e.get('norm')})")
            L.append(f"- n={rat.get('n')}  confidence={rat.get('confidence')}")
            if rat.get("notes"):
                L.append(f"- {rat['notes']}")
        else:
            L.append(f"### {name} — _pending_")
            if rat.get("notes"):
                L.append(f"- needs: {rat['notes']}")
        L.append("")
    L.append("## Triangulation consistency check")
    L.append("")
    for k, v in r.get("triangulation", {}).items():
        L.append(f"- {k}: {v}")
    L.append("")
    est = [x["ratio"] for x in r.get("ratios", []) if x.get("status") == "estimated"]
    pend = [x["ratio"] for x in r.get("ratios", []) if x.get("status") != "estimated"]
    L.append("## Status")
    L.append("")
    L.append(f"- estimated: {', '.join(est) or 'none'}")
    L.append(f"- pending (need more data): {', '.join(pend) or 'none'}")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"report: wrote {OUT.relative_to(DATA)}")


if __name__ == "__main__":
    main()
