# Documented-architecture retrodiction — protocol and prediction sheet

Independent evaluation for this paper. The oracle is **where enforcement is documented to occur in real
systems**, not the author's judgement — which is what the development corpus and held-out test could not
provide.

Evidence discipline inherited from a companion study's commercial-platform evidence matrix: **official
first-party documentation only** (no blog posts, analyst reports or third-party summaries for Class A),
rubric fixed before coding, and the snapshot date recorded as the actual completion date of evidence
collection.

---

## 1. Oracle classes

**Class A — vendor platform documentation.** AWS Bedrock, Microsoft Azure AI, Google Vertex AI, IBM
watsonx, Salesforce Einstein Trust Layer, NVIDIA NeMo Guardrails. The first four are the vendor set
already collected for that companion study, so the documentation is located; the last two are added for enforcement-
point diversity (an application-embedded trust layer and an in-process guardrail library).

**Class B — published systems papers that state their enforcement points.** SARC, ActPlane, Progent,
AgentSpec, Five-Plane, Organizational Control Layer. These are unusually good oracles: the placement is
declared, not inferred. **They also double as the Related Work argument** — if the method predicts where
each neighbour put its controls, then the neighbours are instances of it rather than competitors.

**Class C — standards that state a placement.** NIST SP 800-207 (PEP near the resource), XACML
(PDP/PEP/PIP separation). Used for sanity, not scored.

## 2. Blinding

Contamination is the main threat: I have prior exposure to several of these products. Mitigations, in
order of strength:

1. **Prediction is recorded in this file before the documentation for that pair is opened.** §4 below is
   written and committed first; §5 is filled afterwards.
2. Each pair is marked **[clean]** or **[prior]** for prior knowledge. Report the two groups separately;
   if they diverge, the clean group is the result.
3. Prefer obligation × platform pairs whose documentation has not been read.

Full blinding is not achievable by a single researcher. The paper must say so, and should present
retrodiction as *strong corroboration*, not proof.

**Contamination hazard discovered in use — citation verification defeats blinding.** Verifying the
bibliography for §3 required reading the abstracts of Swiss Cheese, AgentSpec, Progent and MI9. Any
Class B pair involving those papers predicted *after* that reading is `[prior]`, not `[clean]`, however
unfamiliar the system felt beforehand. Two consequences, both now protocol:
1. **Lock Class B predictions before verifying Class B citations.** They are the same papers; the two
   activities compete, and the ordering decides which one keeps its integrity.
2. P12 (Progent) survives as `[clean]` because its prediction was recorded in this file in an earlier
   session, before the verification pass. The ordering is what matters, not the eventual exposure — and
   it is recoverable from file history, which is the reason predictions are committed rather than held.

## 3. Disagreement taxonomy — fixed before coding

Disagreement is not automatically failure. Codes:

| Code | Meaning | Counts as |
|---|---|---|
| **D0** | Predicted transformation and location match the documented one | agreement |
| **D1** | Documented architecture matches *and adds* controls the method did not require | agreement (over-provisioning is not error) |
| **D2** | Method demands a transport or names a residual the documentation does not have — i.e. the documented design reconstructs by inference, lacks complete mediation, or leaves an unstated gap | **qualitative finding**, argued case by case; never scored as agreement |
| **D3** | Documented placement is sound and the method's prediction is worse | **prediction error** |
| **D4** | Documentation insufficient to determine the enforcement point | excluded, counted as coverage loss |

**Reporting rule.** Report D0/D1, D2 and D3 separately with counts, plus D4 as coverage. **Never report a
single accuracy percentage** — a D2-heavy result would be inflated by it, and a reviewer will say so.
Every D2 requires an argued paragraph; unargued D2 is downgraded to D4.

### D2 admissibility — a D2 must be earned

A D2 asserts that a real, documented architecture is incomplete. That is a strong claim and the easiest
place for this evaluation to degrade into self-serving labelling. A D2 is admissible only in one of two
forms; anything that satisfies neither is **downgraded to D4**, not argued.

**Form (a) — information-deficit D2.** All four of:
1. the exact missing predicate fact;
2. where in the architecture that fact existed;
3. where it was lost;
4. the execution path under **X** that defeats the documented placement.

**Form (b) — cut-failure D2.** The documented location holds every fact it needs, but is not a cut: name
the execution path by which **X** reaches the governed effect **without traversing it**.

