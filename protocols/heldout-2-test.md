# Held-out set 2 — applicability of the *final* method to untouched obligations

**Pre-registered.** Sources, selection rule, obligations, method under test, architecture and adversary
models, coding scheme and pass/fail criteria were fixed in `heldout-2-preregistration.md` and sealed
before analysis. The prediction pass and the independent pass were each sealed before the next began.
All four hashes are in `sealed/HELDOUT2-SEAL.txt`.

**Why this study exists.** The first held-out study tested the **pre-test** method; two of its fifteen
obligations were exceptions, and those exceptions produced the actuation dimension, the approximable
epistemic branch and explicit per-fact composition. The method in the manuscript is therefore the method
*after* that data was seen. This study applies the **final** method to twelve obligations from four
sources that had no part in producing it, in either study.

**Result: 11 of 12 routed by the frozen rules — 9 clean, 2 with a recorded strain, 1 exception.** The
pre-registered bar was 9 of 12. No obligation required a transformation outside {T1, T2 fact, T2 verdict,
T3, Terminal}, so the pre-registered method-level failure condition was not met. The exception is a
missing *row*, not a missing transformation, and it is on the mediation axis.

---

## 1. The twelve rows

`App.` — **A** applicable · **A−** applicable with a recorded strain · **X** not applicable.
`Agr.` — agreement between the predicted transformation and the independently reasoned architecture:
**✓** full · **~** partial · **✗** none. `Mir.` — structural resemblance to an obligation already
analysed in the development corpus or held-out set 1: **none** · **partial** · **close**.

| # | Obligation (held-out set 2 source) | Deficit and cause at the cut | Predicted by the frozen method | Independent architecture answer | App. | Agr. | Mir. |
|---|---|---|---|---|:-:|:-:|:-:|
| K1 | Limit number and rate of model queries (ATLAS AML.M0004) | end-user principal collapses into a service credential at Z4 | **T2 fact** + T1 counters; extraction under the limit placed in the residual | delegated end-user identity to the gateway, quota against it, **plus** a detective layer on extraction-shaped query distributions | A− | ~ | none |
| K2 | Sanitize training data (ATLAS AML.M0007) | "poisoned" has no ground truth; for online learning the effect accrues after ingest | **T3** — proxy filter at Z1 + detective baseline evaluation, rollback within latency | source allowlists, near-duplicate and trigger detection, outlier analysis; checkpoint evaluation against a held-back baseline; previous checkpoint kept promotable | A | ✓ | partial |
| K3 | Detect and block adversarial inputs (ATLAS AML.M0015) | span provenance lost at flattening; adversarial-ness is intent | **T2 fact** (segments to Z4) + **T3** (detector) | structured segments with provenance from the orchestration layer; classifier at the gateway weighting untrusted spans | A | ✓ | close |
| K4 | Bind and sign provenance on release (C2PA) | generating assertions unrecoverable from bytes at Z7 | **T2 fact** — manifest travels with the asset; derived integrity closes **T1** at the signing layer | build and sign the manifest at production, egress refuses governed assets without one that validates | A | ✓ | partial |
| K5 | Validate provenance on ingest (C2PA) | truth of the assertions unrenderable at the consumer; the signer can render it | **T1** (signature, binding, trust list) + **T2 verdict** (the assertions) | validate locally; rely on the signer's assertion and inherit exactly the signer's credibility, stated explicitly | A | ✓ | partial |
| K6 | Provenance survives downstream handling (C2PA) | **no location in *L* mediates the effect** | **nothing — Table 3 has no row for a mediation deficit** | fingerprint registry + watermark: approximate, detect, and declare the residual | **X** | **✗** | none |
| K7 | Model inventory completeness (SR 11-7 §VII) | none at Z4 under the frozen adversary | **T1** at Z4 | gateway check **paired with** a network rule permitting model-bound egress only through the gateway | A− | ~ | close |
| K8 | Ongoing monitoring (SR 11-7 §V) | business purpose lost at the gateway; performance is a population property | **T2 fact** (use-case tag) + **T3** (detective baseline) | declared use-case with each call, compared inline against what was approved; performance measured off the serving path per use-case | A | ✓ | partial |
| K9 | Change control (SR 11-7 §V) | approval is a judgement no mechanism at Z1 computes | **T2 verdict** — signed approval bound to the artifact, gating release | promotion gate admits only a signed approval naming the validator and bound to the artifact digest | A | ✓ | close |
| K10 | Notice before an automated decision (TBS Directive) | whether a human's judgement was influenced is unobservable | **T1** (wholly automated) + **T3** (in part, on a surfaced-recommendation proxy) | notice gated in the application; assisted case triggered on the recommendation having been surfaced, divergence monitored | A | ✓ | close |
| K11 | Audit trail linking decision to data (TBS Directive) | decision points and source identity lost before the gateway; causal basis unavailable | **T2 fact** ×2 + **T1** (version) + **T3** (attribution as proxy) | structured decision points and retrieval provenance emitted from the layer that holds them, bound to the served request; attribution labelled a proxy | A | ✓ | close |
| K12 | Pre-production bias testing (TBS Directive) | protected attributes may not cross into the development environment | **T2 verdict** ×2 — signed disparity assessment and signed acceptability determination gating release at Z1 | assessment computed by the party that legitimately holds the attributes and returned signed; release gated on it plus a recorded acceptability determination | A | ✓ | partial |

