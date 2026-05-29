#!/usr/bin/env python3
"""extract.py - merge curated seed + research-agent collected data into observations/*.jsonl.

The source of truth is plain-text JSON Lines (one observation object per line), grouped by
source. Re-runnable and idempotent: dedups by `id`. No hidden database.

Inputs (in data/raw/):
  - seed.jsonl        : curated, hand-verified anchors
  - collected.json    : research-agent output, either {"bySource": {src:[...]}} or a flat list
Output:
  - data/observations/<source>.jsonl
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1]
RAW = DATA / "raw"
OBS = DATA / "observations"
OBS.mkdir(exist_ok=True)

REQUIRED = ["id", "source", "summary", "harm_type", "intent", "informs_ratio", "source_citation", "confidence"]
CONF_RANK = {"high": 3, "medium": 2, "low": 1}


def read_jsonl(p):
    out = []
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"  WARN bad JSON line in {p.name}: {e}")
    return out


def read_collected(p):
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "bySource" in data:
        rows = []
        for src, lst in (data["bySource"] or {}).items():
            for o in (lst or []):
                o.setdefault("source", src)
                rows.append(o)
        return rows
    if isinstance(data, list):
        return data
    return []


def valid(o):
    return all(k in o and o[k] not in (None, "") for k in REQUIRED)


def main():
    rows = read_jsonl(RAW / "seed.jsonl") + read_collected(RAW / "collected.json")

    chosen, dropped = {}, 0
    for o in rows:
        if not valid(o):
            dropped += 1
            continue
        oid = o["id"]
        prev = chosen.get(oid)
        if prev is None or CONF_RANK.get(o.get("confidence"), 0) > CONF_RANK.get(prev.get("confidence"), 0):
            chosen[oid] = o  # keep the higher-confidence duplicate

    by_source = {}
    for o in chosen.values():
        by_source.setdefault(o["source"], []).append(o)

    for src, lst in sorted(by_source.items()):
        lst.sort(key=lambda x: x["id"])
        out = OBS / f"{src}.jsonl"
        with open(out, "w", encoding="utf-8") as fh:
            for o in lst:
                fh.write(json.dumps(o, ensure_ascii=False) + "\n")
        print(f"  {src:20s} {len(lst):4d} -> {out.relative_to(DATA)}")

    print(f"extract: kept {len(chosen)}, dropped {dropped} (missing required fields), {len(by_source)} sources")


if __name__ == "__main__":
    main()
