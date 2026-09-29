# Held-out set 2 — pre-registration

**Status: frozen.** This file was written and sealed before any of the twelve obligations below was
analysed. It fixes the sources, the selection rule, the obligations, the method under test, the
architecture and adversary models, the coding scheme, and the pass/fail criteria. Its SHA-256 is
recorded in `sealed/HELDOUT2-SEAL.txt`. Nothing in it may be added to, removed, or reworded after
sealing; corrections take the form of a dated amendment appended below, as in `sealed/`.

## 1. What this study tests, and what it does not

The first held-out study (`heldout-test.md`) tested the **pre-test** method. Two of its fifteen
obligations were exceptions, and those exceptions produced the actuation dimension, the approximable
epistemic branch, and explicit per-fact composition. The method reported in the manuscript is therefore
the method *after* that data was seen. This is stated plainly in the manuscript, but it leaves one
question open:

> The held-out data helped refine the method. Where is the untouched evaluation of the **final** method?

This study answers that question and nothing else. It is an **applicability** test of the final,
refined method against obligations that played no part in producing it — neither in development nor in
the first held-out set. It is not a test of external validity, it is not blind, and it does not
introduce an external oracle. The single-analyst limitation of the first held-out study applies here
unchanged and is restated in §6.

## 2. Source-selection rule, fixed before any source was opened

A source is admissible iff all four hold:

1. **Disjoint.** It is not among the development sources (EU AI Act Chapter III Section 2 and Article
   50; ISO/IEC 42001 Annex A; NIST AI 600-1; OWASP Top 10 for Agentic Applications), nor among the
   first held-out sources (GDPR; CSA AI Controls Matrix; NIST SP 800-218A; EU AI Act Chapter V), nor
   a sibling document of one of those under the same publisher and subject matter. HIPAA is excluded
   entirely, because the Privacy Rule's minimum-necessary requirement supplied H14.
2. **In scope.** Its obligations bear on enterprise AI systems of the kind the location model of Table 1
   describes. Platform-content regulation, which does not map onto that model, is excluded — the
   architecture model is frozen and may not be stretched to fit a source.
3. **Different genre.** The four sources are drawn from four different kinds of instrument, so that the
   set is not four restatements of one regulatory tradition.
4. **Verifiable.** Each obligation is stated in the source's own terms and can be checked against a
   public copy of it by a reader.

**The four sources.**

| | Source | Genre | Obligations taken |
|---|---|---|---|
| A | MITRE ATLAS mitigations | adversarial-ML knowledge base | 3 |
| B | C2PA Content Credentials specification | technical specification | 3 |
| C | SR 11-7 / OCC 2011-12, *Supervisory Guidance on Model Risk Management* | sectoral supervisory guidance | 3 |
| D | Treasury Board of Canada Secretariat, *Directive on Automated Decision-Making* | public-sector administrative directive | 3 |

Three obligations were taken per source. Within a source, obligations were chosen to be architecturally
enforceable (Class N items are not the object of this study) and to avoid taking three that reduce to
the same predicate shape. No obligation was chosen because its outcome was foreseen, and none was
looked at analytically before this file was sealed; the titles below were taken from the sources.

**Obligation texts are paraphrases** written from the analyst's reading of each source, not verbatim
quotations, except where quotation marks appear. A reader checking this study should check the
paraphrase against the source first; a paraphrase that misstates the obligation invalidates the row.

## 3. The twelve obligations

| # | Source | Obligation |
|---|---|---|
| K1 | ATLAS AML.M0004 | Limit the number and rate of queries a requester may make to a deployed model, to raise the cost of extraction, inversion and discovery. |
| K2 | ATLAS AML.M0007 | Detect and remove or remediate poisoned training data before training, and recurrently for a model that learns online. |
| K3 | ATLAS AML.M0015 | Detect and block adversarial inputs — inputs that deviate from benign behaviour or match patterns seen in previous attacks — before they reach the model. |
| K4 | C2PA | An asset released with provenance claims must carry a manifest whose assertions are hard-bound to the asset bytes and signed, so that later modification of either is detectable. |
| K5 | C2PA | A consumer of an asset must be able to determine whether its provenance manifest validates, whether the signer is trusted, and whether the asset has changed since signing. |
| K6 | C2PA | Provenance must survive downstream handling: when a third party transcodes, crops or re-publishes an asset, the provenance must be preserved or its loss must be detectable. |
| K7 | SR 11-7 §VII | Maintain a comprehensive inventory of models in use, under development, and recently retired; a model may not be in production use without being recorded. |
| K8 | SR 11-7 §V | Monitor models on an ongoing basis to confirm they are being used as intended and remain appropriate for current conditions. |
| K9 | SR 11-7 §V | A model may not be changed in production without validation and approval of the change. |
| K10 | TBS Directive | Give notice, before a decision is rendered, that the decision will be made in whole or in part by an automated decision system. |
| K11 | TBS Directive | The system must produce an audit trail recording the decision points, the system version, and links to the data and information used to make the decision. |
| K12 | TBS Directive | Before production, test the data and the system for unintended bias and other factors that may unfairly affect outcomes. |

