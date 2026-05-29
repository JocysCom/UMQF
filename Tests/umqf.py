#!/usr/bin/env python3
"""Reference implementation of the UMQF Base / Final moral quotient.

The single source of truth for the formula is UMQF.md (repo root); this module
mirrors it so edge cases can be checked numerically. Keep it in sync with UMQF.md.

    UMQ_base(a,e) = ΔOS·VSA·Tc·(1 − sign(ΔOS)·Vc)·(1 − sign(ΔOS)·ΔSc)
    UMQ_final     = UMQ_base · Rp · In

ΔSc (suffering coefficient) is the *change* in physically-manifested suffering the
action causes the entity, measured against its pre-existing suffering. Its lower
bound is the Treatability parameter T:

    ΔSc ∈ [T, +1],   T ∈ [-1, 0]   (T = -(irremediable fraction); default T = 0)

So relief (a negative ΔSc) is admissible only down to T. T = 0 (treatable, the
default) means no relief credit; T = -1 (fully irremediable) allows full relief.

The per-entity result is clamped to [-4, +1]: harm is amplified (down to -4), good
is capped (+1), so relief can neutralize a harm but never super-charge a good.
"""


def sign(x):
    return -1.0 if x < 0 else (1.0 if x > 0 else 0.0)


def umq_base(dOS, VSA, Tc, Vc, dSc, T=0.0, clamp=True):
    """Per-entity UMQ_base. dSc is the raw ΔSc; T is Treatability in [-1, 0]."""
    if not -1.0 <= T <= 0.0:
        raise ValueError(f"T (treatability) must be in [-1, 0], got {T}")
    eff_dSc = min(1.0, max(T, dSc))          # ΔSc bounded to [T, +1]
    s = sign(dOS)
    vc_factor = 1.0 - s * Vc
    sc_factor = 1.0 - s * eff_dSc
    base = dOS * VSA * Tc * vc_factor * sc_factor
    return max(-4.0, min(1.0, base)) if clamp else base


def umq_final(base, Rp=1.0, In=1.0):
    """UMQ_final = UMQ_base · Rp · In (Rp, In ∈ [0, 1])."""
    return base * Rp * In
