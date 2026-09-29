<!-- Anonymised snapshot of the submitted manuscript source.
     Written by build_paper4.py; read by verify.py. Do not edit. -->

::: {custom-style="PaperTitle"}
From Obligation to Enforcement Point: A Deficit-Driven Method for Placing AI Governance Controls in Enterprise Architectures
:::




::: {custom-style="Abstract"}
***Abstract*—** Enterprises deploying AI systems have no shortage of governance obligations, but regulations and standards stop short of the step an architect must take: deriving an obligation's enforcement architecture — where enforcement should occur, what information must cross architectural boundaries, and what remains unenforceable. We identify a recurring tension behind this decision: locations with broad enforcement coverage typically operate through general interfaces that abstract away the application-specific state — such as purpose, entitlement, objective, and contextual sensitivity — needed to evaluate context-dependent obligations. We call this mediation–abstraction coupling. From this observation, we develop a deficit-driven placement method. After establishing what candidate locations actually know, mediate, and can do, the method diagnoses why an obligation cannot be enforced at an adequate enforcement point and derives the corresponding architectural transformation: enforce locally, transport a fact, transport a verdict, approximate and detect, or declare a residual. The resulting enforcement architecture is the composition of these transformations. We evaluate the method through four studies: a development corpus drawn from regulation and standards, a held-out applicability study, a pre-specified test of twelve obligations from sources excluded from method development, and fourteen cases drawn from documented enterprise AI systems and platforms. The pre-specified study routed eleven of twelve obligations; the remaining obligation had no adequate enforcement cut and exposed a case the method does not yet route. Across the documented cases, eight architectures agreed with or extended the method's prediction, three exhibited pre-specified gaps, two contradicted it, and one was undetermined. These results provide external corroboration rather than independent validation.
:::

::: {custom-style="Abstract"}
***Index Terms*—** AI governance, software architecture, enterprise AI, policy enforcement, agentic AI.
:::

# I. Introduction

Enterprises deploying AI systems do not lack governance requirements. The EU AI Act [@aiact], the NIST AI
Risk Management Framework [@airmf] and its Generative AI Profile [@nist6001], and ISO/IEC 42001
[@iso42001] collectively provide regulatory obligations, risk-management guidance, more than two hundred
suggested actions, and a control annex addressing concerns including logging, human oversight,
transparency and robustness. What none supplies is the step an architect actually has to take: given an
obligation, derive the enforcement architecture — where it should be enforced, what information must
cross architectural boundaries, and what remains unenforceable. That step is left to judgement, and it is
not a small one. A single obligation can plausibly be enforced in the application, an agent framework, an
AI gateway, the model endpoint, the data access layer, the network boundary, or the platform runtime —
and these are not interchangeable.

They are not interchangeable for a reason that is easy to state and easy to miss. Take the obligation
that commercially sensitive information must not be disclosed to an externally hosted model unless the
requester has a legitimate business purpose. It needs five facts: sensitivity in context, requester identity,
purpose, entitlement and externality of the destination. In the architecture considered here, the
locations with the broadest mediation hold only the last. §II works the case through.

We argue that this is not only an artefact of immature tooling. A location mediates many paths because
those paths share a general interface, and that generality tends to be achieved by abstracting over what
differs among the applications that share it — including purpose, entitlement, objective and contextual
sensitivity (§IV). Google's network service perimeter illustrates the point: its
documentation describes decisions on client attributes and destination service, and lists no content
inspection among the perimeter's own controls [@vpcsc].

We therefore ask: **how should architects resolve the tension between semantic decision context and
enforcement strength when allocating governance controls across enterprise AI architectures?** And when
no location offers both, what determines whether the obligation is resolved by enforcing elsewhere,
transporting a fact or verdict, approximating and detecting, or declaring part of it unenforceable?

Existing work supplies much of what surrounds this question (§III): layered guardrail architectures
[@swisscheese], complete mediation [@saltzer], reference monitors [@anderson], and the separation of
decision from enforcement in XACML [@xacml] and zero trust architecture [@zta]. Those route
policy-relevant attributes to a decision function; a semantic AI obligation may instead depend on a fact
lost through abstraction, a judgement the enforcement point cannot render, information not yet available,
or information that may not cross an organisational boundary. SARC [@sarc], the closest methodological
antecedent, compiles constraints to four enforcement sites in an agent loop; we generalise to a
heterogeneous enterprise estate, and from constraint class to the *cause* of the placement deficit.

We make five contributions. Two explain the problem: *mediation–abstraction coupling*, a mechanism
explaining why information and enforcement strength come apart, stated as a coupling rather than a law;
and a classification of obligations as non-architectural, transparent or placement-obstructed, applied to
a purposive corpus of governance obligations. Three form the method: the *Deficit-Cause Principle*, under
which the cause of each deficit, rather than the obligation's class, determines the class of architectural
transformation; compositional placement, including a transport recursion in which transported facts or
verdicts create derived integrity obligations; and the residual as a first-class output, so that the
method states explicitly what the architecture cannot enforce.
The method is intended to be applied obligation by obligation and to produce an explicit placement record: where enforcement
occurs, which facts or verdicts must cross boundaries, what integrity dependencies those transports
create, and what remains unenforced.
In evaluation, a pre-specified study routed eleven of twelve obligations from sources that played no
part in the method's development. Across fourteen documented cases, eight architectures agreed with or extended the method's prediction, three exhibited pre-specified
gaps, two contradicted it, and one was undetermined. These results provide external corroboration rather
than independent validation.

# II. A governance obligation and four plausible places to enforce it

An enterprise adopts a policy that reads, in full:

> *Commercially sensitive information must not be disclosed to an externally hosted model unless the
> requester has a legitimate business purpose for the disclosure.*

It sounds like a filtering problem, and enterprise AI stacks offer several places to filter. Each is
plausible and each fails differently. Two provide broad mediation but little of the decision context the
obligation requires. **The network boundary** can block traffic before it leaves: it may know the
destination, but not whether the request constitutes a prohibited disclosure. **The model provider** sees
the prompt in the clear and offers content filters, but has no view of which enterprise data is
sensitive, of the requester's role, or of the entitlements that would make a disclosure legitimate; it
recognises categories of content, not *this* customer's unreleased pricing.

Two are closer to the context, and neither is sufficient alone. **The application** is where "legitimate
business purpose" is available, but it is a weak enforcement point under the adversary model of §V‑A:
applications may implement the check differently or not at all, and an agent acting on injected
instructions can reach the model without passing back through the application-level check. **The AI
gateway** is a strong candidate — model calls within the governed path traverse it and it sees the prompt
text — but it does not know whether that text is sensitive *in this context*, who is really asking, or
why. A
classifier there reconstructs facts that were available upstream but were not carried across the
architectural boundary. The network boundary is at least as strong a cut but sees only traffic; choosing
between equally strong cuts is an operational judgement (§V‑C), and here it favours the gateway, which can
read what travels inside the request. Of the five facts the obligation needs, only destination externality
is available at the broadly mediating locations; the rest must be inferred, asserted or transported.