## 4. What is frozen

**The method under test** is the manuscript's final method, unchanged:

- the seven-step procedure of §7.1 — Filter · Derive $I(o)$ · **Instantiate** · Locate · Diagnose ·
  Transform · Compose;
- the seven deficit causes of Table 2 — representational, authority, epistemic (renderable ·
  approximable · unrenderable), temporal, actuation;
- the four transformations of Table 3 — T1 Relocate, T2 Transport (fact | verdict), T3
  Approximate-and-detect, Terminal (declare residual) — with the cause-to-transformation mapping
  exactly as tabulated;
- per-fact application and composition, with the residual as the union of the terminal parts;
- the transport recursion of §7.5, including the claim that a derived integrity obligation is
  Class T and closes by T1 at an identity or signing layer.

**The architecture model** is the eight zones Z1–Z8 of Table 1, with the availability, cut-scope and
actuation entries as tabulated. **The adversary** *X* is §5.1's: a prompt-injected or misdirected agent
inside an otherwise trusted application, together with a careless user. Neither may be modified to
accommodate an obligation. Where an obligation's natural reading requires an adversary *X* does not
cover — an insider, a developer standing up an unregistered model, a hostile third-party publisher —
the analysis is conducted under the frozen *X* and the sensitivity is recorded in the row rather than
resolved by widening *X*.

**Step 3, Instantiate,** is exercised here for the first time. It was added after the retrodiction
predictions were made and has never been applied prospectively. Because the location model is generic
rather than a named product, instantiation here means establishing what each zone holds *for this
obligation's governed effect* before diagnosing, rather than reading attributes off the zone label.

## 5. Coding scheme, fixed before analysis

Three codes per obligation, each recorded independently.

**(a) Applicability — the primary outcome.** Did the frozen method return a determinate architecture
for every fact in $I(o)$ without requiring a change to the transformation function, the deficit
taxonomy, or the procedure?

- **A** — applicable. Every fact routed by Table 3; a composed architecture and a residual were returned.
- **A−** — applicable with a recorded strain: routed, but the row exposes a boundary condition worth
  naming.
- **X** — not applicable. Some fact could not be routed by the frozen rules.

**(b) Agreement.** Was the transformation predicted from the frozen rules the same as the architecture
reached by reasoning about the obligation directly? **✓** full · **~** partial (the composition
differs but no transformation is wrong) · **✗** no.

**(c) Mirroring — recorded because it bounds what a clean result means.** Does this obligation
structurally mirror one already analysed in the development corpus or the first held-out set — same
predicate shape, same deficit cause, same zone? **none** · **partial** · **close**. Rows coded *close*
are weak evidence and are reported separately from the headline count.

## 6. Procedure

Three passes, each written to its own file and sealed before the next begins, so that the order cannot
be reconstructed favourably afterwards:

1. **Prediction pass** (`heldout-2-predictions.md`) — for each obligation: derive $I(o)$, instantiate,
   locate the cut, diagnose each fact, and record the transformation Table 3 returns. Nothing else.
2. **Independent pass** (`heldout-2-independent.md`) — for each obligation, written without reopening
   the prediction file: what the architecture should be, argued from the obligation and the estate.
3. **Comparison and coding** (`heldout-2-test.md`) — the two are set side by side and the three codes
   assigned.

**This separation is procedural, not cognitive.** One analyst wrote all three passes in one working
session. Sealing each pass before the next fixes what was claimed and when; it does not make the second
pass independent of the first in the sense a second coder would be. The first held-out study carries
the same limitation and states it; nothing here repairs it. What this study adds over that one is not
independence but **untouched input**: none of these twelve obligations, and none of these four sources,
had any part in producing the method being tested.

## 7. Pass and fail criteria, fixed before analysis

- **Pass** iff at least **9 of 12** obligations code **A** or **A−**.
- **Method-level failure** iff any obligation requires a **new transformation** — a fifth kind of
  response that is not T1, T2, T3 or Terminal. This is the criterion that would falsify the paper's
  central claim; it is stated separately from the count because a single such case matters more than
  three unroutable ones.
- **Reporting rule.** All twelve rows are reported whatever they show. No obligation may be dropped,
  reworded, or exchanged after sealing. An exception is reported as an exception, with the refinement
  it suggests recorded as a refinement to the *application* of the method rather than folded silently
  into the method reported in the manuscript. Any refinement arising here is post-hoc with respect to
  this study and may not be claimed as tested by it.
- **The count is applicability, not accuracy,** and is reported as such. So is the first held-out
  study's 13/15; the two are not aggregated, being tests of different versions of the method.
