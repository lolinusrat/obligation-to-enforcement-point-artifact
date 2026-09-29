# T4 extension study — protocol

**Status: sealed before any case below was analysed.** This file and `t4-cases.json` are hashed in
`sealed/T4-SEAL.txt`. Nothing in either may be added to, removed or reworded after sealing; corrections
take the form of dated amendments appended below. The derivation, independent and comparison passes are
sealed in turn, each before the next begins.

## 1. What this study tests, and what it does not

The untouched test (held-out set 2) exposed a case the frozen method could not route: an obligation for
which no single adequate cut exists (K6, a mediation deficit). The method reports such a deficit but
derives nothing. This study proposes and tests one extension, **T4 — complementary enforcement
composition**, for exactly that situation.

It asks two questions:

- **EQ5a.** When no single adequate cut exists, does T4 derive a complementary set of enforcement points
  that the case facts show can enforce the obligation on every path?
- **EQ5b.** Does T4 correctly *refuse* to call an obligation enforced when the combined locations cover
  every path but cannot all decide and act — coverage without enforceability?

It is **not** a test of external validity. The eight cases are constructed by the author to span
feasible, approximable and unenforceable path structures. Constructed cases can test whether the rule
is applied consistently and whether it separates coverage from enforceability; they cannot show that T4
is effective in deployed enterprise architectures. K6 motivated the extension and is used here only as a
diagnostic case (D0); it is excluded from every count. The original 11/12 result of held-out set 2 and
its exception are unchanged by this study, and nothing here is merged into them.

## 2. The rule under test, frozen here

T4 applies only after step 4 of the procedure finds **no single adequate cut** over ⟨S, X⟩. It replaces
the report of a bare mediation deficit with a per-path analysis.

1. **Partition.** List the adversary-available paths $S_X$ by which the governed effect can be realised,
   and for each path the candidate locations in *L* it traverses.
2. **Per-path placement.** For each path *p*, apply steps 5–6 of the procedure (Diagnose, Transform) at
   each location on *p*, as if *p* were the whole scope, and assign *p* to one location using the
   existing precedence: a location feasible after T1/T2 first; otherwise one that can approximate (T3).
3. **Per-path outcome.** Exactly one of:
   - **enforced** — some location on *p* holds, natively or by T2 transport, every fact in $I(o)$, and
     its actuation includes $R(o)$;
   - **approximated** — no location on *p* is enforced, but one has $R(o)$ and every missing fact has a
     defensible proxy, *and* either the preventive over-approximation on *p* is acceptable under the case
     facts, or the effect is reversible and a later detection control is specified;
   - **residual** — neither: *p* traverses no location in *L*, or no location on *p* can act, or the
     missing facts can be neither transported nor adequately approximated.
4. **Compose.** The complementary set is the union of assigned locations, preferring locations that
   serve more paths. For every assertion transported to more than one location, record a
   **cross-control consistency obligation**: the same issuer, binding, validity and policy version must
   govern each use.
5. **Case outcome.** **F** (feasible complementary set) if every path is enforced; **A** (adequate
   approximation with explicit residual) if every path is enforced or approximated and at least one is
   approximated; **U** (not adequately enforceable in the modelled architecture) if any path is residual.

**Reconciliation with the post-test mediation row** (held-out set 2, `heldout-2-test.md` §2): that row
routed a mediation deficit to T3 or Terminal for the obligation as a whole. T4 subsumes it at path
granularity: a path with no adequate location becomes approximated (T3) or residual (Terminal), and
paths that *do* have an adequate location are no longer lumped with them.

## 3. Cases

`t4-cases.json` fixes, for each case, only facts about the estate: the obligation and its $I(o)$ and
$R(o)$; where each fact's authoritative value or judgement lives and whether it (or a verdict on it) may
cross; each location's native facts, responses, and whether its interface can receive transported
assertions; the paths and the locations each traverses; whether the effect is reversible; whether a
proxy exists; whether conservative over-approximation is acceptable on a path; and whether a later
detection control exists. It contains no outcome and no derivation.

Cases C1–C8 are the test set. D0 (K6) is diagnostic only. Every case was written so that no single
location in *L* is an adequate cut; `verify.py` checks this from the file.

## 4. Procedure

Four passes, each written to its own file and hashed before the next begins:

1. **Cases** — this file and `t4-cases.json` (sealed together).
2. **Derivation pass** (`t4-derivations.md`) — T4 applied to each case from the case facts only.
3. **Independent pass** (`t4-independent.md`) — for each case, written without reopening the derivation
   file: what the enforcement architecture should be, and whether the obligation is adequately
   enforceable on every path, argued from the estate directly.
4. **Comparison and coding** (`t4-test.md`) — the two set side by side; one row per case.

**This separation is procedural, not cognitive.** One analyst writes all passes, as in held-out set 2;
sealing fixes what was claimed and when, not independence.

## 5. Coding and criteria, fixed before analysis

Per case: the T4 outcome (F / A / U), the independent outcome (F / A / U), and **agreement** (✓ same
outcome and same complementary set; ~ same outcome, different set; ✗ different outcome).

- **Soundness (must hold for every case).** `verify.py` re-applies §2 mechanically to `t4-cases.json`
  and must reproduce every per-path outcome recorded in the derivation pass. A derivation that calls a
  path enforced when the facts do not support it fails the study outright.
- **EQ5a pass** iff at least one case codes F in the derivation pass and every F agrees (✓ or ~) with the
  independent pass.
- **EQ5b pass** iff every case the independent pass codes U is also U in the derivation pass — T4 never
  declares an unenforceable case enforceable.
- **Overall pass** iff soundness, EQ5a and EQ5b all hold, and at least **6 of 8** cases agree (✓ or ~).
- **Method-level failure** iff the independent pass finds an adequate architecture for some case that
  needs a construct outside T1–T3, Terminal and per-path composition (for example, cross-path
  coordination that no single location can perform).
- **Reporting rule.** All eight cases are reported whatever they show. No case may be dropped, reworded
  or exchanged after sealing. If the study fails, T4 is reported as a failed extension and remains
  future work. If it passes only on these constructed cases, it is reported as a **preliminary extension**,
  never as a validated fourth transformation.
- **Stopping rule.** Exactly these eight cases; none are added after sealing.
