# Abraham Lincoln - Actions Log

### Entity list

1.  **Slaves in Rebellious States** (Group: ~3,500,000) - Primary beneficiaries of Emancipation.
2.  **Slave Owners in Rebellious States** (Group: ~400,000) - Primary victims of property loss.
3.  **US Population (1861)** (Group: ~31,000,000) - Affected by war and peace decisions.
4.  **Civil War Dead** (Group: ~620,000) - Victims of the war initiated/accepted.
5.  **Cabinet Members** (Group: 7) - Seward, Chase, Bates, etc.
6.  **Slaves in Border States** (Group: ~425,000) - Affected by revocation of Frémont's order.
7.  **Union Army** (Group: ~2,000,000) - Affected by leadership choices.
8.  **All Slaves** (Group: ~4,000,000) - Beneficiaries of 13th Amendment.

### 1 Abraham Lincoln - Emancipation Proclamation - Slaves & Owners

**Context:** Lincoln issued the Emancipation Proclamation, declaring all slaves in rebellious states free as of January 1, 1863. This was a military necessity and a moral imperative.

**1 Slaves in Rebellious States**
*   ΔOS = +0.80 (Transition from chattel slavery to potential freedom; massive survival odds increase)
*   VSA = 0.58 (Average Human)
*   Tc = 1.00 (Permanent change)
*   Vc = 0.00 (Full consent)
*   Sc = 0.00 (Relief of suffering)

UMQ_base(a,e) = +0.80 × 0.58 × 1.00 × 1.0 × 1.0 = **+0.464**

**Responsibility & Intention:**
*   PerceivedContext = Real
*   ActualContext = Real
*   At = 0.9 (Passive/Authoritative - Executive Order)
*   Cp = 1.0 (Immediate legal effect)
*   Ri = 1.0 (Unique - Only President could do this)
*   Rp = 0.9 × 1.0 × 1.0 = **0.9**
*   In = 1.0 (Intended)

UMQ_final(a,e) = +0.464 × 0.9 × 1.0 = **+0.4176**
Group Total (3.5M) = +0.4176 × 3,500,000 = **+1,461,600.0**

**2 Slave Owners**
*   ΔOS = -0.20 (Significant economic resource shock; loss of "property")
*   VSA = 0.58
*   Tc = 1.00 (Permanent)
*   Vc = 1.00 (Full violation of will)
*   Sc = 0.50 (Economic and social distress)

sign(ΔOS) = -1
[1 - (-1) × Vc] = 2.0
[1 - (-1) × Sc] = 1.5

UMQ_base(a,e) = -0.20 × 0.58 × 1.00 × 2.0 × 1.5 = **-0.348**

**Responsibility & Intention:**
*   Rp = 0.9 (Executive Order)
*   In = 1.0 (Intended)

UMQ_final(a,e) = -0.348 × 0.9 × 1.0 = **-0.3132**
Group Total (400k) = -0.3132 × 400,000 = **-125,280.0**

**Aggregate results (pre-CF):**
*   Slaves: +1,461,600.0
*   Owners: -125,280.0
*   **Total:** +1,336,320.0

**Complexity Factor adjustment:**
CF = 1.1 (High complexity, war time, uncertain enforcement)
Adjusted Total = +1,470,000 (rounded)

**Actor (self) impact:**
Lincoln risked political suicide and alienation of border states, but secured his legacy.
UMQ_self = +0.5 (Legacy/Moral standing)

**Summary headline:**
Abraham Lincoln - Emancipation Proclamation - Slaves: Total UMQ = +1,470,000 [Extremely moral] {Synergistic}

### 2 Abraham Lincoln - Resupplying Fort Sumter - Nation & Soldiers

**Context:** Lincoln decided to resupply Fort Sumter, knowing it would likely provoke the South to fire the first shot, starting the Civil War.

**1 Civil War Dead (Soldiers)**
*   ΔOS = -1.00 (Death)
*   VSA = 0.58
*   Tc = 1.00
*   Vc = 0.50 (Volunteers consented to risk, draftees did not; mixed)
*   Sc = 1.00 (Death in battle/disease)

sign(ΔOS) = -1
[1 - (-1) × Vc] = 1.5
[1 - (-1) × Sc] = 2.0

UMQ_base(a,e) = -1.00 × 0.58 × 1.00 × 1.5 × 2.0 = **-1.74**

**Responsibility & Intention:**
*   PerceivedContext = Real
*   ActualContext = Real
*   At = 0.9 (Authoritative command)
*   Cp = 0.5 (Direct Consequence - provoked the war, but South fired)
*   Ri = 1.0 (Unique decision)
*   Rp = 0.9 × 0.5 × 1.0 = **0.45**
*   In = 0.5 (Foreseeable - War was likely, though not the specific death count)

