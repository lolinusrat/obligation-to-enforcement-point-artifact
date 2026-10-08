# Worked placement records

Two complete placement records for the examples worked in the paper, filled in
field by field with `apply-the-method.md`. They restate the paper's own analysis
(§II, §VI's running example and §VII‑D, Table 4); nothing here is a new result. Where the paper does not
state a field, the record says so rather than supplying one.

Field order follows step 7 of the procedure and the Governance Placement Record
fields of §VII‑A: ⟨S, X⟩, the selected cut, each missing fact's cause, the transported facts
or verdicts, their integrity bindings, any approximation and detection controls,
and the residual.

---

## Record 1 — Purpose limitation at the data access layer (paper §VII‑D, Table 4)

| Field | Entry |
|---|---|
| Obligation *o* | Personal data must not be further processed in a manner incompatible with the purpose for which it was collected. |
| Filter (step 1) | Constrains a mediated action — retrieval of a record and its inclusion in a prompt. Not Class N. |
| Governed effect, scope *S* | Processing of *this* personal data on the modelled retrieval paths. |
| Adversary *X* | The agent adversary of §V‑A. |
| *I(o)* (step 2) | (1) record is personal data; (2) collection purpose; (3) current processing purpose; (4) compatibility of the two. |
| Candidate locations (step 3) | Gateway **Z4**; data access layer **Z6**; other zones of Table 1 (none is a cut for this effect in the modelled pipeline). |
| Adequate cuts (step 4) | Before *S* is pinned, neither Z4 nor Z6 dominates. Once *S* is pinned: every governed path traverses Z6; some (an export, a report) bypass Z4. **Z6 is the unique maximal adequate cut** among the instantiated candidates. |
| Selected cut | Z6. |

**Per-fact diagnosis at Z6 (steps 5–6; paper Table 4)**

| Fact | Status at Z6 | Cause | Transformation |
|---|---|---|---|
| record is personal data | available (data labels) | none | **T1** — enforce here |
| collection purpose | absent from the served record | representational | **T2 fact** — collection-purpose label carried with the data |
| current processing purpose | absent; rendered in the requester's business context | epistemic-renderable | **T2 verdict** — purpose attestation carried with the request |
| compatibility of the two | policy, once both are present | none | **T1** — Z6 decides |

| Field | Entry |
|---|---|
| Composition (step 7) | Z6 evaluates compatibility using the transported collection-purpose label and the purpose attestation. The attestation states that this request is made for a stated purpose; it is **not** the compatibility decision, which Z6 makes itself. |
| Why a verdict, not a fact | Deciding which of the organisation's defined purposes this use serves needs the business context. Where the purpose is already a stored value (e.g. a purpose code fixed on a case file), carrying it is a transported **fact** instead. |
| Integrity bindings (derived obligations *o′*, §VII‑E) | Both transports create derived integrity obligations; here Class T, closing by T1 at the signing and identity layers. |
| Approximation / detection | None. |
| Residual | Processing for a purpose other than the one declared remains outside this cut; reuse of a copy already retrieved does not pass Z6 again. The placement enforces purpose limitation **at retrieval**, not over every downstream copy. |
| Mediation deficit | None (an adequate cut exists). |

---

## Record 2 — Disclosure of commercially sensitive information (paper §II, §VI running example)

| Field | Entry |
|---|---|
| Obligation *o* | Commercially sensitive information must not be disclosed to an externally hosted model unless the requester has a legitimate business purpose for the disclosure. |
| Filter (step 1) | Constrains a mediated action (an external-model call). Not Class N. |
| Scope *S* and adversary *X* | Model-bound disclosures in the modelled architecture, including calls initiated directly by agents; adversary of §V‑A (an agent acting on injected instructions). |
| *I(o)* | Sensitivity in context; requester identity; purpose; entitlement; externality of the destination. |
| Candidate locations | Network boundary; model provider; application; AI gateway. |
| Why not the others (§II) | **Model provider:** sees the prompt, but not which enterprise data is sensitive, the requester's role or entitlements. **Application:** holds the business purpose but is bypassable under §V‑A. **Network boundary:** a broader cut — it also covers governed paths that the strongest adversary of §X can open around the gateway — but it sees only traffic. The worked design selects the gateway because it can inspect the request and act on the transported information. This is an operational judgement, not a unique placement derived by the deficit-cause rule (paper §II, §X). |
| Adequate cut | **AI gateway** — under the stated architectural assumption that all relevant external-model calls, including agent-initiated ones, traverse it (an assumption, not a general property of gateways). |
| Status at the gateway | Of the five facts only destination externality is available. |

**Per-fact diagnosis at the gateway (paper §II and §VI running example)**

| Fact | Status at the gateway | Cause | Transformation |
|---|---|---|---|
| externality of the destination | available | none | **T1** — enforce here |
| sensitivity in context | label dropped when the record was served | representational | **T2 fact** — label carried with the data, one per record, bound to its segment; the gateway checks every labelled segment and fails closed on any segment unlabelled or whose label cannot be verified |
| requester identity and entitlement | authoritative identity-provider records that may cross but are not carried | representational | **T2 fact** — a claim signed by the identity provider, which the application may relay but cannot alter |
| purpose | only the requester's business context can judge it | epistemic-renderable | **T2 verdict** — purpose attestation carried with the request |

| Field | Entry |
|---|---|
| Composition | The gateway verifies the sensitivity label, the identity claim and the attestation, including their issuers and their bindings to the requester and the request, then applies the disclosure policy to the attested purpose, the claimed entitlement, the sensitivity label and the destination. |
| What the verdict does not establish | A valid attestation establishes the accountable component's judgement; it does not independently establish that the requester's underlying declaration was truthful. |
| Integrity bindings (derived obligations *o′*, §VII‑E) | Label bound to the data; identity claim and attestation bound to the requester and the request. |
| Approximation / detection | None stated. |
| Residual | A purpose falsely asserted upstream of the binding point; a correctly bound but **wrong** label, or a validly signed but out-of-date entitlement record (binding protects against tampering, not error). |
| Correction note | Preprint v1.0.0 had entitlement evaluated in the application and attested inside the purpose attestation, without diagnosing its cause. Applying the paper's own test (authoritative upstream value that may cross → representational) moved it to fact transport in v2. The obligation, scope and adversary are unchanged; the residual gains the identity provider's records. No reported result depends on this example. |

---

## Situations the worksheet asks you to decide (with the paper's rule)

| Situation | What the paper says | Where |
|---|---|---|
| Evidence about a component's properties is missing or only nominal | Establish properties from what the component does, not from its category name (Instantiate). Both retrodiction errors came from wrongly attributed properties; Instantiate mitigates rather than removes this. Record the assumption. | §VII‑A step 3; §X |
| A fact is observed but stale, misbound or untrusted | It is not in *A(l)* until its trust assumptions are met; its shortfall is closed by a derived integrity obligation. | §V‑E; §VII‑E |
| More than one cause applies to the same fact | The record lists every cause, and the transformation must satisfy all their constraints. | §V‑E |
| Several adequate cuts are candidates | Where none is feasible, diagnose the deficits at the maximal adequate cuts; where several are incomparable, operational considerations choose among them, and the choice is recorded. The paper does not provide a complete rule when cuts differ in coverage and in their ability to act on transported information; §II's gateway choice is such a judgement, disclosed as a limitation. | §V‑D "Selecting the cut"; §VII‑A step 4; §II; §X |
| No adequate cut exists | Report a mediation deficit; Table 3 has no row; record it separately as a method-coverage limitation, not as an enforcement residual. | §VII‑A step 4; §VII‑F |
| The fact concerns model-generated content | Upstream labels may not adequately represent the generated output; treat the label's adequacy as an assumption to record. | §X |
| Representational vs authority vs renderable | Authoritative upstream value that may cross → representational; exists but may not cross → authority; needs a judgement some party can render → epistemic-renderable. The approximable/unrenderable boundary is whether a defensible proxy *and* a detection control exist, as judged by the analyst — a judgement, not a mechanical test. | §V‑E |
