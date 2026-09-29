# Corpus classification — falsification run for the context/mediation kernel

**Purpose.** Test the kernel's principal falsification risk: if nearly all real governance obligations
are Class T, the theory is a sophisticated apparatus for an edge case.

**Result: the kernel survives, and the run changed the theory.** Distribution is 15 T / 10 O (60/40),
inside the pre-agreed encouraging band, with instances of every transformation including one clean
terminal residual. More importantly, the corpus revealed that two of the three transformations are the
same transformation, and that **the transformation is a total function of the deficit cause** (§5).
That was not visible from the armchair.

---

## 1. Method, fixed before classification

**Sampling frame (268 items, enumerated before any classification):**

| Source | Items in frame | How obtained |
|---|---|---|
| EU AI Act, Ch. III §2 (Arts 8–15) + Art 50 | 9 | article list fetched from artificialintelligenceact.eu |
| ISO/IEC 42001 Annex A | 38 | full control list, A.2.2–A.10.4 |
| NIST AI 600-1 §3 suggested actions | 211 | `pdftotext` over the July 2024 PDF; count is a mechanical grep for `^(GV|MP|MS|MG)-n.n-nnn` |
| OWASP Top 10 for Agentic Applications 2026 | 10 | ASI01–ASI10 |

**Filter 1 — architectural enforceability.** Does the obligation constrain a runtime or lifecycle
*action* that traverses some path? If it is discharged by writing a document, holding a meeting, or
assigning a role, it is **Class N (non-architectural)** and outside the method's scope entirely.

**Filter 2 — NIST subsample.** Of 211 actions, a fixed keyword filter (*filter, provenance, log, access
control, human review, override, disclose, monitor, leak, watermark, label, real-time, runtime,
intervene, retention, verify*) was applied **before reading**, yielding ~40; 8 were taken.

**Location model (8 zones), fixed before classification.** Each zone is characterised only by
⟨A, cut-scope, α⟩, per the kernel §1.

| Zone | A(l) — natively available | cut-scope under X | α |
|---|---|---|---|
| **Z1** Design-time / CI / registry | code, model artifacts, evals, declared purpose | all *deployments* | block release |
| **Z2** Application & business logic | user identity, session, business object, purpose, entitlement, tenant | own app's *pre-agent* path only | block, escalate |
| **Z3** AI SDK / agent orchestration | prompt, plan, tool-call args, intermediate outputs | model+tool calls *via the SDK* | block, modify, escalate |
| **Z4** AI gateway / model proxy | prompt text, model id, tenant, caller service, tokens, destination | all model-bound traffic | block, modify, log |
| **Z5** Model endpoint / provider | prompt, output | calls to that model | refuse, filter |
| **Z6** Tool & data access layer | resource, query, data labels, caller (if propagated) | all access to that data/tool | deny, redact |
| **Z7** Network egress | destination, volume, TLS metadata | all traffic | block |
| **Z8** Platform runtime / OS | syscalls, processes, files, sockets | all execution incl. non-tool paths | block, kill |

**Adversary model X, fixed before classification:** a *prompt-injected or misdirected agent inside an
otherwise trusted application*, plus a careless user. Not a compromised host, not a malicious insider
with root. Consequence recorded up front: **Z2 and Z3 are not cuts for agent-initiated actions**, since
an injected agent emits calls that never re-enter Z2's checks and may act outside the tool layer.

## 2. Class N — the scope boundary

**24 of 38 ISO/IEC 42001 Annex A controls are Class N**, along with EU AI Act Arts 9, 11 and 13 and the
majority of NIST's 211 suggested actions. A.2.x (policies), A.3.x (roles, reporting concerns), A.5.x
(impact assessment), A.8.x (external reporting), A.10.x (suppliers, customers) have no runtime action
to mediate.

