# Held-out set 2 — prediction pass

**Written against the sealed pre-registration** (`heldout-2-preregistration.md`, SHA-256
`63ad5c99…`), and sealed in turn before the independent pass was begun. This file records only what
the **frozen method returns**: derive $I(o)$, instantiate the candidate locations for this obligation's
governed effect, locate the maximal cut, diagnose each missing fact against Table 2, and read the
transformation off Table 3. It contains no judgement about what the architecture *ought* to be; that is
the next pass.

Notation follows the manuscript: Z1–Z8 are the zones of Table 1; the adversary *X* is §5.1's, frozen.

---

## K1 — ATLAS AML.M0004, limit the number and rate of model queries

$I(o)$ = ⟨principal the limit applies to · that principal's query count in the window · the limit⟩.

**Instantiate and locate.** The governed effect is a query being served. Under *X* every model-bound
path runs application → SDK → gateway → endpoint, so **Z4** mediates all of them; Z5 mediates only
calls to one model and is dominated. $\alpha(Z4) \supseteq \{$block$\}$ = $R(o)$.

| Fact | Status at Z4 | Cause → transformation |
|---|---|---|
| principal | Z4 holds tenant and caller service; a shared service credential collapses many end users into one | representational → **T2 fact** |
| count in window | Z4 can hold its own counters, once keyed on a principal | none → **T1** |
| the limit | configuration | none → **T1** |

**Composed.** Transport an on-behalf-of principal assertion from Z2 into the model call; Z4 counts and
blocks per principal. Derived integrity obligation — the assertion must be unforgeable by *X* — is a
predicate over token provenance, hence Class T, closing by **T1** at the identity layer.
**Residual.** A principal able to obtain several identities. Separately, the obligation as written is a
rate proxy for extraction, so extraction conducted within the limit lies outside its competence.

## K2 — ATLAS AML.M0007, sanitize training data

$I(o)$ = ⟨the sample and its provenance · whether the sample is poisoned⟩.

**Instantiate and locate.** Governed effect: a sample entering a training run, and for an online model
each subsequent update. **Z1** mediates all releases and the training pipeline; $\alpha$ = block release.

| Fact | Status at Z1 | Cause → transformation |
|---|---|---|
| sample and provenance | present | none → **T1** |
| poisoned or not | no party holds ground truth; provenance filtering, near-duplicate and trigger detection and outlier analysis are defensible proxies | epistemic-approximable → **T3** |
| (online variant) effect of the sample on behaviour | accrues over updates after the decision point | temporal → **T3** |

**Composed.** Proxy filtering at ingest plus detective evaluation of model behaviour against a held-back
baseline after each update. The detective half is adequate only where the effect is reversible within
the detection latency; checkpoint rollback supplies that for a batch pipeline.
**Residual.** Poisoned samples no available proxy separates from clean ones; for an online model, the
window between an update and its detection.

## K3 — ATLAS AML.M0015, detect and block adversarial inputs

$I(o)$ = ⟨the input content · the provenance of each span of it · whether it is adversarial⟩.

**Instantiate and locate.** Governed effect: an input reaching the model. **Z4** is the cut over all
model-bound traffic and can block or modify; Z3 holds more but cuts only SDK-mediated calls.

| Fact | Status at Z4 | Cause → transformation |
|---|---|---|
| input content | present | none → **T1** |
| span provenance — author-supplied, retrieved, tool output | existed at Z3, does not survive flattening | representational → **T2 fact** |
| adversarial or not | a property of the sender's intent; no party renders it as a fact, detectors give a defensible proxy | epistemic-approximable → **T3** |

**Composed.** Carry structured segments with provenance from Z3 to Z4; run the detector at Z4 over
content with untrusted spans distinguished; block or strip.
**Residual.** Adversarial inputs the detector does not separate from benign ones; instructions embedded
in spans that are provenance-trusted.

## K4 — C2PA, bind and sign provenance on release

$I(o)$ = ⟨the asset bytes as released · the assertions about what produced or edited it · a signing
credential⟩.

**Instantiate and locate.** Governed effect: an asset leaving the estate with provenance claims, by API
response, download or egress to a third party. **Z7** mediates all traffic; $A(Z7)$ = destination,
volume, metadata; $\alpha(Z7)$ = block, which meets $R(o)$ — refuse release of a governed asset with no
valid manifest. Z3 and Z5 hold the generating actions but cut only their own paths.

| Fact | Status at Z7 | Cause → transformation |
|---|---|---|
| asset bytes | present in the stream | none → **T1** |
| assertions | known at Z3/Z5, not recoverable from the bytes at Z7 | representational → **T2 fact** |
| signing credential | platform key service | none → **T1** |

