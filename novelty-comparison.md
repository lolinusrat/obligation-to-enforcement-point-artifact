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
| Letier & van Lamsweerde (ICSE 2002) | full text §§1–5 read (theorem, tactic catalogue), 7 Oct 2026 | high |
| PTaCL (POST 2012) | missing-attribute passages and conclusion read in full, 7 Oct 2026 | medium |
| Hilty, Basin & Pretschner (ESORICS 2005); Pretschner et al. 2006 | §2.5 and §3 read in full; 2006 partial, 7 Oct 2026 | medium |
| Antignac & Le Métayer (IFIPTM 2015) | §1–2.3 read in full, 7 Oct 2026 | medium |
| PCAA (arXiv 2606.04104) | full text read, 2 Oct 2026; §6.6 re-checked 7 Oct 2026 | high |
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
| **Koch** | four layers (governance objective, design-time, runtime, assurance), with human escalation throughout; no architecture taken as input | six-criterion rubric scoring runtime suitability (timing of harm, pre-action observability, rule determinacy, judgment load, reversibility, evidence clarity) | partly — unobservable or late context goes to the assurance layer, and low-determinacy judgement to human escalation | none | multi-layer assignment per objective | no; a per-control tuple records evidence and owner |
| **SARC** | agent-loop sites, with host layers ranked by robustness up to a policy layer outside the agent (API gateways, network policies, IAM) | constraint class, decidability, cost asymmetry, reversibility, lowest compatible layer; decidability rescue (§9.2) keyed on class | partly — names one reason, state not passed down the call chain, and relocates evaluation to the deepest layer where the predicate is decidable; does not choose between carrying a fact and carrying a verdict | authority intersection and attribution carried down delegation chains; state slice passed to workers | per constraint | declared default-deny or inoperability (§5.3); measured implementation residual (§10.5); no typed design residual |
| **Letier & van Lamsweerde** | agents in a goal model; no adversary, no enforcement location | realizability of a goal by an agent | **yes** — unrealizability causes (lack of monitorability, controllability, reference to future, …) each select tactics | accuracy goal on a variable (≈ fact) or on a predicate (≈ verdict); choice left to heuristics | goal refinement | weaken the goal |
| **PTaCL** | one policy decision point | attribute-based policy | partly — a value missing because withheld calls for delegating evaluation to its source (stated as future work) | fact, or delegated evaluation (≈ verdict) | no | no |
| **Hilty / Pretschner (usage control)** | central reference monitor | observability and time of the obligation | **yes**, keyed on observability and timing | no | per obligation | unobservable → approximation or not enforceable |
| **Antignac & Le Métayer** | components of a privacy architecture | data minimisation under stakeholder trust assumptions | partly — per computed value, chooses attestation, spot-check or proof by the trust stakeholders accept | value, attestation (≈ verdict) or proof | per value | trust assumptions stated |
| **PCAA** | heterogeneous agent control points; final authority at one layer | enforceability offered by each runtime | no — labels approval by control-point capability, not by why a fact is missing | proof-carrying action records | per action | enforceability class recorded |
| **This paper** | heterogeneous enterprise locations, adversary-relative cut | cause of the information or actuation deficit (integrating the three rows above) | yes — six decision-deficit causes plus actuation, split by three questions: exists upstream, may cross, needs judgement | fact and verdict, payload selected by cause (as PTaCL proposes for withheld values) | per fact | yes, classified by the transformation that leaves it |

## What the table is not claiming

- Not that the others are deficient. Each answers a different question.
- Not that placement criteria are novel. **SARC has genuine ones**, and Koch has a
  layer-assignment rubric. Both are conceded in §III and neither is minimised.
- Not that transport is novel as a mechanism. XACML's PIP is the deployed name
  for moving an attribute to a decision point; DIFC labels, sticky policies and
  RFC 2753's partial decisions are older precedents, and Surapani et al.
  (arXiv 2609.15906) already note that placements become adequate when facts are
  supplied.
- Not that selecting a remedy by cause is novel. Letier & van Lamsweerde key
  tactics to the cause of unrealizability; PTaCL delegates evaluation when a value
  is too sensitive to share; usage control keys mechanisms on observability and
  time. Applied together, these reproduce the paper's architecture on every case
  examined in the 7 Oct 2026 stress test. The contribution is the *integration*:
  one per-fact procedure at an adversary-relative cut across heterogeneous
  enterprise-AI locations, with integrity obligations, a classified residual and a
  placement record. It is not shown to produce better architectures than a
  competent combination of these sources.

## The row that carries the argument

Until preprint v1.0.0 this section said the third column distinguished the paper.
It does not: the Letier, PTaCL and usage-control rows answer *yes* or *partly*.
What the paper adds is applying those cause-keyed distinctions together, per fact,
at an adequate cut under a bypassing adversary, and recording the result. XACML still
treats absence as a routing problem. Koch routes late or unobservable context and
low-determinacy judgement to other layers; SARC keys relocation on one cause, state not
passed down; neither makes a per-fact choice among transformations.
