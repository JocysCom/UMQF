#!/usr/bin/env python3
"""categorize_ai.py - normalize / (re)categorize observations.

Collection-time research agents already assign harm_type and intent. This pass keeps the
corpus consistent across re-runs and is the hook for a richer AI re-categorization:
  - validates enum values (harm_type, intent),
  - backfills a default harm_magnitude per harm_type when missing,
  - maintains a label->harm_type cache (categorize_cache.json) for stable re-runs.

To upgrade: replace `rule_categorize` with a call to your AI agent and cache by label_raw,
so re-processing is cheap and deterministic.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1]
OBS = DATA / "observations"
CACHE = Path(__file__).resolve().parent / "categorize_cache.json"

HARM_TYPES = {"death", "bodily", "suffering", "liberty", "property", "psychological", "mixed", "anchor"}
INTENTS = {"intentional", "reckless", "negligent", "accidental", "na"}
DEFAULT_MAG = {"death": 1.0, "bodily": 0.2, "suffering": 0.3, "liberty": 0.1,
               "property": 0.05, "psychological": 0.2, "mixed": 0.3, "anchor": None}


def main():
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    changed = 0
    files = sorted(OBS.glob("*.jsonl"))
    for f in files:
        rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        for o in rows:
            if o.get("harm_type") not in HARM_TYPES:
                o["harm_type"] = "mixed"
                changed += 1
            if o.get("intent") not in INTENTS:
                o["intent"] = "na"
                changed += 1
            if o.get("harm_magnitude") in (None, "") and o["harm_type"] != "anchor":
                o["harm_magnitude"] = DEFAULT_MAG.get(o["harm_type"])
                changed += 1
            cache[o.get("label_raw") or o["id"]] = o["harm_type"]
        with open(f, "w", encoding="utf-8") as fh:
            for o in rows:
                fh.write(json.dumps(o, ensure_ascii=False) + "\n")
    CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"categorize: normalized {changed} fields across {len(files)} files; cache has {len(cache)} labels")


if __name__ == "__main__":
    main()
