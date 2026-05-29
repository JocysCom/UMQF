#!/usr/bin/env python3
"""categorize_ai.py - normalize / (re)categorize observations and backfill diversity tags.

Collection-time research agents assign harm_type, intent, and (in newer rounds) legal_tradition.
This pass keeps the corpus consistent and backfills, for universality bookkeeping:
  - validates enum values (harm_type, intent),
  - backfills a default harm_magnitude per harm_type when missing,
  - backfills legal_tradition from the jurisdiction when missing (so the whole corpus is countable),
  - defaults entity_type to "human",
  - maintains a label->harm_type cache for stable re-runs.

Universality note: the formula aims to be universal across value systems (and, in principle, life
forms). legal_tradition lets sampling_adequacy.py count INDEPENDENT traditions, not just
jurisdictions - distant, independent systems agreeing is the real test of a universal rate.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gcu import to_gcu

DATA = Path(__file__).resolve().parents[1]
OBS = DATA / "observations"
CACHE = Path(__file__).resolve().parent / "categorize_cache.json"

HARM_TYPES = {"death", "bodily", "suffering", "liberty", "property", "psychological", "mixed", "anchor"}
INTENTS = {"intentional", "reckless", "negligent", "accidental", "na"}
DEFAULT_MAG = {"death": 1.0, "bodily": 0.2, "suffering": 0.3, "liberty": 0.1,
               "property": 0.05, "psychological": 0.2, "mixed": 0.3, "anchor": None}

TRADITION = {
    "common_law": {"us", "uk", "england", "england and wales", "england & wales", "wales",
                   "scotland", "canada", "australia", "ireland", "new zealand", "nz", "india"},
    "civil_law": {"germany", "france", "netherlands", "sweden", "japan", "spain", "finland",
                  "denmark", "norway", "switzerland", "brazil", "italy", "south korea", "korea",
                  "mexico", "russia", "indonesia", "chile", "thailand"},
    "islamic_law": {"saudi arabia", "iran", "uae", "united arab emirates", "pakistan", "qatar",
                    "kuwait", "egypt"},
    "chinese_socialist": {"china"},
}
INTERNATIONAL = {"global", "eu", "european union", "international", "who", "oecd"}


def tradition_of(j):
    if not j:
        return None
    s = str(j).strip().lower()
    if s.startswith("us-") or s.startswith("us "):
        return "common_law"
    if s in INTERNATIONAL:
        return "international"
    for trad, names in TRADITION.items():
        if s in names:
            return trad
    for trad, names in TRADITION.items():
        if any(n in s for n in names):
            return trad
    return "other"


SRC_CONSTRUCT = {
    "vsl": "wtp", "vsl_intl": "wtp", "vsl_diverse": "wtp",
    "diyya_blood_money": "compensation", "vsl_wrongful_death": "compensation",
    "tort_pain_suffering": "compensation", "workers_comp": "compensation",
    "historical_codes": "compensation", "qaly": "budget", "qaly_intl": "budget",
}


def construct_of(o):
    """What a money figure measures: willingness-to-pay vs make-whole compensation vs budget threshold."""
    s = ((o.get("summary") or "") + " " + (o.get("label_raw") or "")).lower()
    if any(k in s for k in ("statistical life", "vsl", "willingness", "value of preventing", "vpf")):
        return "wtp"
    if any(k in s for k in ("diyya", "blood money", "wergild", "wrongful death", "wrongful-death", "compensation", "settlement", "qisas", "damages")):
        return "compensation"
    return SRC_CONSTRUCT.get(o.get("source"))


def main():
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    changed = 0
    files = sorted(OBS.glob("*.jsonl"))
    for f in files:
        rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        for o in rows:
            if o.get("harm_type") not in HARM_TYPES:
                o["harm_type"] = "mixed"; changed += 1
            if o.get("intent") not in INTENTS:
                o["intent"] = "na"; changed += 1
            if o.get("harm_magnitude") in (None, "") and o["harm_type"] != "anchor":
                o["harm_magnitude"] = DEFAULT_MAG.get(o["harm_type"]); changed += 1
            if not o.get("legal_tradition"):
                o["legal_tradition"] = tradition_of(o.get("jurisdiction")); changed += 1
            if not o.get("construct"):
                o["construct"] = construct_of(o); changed += 1
            usd = o.get("money_value_usd2024")
            if usd is not None and o.get("money_value_gcu") is None:
                g = to_gcu(usd, o.get("jurisdiction"))
                if g is not None:
                    o["money_value_gcu"] = round(g, 5); changed += 1
            if not o.get("entity_type"):
                o["entity_type"] = "human"
            cache[o.get("label_raw") or o["id"]] = o["harm_type"]
        with open(f, "w", encoding="utf-8") as fh:
            for o in rows:
                fh.write(json.dumps(o, ensure_ascii=False) + "\n")
    CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"categorize: normalized/backfilled {changed} fields across {len(files)} files; cache has {len(cache)} labels")


if __name__ == "__main__":
    main()
