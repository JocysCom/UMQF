#!/usr/bin/env python3
"""download.py - (re)register / refresh raw sources listed in config.json.

Phase 1 uses curated structured figures (data/raw/seed.jsonl) plus research-agent collector
output (data/raw/collected.json). This script records the canonical source URLs to
data/raw/sources_manifest.json and is the place to add real fetchers as the corpus grows:
  - Phase 2: USSC individual-offender datafiles (SPSS/SAS) -> parse into observations
  - Phase 3: CourtListener bulk opinions (CSV) -> NLP-extract (harm, penalty) pairs
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent
CONFIG = HERE / "config.json"


def main():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    manifest = []
    for s in cfg.get("sources", []):
        manifest.append({"key": s["key"], "title": s["title"], "url": s.get("url"),
                         "fetch": s.get("fetch", "manual/curated"), "informs": s.get("informs", [])})
        print(f"  {s['key']:20s} {s.get('fetch','manual'):9s} {s.get('url','')}")
    (DATA / "raw" / "sources_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"download: {len(manifest)} sources registered -> data/raw/sources_manifest.json")
    print("Phase 1 figures are curated in seed.jsonl + agent-collected in collected.json.")
    print("Add real fetchers here for Phase 2 (USSC datafiles) / Phase 3 (CourtListener bulk).")


if __name__ == "__main__":
    main()