The derived architecture is therefore not a filter in one place. Sensitivity travels
with the data, while purpose is rendered where the business context is available and travels with the
request as a verdict. The purpose verdict is bound to requester identity and entitlement, and the gateway
combines these facts with destination externality to enforce the obligation. Transport creates a second, smaller
obligation: each transported fact or verdict must be bound to what it describes. The architecture still leaves a residual: it cannot verify a purpose that is falsely asserted upstream
of the binding point.


None of this is exotic. What is missing is a way to reach it that does not depend on the architect
already knowing the answer: §IV explains why facts and enforcement points come apart, §§V–VI formalise
the gap, and §VII turns the diagnosis into an architecture.

# III. Related work

## A. Obligations without placements

Regulation and standards supply this paper's input and stop short of its question. The EU AI Act
[@aiact] states requirements for risk management, logging, transparency, human oversight and robustness;
the NIST AI Risk Management Framework [@airmf] and its Generative AI Profile [@nist6001] express
outcomes and suggested actions; ISO/IEC 42001 [@iso42001] defines an AI management system. None
prescribes an enterprise technical architecture, and many of their obligations are not architecturally enforceable (§VI, §VIII‑A). Work translating these obligations into engineering terms includes mappings from AI Act requirements to
verification activities [@buscemi] and audit-evidence schemes such as CEDAR-42001 [@cedar]. These
approaches produce assurance artifacts rather than enforcement locations.

The Responsible AI Pattern Catalogue [@raipatterns] is the most systematic attempt to operationalise
responsible AI at the system level, organising governance, process and product patterns; it answers
*what to build*, not which of several competing locations should host a given obligation.

Koch's layered translation method [@koch] goes furthest towards placement. It carries standards-derived
objectives through design-time constraints, runtime mediation and assurance feedback, using a rubric that
reserves runtime guardrails for controls sufficiently observable, determinate and time-sensitive to
justify execution-time intervention. That is a placement criterion, and we treat it as such. Koch
assigns each objective to one or more of these layers, scoring it on six dimensions that include timing of
harm, reversibility and evidence clarity.
Our method instead derives an architecture across heterogeneous enforcement locations from the cause of
each deficit, returning transport, composition or an explicit residual rather than a lifecycle layer.

## B. Architecture and security foundations

Two ideas we rely on are long settled. Complete mediation [@saltzer] and the reference monitor
[@anderson] establish that an enforcement point is only as good as its unbypassability; §V‑C restates unbypassability as a *cut* — a location that every path available to the adversary
traverses — and generalises it from a single system to an estate, where coverage becomes a variable rather
than an assumption. The separation of decision from enforcement is standardised in XACML and central to zero trust
architecture; §IV‑C sets out why that inheritance does not settle the present question. The form of our
contribution is likewise inherited: quality-attribute-driven design and architectural tactics [@bass]
established the pattern of deriving design decisions from requirements under stated trade-offs, and we
claim novelty in content, not form.

## C. Agent runtime enforcement

Agent runtime enforcement is the closest active body of work, and it has matured beyond preprints. AgentSpec [@agentspec] provides a
language of triggers, predicates and enforcement actions evaluated at runtime events such as an
impending action; Progent
[@progent] represents privilege as symbolic rules over tool names and arguments, with an SMT check ensuring that, without approval, an agent's action space can only narrow; and MI9 [@mi9], the Organizational
Control Layer [@ocl] and five-plane runtime architectures [@fiveplane] each propose enforcement
machinery for production agents. These approaches instantiate constraints at predetermined runtime boundaries — such as tool invocation,
action execution or a named control plane — rather than treating selection among heterogeneous
enterprise locations as the architectural decision.

Two results come closest to the mechanism developed in §IV. Bensalem et al. [@bensalem] argue
that safe agent operation depends on information becoming available at different execution stages,
motivating enforcement across multiple layers. ActPlane [@actplane] exposes the same tension within one
stack: policy context resides with the agent closest to the task, while operating-system enforcement
provides broader coverage across the paths considered.

Layered guardrail architectures also exist: the Swiss Cheese model [@swisscheese] contributes a taxonomy of
runtime guardrails with a reference architecture spanning quality attributes, pipeline stages and agent
artifacts. Layering and defence in depth are therefore established; our concern is allocation across layers
rather than the case for layering itself.

Recent work also makes policy context itself an architectural concern. Kaptein et al. model runtime
policies over agent identity, partial execution path, proposed action and organisational state
[@kaptein]. CONTINUITY preserves authenticated security context across component transitions through
explicit security-context contracts [@continuity], while Gopalakrishna's zero-knowledge gateway conveys
proofs of governance-defined predicates rather than the underlying private values, and exposes a
resulting source-integrity gap [@zkgateway]. These works preserve, evaluate or selectively convey
policy-relevant context across runtime boundaries; they do not derive enforcement placement across
heterogeneous enterprise locations from the cause of an obligation's placement deficit.

SARC [@sarc] is the closest methodological antecedent, and we build on it rather than replace it. It
compiles first-class constraints to four enforcement sites in an agent loop, hosting each at the lowest
layer compatible with its class, under genuine placement criteria — predicate decidability, cost
asymmetry by class and a reversibility window — with a reproducible evaluation. Two things change at
enterprise scale: the location space becomes a heterogeneous estate of applications, gateways, data
layers, platforms and organisational boundaries with different owners; and the transformation follows
from the cause of the deficit at an adequate cut rather than from constraint class alone, which yields
fact and verdict transport, compositional placement and explicit residuals (§VII‑B). A related result composes several pre-action gates on one
action, where remediation by one control invalidates another's judgement [@onegate] — composition at a
single enforcement point, not across locations.

## D. Requirements into architectural reasoning

The broader methodological lineage is found in privacy architecture rather than AI. Hoepman's privacy design
strategies [@hoepman] derive eight reusable strategies from data-protection law, pitched at architects and at design time, and applicable to requirements their author never saw. Translating legal requirements
into durable architectural reasoning is established practice; what we contribute is the
enforcement-location analogue for AI governance, not the idea of such translation.

Taken together, this literature supplies obligations, patterns, enforcement mechanisms, layered
architectures, and — in SARC — placement rules within an agent execution loop. To the best of our
knowledge, no existing work takes a stated governance obligation and derives its enforcement
architecture across heterogeneous enterprise locations, while also specifying the transformation
required when no single location is sufficient. The novelty is not another enforcement layer or policy
language but a derivation rule from deficit cause to architectural transformation. The literature search reported here was frozen on 5 September 2026, in an area where directly relevant
preprints appear frequently. The vendor documentation used in §VIII‑F was read earlier, on 19 August
2026, and is dated separately.

# IV. Why the deficit arises: mediation–abstraction coupling

## A. The coupling

For context-dependent governance obligations — those turning on purpose, intent, scope, entitlement
or contextual judgement — the locations holding enough information to evaluate the obligation are often
not those that most broadly mediate its effects. We argue that this reflects a recurring pressure in how
broad mediation is obtained, not only the state of current tooling.

A location mediates many execution paths because those paths share an interface passing through it — an
HTTP boundary, a chat-completions API, a syscall table. Shared interfaces are typically *general* across
the applications that use them, and that generality is achieved by abstracting over whatever differs
between those applications: which customer, which case, which entitlement, which business purpose. Unless that state is
deliberately preserved across the interface, the enforcement location loses the facts on which semantic
governance predicates depend. Mediation tends to be bought with abstraction, and abstraction is paid for
in semantics.

