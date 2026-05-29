#!/usr/bin/env python3
"""Run the UMQF edge-case suite: plug each case's args into umqf, compare to expected.

A case PASSES when |actual - expected| <= tolerance. Cases marked "known_gap": true
are expected to fail today and document a formula gap to fix -- per the test
philosophy, a failing test means the formula (or the expectation) needs work.
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

passed = real_fail = gap_fail = 0
print(f"UMQF edge-case suite -- {len(cases)} cases")
print("=" * 72)
for c in cases:
    a = c["args"]
    base = umqf.umq_base(a["dOS"], a["VSA"], a["Tc"], a["Vc"], a["dSc"], a.get("T", 0.0))
    actual = umqf.umq_final(base, a.get("Rp", 1.0), a.get("In", 1.0))
    exp = c["expected"]["umq_final"]
    tol = c["expected"].get("tolerance", 0.05)
    ok = abs(actual - exp) <= tol
    gap = c.get("known_gap", False)
    tag = "PASS" if ok else ("GAP " if gap else "FAIL")
    print(f"[{tag}] {c['id']}")
    print(f"       actual={actual:+.3f}  expected={exp:+.3f}  (tol {tol})  -- {c['expected']['label']}")
    if not ok:
        print(f"       {c['expected']['reasoning']}")
    if ok:
        passed += 1
    elif gap:
        gap_fail += 1
    else:
        real_fail += 1
print("=" * 72)
print(f"{passed} passed, {gap_fail} known-gap (expected fail), {real_fail} unexpected fail")
sys.exit(1 if real_fail else 0)
