#!/usr/bin/env python3
"""Run the UMQF edge-case suite: plug each case's args into umqf, compare to expected.

A case PASSES when |actual - expected| <= tolerance. A failing test means the formula
(or the test's expectation) needs revisiting.
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # print ΔSc etc. on cp1252 consoles

sys.path.insert(0, str(Path(__file__).resolve().parent))
import umqf

HERE = Path(__file__).resolve().parent
cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))

passed = failed = 0
print(f"UMQF edge-case suite -- {len(cases)} cases")
print("=" * 72)
for c in cases:
    a = c["args"]
    base = umqf.umq_base(a["dOS"], a["VSA"], a["Tc"], a["Vc"], a["dSc"])
    actual = umqf.umq_final(base, a.get("Rp", 1.0), a.get("In", 1.0))
    exp = c["expected"]["umq_final"]
    tol = c["expected"].get("tolerance", 0.05)
    ok = abs(actual - exp) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {c['id']}")
    print(f"       actual={actual:+.3f}  expected={exp:+.3f}  (tol {tol})  -- {c['expected']['label']}")
    if not ok:
        print(f"       {c['expected']['reasoning']}")
    passed += ok
    failed += not ok
print("=" * 72)
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