::: {custom-style="First Paragraph"}
**Mediation–Abstraction Coupling.** For obligations whose decision predicates range
over application-specific state, a location's information availability tends to fall as its cut-scope
(the governed paths that traverse it; §V‑C) rises: broader mediation and reduced application-specific context are both consequences of interface
generality.
:::

Fig. 1 shows the pattern across representative locations of Table 1. The restriction to
application-specific state is important. Obligations whose predicates range over facts the general
interface itself carries — destination, model identity and version, request rate, tenant, retention
window — suffer no such loss. For them, a strong cut may also be a well-informed one. §VI turns this
distinction into the classification on which the method operates.

![](fig-coupling.png){width=3.4in}

**Fig. 1.** Mediation–abstraction coupling across representative zones of Table 1 (Z2, Z3, Z4 and Z7–8), shown in
four groups.
Moving from application-specific locations towards shared infrastructure, cut-scope tends to rise while
available application-specific context tends to fall. The bands represent a design tendency, not a
measured quantity. The dashed arrow (T2, §VII‑B) shows how deliberate transport can move a required fact or verdict to a
strong cut that lacks it.

## B. A coupling, not a law

The relationship is a recurring design pressure, not a monotonic law. Counterexamples are familiar: application-aware
gateways, mandatory SDKs with attestation, service meshes propagating end-user identity, data planes
carrying classification labels. Each weakens or reverses the coupling by deliberate design — moving context to a
strongly mediating location, or hardening a semantically rich location into a cut. The first is transport, which §VII prescribes; the second changes the architecture to
which the method is applied. The coupling is therefore a pressure, not an invariant: absent deliberate measures of this kind, consolidating access behind a general interface tends to trade semantic context for coverage,
often without that trade being made explicit.

## C. This is not zero trust restated

The coupling is not simply a restatement of zero trust or classical access control. The difference lies
in what the policy ranges over and why a required fact is missing. Classical access-control architectures make policy-relevant attributes —
subject, resource, action and contextual attributes retrieved as needed — available to the decision
function; the policy information point exists to route what is not local. For semantic AI obligations, however, a required fact may no longer be represented at the boundary, may
require a judgement no mechanism at the cut can render, may not yet exist at that point in the path, or
may not be permitted to cross the boundary at all. Attribute routing alone does not resolve these cases;
§V‑E formalises the distinctions among them.

Two features of enterprise AI sharpen the difference. First, prompt assembly can act as a lossy join: content from different sources may be
concatenated into a representation that no longer preserves the provenance and trust relationships on
which an injection predicate depends. Second, under the adversary model considered here, the adversary
can operate inside the trust boundary — an agent acting on
injected instructions routes around checks placed where the semantics live, removing the well-informed
locations from the set of cuts exactly when they are needed.

# V. Primitives

## A. Architecture, scope and adversary

We model an enterprise AI architecture as a set of candidate **enforcement locations**
$L = \{l_1 \dots l_n\}$: points at which a control can be interposed on a request, an action or a release.
Two further parameters, the scope and the adversary, must be fixed before any statement about a location
carries meaning. The **governed effect** is the effect the obligation prohibits, constrains or requires;
the **scope** *S* is the set of execution paths through which it can be realised. The
**adversary** *X* is the actor whose avoidance of the control is being reasoned about — in this paper,
a prompt-injected or misdirected agent operating inside an otherwise trusted application, together
with a careless user.

Every property below is relative to ⟨*S*, *X*⟩, and this is not a formality: *bypass resistance* has no
truth value until *X* is named. A location mediating every path available to a careless user may mediate
none of those available to an agent acting on injected instructions. Where the adversary model is left
implicit, placement claims therefore cannot be compared. As candidate locations we use eight generic zones (Table 1); §V‑C explains why this deliberately thin
model is sufficient.

**Table 1.** Generic enforcement zones and the three attributes used for placement (defined in §V‑C). Cut-scope is
relative to the governed effect and the adversary model above; for Z1, the relevant effect is release or
deployment rather than runtime execution.

| Zone | Available facts $A(l)$ | Cut-scope | Responses $\alpha (l)$ |
|---|---|---|---|
| **Z1** Design-time / CI / registry | artifacts, evaluations, declared purpose | all deployments | block release |
| **Z2** Application & business logic | identity, session, business object, purpose, entitlement | own pre-agent path only | block, escalate |
| **Z3** SDK / agent orchestration | prompt, plan, tool arguments, intermediate outputs | calls made via the SDK | block, modify, escalate |
| **Z4** AI gateway / model proxy | prompt text, model, tenant, caller service, tokens | all model-bound traffic | block, modify, log |
| **Z5** Model endpoint | prompt, output | calls to that model | refuse, filter |
| **Z6** Tool & data access | resource, query, data labels | all access to that resource | deny, redact |
| **Z7** Network egress | destination, volume, metadata | all traffic | block |
| **Z8** Platform runtime / OS | syscalls, processes, files, sockets | all execution | block, terminate |

## B. Obligations and information requirements

A **governance obligation** *o* is a decision predicate $\pi_o$ over facts about a contemplated or
completed action. For a chosen decomposition of the obligation, its **information requirement** $I(o)$
is the set of facts whose values $\pi_o$ requires for correct evaluation.

Deriving $I(o)$ is the first analytical step of the method and carries most of its interpretive burden.
For the disclosure obligation of §II, $I(o)$ comprises the five facts listed in §I, of which only
destination externality reaches the locations that broadly mediate the disclosure. That dispersion is
the phenomenon the rest of the paper is about.

## C. What a location offers

Three attributes characterise a location. **Availability** $A(l)$ is the set of facts observable or
derivable at *l* at decision time, without new plumbing. **Mediation** describes how much of the
governed path space passes through a location. Let $M(l) \subseteq S$ be the governed paths that
traverse *l* — its **cut-scope** — and $S_X \subseteq S$ the paths by which *X* can realise the effect.
A location *l* *mediates* the governed effect over ⟨*S*, *X*⟩ iff it is a **cut** — that is,
$S_X \subseteq M(l)$, so every path available to *X* traverses *l*. This is complete mediation stated graph-theoretically and generalised to
an estate; stated this way, coverage becomes a variable rather than an assumption. **Actuation** $\alpha (l)$ is the
response repertoire available at *l*. Locations downstream of the governed effect permit only
observation and whatever compensation the effect admits; the preventive/detective distinction is
therefore positional rather than merely a design choice.

Together these determine **structural placement feasibility**: whether a location *can* host a control at
all. Operational qualities — latency, cost, ownership, maintainability — rank otherwise feasible
placements but do not determine the transformation a deficit generates. This is why Table 1 need
represent only the structural attributes the method uses.

## D. Feasibility

A location can enforce an obligation only if three things hold. It can **decide**: it holds every required
fact, $I(o) \subseteq A(l)$. It **covers every path**: every path by which the adversary can realise the
governed effect traverses it, $\mathit{cut}(l \mid S,X)$. It can **act**: it can perform the responses
$R(o)$ the obligation requires, $\alpha(l) \supseteq R(o)$. The **feasible set** is where all three hold:

$F(o)=\{\,l \in L : I(o) \subseteq A(l) \wedge \mathit{cut}(l \mid S,X) \wedge \alpha(l) \supseteq R(o)\,\}$