**Composed.** Assemble and sign the manifest where the assertions exist; Z7 admits governed asset types
only with a manifest that validates. Derived integrity obligation — the transported manifest must be
unforgeable by *X* — is a predicate over signature and binding provenance, hence Class T, closing by
**T1** at the signing layer.
**Residual.** Release by a path outside *S*; and assertions true of the pipeline but not of the world.

## K5 — C2PA, validate provenance on ingest

$I(o)$ = ⟨manifest and signature · asset bytes · trust list · whether the assertions are true of the
asset's history⟩.

**Instantiate and locate.** Governed effect: an asset being ingested and its provenance relied upon.
**Z6** mediates all access to the resource; $\alpha$ = deny, redact.

| Fact | Status at Z6 | Cause → transformation |
|---|---|---|
| manifest, signature, bytes, trust list | present | none → **T1** |
| truth of the assertions | no mechanism at Z6 establishes that a camera captured the scene or that a model produced the pixels; the signer is the party who can | epistemic-renderable → **T2 verdict** |

**Composed.** Validate signature, hard binding and trust list at ingest; treat the assertions as a
transported verdict carrying the signer's authority, not the consumer's.
**Residual.** A trusted signer that signs a false assertion; and assets with no manifest, about which
absence of provenance is not evidence.

## K6 — C2PA, provenance survives downstream handling

$I(o)$ = ⟨the transformed asset · its original manifest or a link to it⟩.

**Instantiate and locate.** Governed effect: a third party transcoding, cropping or re-publishing an
asset that has already left the estate. Z1–Z6 and Z8 are interior. Z7 mediates traffic leaving the
estate but not what is done to the asset afterwards. **No location in *L* is a cut over this effect.**

**Diagnose.** This is not a decision deficit: whoever performs the transformation has every fact. It is
not an actuation deficit at a cut, because there is no cut whose actuation could be assessed. $F(o)$ is
empty for the second of §5.4's three reasons — no location can **mediate**.

**Transform.** Table 3 is indexed on *the condition at a maximal adequate cut*. There is no such cut,
so **no row applies and the frozen function returns nothing.** The method diagnoses the obstruction
correctly and then has nothing to hand back.

**Predicted code: X — not applicable.**

## K7 — SR 11-7, model inventory completeness

$I(o)$ = ⟨that this is a use of a model · which model · whether it is recorded in the inventory⟩.

**Instantiate and locate.** Governed effect: a model being used in production. Under the frozen *X* —
an injected agent inside the trusted application, and a careless user — the paths available to *X* are
those the application and its SDK expose, all of which traverse **Z4**, which holds model identity, can
perform a registry lookup, and can block.

| Fact | Status at Z4 | Cause → transformation |
|---|---|---|
| use of a model | present | none → **T1** |
| which model | present | none → **T1** |
| recorded in inventory | registry lookup | none → **T1** |

**Composed.** Enforce at Z4: refuse calls to a model not in the inventory.
**Sensitivity, recorded not resolved.** The obligation's natural target is a developer standing up an
unregistered model outside the gateway. That actor is not in *X*. Under an *X* extended to include
them, Z4 ceases to be a cut, Z7 becomes the only cut and lacks model identity, and the diagnosis becomes
representational with a composed answer over Z7 and Z4. Coded under the frozen *X*, per §4 of the
pre-registration.
**Residual.** Under the frozen *X*, none beyond the currency of the registry itself.

## K8 — SR 11-7, ongoing monitoring

$I(o)$ = ⟨declared intended use · the use this call puts the model to · observed performance against
expectation · whether operating conditions have shifted from those validated⟩.

**Instantiate and locate.** Governed effect: a model serving a request, and the accumulation of such
requests. **Z4** cuts all model-bound traffic.

| Fact | Status at Z4 | Cause → transformation |
|---|---|---|
| declared intended use | registry fact | none → **T1** |
| use of this call | business purpose is Z2 state; does not survive the gateway boundary | representational → **T2 fact** |
| observed performance | a property of a population, not of the call in hand | temporal → **T3** |
| conditions shifted | same | temporal → **T3** |

**Composed.** Transport a declared use-case tag from Z2 with each call; Z4 compares declared against
approved inline and accumulates per-tag outcomes for detective evaluation against the validated
baseline. Derived integrity obligation on the tag closes by **T1** at the identity layer.
**Residual.** Degradation inside the detection window; and misdeclared use that is facially approved.

## K9 — SR 11-7, change control

$I(o)$ = ⟨that this is a change to a production model · whether the change has been validated and
approved⟩.