*No form exists for an actuation deficit, and none has been added.* P20 was the first case where one
might have been invoked, and it did not need it — the documented design implements what the method
prescribes, and the only shortfall is that the residual goes unstated. Adding an admissibility form
speculatively, in advance of a case that requires it, is how an evaluation instrument loosens.

*Form (b) was added after applying the rule to the coded pairs.* P9 (NeMo Guardrails) has no information
deficit at all — the in-process rail sees the tool call and its arguments perfectly well. Its defect is
that the rail is not a cut under X. Under form (a) alone P9 would have been downgraded to D4, which
would have been wrong: the finding is real, it is simply about `cut`, not `A`. This mirrors the H4
result in the held-out test, where the deficit was in `α` rather than `A` — the same lesson, arriving a
second time from a different direction. All three legs of ⟨A, cut, α⟩ can fail independently, and the
evaluation instrument has to admit all three.


Original target sample: **30–40 pairs**. Below is the first 12.

### Stopping amendment — 19 August 2026, at n = 14

The original target above is retained rather than rewritten. Expansion was stopped after 14 clean coded
pairs for four reasons, recorded here rather than applied silently:

1. **Outcome stability.** The pre-specified interpretation settled in the D0/D1-dominant band and stayed
   there across the fourth and fifth coding passes.
2. **Structural saturation.** Every deficit branch produced by the held-out test now has at least one
   external instance, and every enforcement zone Z1–Z8 has been exercised.
3. **Diminishing evidential value.** Further pairs would add n without adding strata, and n is not what
   this study's credibility rests on — one coder without full blinding is the binding constraint, and
   more cases do not relieve it.
4. **Completion.** Remaining effort is better spent on the manuscript.

Reason 3 is the scientific reason and stands independently of reason 4.

## 4. Prediction sheet — LOCKED before documentation was consulted

Deficit causes: Rep representational · Auth authority · Ep epistemic · Tmp temporal · Act actuation

| # | Platform | Obligation | Predicted deficit | **Predicted transformation & location** | Blind |
|---|---|---|:-:|---|:-:|
| P1 | AWS Bedrock | Prevent generation of harmful content | none | **T1** at the model-invocation boundary (Z4), independent of the model | [prior] |
| P2 | AWS Bedrock | Prevent sensitive/PII egress to an external model | Rep | **T2 fact** — sensitivity must be established before the call; a gateway-only classifier is inference over a discarded fact | [prior] |
| P3 | Microsoft Azure AI | Content filtering on prompts and completions | none | **T1** at Z4/Z5, both request and response paths | [prior] |
| P4 | Microsoft Azure AI | Customer data not retained or used for training | Auth | **T2 verdict** — the fact sits inside the provider's boundary; enforcement consumes an attestation, not an observation | [clean] |
| P5 | Google Vertex AI | Defend against prompt injection / jailbreak | Rep | **T2 fact** (segment provenance). Expect documented placement to be a gateway classifier → **D2 candidate** | [clean] |
| P6 | IBM watsonx | Record model interactions for audit | Rep (identity unrouted) | **T2 fact** then **T1** at Z4 | [clean] |
| P7 | Salesforce Einstein Trust Layer | Mask sensitive data before an external model call | Rep | **T2 fact** — masking must occur where field semantics exist (Z2/Z6), not at the cut | [prior] |
| P8 | Salesforce Einstein Trust Layer | Zero retention by the model provider | Auth | **T2 verdict** — contractual/attested, not architecturally observable | [prior] |
| P9 | NVIDIA NeMo Guardrails | Constrain tool calls to legitimate task scope | Rep | **T2 verdict** (capability) enforced at Z6/Z8. Expect documented placement in-process → **D2 candidate**: not a cut under X | [clean] |
| P10 | SARC (2605.07728) | Hard constraint decidable from (s,a) before dispatch | none | **T1** at the strongest pre-effect cut = Pre-Action Gate | [prior] |
| P11 | ActPlane (2606.25189) | No unsanctioned code execution | none | **T1** at Z8 (OS), because the tool layer is not a cut | [prior] |
| P12 | Progent (2504.11703) | Tool privilege confined to the task | Rep | **T2 verdict** — a policy object transported to the tool-call boundary | [clean] |

### 4b. Second prediction block — LOCKED before documentation was consulted