The **deficit** at a location,
$\Delta (o,l) = I(o) \setminus A(l)$, is the set of required facts it lacks.

**The strongest cut.** In practice: pin the governed effect, list the locations that every path available
to the adversary must traverse. If one of them can already decide and act, enforce there (Class T, §VI):
broader coverage elsewhere does not justify a transport. Otherwise prefer the one with the broadest
coverage and diagnose it; if several are incomparable, operational considerations choose among them. If
none exists, the obstruction is one of mediation.

Formally, any location satisfying $\mathit{cut}(l \mid S,X)$ is an **adequate cut**, whatever it knows or
can do. Location $l_a$ **dominates** $l_b$, written $l_a \succeq l_b$, iff $M(l_b) \subseteq M(l_a)$ — a
preorder, not a scalar, and because $M$ ranges over all governed paths rather than only the adversary's,
two cuts can still differ in strength; *S* must therefore be pinned to the governed effect first (§VII‑D).
The adequate cuts that no other strictly dominates are the **maximal adequate cuts**, and the maximal
elements of $F(o)$ are the **strongest candidates**, with §V‑C's operational qualities choosing among
several. Where no adequate cut is feasible, the method diagnoses a maximal one rather than retreating to a
narrower location, so a deficit found there is a diagnosis rather than a disqualification.

A candidate location can fail feasibility for three independent reasons, one per attribute: it cannot
**decide** (decision deficit), cannot **mediate** the governed effect (mediation deficit), or cannot
**act** (actuation deficit). $F(o)$ is empty when every candidate fails at least one of these. An
actuation deficit is easily overlooked because it does not appear in $\Delta$ — erasure of data
memorised in model weights is an illustrative case, with no decision deficit whatever and no location
able to act.

## E. Why a fact is missing

Deficits differ in kind, and the kind is what the method acts on. The taxonomy has two levels, keyed to
which attribute fails. **Decision deficits** concern $A(l)$: a fact required by $\pi_o$ is absent because
it is not representable at the location, may not cross to it, cannot be determined there or does not yet exist. Where the missing fact depends on a judgement, we distinguish
three cases: the judgement can be rendered elsewhere, can only be approximated or can be rendered by no identified party. Together with the other causes, these yield the six decision-deficit rows of Table 2. The analysis
asks why a required value is *absent*: a present but untrustworthy fact is not a deficit but a derived
integrity obligation (§VII‑E). An **actuation deficit** concerns $\alpha (l)$: every fact is present and
*l* simply cannot perform the required response. A mediation deficit — no adequate cut — has no cause
row (§VIII‑D). Table 2 enumerates the ways a fact can be absent; it is not a claim that facts usually are
(§VIII‑B).

**Table 2.** Deficit causes routed by the current method. The first six are decision deficits on $A(l)$;
the last is an actuation deficit on $\alpha (l)$. A mediation deficit — no adequate cut — has no row
(§VIII‑D).

| Cause | The deficit cannot be closed at *l* because… | Example |
|---|---|---|
| **Representational** | the representation at *l*'s boundary no longer preserves the fact, though an authoritative representation exists elsewhere and may cross | segment provenance lost during prompt flattening |
| **Authority** | the fact may not lawfully or organisationally cross to *l* (authority over the information, not over the response) | a provider's training corpus, seen from the deployer |
| **Epistemic — renderable** | no *mechanism* at *l* can render the judgement, but some party can | whether a human reviewer intervened |
| **Epistemic — approximable** | no identified party can render the true fact reliably, but a defensible proxy exists | the causal basis of a specific output |
| **Epistemic — unrenderable** | no identified party can render the judgement with adequate reliability | whether a human has been deceived |
| **Temporal** | the fact does not yet exist at *l*'s position in the path | output toxicity, at a pre-inference gate |
| **Actuation** | the fact is present but *l* cannot perform the required response | erasure of a training example from weights |

The epistemic rows are operational judgements relative to the stated architecture and governance
boundary, not claims of uncomputability. A fact that may not cross is an authority deficit, not a
representational one.

# VI. Three classes of obligation

Obligations divide into three classes, relative to a stated architecture, scope and adversary.

**Class N — non-architectural.** The obligation constrains no mediated action. It is discharged by
producing a document, holding a review or assigning a role. No enforcement location is implicated
because there is nothing to interpose upon.

Class N is not a leftover category: it accounts for a substantial share of the governance material examined, as
§VIII‑A quantifies. A method for placing controls should not imply that architecture discharges
governance.

**Class T — transparent.** Some adequate cut has the required actuation and already holds all facts in
$I(o)$. Placement is then immediate (T1) at a strongest candidate, even where a more broadly mediating
cut lacks a fact, with §V‑C's operational qualities choosing among maximal candidates.

**Class O — placement-obstructed.** No adequate cut is immediately feasible because of a
decision, mediation or actuation deficit. Erasure from model weights, for example, is obstructed even
when the architecture knows precisely which data is at issue. Obstructed does not mean unenforceable:
immediate placement fails, and a transformation or residual must be considered — though a mediation
deficit, which §VIII‑D exposed, is not routed by Table 3.

For decision-obstructed obligations, the criterion separating T from O is whether $I(o)$ **survives
abstraction** at an adequate cut for the governed effect. An obligation is also Class O
if such a location lacks the required actuation, or if no adequate cut exists. §IV argued that broad
mediation tends to be purchased with abstraction, so an obligation's class often depends on whether the
facts in its predicate survive that abstraction. Predicates over *content properties*, *destinations*,
*rates*, *versions* and *tenancy* often remain evaluable at general interfaces; predicates over
*purpose*, *entitlement*, *objective*, *scope*, *contextual sensitivity* and *adequacy of review* often
do not.

The boundary of Class N is a judgement, and we record it as one. EU AI Act Article 9, largely a process
obligation with a mediated post-market monitoring component, was coded Class N; ISO/IEC 42001 A.6.2.6,
similarly astride the line, was coded architecturally enforceable. The divergence shows that the
boundary is a coding judgement rather than a mechanical test.

The classification is also architecture-relative. An obligation that is Class O in one estate may be
Class T in another where the necessary fact has already been routed to the mediating layer. In the
latter case, a previous application of the method has effectively been built into the platform.


![](fig-method.png){width=3.4in}

**Fig. 2.** The deficit-driven placement procedure. Steps 1–7 are those of §VII‑A; step 6 applies Table 3 to each missing fact separately and to any actuation deficit. Dashed boxes are outputs the method reports but does not route, and the dashed return is the transport recursion of §VII‑E.

# VII. The deficit-driven placement method

## A. Procedure

1. **Filter.** If the obligation constrains no mediated action, it is Class N and out of scope.
2. **Derive $I(o)$.** Enumerate the facts $\pi_o$ requires.
3. **Instantiate.** Establish each candidate location's actual information, mediation and actuation
   properties from what the component does, not from its category name.
4. **Locate.** Identify the adequate cuts over ⟨*S*, *X*⟩. If any is feasible, select a maximal feasible
   candidate; otherwise identify the maximal adequate cuts for diagnosis. If no adequate cut exists,
   report a mediation deficit. Use §V‑C's operational qualities to choose among incomparable candidates.