**Scope correction, recorded rather than silently applied (1 Sep 2026).** The sentence above claimed
Class N covers "the majority of NIST's 211 suggested actions". That is not a classification result. Filter
2 applied a fixed keyword filter **before reading**, admitting ~40 of the 211, of which 8 were taken into
the corpus; the remaining 171 were excluded by keyword match and were never read or coded. No Class N
determination exists for them. The claim is therefore withdrawn: what the corpus supports is that the
NIST Generative AI Profile contains **many** suggested actions that constrain no mediated architectural
action, which is how the manuscript now states it in §VI and §VIII-A. The ISO figure — at least 24 of the
38 Annex A controls — is unaffected, since every one of the 38 was enumerated and coded.

> **Recount, recorded rather than silently applied (31 Aug 2026).** The 24 was an aggregate; the Class N
> decision was never recorded per control. `artifact/data/iso42001-frame.csv` now enumerates all 38
> controls individually so the result can be checked. On that enumeration **29 of 38 are Class N**, not
> 24. The 16 controls in the families named below are Class N on the original coding and are not in
> dispute; the five controls that entered the development corpus (A.6.2.5, A.6.2.6, A.6.2.8, A.7.5,
> A.9.4) are non-N and are not in dispute either. The disagreement is confined to the 17 controls that
> were never individually recorded, of which the recount reads 13 as Class N.
>
> The recount is a **post-hoc reconstruction by the same single coder**, and its per-control titles
> should be checked against a copy of the standard before it is relied on. It is not a correction of the
> original coding, because there is no per-control original coding to correct. The manuscript therefore
> claims **"at least 24 of 38"**, which holds under both readings, rather than a precise figure that
> only one of them supports. Nothing else in the paper depends on which is right: the scope finding is
> that most of a governance standard is not architecturally placeable, and both codings say so — more
> emphatically under the recount.


This is a finding, not an inconvenience: **most of what a governance standard asks for is not
architecturally placeable at all.** The paper must say so in the scope section — it pre-empts the
reviewer who asks why the method ignores two thirds of ISO 42001, and it is a more honest framing than
implying architecture can discharge governance.

## 3. The classified corpus (n = 25)

Deficit causes: **Tmp** temporal · **Ep** epistemic · **Rep** representational · **Auth** authority · **—** none

