# The method, in two pages

Self-contained summary for applying the method without the paper.

## 0. Fix the frame first

Nothing below is defined without these two:

- **Scope `S`** — the set of execution paths through which the governed effect
  can be realised.
- **Adversary `X`** — whose avoidance of the control you are reasoning about.
  The paper assumes a prompt-injected or misdirected agent inside an otherwise
  trusted application, plus a careless user. *Change `X` and classifications
  change.* "Bypass resistance" has no truth value until `X` is named.

## 1. Three obligation classes

| Class | Test | Consequence |
|---|---|---|
| **N — non-architectural** | constrains no mediated action; discharged by a document, review or role | out of scope. A substantial share of the governance material examined is here: at least 24 of 38 ISO/IEC 42001 Annex A controls |
| **T — transparent** | some location is a cut with adequate actuation and `I(o) ⊆ A(l)` | enforce at a maximal feasible location; operational qualities choose among incomparable candidates |
| **O — placement-obstructed** | every adequate cut carries a deficit, or no cut has adequate actuation | apply §3 |

The T/O criterion is whether `I(o)` **survives the abstraction** at a location
that adequately mediates the effect.

## 2. Three attributes per location

Placement consumes only these:

- **`A(l)`** availability — facts observable or derivable at `l` at decision time, without new plumbing.
- **cut** — `l` is a cut in `S` iff every path by which `X` can realise the effect traverses `l`.
- **`α(l)`** actuation — the responses available at `l` given its position relative to the effect.

`F(o) = { l : I(o) ⊆ A(l) ∧ cut(l | S,X) ∧ α(l) ⊇ R(o) }`. It can be empty for
three independent reasons: cannot decide, cannot mediate, cannot act.

**Instantiate these from the actual component, not from its category name.** Both
prediction errors in the paper's evaluation came from assuming a "registry"
gates deployment and a "monitor" sits on the serving path. Neither did.

## 3. Deficit cause determines the transformation

Apply **per missing fact**, not per obligation.

| Locus | Cause | Transformation |
|---|---|---|
| — | no deficit | **T1 Relocate** — enforce there |
| `A(l)` | representational | **T2 Transport (fact)** — restore the representation across the boundary |
| `A(l)` | authority | **T2 Transport (verdict)** — the fact may not cross; the decision may |
| `A(l)` | epistemic, renderable | **T2 Transport (verdict)** — the party who can judge decides; the cut enforces |
| `A(l)` | epistemic, approximable | **T3 Approximate-and-detect** |
| `A(l)` | epistemic, unrenderable | **Terminal — declare residual** |
| `A(l)` | temporal | **T3 Approximate-and-detect** — preventive over-approximation at the cut, detective evaluation of the true predicate after the effect |
| `α(l)` | actuation | **T3** where an approximation of the required response exists; otherwise **Terminal** |
| `cut(l)` | mediation | *no row — see below* |

T3's detective half is adequate only if the effect is reversible within the
detection latency.

**The table does not cover the mediation locus.** `F(o)` can be empty for three
reasons and this table routes two of them. Held-out set 2 found the third: an
obligation on what a third party does to an asset after it has left the estate
has no cut in `L` at all, so the function diagnoses the obstruction and returns
nothing (`protocols/heldout-2-test.md` §2). The symmetric repair — **T3** where a
detectable approximation of the mediation exists, otherwise **Terminal** — is
recorded there and deliberately *not* applied here or in the paper's Table 3,
because it was derived from the single case that exposed it and nothing has
tested it.

## 4. Compose, recurse, declare

- **Compose.** The architecture is the composition of the per-fact
  transformations; the residual is the union of the terminal ones.
- **Recurse.** Every transport makes a strong location act on an assertion from a
  weaker one. The integrity of that assertion is a new obligation. Its predicate
  ranges over provenance facts, which survive abstraction, so it is Class T and
  closes at the identity or signing layer. *In the seven counted development cases and the five of held-out
  set 2, the derived obligation closed by T1 in one step; Microsoft Purview and
  C2PA's claim signature provide two documented corroborating instances. This is
  not claimed as universal.*
- **Declare.** A placement decision recorded without its residual is incomplete.
