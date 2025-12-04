# Universal Formulas & Distributions in Nature

A collection of the most prevalent mathematical patterns found in the universe and nature. These formulas are simplified for 2D plotting ($y = f(x)$), accepting one main variable ($x$) and optionally one static parameter.

## 1. Normal Distribution (Gaussian)
**"The Bell Curve"**

*   **Context:** Found in natural variations where many small, independent factors contribute to a result. Examples include IQ scores, human height, measurement errors, and blood pressure.
*   **Formula:**
    $$y = e^{-\frac{x^2}{2s^2}}$$
*   **Variables:**
    *   $x$: Deviation from the average (mean).
    *   $s$ (static): Standard deviation (controls the width of the bell).

## 2. Power Law (Pareto Distribution)
**"The Long Tail" / "Fractal Geometry"**

*   **Context:** Describes systems where a small number of items account for a large proportion of the impact. Examples include leaf venation structures, city populations (Zipf's Law), wealth distribution, earthquake magnitudes, and moon craters.
*   **Formula:**
    $$y = x^{-k}$$
*   **Variables:**
    *   $x$: Rank or size.
    *   $k$ (static): Scaling exponent (typically between 1 and 3).

## 3. Exponential Decay
**"The Natural Decline"**

*   **Context:** Describes processes that reduce at a rate proportional to their current value. Examples include radioactive decay, atmospheric pressure at altitude, capacitor discharge, and Newton's law of cooling.
*   **Formula:**
    $$y = e^{-kx}$$
*   **Variables:**
    *   $x$: Time or distance.
    *   $k$ (static): Decay constant (rate of decline).

## 4. Logistic Growth (Sigmoid)
**"The S-Curve"**

*   **Context:** Describes growth that accelerates initially but slows down as it approaches a limit (carrying capacity). Examples include population growth in a finite environment, spread of rumors/viruses, and enzyme kinetics.
*   **Formula:**
    $$y = \frac{1}{1 + e^{-kx}}$$
*   **Variables:**
    *   $x$: Time.
    *   $k$ (static): Steepness of the curve (growth rate).

## 5. Inverse Square Law
**"Field Intensity"**

*   **Context:** Fundamental physics law describing how radiation or forces spread out from a point source. Examples include gravity, electrostatic force, light intensity, and sound intensity.
*   **Formula:**
    $$y = \frac{1}{x^2}$$
*   **Variables:**
    *   $x$: Distance from the source.
    *   *(No static variable required, though a source strength constant $C$ can be added as a multiplier).*