| # | Obligation (source) | Key facts in I(o) | Strongest cut | Deficit @ cut | Class | Transform |
|---|---|---|---|:-:|:-:|---|
| 1 | Automatic event recording over lifetime (AI Act Art 12; ISO A.6.2.8) | event, time, I/O, acting principal | Z4 | end-user identity (gateway authenticates the *service*) | **T\*** | T2-fact → T1 |
| 2 | Human oversight; ability to intervene (AI Act Art 14) | action needs oversight; reviewer authority; **review was meaningful**; reversibility | Z4/Z6 | Ep + Rep | **O** | T2-verdict + T3 + **residual** |
| 3 | Disclose AI interaction / mark AI content (AI Act Art 50) | output is AI-generated; recipient is a natural person | Z4 | recipient type | **T\*** | T2-fact → T1 |
| 4 | Resist adversarial manipulation / prompt injection (AI Act Art 15) | **provenance of each context segment** (trusted vs retrieved); intended task | Z4 | Rep — prompt flattened to one string | **O** | T2-fact → T1 |
| 5 | Training/validation data quality & bias (AI Act Art 10) | dataset properties | Z1 | — | T | T1 |
| 6 | Accuracy/performance within declared envelope (AI Act Art 15) | true outcome vs prediction | Z4 | **Tmp** — ground truth arrives later | **O** | T3 + **residual** |
| 7 | AI system operation & monitoring (ISO A.6.2.6) | traffic, latency, refusals, drift signals | Z4 | — | T | T1 |
| 8 | Data provenance (ISO A.7.5) | origin of each datum | Z1 / Z6 | — | T | T1 |
| 9 | Controlled deployment (ISO A.6.2.5) | artifact identity, approval state | Z1 | — | T | T1 |
| 10 | System used only for its intended purpose (ISO A.9.4) | declared purpose; **actual purpose of this use** | Z4 | **Ep** | **O** | T2-verdict + **residual** |
| 11 | Prevent generation of CSAM/NCII/illegal content (NIST GV-1.4-001) | content properties of the output | Z4 (response path) | — | T | T1 |
| 12 | Architecture can monitor outputs, recover from anomalies (NIST MS-2.6-005) | output stream, error/anomaly state | Z4 / Z8 | — | T | T1 |
| 13 | Prevent malicious usage — manipulation, extortion, impersonation, cyber-attack, weapons (NIST MS-2.6-006) | **user intent**; real-world downstream use | Z4 | Ep + Tmp | **O** | T3 + **large residual** |
| 14 | Privacy-enhancing techniques to minimise linkage (NIST MS-2.2-004) | dataset linkage properties | Z1 | — | T | T1 |
| 15 | Real-time monitoring that provenance protocols remain effective (NIST MG-2.2-003) | provenance metadata present & valid | Z4 | — | T | T1 |
| 16 | Trace origin/provenance of AI-generated content (NIST MG-2.2-002) | generation lineage | Z1 + Z4 | — | T | T1 |
| 17 | Review generated code before downstream use (NIST MS-2.6-004) | code risk properties | Z4 | — | T | T1 |
| 18 | Override, appeal, decommission — "kill switch" (NIST MG-4.1; AI Act Art 14(4)) | operator authority; target; safety of stopping | Z4 / Z8 | minor Ep (is stopping safe) | T | T1 + minor residual |
| 19 | Agent pursues only its authorised objective (OWASP ASI01 Goal Hijack) | **user's authorised objective** vs agent's current objective | Z4 | Rep — objective not represented in the call | **O** | T2-fact → T1 |
| 20 | Tool calls stay within legitimate task scope (OWASP ASI02 Tool Misuse) | task scope; tool semantics; caller | Z6 / Z8 | Rep — scope not represented at the cut | **O** | T2-verdict (capability) → T1 |
| 21 | Agent identity & delegated privilege (OWASP ASI03) | agent identity; delegation chain; on-behalf-of | Z6 | delegation chain not propagated | **T\*** | T2-fact → T1 |
| 22 | No unsanctioned code execution (OWASP ASI05) | process is executing unsanctioned code | **Z8** | — | T | T1 |
| 23 | Memory/context integrity (OWASP ASI06) | **trust level of each memory item at write time** | Z6 (read) | Rep — labels lost between write and read | **O** | T2-fact → T1 |
| 24 | Human not deceived by agent (OWASP ASI09 Human-Agent Trust Exploitation) | **the human's belief state** | — | **Ep, irreducible** | **O** | **Terminal: declare residual** |
| 25 | Detect rogue/unregistered agents (OWASP ASI10) | registration state; behaviour over time | Z4 | Tmp (behaviour accrues) + Ep ("rogue") | **O** | T1 (registry) + T3 + residual |

**T\*** = Class T whose required facts exist but are not propagated to the cut — trivially resolved by
fact transport. Counted as T because no fact is destroyed, only unrouted.

## 4. Distribution

| | count | % |
|---|---:|---:|
| **Class T** (incl. 3 T\*) | **15** | 60% |
| **Class O** | **10** | 40% |
| — of which T2 (transport) terminating | 5 | |
| — of which T3 (approximate + detect) | 4 | |
| — of which terminal residual | 1 | |

Inside the 40–60% band set as the success criterion. All four outcomes are instantiated.

**Per-source breakdown — this is the more interesting result:**

| Source | T | O | Class O rate |
|---|---:|---:|---:|
| EU AI Act | 3 | 3 | **50%** |
| ISO/IEC 42001 (enforceable subset) | 3 | 1 | 25% |
| NIST AI 600-1 | 7 | 1 | 12% |
| OWASP Agentic (ASI) | 2 | 5 | **71%** |

