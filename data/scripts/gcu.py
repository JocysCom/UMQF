#!/usr/bin/env python3
"""gcu.py - normalize money to Global Currency Units (GCU) so exchange rates are income-invariant.

1 GCU = one average human's LIFETIME RESOURCE THROUGHPUT (production ~ consumption), approximated
per jurisdiction as GDP-per-capita x life-expectancy. Money must pass through GCU before converting
to life/welfare: $1 is trivial to a rich economy but life-threatening to a poor one. Dividing by
local lifetime throughput strips that income dependence out - which is what makes the life<->money
rate universal (VSL is ~constant in GCU even though it spans ~30x in absolute USD).

GCU is the MONEY HUB: usd -> GCU -> (life | welfare). Each other value type has its own normalizer
(life = fraction of remaining lifespan; welfare = quality-adjusted life-year).
"""
import json
from pathlib import Path

CONFIG = Path(__file__).resolve().parent / "config.json"
_CFG = json.loads(CONFIG.read_text(encoding="utf-8"))
_TABLE = _CFG.get("gcu_usd_by_jurisdiction", {})
_DEFAULT = _CFG.get("gcu_usd_default", 950000)


def gcu_usd(jurisdiction):
    """USD value of 1 GCU in the given jurisdiction (lifetime throughput). Falls back to world avg."""
    if not jurisdiction:
        return _DEFAULT
    s = str(jurisdiction).strip().lower()
    for key, val in _TABLE.items():
        if s == key.lower():
            return val
    if s.startswith("us-") or s.startswith("us "):
        return _TABLE.get("US", _DEFAULT)
    for key, val in _TABLE.items():
        if key.lower() in s or s.startswith(key.lower()):
            return val
    return _DEFAULT


def to_gcu(usd, jurisdiction):
    if usd is None:
        return None
    g = gcu_usd(jurisdiction)
    return usd / g if g else None