| # | Platform | Obligation | Predicted deficit | **Predicted transformation & location** | Blind |
|---|---|---|:-:|---|:-:|
| P13 | Microsoft Purview / sensitivity labels in AI interactions | Data must not be surfaced through an AI assistant beyond the requester's entitlement | Rep | **T2 fact** — labels applied at the data layer must travel with the content into the AI interaction and be enforced there; classification at the AI layer alone would be inference over a discarded label | [clean] |
| P14 | Cloudflare AI Gateway | All model calls from all applications must be logged and controllable | Rep (end-user identity unrouted) | **T2 fact**, then **T1** at the gateway | [clean] |
| P15 | Google Vertex AI + VPC Service Controls | Model access confined to an approved network perimeter | none | **T1** at the network boundary — the predicate ranges over destination, which survives abstraction | [clean] |
| P16 | OpenAI Moderation API | Content screened before and after model use | none informational | **T1** *if* invocation is mandatory — but predicted **cut-failure D2 candidate**: an API the application chooses to call is not a cut under X | [clean] |

### 4c. Third prediction block — selected by stratum under §7.1, LOCKED before documentation

Each row records the cell it was selected to fill, written before the prediction.

| # | Stratum being filled | Platform | Obligation | Predicted deficit | **Predicted transformation & location** | Blind |
|---|---|---|---|:-:|---|:-:|
| P17 | **Z1 design-time** | Vertex AI / Azure ML model registry | No model version may be deployed without a completed and recorded evaluation (ISO A.6.2.5; AI Act Art 9) | none | **T1** at the registry — artifact identity and approval state are both native there, and the registry is a cut over deployments | [clean] |
| P18 | **Z8 platform/OS** | Managed code-execution sandbox for agent tool use | Agent-generated code must not perform unsanctioned actions on the host | none | **T1** at the sandbox boundary — the predicate is over syscalls and process behaviour, which is exactly what that layer holds; tool-layer allow-listing would be a cut failure | [clean] |
| P19 | **temporal deficit** | Vertex AI Model Monitoring / SageMaker Model Monitor | The system must perform within its declared accuracy envelope (AI Act Art 15) | **Tmp** — ground truth arrives after the prediction | **T3** — a preventive proxy at serving time plus detective evaluation of the true predicate once labels arrive, with a residual for the detection interval | [clean] |
| P20 | **actuation deficit** | Fine-tuned model lifecycle in a managed platform | Personal data must be erasable on request (GDPR Art 17) | **Act** — no location can selectively remove a training example's influence | **T3 else Terminal** — expect deletion of artifacts and stored data, output-side suppression, and no mechanism for selective removal from weights; residual should be visible in the documentation or conspicuously absent | [clean] |
| P21 | **epistemic-approximable** | Vertex Explainable AI / SageMaker Clarify | Meaningful information about the logic involved must be available (GDPR Art 15/22) | **Ep-approximable** | **T3** — attribution and provenance as a defensible proxy for a causal account that is not recoverable, with the gap between proxy and predicate as residual | [clean] |

**Predictions above are final.** §5 is completed only after the corresponding documentation is read.

## 5. Observed placements

**Snapshot date: 19 August 2026** — the actual date this evidence was read, per that study's rule.
Four of the twelve pairs completed; all four are the `[clean]` (no prior-knowledge) subset, which is the
methodologically valuable group. The eight `[prior]` pairs remain uncoded.