5. **Diagnose.** At each selected cut, determine the cause of each missing fact in $\Delta (o,l)$
   (Table 2), and separately whether the required response exceeds $\alpha (l)$.
6. **Transform.** Apply Table 3 **per fact**. A mediation deficit is reported but is not routed by the
   present transformation table.
7. **Compose.** Compose the per-fact transformations into the enforcement architecture. Record the
   selected enforcement location, the transported facts or verdicts and their integrity obligations,
   any approximation and detection controls, and the residual — the terminal outputs together with
   what each approximation or transported verdict leaves unenforced.

A feasible adequate cut therefore takes precedence: a broader but deficient cut is diagnosed only when
no adequate cut is feasible. Fig. 2 summarises the procedure and the transformation function of §VII‑B; §VIII records
how the procedure reached this form.

**Practitioner use.** The procedure is intended to be applied obligation by obligation. Its output is not
only an enforcement location but a placement record: the selected cut, the transported facts or verdicts,
the integrity bindings they require, any approximation and detection controls, and the residual that
remains unenforced.

## B. The transformation function

A contrast shows why the cause, not the missing fact, decides. A gateway may lack a record's sensitivity
classification because the label was dropped when the record was served — a representational deficit,
closed by transporting the fact — or because policy forbids exposing it there — an authority deficit,
closed only by transporting a verdict. The same observable condition, a missing decision fact, yields
different architectures; its cause is architecturally consequential. Table 3 gives the mapping for every
cause, and the principle states it.

::: {custom-style="First Paragraph"}
**Deficit-Cause Principle.** At an adequate cut, the class of architectural transformation is
determined by *why* each required fact is missing, not by the obligation's class alone. A lost
representation permits transport of the fact; an authority or renderable-epistemic deficit permits
only transport of a verdict; a temporal or approximable deficit requires approximation with later
detection; and an actuation deficit permits the same only where an adequate substitute response
exists. An unrenderable predicate admits none of these transformations.
:::

The principle is conditional. It applies only at an adequate cut, and therefore says nothing about an
obligation for which no cut exists (§VIII‑D); it determines the *class* of transformation and not its
implementation, which §V‑C's operational qualities still choose; and it selects T3 for an actuation
deficit only where Table 3's substitution condition holds. §VIII‑D reports how the cause separates the
obligations of the three constructed corpora.

**Table 3.** Deficit cause determines the transformation. The rows cover decision and actuation
deficits; a mediation deficit, where no adequate cut exists, has no row (§VIII‑D). T3's detective
component is adequate only if the effect is reversible within the detection latency, a condition adapted
from SARC's reversibility window [@sarc]; otherwise T3 leaves a residual (§VII‑F).

| Condition at a maximal adequate cut | Transformation |
|---|---|
| no deficit | **T1 Relocate** — enforce there |
| representational | **T2 Transport (fact)** — restore the representation across the boundary |
| authority | **T2 Transport (verdict)** — the fact may not cross; the decision may |
| epistemic, renderable | **T2 Transport (verdict)** — the party who can judge decides; the cut enforces |
| epistemic, approximable | **T3 Approximate-and-detect** |
| epistemic, unrenderable | **Terminal — declare residual** |
| temporal | **T3 Approximate-and-detect** — preventive over-approximation at the cut, detective evaluation of the true predicate after the effect |
| actuation | **T3** if preventive approximation plus later detection or compensation adequately substitutes for the unavailable response; otherwise **Terminal** |


Two features of Table 3 deserve emphasis. First, the payload of a transport is not a design preference
but a consequence of the cause: an authority deficit forbids moving the fact while permitting the
decision, and an epistemic deficit means there is no fact to move — only a rendered judgement. Second,
**T2 Transport (verdict)** recovers the separation of policy decision point from policy enforcement point (PDP/PEP) familiar from
XACML as a special case. The
method adds a precondition: the decision must be computable and transportable *before* the governed
effect occurs. Under a temporal deficit that condition fails, leaving T3 as the available construction.

## C. Composition

An obligation rarely has a single deficit. Purpose limitation (§VII‑D) requires a collection-purpose
label and a verdict on the current purpose, which are missing for different causes; Table 3 applied at
obligation granularity cannot express that. The method therefore operates per fact. Each missing fact receives its
own transformation, and the enforcement architecture is their composition. The residual combines the
terminal outputs with whatever each approximation or transported verdict leaves unenforced. Operating per fact lets the method return the layered answers real obligations require while keeping the underlying
transformation rule single-valued.

## D. The method applied

Consider purpose limitation as it reaches an enterprise retrieval pipeline: *personal data must not be
further processed in a manner incompatible with the purpose for which it was collected.* We apply
the seven steps of §VII‑A in turn.

*Filter (1).* The obligation constrains a mediated action — the retrieval of a record and its inclusion
in a prompt — so it is in scope. *Derive (2).* Its information requirement has four elements, shown in
Table 4.

*Instantiate and locate (3–4).* Instantiated from what they do, Z4 sees model-bound prompts, while Z6
sees every access to the resource with its data labels and can deny or redact (Table 1). Locating the
cut shows why $\succeq$ is defined against a pinned
scope. The gateway **Z4** and the data
access layer **Z6** each mediate some governed paths, and until *S* is pinned neither dominates. Once *S*
is pinned to the governed effect — further processing of *this* personal data — Z6 is a cut and Z4 is
not: every such path traverses Z6, and some (an export, a report) bypass Z4 entirely. Z7 and Z8 are not
cuts for this effect in the modelled pipeline: a retrieved record can be processed without leaving the
network, and processing spans several runtimes, no one of whose platform boundaries sees every path. Every
path, by contrast, begins with an access to the resource, so Z6 is the unique maximal adequate cut. The
cut covers the modelled retrieval paths, not every later use of the personal data: a copy already
retrieved and reused never passes Z6 again, which is why that reuse appears in the residual. *Diagnose and transform (5–6).* Diagnosing
each fact there and applying Table 3 gives Table 4.

*Compose (7).* The composed architecture has Z6 evaluate compatibility using two transported inputs: a collection-purpose
label carried with the data, and a purpose verdict rendered in the requester's business context and
carried with the request. Neither transport is free — the label must be bound to the record and the
verdict to the requester. Both transports create derived integrity obligations (§VII‑E). These are predicates
over provenance facts and are therefore Class T, closing by T1 at the signing and identity layers. The residual is stated rather than
absorbed: the purpose verdict rests on what the requester declares, so processing for a purpose other
than the one declared remains outside this cut, as does reuse of a copy already retrieved, which does not
pass Z6 again.

**Placement record.** Enforce compatibility at Z6; transport the collection-purpose fact with the data; transport the current-purpose
verdict with the request; bind both transported assertions to what they describe, closing each by T1 at the signing and
identity layers; and record
processing for an undeclared purpose, and reuse of a retrieved copy, as the residual.

**Table 4.** Per-fact diagnosis for purpose limitation at Z6.

| Fact in $I(o)$ | Status at Z6 | Cause → transformation |
|---|---|---|
| record is personal data | available (data labels) | none → **T1** here |
| collection purpose | absent from the served record | representational → **T2 fact** |
| current processing purpose | absent; rendered in the requester's business context | epistemic-renderable → **T2 verdict** |
| compatibility of the two | policy, once both are present | none → **T1** here |


