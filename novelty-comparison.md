# Novelty comparison matrix

Reviewer aid. The claim boundary of §III in one table, so it can be checked
rather than reconstructed from prose.

## Source quality — read this before the table

Cells are only as good as the reading behind them, and the readings differ:

| Work | Basis for the cells below | Confidence |
|---|---|---|
| XACML / NIST SP 800-207 | published standards, widely implemented | high |
| Swiss Cheese (ICSA 2025) | full text read (arXiv v4), 1 Oct 2026 | high |
| Koch (arXiv 2604.05229) | full text read (HTML, all sections), 1 Oct 2026 | high |
| SARC (arXiv 2605.07728) | full text read, including §4.3, §5.3, §9 and §10.5 (re-read 1 Oct 2026) | high |
| This paper | — | — |

The Koch and Swiss Cheese rows were closed against the full texts on 1 October
2026 (`novelty-attack-2026-10-01.md`, with the citation full-text check of the
same date); the Koch and SARC cells below were corrected then. An inaccurate
comparison table is worse than none: it converts a defensible positioning
argument into a factual error a reviewer can point at.

## The matrix

| Work | Location space | Placement criterion | Diagnoses *why* a fact is missing | Transport | Composition | Explicit residual |
|---|---|---|---|---|---|---|
| **XACML / Zero Trust** | policy enforcement architecture | policy and attribute driven | no — absence is treated as unrouted | verdict, via PDP/PEP | limited | no |
| **Swiss Cheese** | guardrail layers | design dimensions; layering | no | no | layered, not per-fact | no |
| **Koch** | four layers (governance objective, design-time, runtime, assurance), with human escalation throughout; no architecture taken as input | six-criterion rubric scoring runtime suitability (timing of harm, pre-action observability, rule determinacy, judgment load, reversibility, evidence clarity) | partly — absent or late context is one criterion, answered by moving the control to another layer | none | multi-layer assignment per objective | no; a per-control tuple records evidence and owner |
| **SARC** | agent-loop sites, with host layers ranked by robustness up to a policy layer outside the agent (API gateways, network policies, IAM) | constraint class, decidability, cost asymmetry, reversibility, lowest compatible layer; decidability rescue (§9.2) keyed on class | partly — decidability rescue responds to a missing predicate by class, with no attribute for what a layer can observe | authority intersection and attribution carried down delegation chains; state slice passed to workers | per constraint | declared default-deny or inoperability (§5.3); measured implementation residual (§10.5); no typed design residual |
| **This paper** | heterogeneous enterprise locations | **cause of the information or actuation deficit** | **yes — six decision-deficit causes plus actuation** | **fact and verdict, payload selected by cause** | **per fact** | **yes, classified by the transformation that leaves it** |

## What the table is not claiming

- Not that the others are deficient. Each answers a different question; three of
  the four predate the one asked here.
- Not that placement criteria are novel. **SARC has genuine ones**, and Koch has a
  layer-assignment rubric. Both are conceded in §III and neither is minimised.
- Not that transport is novel as a mechanism. XACML's PIP is the deployed name
  for moving an attribute to a decision point; DIFC labels, sticky policies and
  RFC 2753's partial decisions are older precedents, and Surapani et al.
  (arXiv 2609.15906) already note that placements become adequate when facts are
  supplied. What is new is that the *payload* — fact or verdict — is selected by
  the cause rather than chosen.

## The row that carries the argument

The distinguishing column is the third: whether the work asks *why* a required
fact is unavailable at the location that could enforce. XACML treats absence as
a routing problem. Koch and SARC both use inputs that correlate with cause
(runtime observability, decidability) without making cause the selector; SARC's
decidability rescue is the closest deficit-to-response rule, and it is keyed on
constraint class. Making the cause the selector is what produces the
fact/verdict distinction, per-fact composition, and a residual classified by the
transformation that leaves it.
