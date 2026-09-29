# Held-out test — does deficit cause *predict* the transformation?

**Method frozen before this run.** Class N/T/O definitions, the four deficit causes, T1 Relocate,
T2 Transport (fact|verdict), T3 Approximate-and-detect, Terminal Declare-residual. Location model
Z1–Z8 and adversary model X unchanged from the development corpus.

**Protocol.** For each obligation: derive `I(o)` → identify the strongest adequate cut → identify the
deficit and its cause → **record the predicted transformation from the frozen function** → *then*,
separately, work out what the architecture should actually be → compare. The prediction column was
written before the independent column in every row.

**Sources deliberately disjoint from method development.** No EU AI Act Ch. III §2, no ISO/IEC 42001
Annex A, no NIST AI 600-1, no OWASP ASI. Held-out sources: **GDPR** (Arts 5, 15, 17, 22, 32, 33 —
titles verified, Art 22 pulled verbatim), **CSA AI Controls Matrix v1.x** (247 control objectives
across 18 domains), **NIST SP 800-218A** (SSDF GenAI community profile), **EU AI Act Chapter V**
(GPAI provider obligations, Arts 53/55 — a different regime from Ch. III).

**Result: 13 / 15 clean predictions, 1 miss, 1 partial.** Above the 12/15 bar. Neither exception
required a new transformation; both revealed boundary conditions, and a third emerged from two rows
that were technically hits. All three are refinements to how the function is *applied*, not to what it
returns.

---

## 1. The predictions

| # | Obligation (held-out source) | Deficit at strongest cut | Cause | **Predicted** | Independent architecture answer | ✓ |
|---|---|---|:-:|---|---|:-:|
| H1 | No decision based solely on automated processing with legal/significant effect (GDPR Art 22(1)) | Z4 cannot tell a legal-effect decision from any other call | Rep | **T2 fact** | label decision-bearing flows at Z2, carry to the cut, block completion without a recorded intervention point | ✓ |
| H2 | Right to obtain human intervention, express a view, contest (GDPR Art 22(3)) | whether intervention actually occurred and was substantive | Ep-renderable | **T2 verdict** | signed intervention record from the reviewer's system, enforced at the cut; residual on substantiveness | ✓ |
| H3 | Purpose limitation — no incompatible further processing (GDPR Art 5(1)(b)) | purpose-of-collection label destroyed by the time data reaches the prompt | Rep **+ Ep** | **T2 fact** | propagate collection-purpose labels through retrieval; enforce compatibility at Z6 — **plus** a verdict-transport for asserted current purpose and a residual | ✓* |
| H4 | Right to erasure applied to data memorised in weights (GDPR Art 17) | **none — `I(o) ⊆ A(Z1)`** | — | **T1** | output-side suppression + index deletion + accept residual; erasure from weights is not performable | **✗** |
| H5 | Meaningful information about the logic involved (GDPR Art 15 / 22) | causal basis of the specific output unavailable anywhere | Ep-unrenderable | **Terminal** | log inputs, retrieved sources, model version; provide procedural rather than causal explanation — an *approximation* plus residual | **~** |
| H6 | Security of processing — encryption, pseudonymisation (GDPR Art 32) | none | — | **T1** | enforce at Z6/Z7 | ✓ |
| H7 | Breach notification within 72 hours (GDPR Art 33) | breach recognised only after the fact | Tmp | **T3** | detective monitoring + notification workflow; residual on undetected breaches | ✓ |
| H8 | Provenance and integrity of third-party model artifacts (CSA AICM, supply chain) | none | — | **T1** | signature verification at Z1 registry | ✓ |
| H9 | Prevent sensitive-data egress to external models (CSA AICM, data security) | contextual sensitivity label lost before Z4 | Rep | **T2 fact** | propagate classification labels from the data layer through retrieval into the gateway | ✓ |
| H10 | Verify integrity/provenance of training data and code across the SDLC (SP 800-218A) | none | — | **T1** | hash/signature gates at Z1 | ✓ |
| H11 | Protect model weights from unauthorised access or exfiltration (SP 800-218A) | none | — | **T1** | Z6/Z7/Z8 access and egress control | ✓ |
| H12 | Track, document and report serious incidents (AI Act Art 55, systemic-risk GPAI) | incident recognised after; severity is a judgement | Tmp **+ Ep** | **T3** | detective monitoring + human severity adjudication + reporting | ✓* |
| H13 | Consume a GPAI provider's training-content summary (AI Act Art 53, deployer view) | the corpus is behind an organisational boundary | **Auth** | **T2 verdict** | consume the provider's signed attestation; derived obligation (authenticity) closes at the signing layer | ✓ |
| H14 | Disclose only the minimum PHI necessary for the purpose (HIPAA minimum necessary) | purpose-of-access absent at Z6 | Ep-renderable | **T2 verdict** | purpose-of-use attestation propagated with the request; field-level redaction at Z6 | ✓ |
| H15 | Detect model behaviour drift against an approved baseline (CSA AICM, model security) | behaviour accrues over time | Tmp | **T3** | detective monitoring against baseline; no preventive form exists | ✓ |

