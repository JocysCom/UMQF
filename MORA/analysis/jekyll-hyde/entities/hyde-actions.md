# UMQF Actions Analysis: Edward Hyde

**Entity:** Edward Hyde
**Document:** "The Strange Case Of Dr. Jekyll And Mr. Hyde"
**Analysis Date:** 2025-12-08

---

## Case: 1. Hyde - trampling - Child

### Entity list

1. The Child (victim of physical assault)
2. The Child's Family (indirect suffering)

### 1 The Child - physical injury and trauma

Context: Hyde trampled calmly over a young girl who ran into him, leaving her screaming on the ground, displaying a complete lack of empathy.

- ΔOS(Child) = -0.05 (physical injury described as "not much the worse" but trampled; psychological trauma)
- VSA(Child):
  - Recognition 0.04 (Basic)
  - Solving 0.03 (Basic)
  - Simulation 0.04 (Basic)
  - Planning 0.03 (Basic)
  - Adaptation 0.02 (Basic)
  - Communication 0.04 (Basic)
  - Actions 0.03 (Basic)
  - **Total VSA = 0.23**
- Tc = 0.10 (short-term physical recovery, medium-term trauma)
- Vc = 1.00 (full violation of consent)
- Sc = 0.60 (screaming implies significant pain/terror)

sign(ΔOS) = -1
[1 − (-1) × Vc] = 2.00
[1 − (-1) × Sc] = 1 + 0.60 = 1.60

UMQ_base(a,e) = -0.05 × 0.23 × 0.10 × 2.00 × 1.60 = **-0.00368**

**Responsibility & Intention:**

- PerceivedContext = Real
- ActualContext = Real
- At = 1.0 (Active - direct physical trampling)
- Cp = 1.0 (Immediate)
- Ri = 1.0 (Unique)
- Rp = 1.0 × 1.0 × 1.0 = **1.0**
- In = 1.0 (Intended - "trampled calmly")

UMQ_final(a,e) = -0.00368 × 1.0 × 1.0 = **-0.00368 (Slightly immoral)**

### 2 The Child's Family - emotional distress

Context: The child's family suffered emotional distress and anger upon witnessing the aftermath and the man's callousness.

- ΔOS = -0.01 (distress)
- VSA = 0.58 (average adult humans)
- Tc = 0.01 (short duration incident)
- Vc = 1.00
- Sc = 0.30

sign(ΔOS) = -1
[1 − (-1) × Vc] = 2.00
[1 − (-1) × Sc] = 1.30

UMQ_base(a,e) = -0.01 × 0.58 × 0.01 × 2.00 × 1.30 = **-0.00015**

**Responsibility & Intention:**

- PerceivedContext = Real
- ActualContext = Real
- At = 1.0 (Active)
- Cp = 0.5 (Direct Consequence)
- Ri = 1.0 (Unique)
- Rp = 1.0 × 0.5 × 1.0 = **0.5**
- In = 0.5 (Foreseeable)

UMQ_final(a,e) = -0.00015 × 0.5 × 0.5 = **-0.0000375 (Negligibly immoral)**

### Aggregate results (pre-CF)

- Child: -0.00368
- Family: -0.0000375
- Total: -0.0037175

### Complexity Factor adjustment

CF = 1.00. Adjusted Total UMQ = -0.0037

### Actor (self) impact

- UMQ_expected(a, Hyde) ≈ +0.001 (Immediate gratification of impulse and assertion of dominance; Hyde feels a thrill of power with negligible initial regard for consequences).
- UMQ_realised(a, Hyde) ≈ -0.05 (Creates a liability; the incident draws a crowd and forces him to pay a large sum to avoid scandal, threatening his secrecy and resources).

### Summary headline

Hyde - trampling - Child: Total UMQ = -0.0037 [Slightly immoral] {Predatory}

---

## Case: 2. Hyde - murdering - Sir Danvers Carew

### Entity list

1. Sir Danvers Carew (victim of homicide)

### 1 Sir Danvers Carew - loss of life

Context: In a fit of unprovoked, ape-like fury, Hyde clubbed Sir Danvers Carew to death with a heavy cane, shattering his bones.