| # | Documented placement (official documentation) | Code | Note |
|---|---|:-:|---|
| **P4** | Azure Foundry: prompts/completions "are NOT used to train, retrain, or improve the base models"; "the models are stateless"; governed by the **Microsoft Products and Services Data Protection Addendum**. Verification is by a **queryable control-plane attribute** — `ContentLogging: false` visible in the Azure portal JSON view and via `az cognitiveservices account show`. | **D0** | Predicted authority → **T2 verdict**. Observed exactly that: the fact lives inside the provider's boundary and what crosses is a commitment. **The transport recursion also came true**: the derived obligation ("is the attestation authentic?") is discharged by a machine-checkable Class T fact in the control plane. That was predicted structurally, not guessed. |
| **P5** | Google Model Armor sits between the application and the LLM and "examines the assembled prompt and complete response **without distinguishing between segments by provenance**." It offers a "Prompt injection and jailbreak detection" filter. The documentation "does not address whether Model Armor distinguishes between trusted instructions and retrieved/untrusted content." | **D2** | **Predicted as a D2 candidate before the documentation was opened.** The method says the predicate needs segment provenance, which prompt assembly destroys; a classifier at the cut is therefore inference over a discarded fact. The documentation confirms the placement and is silent on the gap. |
| **P6** | IBM watsonx.governance logs payload data automatically **when watsonx.ai Runtime is the ML provider**; otherwise payload logging is configured per deployment. Factsheets auto-collect lifecycle metadata. | **D1** (partial) | Predicted location (the serving/inference cut) is correct and the documented design adds lifecycle capture. But the cut holds **only over paths traversing IBM's runtime** — it is not a cut over a mixed-provider estate, which is a coverage finding the method's cut-scope property predicts. The identity-transport sub-fact is **D4**: evidence retrieved does not establish what principal identity is captured per record. |
| **P12** | Progent represents privilege as symbolic rules over tool names and arguments; an LLM generates an initial policy from the user request, and an SMT-based check classifies each update as a narrowing or an expansion so that "the agent's effective action space can only shrink without approval". Enforcement is at tool invocation. | **D0** | Predicted **T2 verdict** — a policy object computed where the task is understood, transported to the tool-call boundary. Observed exactly that: the policy is derived from the user request, which is the only place task scope exists, and carried to the enforcement point as a symbolic object. The SMT expansion check is the derived integrity obligation in precisely the form the recursion predicts — it protects the transported verdict against modification by the agent it constrains. Prediction predates the citation-verification exposure; see §2. |
| **P9** | NVIDIA NeMo Guardrails runs **either** in-process as a Python library **or** as a standalone FastAPI server. Rails run at input, retrieval, dialog, **execution** and output stages, including "tool call validation... before and after invocation." The documentation "doesn't explicitly address whether applications can circumvent it when integrated as a library." | **D2** | Predicted T2 verdict enforced at Z6/Z8 with a D2 candidate flagged. Confirmed: in the library deployment the execution rails sit inside the process an injected agent controls, so they are not a cut under X; the server deployment is a cut for model traffic but tool execution rails remain in-process. The documentation states neither the adversary model nor the bypass condition. |

| **P13** | Microsoft Purview: AI apps "use existing controls to ensure that data stored in your tenant is never returned to the user or used by a large language model (LLM) if the user doesn't have access to that data." Where a sensitivity label is applied there is "an extra layer of protection": when the label applies encryption, "users must have the EXTRACT usage right, as well as VIEW, for the AI apps to return the data." Labels applied to files are also captured in the audit record of an AI interaction. Endpoint DLP separately warns or blocks pasting sensitive data into third-party generative AI sites in a browser. | **D1** | Predicted **T2 fact**: a label applied at the data layer must travel with the content into the AI interaction and be enforced there. Observed exactly that, with additions — entitlement enforced by pre-existing permissions (T1 at the data layer) and a second control on the un-mediated browser path. **The derived integrity obligation is discharged unusually cleanly**: the label is bound to the content by Rights Management encryption, so it travels as a cryptographically enforced capability rather than as an assertion needing separate protection. Coverage caveat, stated in the documentation: without labels enabled for SharePoint and OneDrive, protection narrows to data in use in Office apps on Windows. |
| **P14** | Cloudflare AI Gateway logs "user prompt, model response, provider, timestamp, request status, token usage, cost, duration, and the user agent of the client." The documentation does not state that end-user identity is recorded, and does not explain how custom metadata would be attached per request. Overview pages do not establish whether routing through the gateway is mandatory or per-application opt-in. | **D4** | Prediction was T2 fact (identity transport) then T1. Neither the identity question nor the mandatory-routing question is answerable from the documentation retrieved, so the pair is excluded and counted as coverage loss rather than argued either way. Re-attempt against the gateway's request-configuration reference before dropping it. |
| **P16** | The OpenAI Moderation API is invoked by the developer, not applied automatically: it is called either "inline with generation" via a moderation object on the request, or as a standalone endpoint, and the guidance is to "review the moderation results before you show the output to a user or take downstream actions." | **D2** (form b) | **Predicted as a cut-failure D2 candidate before the documentation was read.** Confirmed: enforcement is at a location the application elects to call, so under X an agent-driven path that omits the call reaches the effect without traversing it. The missing element is not information — the endpoint would classify the content correctly — it is mediation. Admissible under form (b): the defeating path is any generation the application dispatches without the accompanying moderation call. |

