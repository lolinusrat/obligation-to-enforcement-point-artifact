# Adversary sensitivity of the classification

**What this is.** A sensitivity analysis of a claim the paper makes throughout: that Class N/T/O is
relative to ⟨*S*, *X*⟩, and that a placement statement has no truth value until the adversary is named.
The paper asserts this and gives one instance (§VIII‑D's model-inventory row). Here the claim is
enumerated: five obligations already analysed elsewhere in the paper, re-classified under three
adversary models, with all fifteen cells reported.

**What this is not.** It is not a fifth study and is not sealed as one. Its central prediction is
*derivable* rather than empirical — see §3 — so pre-specification would add little; what matters is that
the enumeration is complete and checkable. No obligation was added, dropped or reworded to produce the
pattern, and the five were chosen before the cells were worked out, to span the classes and the deficit
causes already reported rather than to produce a particular distribution.

## 1. The three adversary models

| | Adversary | Paths available to it |
|---|---|---|
| **X1** | **Careless user.** A legitimate user who may mishandle data but does not deliberately route around controls. | the sanctioned application path only |
| **X2** | **The paper's model (§V‑A).** A prompt-injected or misdirected agent inside an otherwise trusted application. | any call the application and its SDK expose, in any order, without passing back through application-layer checks |
| **X3** | **Off-path originator.** An adversary able to originate model-bound traffic outside the sanctioned application path — a compromised application host, or an insider standing up an unsanctioned deployment. | additionally, direct traffic to model endpoints and external services, bypassing the gateway |

The three are nested by construction: every path available to X1 is available to X2, and every path
available to X2 is available to X3. X3 stops short of a compromised platform runtime, which would
dissolve Z8 as well and is out of scope for all of the paper's studies.

## 2. The five obligations

Chosen to span the reported classes and deficit causes, and all analysed elsewhere in the paper so that
the X2 column can be checked against what is already published.

| | Obligation | Where it is analysed | Deficit at its strongest cut under X2 |
|---|---|---|---|
| O1 | Commercially sensitive information must not be disclosed to an externally hosted model without a legitimate business purpose | §II, §VII‑D | representational + epistemic |
| O2 | Personal data must not be further processed incompatibly with its collection purpose | §VII‑D, Table 4 | representational + epistemic-renderable |
| O3 | Agent-generated code must not execute outside a sanctioned sandbox | §VIII‑E | none |
| O4 | A model may not be in production use without being recorded in the inventory | §VIII‑D (K7) | none |
| O5 | A consequential decision requires human review before it is issued | §VIII‑E (naïve placement) | epistemic-renderable |

## 3. The prediction, and why it is derivable

*cut(l | S, X)* holds iff every path by which *X* can realise the governed effect traverses *l*. If the
paths available to X′ are a superset of those available to X, then any *l* that is a cut under X′ is a
cut under X. Feasible sets therefore shrink monotonically as the adversary strengthens, so:

> **An obligation may move from Class T to Class O as the adversary strengthens, and never the reverse.**

This follows from the definition and is not an empirical finding. What the enumeration can show is
(a) whether the analysis is internally consistent with it across fifteen cells, and (b) *how much*
classification actually moves — which the definition does not tell us.

## 4. Results

| | Obligation | X1 | X2 | X3 | Why it moves, or does not |
|---|---|:-:|:-:|:-:|---|
| O1 | Sensitive disclosure to an external model | **T** | **O** | **O** | Z2 holds all five facts and mediates every path a careless user takes. An injected agent reaches the model without passing back through Z2, so the cut moves to Z4, which lacks sensitivity in context, purpose and entitlement. X3 additionally bypasses Z4, leaving only Z7 and a larger deficit. |
| O2 | Purpose limitation | **O** | **O** | **O** | Invariant. Z6 mediates every path to the record under all three adversaries, including X3, since it is enforced by the data service rather than the application. The obstruction is informational — collection purpose is absent from the served record — and no adversary changes that. |
| O3 | Unsanctioned code execution | **T** | **T** | **T** | Invariant. The cut is the platform runtime Z8, which lies *below* every adversary in scope; the predicate ranges over process and host behaviour, which Z8 holds natively. |
| O4 | Model inventory completeness | **T** | **T** | **O** | Z4 mediates all model-bound traffic for X1 and X2 and can perform the registry lookup. X3 originates traffic outside the gateway, so Z4 ceases to be a cut; Z7 remains one but cannot see model identity, and the deficit becomes representational. |
| O5 | Human review before a decision | **T** | **O** | **O** | The application mediates the careless user's path and holds the review state. An injected agent reaches the governed effect without traversing the approval workflow, which is why §VIII‑E records this placement as one the method rejects under X2. |

**Class T count: 4 / 5 under X1, 2 / 5 under X2, 1 / 5 under X3.**

Every row is non-increasing in adversary strength. **Fifteen of fifteen cells are consistent with the
monotonicity property**; a single T appearing to the right of an O would have indicated an error in the
analysis, since it is impossible under the definition.

## 5. What it shows

**The classification is adversary-relative, and by a large margin.** Four of these five obligations are
transparent against a careless user; one is transparent against an off-path originator. A placement
claim made without naming *X* is therefore not merely imprecise, it is unfalsifiable.

**Two obligations do not move, for opposite reasons.** O2 is Class O under every adversary because its
obstruction is informational rather than mediational — strengthening the adversary cannot destroy a fact
that was already absent. O3 is Class T under every adversary because its cut lies below all of them.
Adversary sensitivity is therefore not a uniform degradation: it bites exactly where classification
depends on mediation, which is what the definition predicts and what §IV's coupling is about.

**Our adversary is not the one that most favours the method.** Under X1, four of these five obligations
are transparent, and the placement problem the paper describes would look considerably smaller. X2 was
fixed before the first obligation was coded, for the reason §V‑A gives — it is the adversary an
enterprise deploying agents actually faces — and not because it maximises Class O. A reader who thinks
X2 too strong can read the X1 column; a reader who thinks it too weak can read X3.

## 6. Limits

Same analyst, same interpretive judgement as everywhere else in the paper; this is a re-analysis of the
author's own classifications under varied assumptions, not an independent check of them. Five
obligations is a small enumeration, chosen to span rather than to sample. And X3 is bounded: a
compromised platform runtime would dissolve Z8 and would make O3 Class O as well, which is outside the
scope every study in this paper assumes.