## E. The transport recursion

Every transport creates a dependency: a strongly mediating location now acts on a fact or verdict
asserted by a location it does not control. The integrity of that assertion is a new obligation — the
**derived integrity obligation** *o′* — which must itself be placed. Recent context-contract and zero-knowledge gateway designs provide
concrete mechanisms for discharging such derived integrity obligations [@continuity], [@zkgateway].

The argument for why the recursion stops is that transported assertions generate predicates over
provenance facts — signatures, issuance time, binding to a request — which are transparent by the
criterion of §VI, provided the identity and signing layers are themselves cuts under the stated
adversary. The evidence: in the seven development transport cases whose derived obligation was recorded
(items 1, 3, 4, 19, 20, 21 and 23) and the five transport cases of the pre-specified study whose sealed predictions named it (§VIII‑D), the
derived obligation was Class T and closed by T1 at an identity or signing layer, with no second
recursion. Three documented retrodiction cases (P4, P12 and P13; §VIII‑F) show the same pattern. The
other constructed transport cases did not record their derived obligation and are not counted. Twelve
constructed cases and three documented ones do not establish universal one-step termination, and we do
not claim it; the case-level records are in the artifact.

## F. Residual as an output

A placement method should be able to report when no available architecture can fully enforce an
obligation. The method's residual collects the terminal outputs of Table 3 — an unrenderable deficit, or
an actuation deficit with no adequate substitute — together with what each transported verdict and each
approximation leaves unenforced, including any T3 whose effect is not reversible within its detection
latency. For each, it states what remains unenforced and why.

One failure the method exposes is an unstated residual: a control that approximates a predicate it cannot
fully evaluate, presented without stating where its competence ends. Making the residual an output
rather than an omission distinguishes an explicitly identified residual from an unnoticed enforcement
gap; whether the residual is acceptable is a governance decision that the method informs but does not
make.

# VIII. Evaluation

We evaluate the method through four studies addressing progressively stronger questions and providing
increasing separation from method development (Table 5): development, refinement, frozen testing and external
comparison. The fourth takes as an **external reference** where documented enterprise AI platforms and
systems enforce, rather than our own architectural judgement.

**Chronology.** Studies are reported in methodological order; the documented-architecture study
(§VIII‑F) preceded the untouched test (§VIII‑D). The held-out set produced three refinements (§VIII‑C). The
two documented-architecture prediction errors prompted the Instantiate step, and the predictions reported
there were made without it. The untouched test prompted two clarifications — actuation is considered
separately from locating a cut, and a missing cut is reported as a mediation deficit. Step 4 now also
states the precedence of a feasible adequate cut, which the definition of Class T already implied; in the
untouched test every alternative location the sealed predictions considered covered only its own paths,
so it was not an adequate cut. None of these changes alters a recorded outcome. We do not aggregate the four studies; even the fourth is not fully
independent, since one researcher selected the cases, made the predictions, read the documentation and
assigned the codes.

## A. Corpus construction

A sampling frame of 268 items was fixed before any classification: the EU AI Act Chapter III Section 2
together with Article 50 (9 items), the 38 controls of ISO/IEC 42001 Annex A, the 211 suggested actions
of the NIST Generative AI Profile, and the ten risks of the OWASP Top 10 for Agentic Applications
[@owasp]. The first filter, fixed in advance, retained only architecturally enforceable obligations.

**Table 5.** Evaluation design: four questions, four studies, increasing separation from method development.

| Study | n | Question | Independence | Result |
|---|--:|---|---|---|
| Development corpus | 25 | **EQ1** Do placement-obstructed obligations occur across governance sources? | constructed and coded by us | 15 T / 10 O as coded; 12 T / 13 O under the definition of §VI |
| Held-out refinement set | 15 | **EQ2** Do the pre-test rules extend beyond the corpus that produced them? | disjoint in source or chapter | 13 handled, 2 exceptions |
| Untouched test set | 12 | **EQ3** Does the frozen method route obligations from sources excluded from its development? | pre-specified and sealed, source-disjoint | 11 routed, 1 exception |
| Documented-architecture retrodiction | 14 | **EQ4** Do predictions agree with documented enforcement placement? | external documented architectures | 8 agree or extend, 3 gaps, 2 errors, 1 undetermined |

Because the NIST profile alone contributes 211 suggested actions, a fixed keyword filter was applied to
them before they were read, and eight matching actions were taken. The sixteen terms are in the artifact;
the protocol recorded about forty matches, but the match list was not retained, so that count cannot be
reproduced. Table 1's location model
and §V‑A's adversary model were also fixed before the first obligation was coded.

The first result concerns scope rather than method. At least 24 of the 38 ISO/IEC 42001 Annex A controls
are Class N — the policy, roles, impact-assessment, external-reporting and supplier families entirely so
— as are several AI Act articles and many NIST suggested actions. All are discharged by producing a
document, holding a review or assigning a role. In the sources examined, a substantial share of
governance requirements is organisational or procedural rather than architecturally placeable.

## B. Obligation classification (EQ1)

Under the development-time coding, twenty-five architecturally enforceable obligations remained: fifteen
Class T, ten Class O. Three of the fifteen (items 1, 3 and 21), however, required a fact that exists in the
estate to be transported to the enforcement cut. Under the definition of §VI those three are Class O, so
applying that definition retrospectively gives twelve Class T and thirteen Class O. We report the
development study as coded rather than recode it after the method was refined. Many obligations needed
no transformation at all: 11 of the 25 had an empty deficit at some adequate cut and a twelfth only a
minor epistemic residual, and the three just named lacked only a fact that already existed elsewhere in
the estate.

Within this purposive corpus — descriptive counts, not prevalence estimates — 71% of the agentic
obligations were coded Class O, against 50% of the rights-based legal obligations and 17% of the
operational controls from the management and security standards. Applying the §VI definition
retrospectively gives 86%, 83% and 17%: the agentic-versus-legal contrast largely disappears, while the
operational controls remain predominantly transparent. The cells are small and were classified with the
same criterion, so the pattern is consistent with §VI rather than a test of it: agentic and most legal
obligations need application-specific state or a fact held elsewhere in the estate, whereas operational
controls are predominantly predicates over content properties, destinations and rates, which reach a
gateway intact. The overall Class O share (40% as coded) is likewise not a prevalence claim.

## C. Held-out applicability (EQ2)

To test whether the rules extend beyond the corpus that produced them, we froze the **pre-test method** —
class definitions, deficit causes, the four transformations (T1, T2, T3 and Terminal), the location model and the adversary model —
before opening a held-out set of 15 obligations from sources, or parts of sources, not used in method
development: the GDPR [@gdpr], the CSA AI Controls Matrix [@csaaicm], NIST SP 800-218A [@ssdf218a], the
HIPAA minimum-necessary standard [@hipaa], and Chapter V of the EU AI Act [@aiact], a chapter the
development corpus did not draw on. For each obligation, the predicted transformation was recorded before
a separate architecture-reasoning pass was performed.

Thirteen of the 15 were handled by those frozen rules; we report this as applicability rather than
accuracy. The two exceptions exposed omissions in the pre-test method and are retained as exceptions.
First, erasure of data memorised in model weights has no decision deficit at all — the training
registry knows precisely which data entered the model — yet no location can selectively remove that data's influence, which established actuation as an independent feasibility dimension. Second, explanation
under GDPR Articles 15 and 22 proved neither renderable nor unrenderable but *approximable*, adding the
third epistemic branch.