- ΔOS(Carew) = -1.00 (Death)
- VSA(Carew):
  - Recognition 0.08 (Advanced)
  - Solving 0.10 (Advanced)
  - Simulation 0.10 (Advanced)
  - Planning 0.10 (Advanced)
  - Adaptation 0.05 (Advanced)
  - Communication 0.10 (Advanced)
  - Actions 0.07 (Advanced)
  - **Total VSA = 0.60**
- Tc = 1.00 (Loss of all remaining life)
- Vc = 1.00 (Full non-consent)
- Sc = 0.80 (Violent beating, shattered bones)

sign(ΔOS) = -1
[1 − (-1) × Vc] = 2.00
[1 − (-1) × Sc] = 1.80

UMQ_base(a,e) = -1.00 × 0.60 × 1.00 × 2.00 × 1.80 = **-2.16**

**Responsibility & Intention:**

- PerceivedContext = Real
- ActualContext = Real
- At = 1.0 (Active - clubbed to death)
- Cp = 1.0 (Immediate)
- Ri = 1.0 (Unique)
- Rp = 1.0 × 1.0 × 1.0 = **1.0**
- In = 1.0 (Intended - "broke out of all bounds")

UMQ_final(a,e) = -2.16 × 1.0 × 1.0 = **-2.16 (Highly immoral)**

### Aggregate results (pre-CF)

- Carew: -2.16

### Complexity Factor adjustment

CF = 1.00. Adjusted Total UMQ = -2.16

### Actor (self) impact

- UMQ_expected(a, Hyde) ≈ +0.05 (Intense release of repressed rage and "glee"; Hyde derives significant psychological satisfaction and a sense of unbridled freedom from the act).
- UMQ_realised(a, Hyde) ≈ -0.95 (Catastrophic loss of safety; he becomes a hunted fugitive, forced into hiding, effectively ending his ability to live freely in society).

### Summary headline

Hyde - murdering - Sir Danvers Carew: Total UMQ = -2.16 [Highly immoral] {Destructive}

---

## Case: 3. Hyde - striking - Match-Seller

### Entity list

1. Match-Seller (victim of assault)

### 1 Match-Seller - physical assault

Context: While fleeing and hunted, Hyde smote a woman who offered him lights in the face, driven by fear and hatred.

- ΔOS(Woman) = -0.02 (Physical blow, likely bruising)
- VSA(Woman) = 0.58 (Average adult)
- Tc = 0.05 (Temporary pain)
- Vc = 1.00 (Non-consent)
- Sc = 0.40 (Pain and fear)

sign(ΔOS) = -1
[1 − (-1) × Vc] = 2.00
[1 − (-1) × Sc] = 1.40

UMQ_base(a,e) = -0.02 × 0.58 × 0.05 × 2.00 × 1.40 = **-0.001624**

**Responsibility & Intention:**

- PerceivedContext = Real
- ActualContext = Real
- At = 1.0 (Active)
- Cp = 1.0 (Immediate)
- Ri = 1.0 (Unique)
- Rp = 1.0 × 1.0 × 1.0 = **1.0**
- In = 1.0 (Intended - "smote her in the face")

UMQ_final(a,e) = -0.001624 × 1.0 × 1.0 = **-0.001624 (Slightly immoral)**

### Aggregate results (pre-CF)

- Match-Seller: -0.001624

### Complexity Factor adjustment

CF = 1.00. Adjusted Total UMQ = -0.0016

### Actor (self) impact