**Instantiate and locate.** Governed effect: a changed model reaching production. **Z1** mediates all
deployments and can block release. Step 3 does real work here: Z1 must be instantiated as the component
that *gates deployment*, not one that catalogues artifacts — the distinction behind one of the two
prediction errors in §8.5.

| Fact | Status at Z1 | Cause → transformation |
|---|---|---|
| this is a change | artifact and version present | none → **T1** |
| validated and approved | a judgement rendered by a validation function outside the pipeline; no mechanism at Z1 computes it and a named party can | epistemic-renderable → **T2 verdict** |

**Composed.** A signed approval record, bound to the exact artifact, enforced as a release gate at Z1.
Derived integrity obligation is a provenance predicate, Class T, closing by **T1** at the signing layer.
**Residual.** An approval that is genuine and wrong.

## K10 — TBS Directive, notice before an automated decision

$I(o)$ = ⟨that a decision is about to be rendered about this person · whether an automated system
determines it in whole · whether one determines it in part · that notice has been given⟩.

**Instantiate and locate.** Governed effect: a decision being issued. **Z2** holds identity, session and
business object and mediates the decision path for this effect; $\alpha$ = block, escalate.

| Fact | Status at Z2 | Cause → transformation |
|---|---|---|
| a decision is imminent | present | none → **T1** |
| automated in whole | Z2 knows whether it acted on the output without human involvement | none → **T1** |
| automated in part | whether a human's judgement was materially influenced by a recommendation is a property of that person's reasoning; no party renders it, but *was the recommendation surfaced before the decision was recorded* is a defensible proxy | epistemic-approximable → **T3** |
| notice given | Z2's own state | none → **T1** |

**Composed.** Z2 refuses to issue a wholly automated decision with no recorded notice; for the assisted
case the notice trigger is the proxy, with divergence between proxy and influence monitored.
**Residual.** A decision influenced by a recommendation the proxy does not register, and the converse
over-notification.

## K11 — TBS Directive, audit trail linking decision to data

$I(o)$ = ⟨the decision points taken · system and model version · the data and information used · which
of it determined the output⟩.

**Instantiate and locate.** Governed effect: a decision being produced. Z3 holds plan, tool arguments
and intermediate outputs but cuts only SDK-mediated calls; **Z4** cuts all model-bound traffic.

| Fact | Status at Z4 | Cause → transformation |
|---|---|---|
| decision points | exist at Z3, not recoverable from a flattened request | representational → **T2 fact** |
| system and model version | present | none → **T1** |
| data and information used | retrieved context arrives as prompt text with document identity discarded | representational → **T2 fact** |
| which of it determined the output | the causal contribution of an input to an output is unavailable to any party; attribution and provenance logging are a defensible partial answer | epistemic-approximable → **T3** |

**Composed.** Z3 emits structured decision points and retrieval provenance into the trace; Z4 records
version and binds the trace to the served request; attribution stands in for causal contribution and is
labelled a proxy.
**Residual.** The trail records what was available to the decision, not what determined it. §7.6's
unstated-residual failure applies directly: a trail presented as an explanation overstates its
competence.

## K12 — TBS Directive, pre-production bias testing

$I(o)$ = ⟨evaluation data · group membership on the attributes at issue · outcome distribution by group
· whether a disparity is unfair⟩.

**Instantiate and locate.** Governed effect: a system entering production. **Z1** mediates all
deployments; $\alpha$ = block release.

| Fact | Status at Z1 | Cause → transformation |
|---|---|---|
| evaluation data | present | none → **T1** |
| group membership | protected attributes are frequently absent by design, and where held may not lawfully or organisationally be transferred into the development environment — a fact that may not cross, not a representation lost at a boundary | authority → **T2 verdict** |
| outcome distribution by group | computable once the attributes are available, in the environment that holds them | none → **T1** (in that environment) |
| unfair or not | the choice of criterion and threshold is a judgement a designated party renders, not a mechanism | epistemic-renderable → **T2 verdict** |

**Composed.** An authorised holder of the attribute data computes the disparity and returns a signed
assessment; the accountable party returns a signed acceptability determination; Z1 admits the
deployment only on both. Derived integrity obligation — the assessment must be unforgeable and bound to
the exact artifact — is a provenance predicate, Class T, closing by **T1** at the signing layer.
**Residual.** Groups absent from the attribute data; disparities on unmeasured attributes; and the
assessor's criterion choice, which the gate enforces but cannot evaluate.

---

## Predicted outcome, recorded before the independent pass

Eleven rows routed by the frozen rules; **K6** did not. No row required a transformation outside
{T1, T2 fact, T2 verdict, T3, Terminal}.
