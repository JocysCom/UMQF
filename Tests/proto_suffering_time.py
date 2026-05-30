#!/usr/bin/env python3
"""PROTOTYPE — NOT the current formula, and NOT wired into run_tests.py.

Explores the open issue (see data/README.md, "Suffering needs its own term"):
UMQF's ΔSc only *multiplies* the ΔOS term, so an action that causes suffering but no
change in survival odds (ΔOS = 0 — e.g. torturing an immortal, or a victim who fully
recovers) scores 0. Pure suffering is invisible.

Proposed survival-grounded fix — count a stretch of suffering as degraded survival-time:

    suffering_harm = -ΔSc × VSA × (time_suffering ÷ entity_lifespan)

Weighted by the entity's OWN lifespan, so torture is always some negative but a
near-zero blip for an immortal. Run this to see the numbers; nothing here touches
UMQF.md or the main test suite.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def suffering_harm(dSc, VSA, time_suffering, lifespan):
    return -dSc * VSA * (time_suffering / lifespan)


SCENARIOS = [
    # label,                          dSc,  VSA,  time, lifespan (same unit as time)
    ("immortal tortured 1 yr",        0.80, 0.95, 1.0,  1e9),    # ~infinite lifespan
    ("human tortured 1 yr",           0.80, 0.58, 1.0,  80.0),
    ("human tortured 10 yr",          0.80, 0.58, 10.0, 80.0),
    ("human, mild distress 1 yr",     0.20, 0.58, 1.0,  80.0),
    ("mayfly tortured 1/2 its life",  0.80, 0.05, 0.5,  1.0),
]

print("PROTOTYPE: suffering as degraded survival-time (NOT the current formula)")
print("=" * 74)
print(f"{'scenario':32} {'dSc':>5} {'VSA':>5} {'time/life':>10} {'harm':>11}")
print("-" * 74)
for label, dSc, VSA, t, life in SCENARIOS:
    print(f"{label:32} {dSc:5.2f} {VSA:5.2f} {t / life:10.4g} {suffering_harm(dSc, VSA, t, life):11.4g}")
print("=" * 74)
print("immortal -> ~0 (blip); finite lives -> real negative, scaled by the fraction")
print("of their OWN life spent suffering. How to combine this added term with the")
print("existing (1 - sign*dSc) death-amplifier is the open question (data/README.md).")
