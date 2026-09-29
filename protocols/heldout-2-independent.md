# Held-out set 2 — independent pass

What the architecture should be for each of the twelve obligations, argued from the obligation and the
estate rather than from Table 3. Written after the prediction pass was sealed and without reopening it.
The separation is procedural, not cognitive: one analyst wrote both, and this pass cannot be read as a
second coder's answer. It can be read as an answer that was not permitted to revise the first.

---

**K1 — limit the number and rate of model queries.** Quotas belong at the gateway, since that is the
only place all model-bound traffic is visible and refusable. The unit matters more than the mechanism:
quotas enforced on the calling service's credential are close to useless against extraction, because a
shared service account makes one bucket out of every user behind the application. The gateway therefore
has to be given the acting end-user's identity, propagated from the application as a delegated
assertion, and count against that.

A rate limit is also a poor instrument for what the mitigation is for. Extraction conducted slowly, or
spread across identities, is inside any quota an ordinary workload can live with. A defensible design
adds detection of extraction-*shaped* query distributions — coverage of the input space, boundary
probing, near-duplicate sequences — as a detective layer behind the preventive quota, with the
understanding that the detector is a proxy for an intent no one can observe. I would ship both, and I
would state that the quota is a cost multiplier rather than a control.

**K2 — sanitize training data.** Filter at ingest on what can be checked: source allowlists and
provenance, near-duplicate and known-trigger detection, outlier analysis against the established
distribution. None of these decide whether a sample is poisoned; they narrow the population that
reaches training. Behind them, evaluate each trained checkpoint against a held-back benign baseline and
a set of trigger probes, and keep the previous checkpoint promotable, so that a poisoning that survives
the filter is caught by its effect and reversed. For an online model the same pair applies per update,
and the detection latency is what determines how much damage an accepted sample can do. What no design
here achieves is a decision, per sample, about poisoning; that has to be written down as accepted.

**K3 — detect and block adversarial inputs.** A detector at the gateway is right, and is not enough by
itself, because by the time the request arrives the prompt is one flat string and the detector cannot
tell an instruction the user typed from one that arrived inside a retrieved document. The orchestration
layer knows that distinction and must carry it forward — structured segments with provenance, rather
than a concatenated prompt — so the gateway can weight or refuse instruction-shaped content in
untrusted spans. The detector itself is a classifier over content standing in for the sender's intent
and will be wrong in both directions; the residual is that, plus injected instructions arriving in spans
the architecture regards as trusted.

**K4 — bind and sign provenance on release.** The assertions exist where the asset is produced and
edited, and nowhere else; egress sees bytes. So the manifest has to be built and signed at the point of
production and travel with the asset, and the egress path enforces that governed asset types do not
leave without one that validates. The signature is not decoration: it is what makes the manifest usable
by a party that does not trust the pipeline, and without it the transport has moved a fact that the
recipient has no reason to believe. Assets leaving by a path the egress control does not see are outside
this design, and so is the gap between what the pipeline asserts and what is true.

**K5 — validate provenance on ingest.** At ingest, check the signature, check that the hard binding
still matches the bytes, and check the signer against a trust list. All three are local decisions. The
part that is not local is whether the assertions are *true* — that a camera captured this, that this
model generated it. Nothing at the ingest point can establish that, and nothing needs to: the design
relies on the signer's assertion and inherits exactly as much confidence as the signer deserves. That
should be explicit, because it is where the whole scheme rests. Two things stay outside: a trusted
signer that lies, and an asset with no manifest at all, which is not evidence of anything.

**K6 — provenance survives downstream handling.** Nothing the producing estate controls touches the
asset once a third party has it. There is no gate to place. What is left is to make the loss
*recoverable*: register a perceptual fingerprint of the asset alongside its manifest so a stripped copy
can be matched back, and watermark the content so that a claim of provenance can be re-asserted from
the pixels. Both are approximations — fingerprints fail under heavy transformation, watermarks are
removable by anyone who cares — and neither prevents stripping. The honest architecture is the
approximation plus a stated residual: provenance is preserved against ordinary handling and not against
an adversary, and any assurance framed as "provenance survives" overstates it.

**K7 — model inventory completeness.** The gateway is where a model call can be checked against the
inventory, so the inline control is there: refuse calls to models that are not registered. But the
control this obligation is actually reaching for is the model nobody registered, and that model is
reached by not using the gateway at all. So the gateway check has to be paired with a network-layer
rule that permits model-bound egress only through the gateway; otherwise the inventory is a list of the
models that are already known. The network layer cannot tell which model is being called — that is
exactly why it is a routing rule rather than a policy decision — and the two halves together are what
makes the inventory complete.

**K8 — ongoing monitoring.** Two questions are being asked at once. *Is this model being used as
intended* is answered by making the intended use visible at the point of use: the application declares
a use-case with each call, the gateway compares it against what was approved for that model, and a call
outside the approved envelope is refused inline. *Is the model still performing* cannot be answered at a
call at all; it is a property of a population over time, so it is measured behind the serving path
against the validated baseline, per declared use-case, and it triggers review rather than blocking.
The declared use-case is an assertion by the application, so a misdeclaration that is facially approved
passes; and anything degrading inside the monitoring interval is served before it is noticed.

**K9 — change control.** The deployment path is the gate — the component that actually promotes an
artifact to production, which is not necessarily the one that catalogues artifacts. It admits a
promotion only against an approval record that is signed, that names the validator, and that is bound to
the exact artifact digest being promoted, so that an approval cannot be reused for a different build.
The pipeline cannot evaluate whether the validation was any good; it can only establish that the
accountable party performed it on this artifact.

**K10 — notice before an automated decision.** The application is the only place that knows a decision
about a person is being issued, and it is where the notice has to be gated: no wholly automated
decision leaves without a recorded notice event. The awkward half is "in part". Whether a caseworker's
judgement was actually shaped by a model's recommendation is not observable, so the trigger has to be
something that is — the recommendation having been generated and surfaced to the decision-maker before
the decision was recorded. That over-notifies where the recommendation was ignored and under-notifies
where influence arrived by some other route, and the gap between the trigger and the thing it stands for
should be monitored rather than assumed away.

**K11 — audit trail linking decision to data.** Versions and timestamps are easy and belong wherever
the request is served. The two hard parts are that the orchestration layer's decision points — which
tools ran, with what arguments, what came back — are gone by the time a request reaches the gateway,
and that retrieved context arrives as prose with the identity of the source document discarded. Both
have to be emitted as structure from the layer that still has them and bound to the served request, or
the trail records that a decision happened without recording what it was made of. The fourth thing the
directive asks for — which of that data the decision was *based on* — is not recoverable. Attribution
gives a defensible partial answer. A trail that presents itself as an explanation, rather than as a
record of what was available, claims more than it has.

**K12 — pre-production bias testing.** The measurement cannot be done where the model is built, because
the attributes it needs are usually not there, and often may not be moved there. So the assessment goes
to the party that legitimately holds them: they compute the disparity in their own environment and
return a signed result. Release is gated on that result plus an explicit determination, by whoever is
accountable, that the disparity is acceptable — the second is a judgement and should be recorded as one
rather than encoded as a threshold in a pipeline. What the gate cannot reach: groups the attribute data
does not cover, disparities on attributes nobody measured, and the choice of criterion itself, which the
gate enforces without being able to assess.