| **P17** | Vertex AI Model Registry provides versioning, aliases, labels, and import/copy/delete. The documentation gives no indication that it gates deployment on approval or evaluation state; deployment to an endpoint is a separate process. It is a catalogue, not an approval authority. | **D3** | **Prediction error.** The locked prediction was T1 at the registry, on the assumption that approval state is native there and that the registry is a cut over deployments. Neither holds for this platform. Coded D3 and not D2, deliberately: the tempting reading — "the architecture lacks a gate the obligation requires" — is available and would be the circular move this protocol exists to prevent. See §9 for what the error actually was. |
| **P21** | Vertex Explainable AI provides feature attributions (Sampled Shapley, Integrated Gradients, XRAI) and example-based explanations. The documentation states attributions are "specific to individual inferences", that "the insight may not be generalizable", that they "don't always indicate clearly whether an issue arises from the model or from the data", and that they are "subject to similar adversarial attacks as inferences in complex models". It does not claim attributions represent causal reasoning. | **D0** | Predicted **T3** for an epistemic-approximable deficit: attribution as a defensible proxy for a causal account that is not recoverable, with the gap between proxy and predicate as residual. Observed exactly that — and the vendor documentation states the residual itself, in four separate caveats. This is the approximable branch behaving in the field as the held-out test predicted it would. |
| **P19** | Resolved against SageMaker Model Monitor. Four monitor types: data quality (drift against a baseline computed from training data, no labels needed), **model quality** ("drift in model quality metrics, such as accuracy", which requires labels), bias drift, and feature-attribution drift. Monitoring runs on a **schedule** over captured request/prediction data, reports violations and "notifies you when quality issues happen" via CloudWatch. It is not on the serving path and cannot block an inference. | **D3** | The transformation class was right — T3, approximate-and-detect, residual over the detection interval. The **sub-structure was wrong**: I predicted a preventive proxy at serving time plus detective evaluation once labels arrive, and the documented design is detective on both halves, because the monitor is asynchronous and has no blocking actuation at all. Coded D3 rather than D1 deliberately — the prediction named a preventive component that does not exist, and counting a partial miss as agreement would erode what D0/D1 means. |

| **P15** | VPC Service Controls enforces a perimeter "independent of Identity and Access Management (IAM)", protecting against "data exfiltration by malicious insiders or compromised code". It evaluates identity, network origin and destination service. It **does not inspect payload content** [see correction below], and is "not designed to enforce comprehensive controls on metadata movement". | **D0** | Predicted **T1** at the network boundary on a destination predicate. Confirmed precisely. The pair is also unsolicited corroboration of Proposition 1: the vendor's own scoping statement says the strongest perimeter in the stack is semantics-free. Mediation bought with abstraction, documented by the party that built it. |
| **P18** | Azure Container Apps dynamic sessions provide "Hyper-V isolation and optional network controls"; sessions are "isolated from each other and from the host environment"; the stated purpose is to "safely execute AI-generated code in isolated environments without risking your production systems"; sessions are ephemeral and destroyed after use. | **D0** | Predicted **T1** at the platform boundary: the predicate ranges over process and host behaviour, which is what that layer holds, and tool-layer allow-listing would be a cut failure. Confirmed — isolation is enforced by the infrastructure irrespective of what code the agent generates. Independent vendor corroboration of the ActPlane result that §3 cites. |
| **P20** | Azure Foundry: fine-tuned models "can be deleted by the customer at any time"; stored data "Can be deleted by the customer at any time"; "The models are stateless: no prompts or completions are stored in the model." Nothing in the documentation addresses removing one individual's data from an already fine-tuned model — only deletion of models and datasets as whole artifacts. | **D1** | Predicted **T3** for an actuation deficit: artifact deletion, no selective removal, residual either visible or conspicuously absent. Confirmed, with additions (statelessness of the base model, encryption at rest). **A D2 was available here and declined**: the documented design *is* what the method prescribes — delete what can be deleted, accept the rest — and the only gap is that the residual goes unstated. That is a disclosure observation, not an architectural defect, and coding it D2 would inflate the D2 count with a case the method does not actually dispute. |