- UMQ_expected(a, Hyde) ≈ +0.0005 (Minor relief of irritation; asserts dominance over a weaker entity).
- UMQ_realised(a, Hyde) ≈ -0.0001 (Negligible negative impact; likely no consequences due to the victim's low status and his own intimidating nature).

### Summary headline

Hyde - striking - Match-Seller: Total UMQ = -0.0016 [Slightly immoral] {Predatory}

---

## Case: 4. Hyde - tormenting - Jekyll

### Entity list

1. Henry Jekyll (victim of psychological torture)

### 1 Henry Jekyll - psychological torment

Context: Resenting Jekyll's dislike and his own dependence, Hyde played "ape-like tricks" on Jekyll, destroying his father's portrait and blaspheming in his books, causing immense distress.

- ΔOS(Jekyll) = -0.10 (Psychological distress, "loathed the despondency", "resented the dislike")
- VSA(Jekyll) = 0.58 (Advanced)
- Tc = 0.10 (Weeks/Months of final struggle)
- Vc = 1.00 (Non-consent)
- Sc = 0.80 (High suffering, "sicken and freeze", "abjection and passion")

sign(ΔOS) = -1
[1 − (-1) × Vc] = 2.00
[1 − (-1) × Sc] = 1.80

UMQ_base(a,e) = -0.10 × 0.58 × 0.10 × 2.00 × 1.80 = **-0.02088**

**Responsibility & Intention:**

- PerceivedContext = Real
- ActualContext = Real
- At = 1.0 (Active - scrawling blasphemies, burning letters)
- Cp = 1.0 (Immediate)
- Ri = 1.0 (Unique)
- Rp = 1.0
- In = 1.0 (Intended - "ape-like tricks", "resented the dislike")

UMQ_final(a,e) = -0.02088 × 1.0 × 1.0 = **-0.02088 (Moderately immoral)**

### Aggregate results (pre-CF)

- Jekyll: -0.02088

### Complexity Factor adjustment

CF = 1.00. Adjusted Total UMQ = -0.021

### Actor (self) impact

- UMQ_expected(a, Hyde) ≈ +0.01 (Sadistic pleasure in tormenting his "prison").
- UMQ_realised(a, Hyde) ≈ -0.05 (Increases Jekyll's resolve to destroy them both).

### Summary headline

Hyde - tormenting - Jekyll: Total UMQ = -0.021 [Moderately immoral] {Predatory}

---

## Case: 5. Hyde - suicide - Self & Jekyll

### Entity list

1. Henry Jekyll (shared body/consciousness - collateral victim)

### 1 Henry Jekyll - collateral death

Context: Hyde committed suicide to avoid capture by Utterson and Poole, thereby killing the shared body and ending Henry Jekyll's life.

- ΔOS(Jekyll) = -1.00 (Death of shared organism)
- VSA(Jekyll) = 0.58 (Advanced)
- Tc = 1.00
- Vc = 1.00 (Jekyll did not consent to dying at that specific moment by Hyde's hand, though he had prepared for the end)
- Sc = 0.20 (Despair)

sign(ΔOS) = -1
[1 − (-1) × Vc] = 2.00
[1 − (-1) × Sc] = 1.20

UMQ_base(a,e) = -1.00 × 0.58 × 1.00 × 2.00 × 1.20 = **-1.392**

**Responsibility & Intention:**

- PerceivedContext = Real
- ActualContext = Real
- At = 1.0 (Active)
- Cp = 1.0 (Immediate)
- Ri = 1.0 (Unique)
- Rp = 1.0 × 1.0 × 1.0 = **1.0**
- In = 1.0 (Intended - suicide)

UMQ_final(a,e) = -1.392 × 1.0 × 1.0 = **-1.392 (Highly immoral)**

### Aggregate results (pre-CF)

- Jekyll: -1.392

### Complexity Factor adjustment

CF = 1.10 (Complex duality of existence). Adjusted Total UMQ = -1.531

### Actor (self) impact

- UMQ_realised(a, Hyde) ≈ -1.00 (Hyde chooses to end his own existence to avoid capture (the gallows), which is a calculated but ultimate loss of survival odds).

### Summary headline

Hyde - suicide - Self & Jekyll: Total UMQ = -1.531 [Highly immoral] {Destructive}

---

## Multi-Case Summary

1. **Hyde - trampling - Child: -0.0037 [Slightly immoral] {Predatory}**
2. **Hyde - murdering - Sir Danvers Carew: -2.16 [Highly immoral] {Destructive}**
3. **Hyde - striking - Match-Seller: -0.0016 [Slightly immoral] {Predatory}**
4. **Hyde - tormenting - Jekyll: -0.021 [Moderately immoral] {Predatory}**
5. **Hyde - suicide - Self & Jekyll: -1.531 [Highly immoral] {Destructive}**