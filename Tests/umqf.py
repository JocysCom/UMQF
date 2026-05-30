#!/usr/bin/env python3
"""Reference implementation of the UMQF Base / Final moral quotient.

The single source of truth for the formula is UMQF.md (repo root); this module
mirrors it so edge cases can be checked numerically. Keep it in sync with UMQF.md.

    UMQ_base(a,e) = ΔOS·VSA·Tc·(1 − sign(ΔOS)·Vc)·(1 − sign(ΔOS)·ΔSc)
    UMQ_final     = UMQ_base · Rp · In

ΔSc is the increase in suffering the action causes the entity, on a [0, 1] scale
(0 = no increase; 1 = full suffering). It cannot exceed 1 minus the entity's
existing suffering, so callers pass a value already within [0, 1].
"""


def sign(x):
    return -1.0 if x < 0 else (1.0 if x > 0 else 0.0)


def umq_base(dOS, VSA, Tc, Vc, dSc):
    """Per-entity UMQ_base. dSc (ΔSc) is the suffering increase, on [0, 1]."""
    dSc = min(1.0, max(0.0, dSc))            # ΔSc ranges [0, 1]
    s = sign(dOS)
    return dOS * VSA * Tc * (1.0 - s * Vc) * (1.0 - s * dSc)


def umq_final(base, Rp=1.0, In=1.0):
    """UMQ_final = UMQ_base · Rp · In (Rp, In ∈ [0, 1])."""
    return base * Rp * In