Two otherwise successful cases, purpose limitation and serious-incident reporting, each carried two
deficits of different causes, which made per-fact composition explicit.

The count of 13 is against the pre-test rules, not the refined ones. The three refinements — actuation
as an independent feasibility dimension, the approximable epistemic branch and per-fact composition —
were fixed before the documented-architecture study began.

## D. Untouched applicability of the frozen method (EQ3)

We then froze the refined method and applied it, with no further development, to an untouched,
pre-specified test set — the first study in which the method, cases, predictions and pass criterion were
all fixed before any architectural analysis. The prediction and architecture-reasoning passes were each
hashed and sealed before the next began. The protocol was sealed by hash rather than deposited with a
registry, so the seals establish that the published protocol is the one the analysis used, not
independently timestamped priority.

The twelve obligations, three from each source, came from sources that had to be disjoint from the two
earlier sets and to differ from one another in genre: MITRE ATLAS mitigations
[@atlas], the C2PA provenance specification [@c2pa], SR 11-7 on model risk management [@sr117], and the
Treasury Board of Canada *Directive on Automated Decision-Making* [@tbsdirective]. SR 11-7 had been
superseded on 17 April 2026, before the protocol was sealed, which the protocol does not record; since
the study tests routing of the obligations as the source states them, this does not change what was
tested. The pass criterion required at least nine of twelve obligations to be
routed using only the four pre-specified transformations. Any obligation requiring a fifth
transformation counted as a method failure, regardless of the total routed.

Eleven of the twelve were routed — nine cleanly, two with a recorded strain — and none required a
transformation outside the four.

The remaining obligation exposed a different incompleteness: a missing row rather than a missing
transformation. Provenance that must survive a third party's re-publication has no adequate cut in the
modelled estate. The method diagnoses this as a mediation deficit. §V‑D gives three reasons the feasible set can be empty,
but Table 3 routes only two, so the method had nothing to return and the case
counts as an exception.

After observing this exception, we derived a symmetric row: a mediation deficit routes to T3 where a detectable
approximation exists and to Terminal otherwise. This closes Table 3 over all three feasibility attributes
without introducing a new transformation. Because it was derived from the case that exposed it, the row is untested by
this study, and we report it rather than fold it into Table 3.

The two strained cases are instructive. Model-inventory completeness is transparent at the gateway under our
adversary and placement-obstructed under one that includes a developer standing up an unregistered model:
both answers are correct for their adversary. Classification is therefore relative to the stated
adversary rather than an intrinsic property of the obligation — the plainest illustration we have of
§V‑A's claim. The second, query-rate limiting, exposed sensitivity to the level of abstraction at which an obligation enters the
method: ATLAS, as a control catalogue, states the obligation one level below a statute.

One qualification bounds the count. Five of the twelve rows structurally resemble an obligation already
analysed; only two resemble nothing in the earlier corpora, and one of those two is the exception. Clean
results concentrate where obligations look like ones the method was built on, so further evaluation
should select for distance from the existing corpora rather than for size.

**The cause across the three corpora.** Of the 35 deficit-bearing obligations in the three constructed
corpora, 33 require T2, T3 or Terminal: 14 transport a fact, 9 transport a verdict, 8 approximate and
detect, and 2 are terminal; the other two are the mediation case above and one obligation resolved by T1
with a minor residual. Obligation class alone does not distinguish among these transformations. The
counts re-tabulate our own codings, so they show that the cause dimension separates these obligations,
not that each separation is correct; the counting rules are in the artifact. Three committed
codings — development item 20 and retrodiction cases P9 and P12 — depart from Table 3: task scope is
recorded as representational yet routed to a verdict, where it is better read as epistemic-renderable.
They are retained unchanged rather than recoded; the artifact gives the reasoning.

## E. Discrimination

Applicability alone is insufficient: a method could appear successful simply by generating plausible
placements. We therefore also asked whether it rejects plausible but structurally wrong ones. For six of
the ten Class O obligations we recorded a placement a competent architect might propose — our own
construction, not an independent architect's — and what the method returned.

Prompt-injection filtering at the gateway operates on a prompt stripped of segment provenance; an
approval workflow in the application sits at a location that is not a cut under our adversary model;
tool allow-listing, content classification and read-time memory sanitisation fail likewise, each standing
in for a fact held elsewhere. These share a shape: the naïve placement reconstructs by inference a fact
the architecture held upstream but did not preserve across the interface.

The method also endorses the obvious answer where it is right. For unsanctioned code execution it
returns the platform boundary, because the predicate ranges over process and host behaviour and that is what the layer holds. Azure Container Apps dynamic sessions [@aca] enforce exactly there,
through
Hyper-V isolation applied irrespective of the code an agent generates. Without that case the method could
be read as biased towards elaborate distributed controls.

## F. Documented-architecture retrodiction (EQ4)

The fourth study compares the method's predictions with documented enforcement placements. Predictions
were committed to file before the corresponding documentation was opened, and marked *[clean]* where the prediction preceded substantive exposure to the implementation evidence and *[prior]* otherwise; only clean
pairs are analysed. To avoid selecting cases only after seeing their fit, the last six cases were each
chosen to fill a cell in a stratification over deficit type, enforcement zone and system type, with the
stratum recorded before the prediction; that rule was fixed after the first eight cases had been coded.

Evidence was restricted to official first-party documentation. Outcomes were coded using a fixed five-point scheme:
agreement, agreement with additional controls, an argued gap, a prediction error, or insufficient
evidence. The admissibility test for a gap was fixed in advance and is reproduced in the artifact.

Across 14 clean cases, eight documented architectures agreed with or extended the method's prediction,
three exhibited pre-specified information or mediation gaps, two contradicted the predicted architecture,
and one could not be determined from the available documentation. Under the interpretation rule, fixed
after the first coding pass and before the second, this places the study in the rule's agreement-dominant band, defined as agreement
or extension predominating with at most two prediction errors. It sits at the boundary of that band
rather than comfortably inside it, since there are exactly two.

The rule also specified what would count against the method: four or more prediction errors, or errors
concentrated in one deficit cause, would weaken the Deficit-Cause Principle — in the rule's own terms, from *determines* to
*predicts in the majority of observed cases*. Neither weakening condition was met.

The protocol's original target was 30–40 cases. Collection stopped at 14 under an amendment recorded at
the time, which gives four reasons: the result had stayed in the agreement-dominant band across the fourth
and fifth coding passes, every deficit branch and enforcement zone had an external instance, further cases
would not relieve the single-coder constraint, and effort was better spent elsewhere. Because the first
reason depends on the outcome, the decision to stop was not independent of the result.

Three cases illustrate different outcome categories. All documentation was read on **19 August 2026**,
and vendor architectures change. **Google VPC Service Controls** [@vpcsc] was predicted to enforce at the
network boundary on a destination predicate; its documentation agrees, states that the perimeter "is not
designed to enforce comprehensive controls on metadata movement", and points to a separate service for
classifying sensitive data. **Microsoft Purview** [@purview] was predicted to transport classification
labels from the data layer into the AI interaction; its documentation agrees, and where a label applies
encryption, AI apps honour it through Rights Management usage rights — consistent with the transport
recursion of §VII‑E. **Google Model Armor** [@modelarmor] was flagged as a gap *before* its documentation
was read; the documentation confirms the placement, describes screening each prompt and response as a
single, independent request, and describes no provenance-aware treatment of its segments.