UMQ_final(a,e) = -1.74 × 0.45 × 0.5 = **-0.3915**
Group Total (620k) = -0.3915 × 620,000 = **-242,730.0**

**2 US Population (Preservation of Union)**
*   ΔOS = +0.20 (Preservation of nation/democracy vs fragmentation)
*   VSA = 0.58
*   Tc = 1.00 (Long term benefit)
*   Vc = 0.00
*   Sc = 0.00

UMQ_base(a,e) = +0.20 × 0.58 × 1.00 = **+0.116**

**Responsibility & Intention:**
*   Rp = 0.45
*   In = 1.0 (Intended to save Union)

UMQ_final(a,e) = +0.116 × 0.45 × 1.0 = **+0.0522**
Group Total (31M) = +0.0522 × 31,000,000 = **+1,618,200.0**

**Aggregate results (pre-CF):**
*   Dead: -242,730.0
*   Population: +1,618,200.0
*   **Total:** +1,375,470.0

**Complexity Factor adjustment:**
CF = 1.2 (Extreme complexity and uncertainty of war)
Adjusted Total = +1,650,000 (rounded)

**Actor (self) impact:**
Immense personal suffering and stress.
UMQ_self = -0.5

**Summary headline:**
Abraham Lincoln - Resupplying Sumter/War - Nation: Total UMQ = +1,650,000 [Extremely moral] {Synergistic}

### 3 Abraham Lincoln - Trent Affair Resolution - Nation

**Context:** Lincoln supported Seward's decision to release Mason and Slidell to avoid war with Britain.

**1 US Population**
*   ΔOS = +0.30 (Avoidance of disastrous two-front war)
*   VSA = 0.58
*   Tc = 1.00
*   Vc = 0.00
*   Sc = 0.00

UMQ_base(a,e) = +0.30 × 0.58 × 1.00 = **+0.174**

**Responsibility & Intention:**
*   PerceivedContext = Real
*   ActualContext = Real
*   At = 0.9
*   Cp = 1.0
*   Ri = 1.0
*   Rp = 0.9
*   In = 1.0

UMQ_final(a,e) = +0.174 × 0.9 × 1.0 = **+0.1566**
Group Total (31M) = +0.1566 × 31,000,000 = **+4,854,600.0**

**Aggregate results (pre-CF):**
*   Population: +4,854,600.0

**Complexity Factor adjustment:**
CF = 1.0
Adjusted Total = +4,854,600

**Actor (self) impact:**
Swallowed pride, accepted political criticism.
UMQ_self = -0.1

**Summary headline:**
Abraham Lincoln - Trent Affair - Nation: Total UMQ = +4,854,600 [Extremely moral] {Synergistic}

### 4 Abraham Lincoln - Cabinet Appointments - Rivals

**Context:** Lincoln appointed his chief rivals (Seward, Chase, Bates) to the Cabinet to unify the party and country.

**1 Cabinet Members (7)**
*   ΔOS = +0.10 (Career peak, power)
*   VSA = 0.70 (High status)
*   Tc = 0.10 (4 years)
*   Vc = 0.00
*   Sc = 0.00

UMQ_base(a,e) = +0.10 × 0.70 × 0.10 = **+0.007**

**Responsibility & Intention:**
*   Rp = 1.0
*   In = 1.0

UMQ_final(a,e) = +0.007
Group Total (7) = +0.049

**2 US Population (Better Governance)**
*   ΔOS = +0.05 (Effective leadership)
*   VSA = 0.58
*   Tc = 0.10
*   UMQ_base = +0.0029
*   Rp = 1.0
*   In = 1.0
*   UMQ_final = +0.0029
*   Group Total (31M) = +89,900

**Aggregate results (pre-CF):**
*   Cabinet: +0.05
*   Population: +89,900
*   **Total:** +89,900

**Complexity Factor adjustment:**
CF = 1.0
Adjusted Total = +89,900

**Actor (self) impact:**
Created a difficult working environment for himself but secured his administration.
UMQ_self = +0.1

**Summary headline:**
Abraham Lincoln - Cabinet Appointments - Nation: Total UMQ = +89,900 [Highly moral] {Synergistic}

### 5 Abraham Lincoln - Revoking Frémont's Emancipation Order - Slaves & Border States

**Context:** Lincoln revoked General Frémont's order freeing slaves in Missouri to prevent the border states (especially Kentucky) from seceding, which he believed would lose the war.