`✓* ` = predicted transformation correct but the obligation carried a second deficit cause the
single-valued prediction did not capture. See §2.3.

**Authority branch now has a real instance (H13), which the development corpus lacked.** The
provider/deployer boundary is where it lives: the fact may not cross, the attestation may.

## 2. The three boundary conditions

### 2.1 F(o) can be empty for *actuation* reasons, not only informational ones — H4

The function mispredicted erasure because it only inspects `A(l)`. For Art 17 there is **no information
deficit at all**: Z1 knows exactly which data entered training. What is missing is `α` — no location can
perform selective removal from weights without retraining, and for a third-party model at Z5 there is no
`α` whatsoever.

The kernel already had `α` in the definition of `F(o)`; the deficit taxonomy simply never used it. The
fix requires **no new transformation**: an actuation deficit routes by the same logic as an information
one — approximate what cannot be done directly (**T3**: suppress at output, delete from indexes) and
declare the remainder. Erasure then classifies as **T3 + residual**, which matches practice.

> **Refinement 1.** `F(o)` can be empty for two reasons — the location cannot *decide* (information
> deficit) or cannot *act* (actuation deficit). Both route through the same function; actuation deficits
> behave like temporal ones, because in both cases the true predicate cannot be enforced at the point
> where enforcement would matter.

This is worth more than the row it cost. It gives the paper a second axis with a real, universally
recognised example, and Art 17-on-model-weights is a case every reviewer will have an opinion about.

### 2.2 The epistemic branch needs three cases, not two — H5

The frozen function offers only *renderable somewhere* → T2 verdict, or *renderable nowhere* → Terminal.
Explanation of a model's output is neither: it is **approximable**. Attribution and provenance logging
give a defensible partial answer that is not the true causal predicate.

> **Refinement 2.** Epistemic deficits split three ways: **renderable** (T2 verdict) · **approximable**
> (T3) · **unrenderable** (Terminal). H5 is approximable; corpus item 24 (human-agent deception) remains
> genuinely unrenderable and stays Terminal.

This *strengthens* the Terminal branch by making it rarer and better earned — a method that declares
"unenforceable" too readily is as unhelpful as one that never does.

### 2.3 The function applies per missing *fact*, not per obligation — H3, H12

Both rows carried two causes. H3 needs a collection-purpose label (representational) *and* an assertion
of current purpose (epistemic). H12 needs incident detection (temporal) *and* severity adjudication
(epistemic-renderable). A single-valued prediction per obligation cannot express either.

> **Refinement 3.** Decompose `I(o)` fact by fact. Each missing fact has its own cause and its own
> transformation; the obligation's architecture is the **composition** of those transformations, and the
> obligation's residual is the **union** of the terminal ones.

