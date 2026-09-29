# T4 extension study — comparison and coding

Against the sealed protocol, case file, derivation pass and independent pass (hashes in
`sealed/T4-SEAL.txt`). Codes as fixed in protocol §5.

## 1. Soundness

The rule of protocol §2 was re-applied mechanically to `t4-cases.json` (the implementation is in
`verify.py`). It reproduced all **18 of 18** per-path outcomes recorded in the derivation pass, including
the two diagnostic D0 paths. **Soundness holds.**

## 2. Results (machine-read by `extract.py`)

| case | T4 outcome | independent outcome | agreement | note |
|---|---|---|---|---|
| C1 | F | F | ✓ | same set {Z4, Z7}; both identify the shared-issuer consistency obligation |
| C2 | A | A | ✓ | same set; T4's residual understated — see §3.1 |
| C3 | U | U | ✓ | same set {Z4}; unmanaged device residual in both |
| C4 | F | F | ✓ | same set; independent pass adds refusal of unlabelled legacy index entries — see §3.2 |
| C5 | F | F | ✓ | same set {Z3, Z6}; capability token in both |
| C6 | U | U | ✓ | coverage without enforceability recognised by both |
| C7 | F | F | ✓ | same set {Z4, Z8}; shared register version |
| C8 | A | A | ✓ | same set; requester attribution missing on batch calls in both |

## 3. Criteria

- **Soundness:** 18/18. **Holds.**
- **EQ5a** (feasible sets derived and confirmed): four cases code F (C1, C4, C5, C7), and all four agree.
  **Pass.**
- **EQ5b** (no unenforceable case declared enforceable): the independent pass codes C3 and C6 U; T4 codes
  both U. C6 is the coverage-without-enforceability case: {Z5a, Z7} covers both paths, and T4 still
  returns a residual. **Pass.**
- **Agreement:** 8 of 8 (✓). Threshold 6. **Pass.**
- **Method-level failure:** none. No case needed a construct outside T1–T3, Terminal and per-path
  composition.

**Overall: pass — on constructed cases only.** Per the reporting rule, T4 is reported as a
**preliminary extension**, not a validated fourth transformation.

## 4. What the comparison exposed

### 3.1 An over-approximation's residual must say what the approximation still admits

In C2, the derivation's residual was "the functional cost of over-blocking; no disclosure path is left
unenforced". The independent pass saw that a destination allow-list leaves anything sent to an
allow-listed *external* endpoint unchecked. The outcome and the set agree, but T4's residual statement
was incomplete: the rule records that over-approximation is acceptable without requiring the record to
say what the approximation boundary still lets through. This is a refinement to the *application* of
the rule, recorded here and not folded into the rule as tested.

### 3.2 Transport does not repair copies made before it

In C4, transporting the collection-purpose label into the index protects entries ingested from now on.
Entries already in the index carry no label, and until they are re-ingested the index must refuse them.
T4, like the per-fact method it extends, reasons about the flow of facts, not about state already
copied. The independent pass handled this; the rule does not. Recorded as a post-test observation.

### 3.3 What the 8/8 does and does not show

The author constructed the cases, fixed their facts, wrote both passes and coded them. Agreement at 8/8
therefore shows that the rule is applied consistently, separates path coverage from enforceability, and
localises K6's gap to a single path; it does not show that T4 finds adequate complementary sets in
architectures nobody constructed for the purpose. The two observations above are the more informative
result: each is a place where reasoning about the estate saw something the rule does not represent.
