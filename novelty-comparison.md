# Novelty comparison matrix

Reviewer aid. The claim boundary of §III in one table, so it can be checked
rather than reconstructed from prose.

## Source quality — read this before the table

Cells are only as good as the reading behind them, and the readings differ:

| Work | Basis for the cells below | Confidence |
|---|---|---|
| XACML / NIST SP 800-207 | published standards, widely implemented | high |
| Swiss Cheese (ICSA 2025) | abstract and secondary description; **full text not read** | medium — verify before relying on the "no transport" cell |
| Koch (arXiv 2604.05229) | abstract only; the rubric's mechanics are in the full paper | **low — verify every cell** |
| SARC (arXiv 2605.07728) | full HTML read, including §4.3 and Table 3 | high |
| This paper | — | — |

**Do not publish this table without closing the Koch and Swiss Cheese rows.** An
inaccurate comparison table is worse than none: it converts a defensible
positioning argument into a factual error a reviewer can point at.

## The matrix

| Work | Location space | Placement criterion | Diagnoses *why* a fact is missing | Transport | Composition | Explicit residual |
|---|---|---|---|---|---|---|
| **XACML / Zero Trust** | policy enforcement architecture | policy and attribute driven | no — absence is treated as unrouted | verdict, via PDP/PEP | limited | no |
| **Swiss Cheese** | guardrail layers | design dimensions; layering | no | no | layered, not per-fact | no |
| **Koch** | four lifecycle strata | runtime enforceability: observable, determinate, time-sensitive | partly — the rubric's inputs are adjacent to epistemic and temporal causes | limited | assurance feedback loop | no |
| **SARC** | four sites in one agent loop | constraint class, decidability, cost asymmetry, reversibility, lowest compatible layer | partly — decidability timing is a cause-like input | limited | per constraint | response protocol, not a residual |
| **This paper** | heterogeneous enterprise locations | **cause of the information or actuation deficit** | **yes — five causes plus actuation** | **fact and verdict, payload determined by cause** | **per fact** | **yes, as a first-class output** |

## What the table is not claiming

- Not that the others are deficient. Each answers a different question; three of
  the four predate the one asked here.
- Not that placement criteria are novel. **SARC has genuine ones**, and Koch has a
  layer-assignment rubric. Both are conceded in §III and neither is minimised.
- Not that transport is novel as a mechanism. XACML's PIP is the deployed name
  for moving an attribute to a decision point. What is new is that the *payload*
  — fact or verdict — is determined by the cause rather than chosen.

## The row that carries the argument

The distinguishing column is the third: whether the work asks *why* a required
fact is unavailable at the location that could enforce. XACML treats absence as
a routing problem. Koch and SARC both use inputs that correlate with cause
(enforceability, decidability) without making cause the determinant. Making it
the determinant is what produces the fact/verdict distinction, per-fact
composition, and a residual the method can return instead of a location.