**Count correction, recorded rather than silently applied (31 Aug 2026).** The NIST row previously read
6 T / 2 O (25%). The row-level coding in §3 gives seven Class T and one Class O across the eight NIST
items (#11–#18): #13 is the only NIST Class O. The likely origin of the slip is #18 ("kill switch"),
which carries a *minor* residual and was evidently tallied as O here, but which §3 codes **T** —
`T1 + minor residual` — because its facts reach the cut. The §3 coding is the frozen record and stands;
this derived table is corrected to agree with it. Source allocation is by primary citation, so the two
dual-cited items sit in one column each: #1 (AI Act Art 12; ISO A.6.2.8) counts to the AI Act, #18
(NIST MG-4.1; AI Act Art 14(4)) counts to NIST. Column totals are unchanged at 15 T / 10 O and the
NIST row still holds the 8 items Filter 2 admitted; only the split within it moves.

The correction *sharpens* the finding rather than weakening it: operational controls drawn from the
management and security standards are ISO 1/4 and NIST 1/8, i.e. **2 of 12 (17%)** Class O, against 71%
for agentic obligations. Any downstream text quoting 25% for the standards-derived controls must read
17%.

**Class O concentrates in agentic obligations and in rights-based legal obligations; standards-derived
operational controls are mostly Class T.** The reason is visible in the table: agentic risks are about
*intent, scope, objective and trust*, which are precisely the facts abstraction destroys, whereas
NIST's runtime actions are predominantly predicates over *content properties*, which survive to the
gateway intact. This is a scoping statement the paper should make explicitly — the method earns its
keep on agentic enterprise AI, and says so rather than claiming universal necessity.

## 5. What the run changed in the theory

**(a) T2 and T3(a) are the same transformation.** Every "split control" case in the corpus turned out to
be "send something from the informed location to the cut" — differing only in *what crosses*: a **fact**
(items 1, 3, 4, 19, 21, 23) or a **verdict** (items 2, 10, 20). Both create the same derived integrity
obligation on the receiving end. They should be one transformation, **Transport**, parameterised by
payload.

**(b) The payload parameter has a principled determinant.** Why would anyone move a verdict rather than
the facts? Because of the deficit cause. An **authority** deficit forbids moving the fact but permits
moving the decision. An **epistemic** deficit means no fact exists to move — only a rendered judgement.
A **representational** deficit means the fact exists and may move; it just needs a channel. The payload
is not a design preference; it is dictated.

**(c) Therefore: deficit cause → transformation is a total function.** This is the strongest result of
the run and it did not exist before it:

| Deficit cause at the strongest cut | Transformation |
|---|---|
| none | **T1** — enforce at the strongest sufficiently informed cut |
| representational | **T2 (fact)** — restore the representation across the boundary |
| authority | **T2 (verdict)** — the fact may not cross; the decision may |
| epistemic, renderable somewhere | **T2 (verdict)** — the renderer decides, the cut enforces |
| epistemic, renderable nowhere | **Terminal** — declare residual |
| temporal | **T3** — preventive over-approximation at the cut + detective true predicate after the effect; adequate iff the effect is reversible within detection latency |

The method is now deterministic given ⟨obligation, architecture, adversary⟩. That is a materially
stronger claim than "here are three things an architect might do," and it is falsifiable: one obligation
whose deficit cause does not predict its transformation breaks it.

**(d) Revised transformation set** (also fixes the naming mismatch): **T1 Relocate · T2 Transport
(fact | verdict) · T3 Approximate-and-detect · Terminal Declare-residual.**

**(e) The Move-Context recursion held on every instance.** Items 1, 3, 4, 19, 20, 21, 23 each spawned a
derived integrity obligation ("this propagated label/token/claim must be unforgeable by X"), and each
derived obligation was Class T, closed by T1 at the identity or signing layer. Seven for seven, with no
case requiring a second recursion.

## 6. Discrimination test

For each, the naïve placement a competent architect would propose, and what the method says.

| # | Naïve placement | Why the method rejects it |
|---|---|---|
| 4 | "Prompt-injection filter at the gateway." | Z4 receives one flat string. The fact the predicate needs — *which segment came from a trusted instruction vs. retrieved content* — was destroyed at prompt assembly. A classifier at Z4 is guessing at a fact that was available and thrown away. Fix the interface (structured, provenance-labelled context), then filter. |
| 2 | "Approval workflow in the application." | Z2 is not a cut under X: an injected agent reaches the SDK without re-entering Z2. Approval must be *enforced* where the action is mediated, with the verdict transported — and even then, meaningfulness of review is an irreducible residual, which the naïve design silently claims to have solved. |
| 20 | "Allow-list tools in the agent framework." | Z3 is not a cut — ActPlane's result. The agent can reach effects outside the tool layer. Scope must be transported to Z6/Z8 as a capability, not enforced where the agent runs. |
| 13 | "Content classifier at the gateway blocks malicious use." | The predicate ranges over *user intent* and *downstream real-world use*. Content is a proxy, not the predicate. The method returns the classifier **plus an explicit statement that intent is unobservable** — the naïve design's real failure is claiming coverage it does not have. |
| 10 | "Per-API-key purpose declaration." | Declared purpose ≠ actual purpose. Coarse-grained and self-asserted; residual is misuse *within* a declared purpose. Method returns it as a partial control with a named gap rather than as compliance. |
| 23 | "Sanitise memory on read." | Trust level is assigned at *write* time and lost by read time. Sanitising at read is inference over a destroyed fact; label at write and carry. |
| 22 | "Sandbox the tool executor." | Accepted — Z8 is the correct cut. **The method endorses the obvious answer**, which matters: it is not biased toward complexity. |

Rows 4, 20 and 23 share a shape worth naming in the paper: **the naïve placement tries to
*reconstruct by inference* a fact that was available upstream and discarded.** That is the single most
common architectural error the method detects, and it is not a failure of the control — it is a failure
of the interface between locations.

## 7. Threats to this result

1. **Not blind.** I designed the kernel and performed the classification. This is a *feasibility* run,
   not an evaluation. The paper's evaluation needs classification by someone who did not build the
   theory, or at minimum a pre-registered coding protocol with a second coder and an agreement statistic.
   Do not present §4's numbers as evaluation results.
2. **n = 25, one location model, one adversary model.** Changing X changes cut-scope and therefore
   changes classifications — item 22 moves if the host is assumed compromised.
3. **Source mix drives the distribution.** NIST's 211 actions are heavily process-oriented; taking more
   of them pushes toward T and N. The 60/40 figure is a property of the sample, not of governance.
   Report per-source rates (§4), never the aggregate alone.
4. **The Class N filter is a judgement call.** AI Act Art 9 (post-market monitoring) and ISO A.6.2.6 sit
   near the boundary. A different coder could move 2–3 items.
5. **§5's total function is a hypothesis generated from this corpus, not tested on it.** It must be
   tested on a *held-out* set of obligations, or it is curve-fitting. This is now the top priority.

## 8. Verdict

The falsification risk the kernel identified did not materialise: 40% Class O, concentrated in exactly
the obligations enterprises currently care most about (agentic scope, objective, oversight, purpose),
and the method both rejects plausible-but-wrong placements and endorses the correct obvious one.

**Recommendation: commit to this paper.** Before drafting, run §7.5 — a held-out corpus of 10–15 further
obligations, classified against the §5 function, to confirm the deficit-cause → transformation mapping
predicts rather than merely describes. If it holds, that mapping is the paper's central table and the
contribution is considerably sharper than the one we set out to make.