**1 Slaves in Missouri (approx 115,000)**
*   ΔOS = -0.10 (Delayed freedom; continued bondage)
*   VSA = 0.58
*   Tc = 0.10 (Temporary delay until Emancipation Proclamation/13th Amendment)
*   Vc = 1.00 (Violation of will)
*   Sc = 0.20 (Continued suffering)

sign(ΔOS) = -1
[1 - (-1) × Vc] = 2.0
[1 - (-1) × Sc] = 1.2

UMQ_base(a,e) = -0.10 × 0.58 × 0.10 × 2.0 × 1.2 = **-0.01392**

**Responsibility & Intention:**
*   PerceivedContext = Real
*   ActualContext = Real
*   At = 0.9 (Executive Order)
*   Cp = 1.0 (Immediate)
*   Ri = 1.0 (Unique)
*   Rp = 0.9
*   In = 1.0 (Intended to revoke order, though motive was Union preservation)

UMQ_final(a,e) = -0.01392 × 0.9 × 1.0 = **-0.012528**
Group Total (115k) = -0.012528 × 115,000 = **-1,440.72**

**2 Border State Unionists (approx 2,000,000)**
*   ΔOS = +0.20 (Prevented secession, civil war in their states, potential Union defeat)
*   VSA = 0.58
*   Tc = 1.00
*   Vc = 0.00
*   Sc = 0.00

UMQ_base(a,e) = +0.20 × 0.58 × 1.00 = **+0.116**

**Responsibility & Intention:**
*   Rp = 0.9
*   In = 1.0

UMQ_final(a,e) = +0.116 × 0.9 × 1.0 = **+0.1044**
Group Total (2M) = +0.1044 × 2,000,000 = **+208,800.0**

**Aggregate results (pre-CF):**
*   Slaves: -1,440.72
*   Unionists: +208,800.0
*   **Total:** +207,359.28

**Complexity Factor adjustment:**
CF = 1.1 (High strategic complexity)
Adjusted Total = +228,095

**Actor (self) impact:**
Incurred wrath of radicals, but saved his strategy.
UMQ_self = +0.1

**Summary headline:**
Abraham Lincoln - Revoking Frémont's Order - Nation: Total UMQ = +228,095 [Highly moral] {Synergistic}

### 6 Abraham Lincoln - Appointment of Grant - Union Army

**Context:** After years of frustration with ineffective generals, Lincoln appointed Ulysses S. Grant as Lieutenant General, giving him command of all Union armies.

**1 Union Army (2,000,000)**
*   ΔOS = +0.20 (Competent leadership increased odds of victory and survival for the cause, though individual risk remained high)
*   VSA = 0.58
*   Tc = 1.00
*   Vc = 0.00
*   Sc = 0.00

UMQ_base(a,e) = +0.20 × 0.58 × 1.00 = **+0.116**

**Responsibility & Intention:**
*   PerceivedContext = Real
*   ActualContext = Real
*   At = 0.9 (Appointment)
*   Cp = 1.0
*   Ri = 1.0
*   Rp = 0.9
*   In = 1.0

UMQ_final(a,e) = +0.116 × 0.9 × 1.0 = **+0.1044**
Group Total (2M) = +0.1044 × 2,000,000 = **+208,800.0**

**Aggregate results (pre-CF):**
*   Union Army: +208,800.0

**Complexity Factor adjustment:**
CF = 1.0
Adjusted Total = +208,800

**Actor (self) impact:**
Relief from micromanaging the war; confidence in victory.
UMQ_self = +0.3

**Summary headline:**
Abraham Lincoln - Appointment of Grant - Union Army: Total UMQ = +208,800 [Highly moral] {Synergistic}

### 7 Abraham Lincoln - Lobbying for 13th Amendment - Slaves

**Context:** Lincoln used his full political power, including patronage and personal persuasion, to ensure the passage of the 13th Amendment in the House, permanently abolishing slavery.

**1 All Slaves (4,000,000)**
*   ΔOS = +1.00 (Permanent legal freedom; end of the institution)
*   VSA = 0.58
*   Tc = 1.00 (Permanent)
*   Vc = 0.00
*   Sc = 0.00

UMQ_base(a,e) = +1.00 × 0.58 × 1.00 = **+0.58**

**Responsibility & Intention:**
*   PerceivedContext = Real
*   ActualContext = Real
*   At = 1.0 (Active lobbying/influence)
*   Cp = 1.0
*   Ri = 1.0 (Crucial intervention)
*   Rp = 1.0
*   In = 1.0