The two errors share a methodological root: each arose from incorrect assumptions about the candidate component,
not from a deficit the method failed to represent. One predicted enforcement at the Vertex AI
Model Registry [@vertexreg], assuming it holds deployment-approval state and mediates deployment; the
documentation describes a catalogue from which a model is deployed to an endpoint as a separate step,
with no deployment-approval state. The other predicted a preventive serving-time proxy alongside
detective evaluation for Amazon SageMaker Model Monitor [@sagemaker]; monitoring there is scheduled and
asynchronous, off the serving path, so both halves are detective. Neither prediction is rescued, and the
count is unchanged. Reapplying the method with the documented properties yields, in our judgement, a
defensible architecture in each case; this is what prompted the **Instantiate** step of §VII‑A. Every
prediction
reported here was made before that step existed, and none is revised in light of it.

# IX. Discussion

**Preserve, do not reconstruct.** The naïve placements of §VIII‑E and the gap argued at Model Armor
(§VIII‑F) share the same pattern: a control is positioned where it must infer a fact that the
architecture previously held but did not preserve. The remedy is not a better classifier but an
interface that carries the fact:

> **Do not reconstruct by inference what the architecture could have preserved by representation.**

Reconstruction is not merely less accurate: it silently converts a decidable predicate into a
probabilistic one at a boundary the architecture chose. Where the fact cannot be preserved, the answer
is transport, approximation with a named residual or a statement that the obligation is not
architecturally enforceable.

**Residuals should be explicit, not implicit.** The documented systems we examined generally contain
controls; the revealing question is what those controls cannot decide or enforce. Microsoft Foundry
[@foundry] permits deletion of fine-tuned models and uploaded training data but offers no selective removal
of an individual's influence from trained weights, and does not state that residual. We did not count
this as a gap: deleting what can be deleted and declaring the remainder as residual is what the method
prescribes, so the shortfall is one of disclosure rather than placement. Model Armor's documentation
(§VIII‑F) likewise leaves the boundary of its controls implicit. The residual belongs in the
architectural decision record beside the chosen control.

**Governance is often won or lost at the contracts between components.** A characteristic output of the
method is not simply "put the control at X" but "carry this fact, or this verdict, from X to Y, and
protect it in transit". The contract between components therefore becomes a governing artifact, and the
derived integrity obligation of §VII‑E becomes a first-class part of the design. Purview (§VIII‑F)
illustrates this: where its label applies encryption, the label is enforced rather than merely trusted.

# X. Threats to validity

**The method reasons over a model of the architecture, not the architecture.** Both prediction errors in
§VIII‑F arose from structural properties incorrectly attributed to a candidate component rather than from
the transformation rules. Category names such as "registry" and "monitor" implied properties that the
documented products did not have. This is the most practically consequential limitation we identified,
and the Instantiate step (§VII‑A) mitigates rather than removes it.

**Every result is relative to a stated adversary.** We reclassified five obligations under three
adversaries: a careless user (X1), the agent adversary used in the main analysis (X2), and an adversary
able to originate model-bound traffic outside the sanctioned path (X3). As Table 6 shows, Class T falls
from four of five to one. Two obligations are invariant for opposite reasons. Purpose limitation remains
Class O because no location in *L* holds all of $I(o)$; unsanctioned code execution remains Class T
because its enforcement cut lies below every adversary considered. For these nested adversary models,
strengthening the adversary adds available paths, so an obligation can move from T to O and never the
reverse; all fifteen cells are consistent with that. X2 is a middle choice: under X1 four of these five are transparent, under X3 only one.

**Table 6.** Classification of five obligations under three adversary models; the supporting reasoning
for each cell is enumerated in the artifact.

| Obligation | X1 | X2 | X3 |
|---|:-:|:-:|:-:|
| Sensitive disclosure to an external model (§II) | T | O | O |
| Purpose limitation (§VII‑D) | O | O | O |
| Unsanctioned code execution (§VIII‑E) | T | T | T |
| Model inventory completeness (§VIII‑D) | T | T | O |
| Human review before a decision (§VIII‑E) | T | O | O |

**One researcher, incomplete blinding.** All predictions, readings and codings were performed by the same
researcher. Predictions were committed before the corresponding evidence was opened, protocols were sealed by hash before analysis, and the interpretation rule was
fixed before the final coding passes; the hashes, however, were self-recorded rather than
registry-deposited. These safeguards reduce opportunities for
retrospective adjustment but do not substitute for an independent coder. Bibliography verification also
required reading implementation details of retrodiction candidates, causing several cases to be
reclassified from *[clean]* to *[prior]*. Bibliography verification and prediction blinding can therefore compete,
and their ordering must be planned in advance.

**Table 3 does not route every way placement can fail.** It covers deficits of decision and of actuation;
a mediation deficit — no location in *L* cuts the governed effect — has no row, which §VIII‑D's exception
exposed. The symmetric row derived after observing that exception is stated there but remains untested.

**The corpora are purposive, and partly self-similar.** The development corpus was sampled from a fixed
frame but is not representative, and its class distribution depends on the source mix. The untouched test
set was source-disjoint, but source disjointness does not give predicate disjointness: five of its twelve
obligations resemble ones already analysed, while only two resemble nothing in the earlier corpora — and
one of those is the exception. Retrodiction selection was only partly pre-recorded and stopped short of
its target partly on outcome stability (§VIII‑F), and within each stratum the candidate pool was not
enumerated.

**Documentation is a proxy for implementation.** Retrodiction tests what vendors document, not what their
systems actually do. The documentation was read on a single date for products that continue to change.
Findings resting on documented presence are stronger than those resting on omission. This asymmetry
matters for the three gap findings: some rest on documented invocation semantics, whereas others depend
on the absence of documented provenance handling.

**No practitioner study.** No architect other than the author has applied the method or used its
placement records; claims about their usability and review value are design claims, not findings.

**The coupling is a tendency, not a law**, and §IV‑B gives constructions that deliberately defeat it. It
is also stated over a model we constructed: Table 1's attributes are assigned rather than empirically
measured. Table 1 therefore illustrates the proposed tendency; it does not independently test it.

# XI. Conclusion

Context-dependent governance obligations and their enforcement locations tend to be pulled apart by a
recurring design pressure: broad mediation is often obtained through general interfaces that abstract over the application-specific state on which context-dependent
obligations depend — purpose, entitlement, objective and contextual sensitivity. We turn that pressure into a placement method in which the cause of
each deficit determines whether to enforce locally, transport a fact or verdict, approximate and detect,
or declare a residual.

The resulting design lesson is simple: in the cases we examined, placement often turned on the
contracts between components, and every placement decision should state both what its control enforces
and what it cannot.

**Acknowledgment.** OpenAI ChatGPT and Anthropic Claude were used for drafting and language revision; the author reviewed all AI-generated content and retains full responsibility for the research and conclusions.

# References

<!--REFERENCES-->