**Tally.** Applicability **A** 9 · **A−** 2 · **X** 1. Agreement **✓** 9 · **~** 2 · **✗** 1.
Mirroring **none** 2 · **partial** 5 · **close** 5.

## 2. The exception — K6, and what it costs

Table 3 is indexed on *the condition at a maximal adequate cut*. For K6 there is no cut: once an asset
has left the estate, no location in *L* mediates what a third party does to it. The method's own §5.4
anticipates this — $F(o)$ can be empty because a location cannot **decide**, cannot **mediate**, or
cannot **act** — but only two of those three are routed. The decision deficits have six rows and
actuation has one; **mediation has none.** The method therefore diagnosed K6 correctly and returned
nothing.

The independent pass reached a defensible architecture without difficulty: register a perceptual
fingerprint so a stripped copy can be matched back, watermark so provenance can be re-asserted from the
content, and state plainly that both fail against an adversary who cares. That is
approximate-and-detect with a declared residual — an existing transformation.

> **Refinement 4, post-hoc with respect to this study.** A mediation deficit routes like an actuation
> deficit: **T3** where a detectable approximation of the mediation exists, otherwise **Terminal**. In
> both cases the true predicate cannot be enforced at the point where enforcement would matter, and in
> both the honest output is an approximation plus a residual — which is the argument §2.1 of
> `heldout-test.md` already made for actuation, applied to the remaining attribute.

This closes Table 3 over all three attributes of §5.3, which it did not previously cover, and requires
no new transformation. It is **not tested by this study**: it was derived from the row that exposed it,
and the pre-registration forbids claiming otherwise. It is reported as a refinement to the application
of the method, in the same posture as the three refinements the first held-out study produced.

## 3. The two strains

**K7 — the answer is only as good as the adversary model.** The frozen *X* is a prompt-injected agent
inside a trusted application, plus a careless user. Neither stands up an unregistered model outside the
gateway. Under that *X*, Z4 is a cut, there is no deficit, and T1 is right. Under an *X* that includes a
developer doing exactly what the inventory obligation exists to catch, Z4 stops being a cut, Z7 becomes
the only cut, and Z7 does not hold model identity — the diagnosis becomes representational and the
architecture becomes the composition the independent pass gave. Both answers are correct for their
adversary. The disagreement is entirely in *X*, and it is the plainest demonstration we have of §5.1's
claim that a placement statement has no truth value until the adversary is named. The row is coded A−
rather than X because the method behaved correctly on the input it was given.

**K1 — the corpus is one of controls, not obligations.** ATLAS mitigations are already-approximated
responses to a threat. Applying the method to "limit the number and rate of queries" places a rate
limit; applying it to the thing the mitigation is for — do not permit model extraction — gives a
temporal-plus-epistemic diagnosis and puts the quota itself in the T3 preventive half. The frozen method
routed the obligation as written and put extraction-within-the-limit in the residual; the independent
pass, reasoning about the purpose, added the detective half. Neither is wrong, and the difference is not
in the function. **The method is sensitive to the altitude at which its input is stated**, and a corpus
drawn from control catalogues will systematically enter it one level below a corpus drawn from law. This
was visible in the development corpus in retrospect and is stated here for the first time.

## 4. What this study establishes, and what it does not

**Does.** Twelve obligations from four sources with no part in the method's development were routed by
the final method under a pre-registered protocol, eleven of them successfully, against a bar of nine
fixed in advance. No obligation required a fifth transformation, which was the pre-registered condition
that would have falsified the paper's central claim. The authority branch acquired a second instance
(K12) of a different shape from the first (H13, a provider/deployer boundary): an intra-organisational
legal restriction on moving protected attributes. The transport recursion held in the five T2 rows whose
prediction recorded a derived integrity obligation — K1, K4, K8, K9, K12 — closing by T1 at an identity
or signing layer in each; in K4 that derived obligation is discharged by a published specification
rather than by our reasoning, which makes it a second documented instance alongside Microsoft Purview.
Three further rows carry a T2 whose derived obligation the prediction pass did not name — K3, K5 and
K11 — and they are recorded as uncounted, on the same basis as the two uncounted development cases.

**Does not.** This is not an external-validity test and not a blind one. One analyst wrote the
predictions and the independent answers in one working session; sealing fixes the order, not the
independence. There is no external oracle: the "independent architecture answer" is the same person's
judgement, as in held-out set 1.

**And the count needs one more qualification, which is the most important sentence here.** Five of the
twelve rows structurally resemble an obligation the method has already seen — K3 is the paper's own
prompt-injection discrimination case, K11's causal-basis fact *is* H5, the row that produced the
approximable branch, and K7, K9 and K10 resemble inventory, release-gate and automated-decision
obligations already analysed. Only **two** rows, K1 and K6, resemble nothing in the earlier corpora —
**and one of those two is the exception.** The clean results concentrate where the obligations look
like ones the method was built on. That is what a set of twelve can show; it is also a reason not to
read 11/12 as a stronger result than it is, and it argues that further evaluation should select for
distance from the existing corpora rather than for count.

## 5. Verdict against the pre-registered criteria

| Criterion, fixed before analysis | Outcome |
|---|---|
| At least 9 of 12 code A or A− | **11** — met |
| No obligation requires a new transformation | none did — met |
| All twelve rows reported, none dropped or reworded | met; the seals evidence it |
| Refinements arising here are post-hoc and not claimed as tested | Refinement 4 is so marked |
