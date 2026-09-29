# Apply the method — worksheet

One obligation per sheet. Fill top to bottom; do not skip to the transformation.

---

**Obligation** (verbatim, with source): ______________________________________

**Frame**
- Scope `S` — the effect being governed, and the paths that realise it: ________
- Adversary `X`: ______________________________________________________________

**Step 1 — Filter.** Does it constrain a mediated action?
☐ No → **Class N**, out of scope. Stop.  ☐ Yes → continue.

**Step 2 — Derive `I(o)`.** Every fact the predicate needs.

| # | Fact |
|---|---|
| f1 | |
| f2 | |
| f3 | |
| f4 | |

**Step 3 — Instantiate.** Establish each candidate location's actual
information, mediation and actuation properties from what the component
actually does, not from its category name. Read them from the component's
own documentation. Both prediction errors in the paper's retrodiction study
came from skipping this step.

| Location | `A(l)` holds | cut over ⟨S,X⟩? | `α(l)` admits | Evidence for these properties |
|---|---|---|---|---|
| | | | | |
| | | | | |

*Evidence* means a documentation reference, an architecture diagram or an
observed implementation — not the component's category name. A property with
no evidence is an assumption; mark it as one.

**Step 4 — Locate.** Identify the maximal *adequate* cuts over ⟨S, X⟩: the
locations every path available to `X` must traverse, whatever they know or can
do. Do **not** exclude a cut because its actuation looks inadequate; actuation is
diagnosed in step 5. Use the operational qualities to choose among incomparable
candidates.

- If some adequate cut already holds every fact in `I(o)` and admits the
  required responses, the obligation is **Class T**: enforce there (T1), even if a
  more broadly mediating cut lacks a fact.
- If **no** adequate cut exists, record a **mediation deficit**. The
  transformation table has no row for it: go to step 7 and state it in the
  residual.

Maximal adequate cuts (there may be more than one): _____________________________

Selected cut, and the operational quality that chose it: _____________________

**Step 5 — Diagnose, per fact.**

| Fact | Present at the cut? | If absent, cause | Or is the obstacle `α`? |
|---|---|---|---|
| f1 | | | |
| f2 | | | |
| f3 | | | |
| f4 | | | |

Causes: representational · authority · epistemic (renderable / approximable /
unrenderable) · temporal · actuation.

**Step 6 — Transform.** Apply the table in `method-summary.md` §3, per fact.

| Fact | Transformation | If transport: fact or verdict? |
|---|---|---|
| f1 | | |
| f2 | | |
| f3 | | |
| f4 | | |

**Step 7 — Compose.**
- Resulting architecture: ______________________________________________________
- Derived integrity obligations from each transport, and where each closes: ____
- For each transported **verdict**, its validity condition:

  | Verdict | Issued by | Bound to | Expires | Invalidated by |
  |---|---|---|---|---|
  | | | | | |

  Binding prevents substitution and tampering; it does not make the original
  judgement true. What the issuer could get wrong belongs in the residual.
- **Residual** — everything the architecture leaves unenforced, stated plainly.
  Check each source:
  - terminal outputs (an unrenderable fact; an actuation deficit with no
    adequate substitute; a mediation deficit from step 4): ____
  - what each transported **verdict** leaves unenforced — the cut acts on what
    another party asserts (for example, a falsely declared purpose): ____
  - what each **approximation** leaves unenforced, including any T3 whose effect
    is not reversible within its detection latency: ____
  - paths outside the stated scope that still realise the effect (for example,
    reuse of a copy already retrieved): ____

---

*A blank residual for a placement-obstructed obligation means the worksheet is
not finished. Whether a stated residual is acceptable is a governance decision
the method informs but does not make.*