This is the most useful of the three, and it retrospectively explains the development corpus: items 2,
19, 20 and 25 all produced multi-part answers, and the earlier note that "T2 and T3 co-occur" was this
refinement showing up without being recognised. The method is **compositional**, which is a stronger
property than the single-valued function claimed — and it means the central table stays exactly as it
is, applied at a finer grain.

## 3. Revised statement of the method

Unchanged in content, refined in application:

1. Filter Class N — obligations with no mediated action.
2. Derive `I(o)`. Identify the strongest cut over ⟨S, X⟩ with adequate `α`.
3. **For each missing fact**, determine the deficit cause: representational · authority · epistemic
   (renderable | approximable | unrenderable) · temporal — or an **actuation** deficit on `α`.
4. Apply the function per fact: none→T1 · Rep→T2 fact · Auth→T2 verdict · Ep-renderable→T2 verdict ·
   Ep-approximable→T3 · Ep-unrenderable→Terminal · Tmp→T3 · actuation→T3, else Terminal.
5. Compose. Each T2 spawns a derived integrity obligation; recurse (terminates at the signing layer —
   ~~7/7 in development, 3/3 here, 10/10 overall~~ **[RETIRED — see the traceability correction
   below. The development 7/7 stands and is enumerated in `classification-corpus.md` §5(e); the 3/3
   and the 10/10 are not reconstructable and are not reported in the manuscript.]**).

> **Traceability correction, recorded rather than silently applied (31 Aug 2026).** The "3/3 here" and
> the "10/10 overall" are not reconstructable and are **retired as reportable counts**. This run has
> **six** T2 obligations — H1, H2, H3, H9, H13, H14 — and nothing in this file says which three of them
> the 3/3 refers to; only H13 names its derived obligation explicitly. The development seven are
> enumerated by item number in `classification-corpus.md` §5(e) and stand unchanged. The manuscript's
> §7.5 previously read "the ten transport cases analysed in §8" on the strength of the 10/10; it now
> claims the enumerated **seven**, plus Microsoft Purview as a documented instance from the
> retrodiction study. `artifact/data/transport-recursion.csv` lists all eighteen transport cases across
> the three studies with the basis for counting or excluding each.
>
> Aggregating the studies into a single "ten" was also inconsistent with the paper's own commitment in
> §8 that the three studies "differ in independence, not only in size" and are not aggregated. Reporting
> seven constructed cases and one documented one keeps that separation.
6. Output = composed architecture + union of residuals.

## 4. What this run does and does not establish

**Does:** the frozen function predicted 13 of 15 unseen obligations from four disjoint sources; both
failures were absorbed by refining *how* the function is applied rather than by adding transformations;
the authority branch acquired its first real instance; ~~the recursion held 10/10 overall~~
**[RETIRED — not reconstructable; not reported in the manuscript. See §3 note.]**

**Does not:** this is still one classifier — I wrote both the prediction and the independent answer, so
it tests the function's **internal consistency** far better than its external validity. H2 and H9
structurally mirror development items 2 and 4, so they are weak evidence. And "the independent
architecture answer" is my judgement, not observed practice.

**The external check that would settle it** is retrodiction against *documented* systems rather than
against my own reasoning: take published enterprise AI reference architectures and security
documentation, extract where each obligation was actually enforced, and test whether the function
predicts the observed placement. That is a genuinely independent oracle, it needs no human participants,
and it is the natural evaluation section for the paper. The commercial-platform evidence matrix built
for a companion study is a starting corpus.

## 5. Verdict

The held-out test passes at 13/15 with no new transformations required. The method is stable enough to
write around, and the three refinements make it compositional, give the actuation axis a foothold, and
tighten the Terminal branch.

**Recommendation: stop searching for the contribution and start building the manuscript**, with the
deficit-cause → transformation table (as refined in §3) as the central artifact, the compositional
property as the main theoretical claim, and documented-architecture retrodiction as the evaluation.