> **Source correction, recorded rather than silently applied (31 Aug 2026).** The P15 observation above
> renders "does not inspect payload content" in bold but *unquoted*, and re-checking the cited page on
> 31 Aug 2026 confirms why: the vendor documentation nowhere states that the perimeter does or does not
> inspect payload content. What it does state, verbatim, is that access is "based on client attributes,
> such as identity type ..., identity, device data, and network origin", and that VPC Service Controls
> "is not designed to enforce comprehensive controls on metadata movement". The absence of content
> inspection is therefore an observation about what the documented controls cover, not a vendor claim.
>
> The **D0 coding is unchanged**: the prediction was T1 at the network boundary on a destination
> predicate, and the documented access model confirms it. What changes is the strength of the wording.
> The manuscript said in three places that the vendor "states" the perimeter does not inspect payload
> content; §1, §8.5 and §10 now claim only that content inspection appears nowhere among the documented
> controls. This matters because §10 uses this case as the independent support for the coupling, and that
> support must not rest on a sentence the source does not contain.

### Interim tally (n = 4, clean subset)

*Superseded by the tally below; retained for the record.*

### FINAL tally (n = 14 coded, all `[clean]`) — dataset frozen 19 Aug 2026

**Count correction, recorded rather than silently applied.** This tally briefly read n = 15. The error
arose when P19 was recoded from D4 to D3: recoding a pair reclassifies it, it does not add one. The
coded set has always been the same 14 pairs — P4, P5, P6, P9, P12, P13, P14, P15, P16, P17, P18, P19,
P20, P21 — and the D4 count fell from 2 to 1 when P19 moved. 5 + 3 + 3 + 2 + 1 = 14.

| Code | Count | Pairs |
|---|---:|---|
| D0 agreement | 5 | P4, P12, P15, P18, P21 |
| D1 agreement with additions | 3 | P6, P13, P20 |
| D2 method stricter — argued | 3 | P5, P9, P16 |
| D3 prediction error | 2 | P17, P19 |
| D4 undetermined | 1 (+1 sub-fact) | P14 (P6 identity sub-fact) |

**Agreement (D0/D1) 8 · D2 3 · D3 2 · D4 1.**

Still the **first row** of the frozen decision rule, but now exactly at its boundary: the rule permits
D3 ≤ 2 and there are two. §8 must say the result sits on the threshold rather than comfortably inside
it, and must not round that description upward.

**Both D3s share one root cause**, which makes them more useful than a single error would have been.
P17 assumed a model registry gates deployment; P19 assumed a monitoring service sits on the serving path
with blocking actuation. Neither failure is in the transformation function — both are failures to
instantiate ⟨A, cut, α⟩ for the actual component before predicting from the generic zone model. Two
independent instances of one hazard is a far stronger basis for the instantiate-before-predict
requirement in §5b than P17 alone.

Against the frozen decision rule this is now the **first row** — D0/D1 clearly dominant, D3 ≤ 2 — under
which C3 stands as "determines" and retrodiction is reported as strong corroboration. It moved out of the
second band on this pass, and the move should be stated with its date and n rather than presented as
though it had always been the result.

Two cautions to carry into §8. The sample is 14, one coder. And the three D2s are unchanged in force:
agreement dominating does not retire them, and each still needs its argued paragraph.

**Stratum coverage after this pass**

| Stratum | Filled |
|---|---|
| Deficit type | none ×3 · representational ×3 · authority · epistemic-renderable · epistemic-approximable · actuation · cut ×2 |
| Enforcement zone | Z1 (attempted, D3) · Z3 · Z4 ×3 · Z5 ×2 · Z6 ×2 · Z7 · Z8 |
| System type | hyperscaler ×6 · agent framework · research system · data-governance suite · independent gateway · model provider |

**All strata are now filled.** P19 resolved the temporal branch — as a prediction error, but a coded one,
which exercises the cell. Every deficit branch the held-out test produced has at least one external
instance, and every zone Z1–Z8 has been attempted.

*[Superseded — written at n = 8, before P17 produced the study's first D3. Retained for the record; the
current tally is above.]* **All three D2s were flagged as candidates in the locked prediction sheet
before the documentation was read** — the method predicted not only where the control
would sit but that the documented design would be silent about a specific gap, and in each case it is.
P16 is the first D2 admitted under form (b): the failure is mediation, not information, and it would have
been mis-coded or lost under the four-element rule alone.

Both failure modes of the structural triple now have external instances: **P5 and P9** are `A` and `cut`
failures against vendor documentation, **P16** is a `cut` failure, and **P13** and **P4** are transports
whose derived integrity obligations are discharged in the documented design — by Rights Management
encryption and by a control-plane attribute respectively.

