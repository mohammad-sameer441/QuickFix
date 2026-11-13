# AegisCode System Architecture & Technical Specification

## 1. Executive Overview
AegisCode is an end-to-end intelligent code analysis and automated remediation engine. Unlike traditional static analyzers (linters, AST pattern regexes) that only flag syntax and stylistic issues, AegisCode bridges the gap between **predictive risk forecasting**, **deep semantic logic reasoning**, and **automated verifiable program repair (APR)**.

```
                      +-----------------------------+
                      |   Source Code / GitHub PR   |
                      +--------------+--------------+
                                     |
                                     v
                  +-----------------------------------+
                  |  Stage 1: AST Ingestion & Churn   |
                  +------------------+----------------+
                                     |
                                     v
                  +-----------------------------------+
                  | Stage 2: Predictive Risk Scoring  |
                  |  - McCabe Cyclomatic Metric       |
                  |  - Cognitive State Mutation Depth |
                  +------------------+----------------+
                                     |
                         [ Defect Probability > Threshold ]
                                     |
                                     v
                  +-----------------------------------+
                  | Stage 3: Semantic Bug Localizer   |
                  |  - CWE Classification            |
                  |  - Pinpoint Fault Lines (Start/End)|
                  |  - Natural Language Root-Cause   |
                  +------------------+----------------+
                                     |
                                     v
                  +-----------------------------------+
                  | Stage 4: Automated Program Repair |
                  |  - Unified Git Diff Synthesizer   |
                  |  - Invariant Test Generator       |
                  +------------------+----------------+
                                     |
                                     v
                  +-----------------------------------+
                  | Stage 5: Sandboxed Validation     |
                  |  - Pre-patch Test Fails (Repro)   |
                  |  - Post-patch Test Passes (Fix)   |
                  |  - Regression Assertion Checks    |
                  +-----------------------------------+
```

---

## 2. Mathematical Formulation of Predictive Defect Likelihood

Traditional McCabe Cyclomatic Complexity counts independent linear paths $M = E - N + 2P$.
However, modern logical bugs (like race conditions or IDOR) frequently occur in code with low cyclomatic complexity but high cognitive state hazards.

AegisCode computes an aggregated **Hazard Index ($H$)**:

$$H = \alpha \cdot CC + \beta \cdot SM + \gamma \cdot \text{LOC} + \omega \cdot \mathbb{I}_{\text{async\_unlocked}}$$

Where:
- $CC$ = Cyclomatic Complexity (branching operations: `if`, `while`, `for`, `except`, `bool_op`)
- $SM$ = State Mutation Density (assignments to shared scopes/dictionaries/globals)
- $\text{LOC}$ = Length of Function in Lines
- $\mathbb{I}_{\text{async\_unlocked}}$ = Indicator flag (1 if async code performs mutation without an active mutex lock, 0 otherwise)
- $\alpha = 4.5, \beta = 2.5, \gamma = 0.8, \omega = 25.0$

The normalized **Defect Probability Score ($P_{\text{defect}}$)** is computed via a sigmoid transfer function:

$$P_{\text{defect}} = \frac{100}{1 + e^{-H / 20}}$$

---

## 3. Four Core Pillars

### Pillar 1: Predictive Code Intelligence
- Analyzes code before deployment or pull request merges.
- Flags dangerous anti-patterns:
  - Time-of-check to time-of-use (TOCTOU).
  - Unsynchronized concurrency mutations.
  - Excessive branching depth.

### Pillar 2: Identification of Logical Vulnerabilities
- Standard linters (`flake8`, `eslint`, `pylint`) cannot detect when business logic is violated.
- AegisCode specifically inspects:
  - **Concurrency:** Yielding I/O (`await`, `sleep`) between validation and mutation.
  - **Authorization:** Authenticated context without resource-ownership checks (IDOR).
  - **Boundary Conditions:** Slice boundaries with $+1$ off-by-one errors.

### Pillar 3: Semantic Bug Localization
- Rather than vague warnings ("Consider checking line 1-100"), AegisCode outputs:
  - Exact target function name.
  - Specific start line and end line.
  - Contextual explanation of the semantic disconnect between programmer intent and runtime consequence.

### Pillar 4: Automated Program Repair (APR) & Verification
- Generates standard **Unified Git Diffs** that can be piped directly into `git apply`.
- **Closed-Loop Verification:**
  1. Synthesizes a dedicated reproduction unit test that triggers the bug on the original code.
  2. Applies the surgical patch.
  3. Re-runs the test to prove that the invariant now holds.
  4. Guarantees zero regressions.
