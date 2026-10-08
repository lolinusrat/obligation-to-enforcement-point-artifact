# Independent Reproducibility Study — protocol

Inter-rater study of whether architects other than the author can apply the
deficit-driven placement method and reach the same diagnosis. Addresses the
limitation §VIII.3 and §X state plainly: every prediction, documentation reading
and coding in the current evaluation was performed by the same researcher.

> ## ⚠ ETHICS-GATED — NOT PART OF THE PUBLISHED STUDIES
>
> **This protocol is specified and not run.** The gate below must close first.
>
> **Why, and why this matters more here than it looks.** On 2026-08-12 the
> equivalent study for a companion paper was deferred on the reasoning that its
> publisher's author guidance requires authors to indicate at submission whether
> approval was obtained from a review board when an article reports research
> involving human subjects, and that the venue published no track-specific exemption
> for expert studies. That reasoning applies to this study *with greater force*,
> not less. That paper's deferred instrument collected Likert ratings; this one
> assigns predefined tasks to identifiable professionals, computes inter-rater
> agreement statistics, and reports the result as a fourth evaluation study.
> That is more clearly human-participant research, not less.
>
> **The ordering constraint is the hard one.** A determination obtained after
> collection cannot retrospectively cover data already gathered. If responses
> are collected before the gate closes, they cannot be used in the paper at all
> — the work is not merely delayed, it is wasted.
>
> **Informal formative feedback remains available and is unaffected.** Showing
> the method to an experienced architect and asking whether a diagnosis makes
> sense is ordinary practice. If it surfaces a genuine weakness, the method is
> revised on its merits. What must not happen is presenting those conversations
> as a study: no dataset, no agreement statistic, no "participants", no reported
> responses as empirical results.

## Ethics gate

Complete before any invitation is sent.

- [ ] Determine whether the author's circumstances require human-participant
      ethics review, an exemption, or a formal determination of
      non-applicability. Do not assume exemption.
- [ ] Check the target venue's stated expectations for human-participant studies,
      including any disclosure required at submission.
- [ ] Confirm what participants are told before responding: purpose,
      voluntariness, what is collected, storage, reporting, withdrawal.
- [ ] Confirm retention and anonymization for raw responses.

**Data minimization.** Names, employers and email addresses are not part of the
research dataset. Contact details, if used for distribution, are held separately
and never linked to responses.

## What this study measures — and why it is worth gating for

Not whether architects like the method. Whether they **reproduce its reasoning**.

Three agreement levels, reported separately because they are not equally hard:

| Level | Question | Expected difficulty |
|---|---|---|
| **L1 Classification** | Is the obligation N, T, or placement-obstructed? | easiest — should be high or the method is not teachable |
| **L2 Deficit cause** | Which cause applies to each missing fact? | the substantive test; this is where the method's content lives |
| **L3 Transformation** | Which transformation follows? | mechanical *given* L2, so L3 agreement conditional on L2 agreement is the number that matters |

**The conditional statistic is the point.** High L3 agreement alone proves little
— Table 3 is a lookup. High L3 *conditional on* independently-reached L2 shows
the function is applied consistently rather than guessed. Report
`P(L3 agree | L2 agree)` alongside raw agreement.

## Design

**Participants.** Approximately **3–5** practising software or AI architects with
enterprise experience, with a target of at least three completed evaluations. Not
students. Not co-authors. Report count, not identities. Three is the floor set
under "What counts as a result" below, not a target to be trimmed: below three
there is no study, only formative feedback. Above three, an additional
participant is included rather than excluded — every participant receives the
same five cases, so each one adds an independent judgement of every case.

**Materials** (the pack, built separately):
1. Method summary, two pages: classes, deficit causes, Table 3, composition rule.
2. The Z1–Z8 zone model with ⟨A, cut-scope, α⟩ per zone.
3. The adversary model, stated explicitly — the method is undefined without it.
4. The "Apply the Method" worksheet: obligation → I(o) → candidate locations →
   ⟨A, cut, α⟩ → deficit → cause → transformation → composition → residual.
5. **The same five obligations for every participant**, with the source text.
   Not split across participants: agreement is only measurable where each case
   is judged independently by everyone.

**Obligation selection, fixed before recruitment.** Stratified over deficit cause
so the instrument cannot accidentally test only the easy branches: at least one
each of no-deficit, representational, authority, epistemic and temporal. Drawn
from the held-out sources, not the development corpus. The five selected are
recorded in `sealed/AMENDMENT-2026-08-20.md` with their mapping to the sealed
key; that mapping must be used when responses are scored.

**Author's coding sealed first.** The author's own diagnosis for each obligation
is recorded and hashed before any pack is sent. Without this the study measures
agreement with a moving target.

**Statistic.** Percentage agreement and Krippendorff's α per level, with the
conditional statistic above. With 3–5 raters over five cases — 15 to 25 codings
per level — report α with its interval and resist reading precision into it.

## What counts as a result — decided in advance

| Outcome | Reading |
|---|---|
| L2 agreement high, L3 conditional high | The method is reproducible by others. §VIII.3's limitation is answered directly. |
| L2 moderate, L3 conditional high | The function is applied consistently but diagnosis is the hard step — a real finding, and one that says where the method needs better guidance. |
| L2 low | The method depends on the author's judgement more than the paper claims. This must be reported as such, and C3's precondition widened accordingly. |
| Any outcome with n < 3 | Not reportable as a study. Formative feedback only. |

Deciding this now is what stops a weak result from being written up as a
qualified success.

## Threats specific to this design

- **Training effect.** Participants read a method summary written by its author.
  Agreement partly measures the clarity of that summary, not the method. Say so.
- **Small n.** Three to five raters over five cases cannot support strong claims.
  The study answers "can anyone else do this at all", not "how reliably".
- **Reduced branch coverage.** Actuation is no longer exercised by any case, and
  the epistemic-approximable branch is reached only via the temporal case. No
  claim may be made about participants reproducing those branches. See
  `sealed/AMENDMENT-2026-08-20.md`.
- **Self-selection.** Architects who agree to spend half an hour on a placement
  method are not a random sample of architects.
- **Anchoring.** The worksheet's ordering suggests the method's own reasoning
  path. That is intended — it is the method — but it means the study tests
  application, not discovery.

## Amendment 2026-08-20 — eight cases reduced to five, before recruitment

The participant instrument now carries five cases rather than eight, given
identically to every participant, and runs approximately 30–35 minutes rather
than approximately an hour. Cases 5, 6 and 8 of the sealed key are
withdrawn prospectively from the instrument and preserved as research records.

The full amendment — the pack-to-key case mapping, the rationale, the coverage
that is retained, and the two branches that are no longer tested — is recorded
in `sealed/AMENDMENT-2026-08-20.md`. The sealed answer key itself is unchanged
and its SHA-256 still verifies against `sealed/SEAL.txt`.

This is a pre-recruitment amendment. No invitation had been sent and no response
collected for any version of the pack, so no participant has seen either the
eight-case or the five-case instrument.

## Status

Specified 19 Aug 2026. Amended 20 Aug 2026 (eight cases to five) and 5 Sep 2026
(instrument redesigned around two diagrams, five cases reduced to four, and
"cannot determine" added as a third response state — see
`sealed/AMENDMENT-2026-09-05.md`). Not started. No invitation sent, no
response collected.
Everything above is preserved for the point at which the gate closes, at which
stage this becomes the fourth study and §VIII.3's limitation can be answered
rather than only stated.