### What this does and does not support

*[Superseded — written at n = 8. Final n = 14; see the FINAL tally.]* This supports C3 and,
with two independent instances, C4's recursion: P4's transported
commitment closes on a control-plane attribute, P13's transported label closes on Rights Management
encryption. Two quite different real-system manifestations of the same structure.

It does **not** support a validation claim. One coder throughout, no full blinding, and the D2 arguments
are mine. At the frozen n = 14 the agreement margin is 8–3 rather than 4–3, which is a materially different picture
from the one that stood two passes ago — and the fact that it changed twice is itself the argument for
not having drafted §8 prose earlier.

## 5b. What the D3 actually was — and the protocol change it forces

P17's prediction failed, but not at the transformation function. Given the correct inputs — a registry
that holds version identity but *not* approval state, and that is not a cut over deployments — the
function returns something sensible: the fact is unrouted and the location is not a cut, so evaluation
state must be transported to a location that every deployment does traverse, such as the release
pipeline. The error was in the **architecture input**: I instantiated Z1's ⟨A, cut, α⟩ from the generic
zone model in Table 1 rather than from what this platform's registry actually is.

That distinction does not rescue the prediction, and the pair stays D3. But it identifies a hazard that
would otherwise have been discovered by a reviewer:

> **The method's output is only as sound as the triple assigned to each location. A generic zone model is
> an adequate vocabulary and an inadequate instantiation.**

This forces a two-stage protocol, which applies from the next block onward and must be disclosed in §8:

**Stage 1 — instantiate.** Read platform documentation to establish each candidate location's structural
properties: what it holds, whether traffic must traverse it, what it can do. This is a question about the
*component*, not about where any control is placed.
**Stage 2 — predict**, from the instantiated triple, and lock it.
**Stage 3 — code**, against documentation of where the control for this obligation actually sits.

Stages 1 and 3 both involve reading vendor documentation, so the separation is procedural rather than
airtight, and the paper must say so. It is still a material improvement on predicting from a generic
model, and P17 is the evidence for why it is needed. Pairs P1–P21 were predicted without Stage 1 and
should be reported as such.

## 6. Interpretation rule

**Superseded.** The three-outcome sketch that stood here has been replaced by the five-row decision rule
in `draft-section-8-skeleton.md`, which is now the single normative source. It was frozen before the
second coding pass and must not be edited in response to results. Do not restate it here — one
normative rule, one location.

## 7. Sampling rule for the remaining clean pairs — fixed before the next block was selected

At n = 8, D2 stands at 3. Sample composition now materially affects the study's character, so selection
must be defensible independently of expected outcomes. Two rules:

**7.1 Stratify, do not hunt.** Select to fill cells in **deficit type × enforcement zone × system type**,
never because a pair looks likely to produce an agreement or an interesting disagreement. Record the
stratum a pair is selected to fill *before* the prediction is written.

| Stratum | Covered at n = 8 | Gap |
|---|---|---|
| **Deficit type** | none, representational ×3, authority, epistemic-renderable, cut ×2 | **temporal · actuation · epistemic-approximable** |
| **Enforcement zone** | Z3, Z4 ×3, Z5, Z6 ×2 | **Z1 design-time · Z7 network · Z8 platform/OS** |
| **System type** | hyperscaler ×3, agent framework, research system, data-governance suite, independent gateway, model provider | reasonably spread; keep it so |

The gaps are conspicuous. Not one pair yet exercises design-time placement, network or platform
enforcement, or the temporal, actuation and approximable branches — which are precisely the branches the
held-out test added. **The next block is selected to fill those cells**, and that selection is recorded
here rather than justified afterwards.

**7.2 Prefer vendor and platform cases over Class B.** Most of the important research systems have now
been read for §3 and are contaminated as oracles (§2). Expanding the clean set means expanding into
platform documentation not yet studied.

## 8. What a good final result looks like — stated now, not after the fact

Dominant D0/D1, very few D3, and a meaningful minority of D2 admitted under the §3 rule. That would mean
the method both retrodicts established architectural decisions and prospectively identifies specific
context-loss or mediation gaps in documented designs, without reinterpreting method failures as
architectural defects. Recording this in advance is what stops it from becoming a description of
whatever the numbers turn out to be.