UMQ_final(a,e) = +0.58 × 1.0 × 1.0 = **+0.58**
Group Total (4M) = +0.58 × 4,000,000 = **+2,320,000.0**

**Aggregate results (pre-CF):**
*   Slaves: +2,320,000.0

**Complexity Factor adjustment:**
CF = 1.0
Adjusted Total = +2,320,000

**Actor (self) impact:**
Fulfillment of his "greatest work."
UMQ_self = +0.5

**Summary headline:**
Abraham Lincoln - Lobbying for 13th Amendment - Slaves: Total UMQ = +2,320,000 [Extremely moral] {Synergistic}

### 8 Abraham Lincoln - Second Inaugural Address - Nation

**Context:** Lincoln delivered a speech calling for "malice toward none; with charity for all," setting a moral framework for reconciliation and healing the nation's wounds.

**1 US Population (31,000,000)**
*   ΔOS = +0.10 (Promoted healing, reduced future conflict risk, established moral peace)
*   VSA = 0.58
*   Tc = 1.00 (Long-term impact)
*   Vc = 0.00
*   Sc = 0.00

UMQ_base(a,e) = +0.10 × 0.58 × 1.00 = **+0.058**

**Responsibility & Intention:**
*   PerceivedContext = Real
*   ActualContext = Real
*   At = 1.0 (Active speech)
*   Cp = 1.0
*   Ri = 1.0
*   Rp = 1.0
*   In = 1.0

UMQ_final(a,e) = +0.058 × 1.0 × 1.0 = **+0.058**
Group Total (31M) = +0.058 × 31,000,000 = **+1,798,000.0**

**Aggregate results (pre-CF):**
*   Nation: +1,798,000.0

**Complexity Factor adjustment:**
CF = 1.0
Adjusted Total = +1,798,000

**Actor (self) impact:**
Cemented his legacy as a spiritual leader.
UMQ_self = +0.5

**Summary headline:**
Abraham Lincoln - Second Inaugural Address - Nation: Total UMQ = +1,798,000 [Extremely moral] {Synergistic}

### 9 Abraham Lincoln - Visit to Richmond - Freed Slaves

**Context:** Lincoln walked through the captured Confederate capital, demonstrating federal authority and personal courage, and greeting freed slaves who hailed him as a messiah.

**1 Freed Slaves (4,000,000)**
*   ΔOS = +0.05 (Symbolic affirmation of freedom and safety; psychological boost)
*   VSA = 0.58
*   Tc = 1.00
*   Vc = 0.00
*   Sc = 0.00

UMQ_base(a,e) = +0.05 × 0.58 × 1.00 = **+0.029**

**Responsibility & Intention:**
*   PerceivedContext = Real
*   ActualContext = Real
*   At = 1.0 (Active presence)
*   Cp = 1.0
*   Ri = 1.0
*   Rp = 1.0
*   In = 1.0

UMQ_final(a,e) = +0.029 × 1.0 × 1.0 = **+0.029**
Group Total (4M) = +0.029 × 4,000,000 = **+116,000.0**

**Aggregate results (pre-CF):**
*   Slaves: +116,000.0

**Complexity Factor adjustment:**
CF = 1.0
Adjusted Total = +116,000

**Actor (self) impact:**
Personal fulfillment of his work; extreme physical risk.
UMQ_self = +0.5

**Summary headline:**
Abraham Lincoln - Visit to Richmond - Freed Slaves: Total UMQ = +116,000 [Highly moral] {Synergistic}

### Multi-Case Summary

1. **Abraham Lincoln - Emancipation Proclamation - Slaves:** +1,470,000 [Extremely moral] {Synergistic}
2. **Abraham Lincoln - Resupplying Sumter/War - Nation:** +1,650,000 [Extremely moral] {Synergistic}
3. **Abraham Lincoln - Trent Affair - Nation:** +4,854,600 [Extremely moral] {Synergistic}
4. **Abraham Lincoln - Cabinet Appointments - Nation:** +89,900 [Highly moral] {Synergistic}
5. **Abraham Lincoln - Revoking Frémont's Order - Nation:** +228,095 [Highly moral] {Synergistic}
6. **Abraham Lincoln - Appointment of Grant - Union Army:** +208,800 [Highly moral] {Synergistic}
7. **Abraham Lincoln - Lobbying for 13th Amendment - Slaves:** +2,320,000 [Extremely moral] {Synergistic}
8. **Abraham Lincoln - Second Inaugural Address - Nation:** +1,798,000 [Extremely moral] {Synergistic}
9. **Abraham Lincoln - Visit to Richmond - Freed Slaves:** +116,000 [Highly moral] {Synergistic}