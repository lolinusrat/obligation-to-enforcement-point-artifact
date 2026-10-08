# Reproducibility artifact — *From Obligation to Enforcement Point*

Everything needed to check the paper's analysis, or to apply the method to an
obligation the paper never saw.

## Reproduce the paper's results

One command. No configuration, no network, no dependencies beyond Python 3,
run from this folder (the repository root, or `artifact/` in the zip):

```
python3 verify.py
```

It exits 0 only if every check passes, and non-zero on any disagreement. Check
the exit code, not just the count line: the recomputed evaluation section is
printed after the count.

```
175/175 checks passed

The paper's evaluation section, recomputed from the data files:

  VIII.A  sampling frame, fixed before classification        268 items; 25 admitted
  VIII.A  ISO/IEC 42001 Annex A controls that are Class N    29 of 38 (the paper claims at least 24)
  VIII.B  classification of the development corpus           15 Class T, 10 Class O of 25
  VIII.B  Class O rate by source                             agentic 71%, rights-based 50%, operational 17%
  VIII.B  the same under the §VI definition                  agentic 86%, rights-based 83%, operational 17%
  VIII.C  held-out set 1, the pre-test rules                 13 of 15 handled; 2 exceptions
  VIII.D  held-out set 2, the final method, pre-specified    11 of 12 routed (9 clean, 2 strained); 1 exception
  VIII.D  mirroring of held-out set 2 against earlier corpora 5 close, 5 partial, 2 none
  VIII.F  documented-architecture retrodiction               D0+D1 8, D2 3, D3 2, D4 1 of 14
  VII.E   transport recursion, one-step terminations         12 constructed, 3 documented
  VII.B   cause ablation, deficit-bearing obligations        33 of 35 across 4 transformations
  X       adversary sensitivity, Class T by adversary        4 of 5 (X1), 2 of 5 (X2), 1 of 5 (X3)
  VIII.G  T4 extension (constructed cases, preliminary)      F 4, A 2, U 2 of 8; agreement 8/8; soundness 18/18
```

Every line above is computed from a column of a CSV in `data/`, which is in turn
derived from a protocol file in `protocols/`. `CLAIMS.md` names the file and the
column behind each one, with a shell command to recompute it by hand, and holds
the counting rules the paper refers to.

### What the 175 checks are

Each check prints its source in brackets, so the kinds can be told apart
without reading the Python:

- **109 recompute results from the data.** Their source is a CSV or protocol
  file only. They count, tally and cross-check the corpora, independently of
  the paper's text.
- **23 compare the paper with the data.** Their source is
  `manuscript-claims.md`, and they read a number or an id list out of the
  paper's prose and require it to equal the recomputed value.
- **43 are true/false checks on the paper's wording.** Their source is also
  `manuscript-claims.md`. Most require a qualification to be present (for
  example, that the protocol was "sealed by hash rather than deposited with a
  registry") or a withdrawn claim to be absent (for example, "pre-registered");
  these guard against drift and recompute nothing. A few pair such a phrase with
  a recomputed value — the per-source Class O rates, for example — and pass only
  if both hold.

`manuscript-claims.md` is the shared text of the paper with author identity removed,
written by the build. The public preprint adds explanatory material but no counts.

## The T4 extension study (public preprint only)

A preliminary extension, T4 (complementary enforcement composition), is tested
separately on eight constructed cases. Its rule, case facts and three analysis
passes are in `protocols/t4-*.md` and `protocols/t4-cases.json`, sealed in order
in `protocols/T4-SEAL.txt`; `protocols/t4-errata.md` records one numbering slip
in the sealed coding file. `verify.py` checks every seal, re-applies the rule to
the case facts independently of the derivation file (soundness: 18/18 per-path
outcomes), and recomputes the counts. The cases were constructed by the author:
the study shows consistent application and the separation of coverage from
enforceability, not effectiveness in real architectures.

## Contents

| Path | What it is |
|---|---|
| `method-summary.md` | The method in two pages: classes, location attributes, deficit causes, transformations, composition |
| `apply-the-method.md` | Worksheet — obligation to residual, one sheet per obligation |
| `worked-placement-records.md` | The paper's two worked examples (§II, §VII‑D) filled in as complete placement records, plus the paper's rule for each judgement the worksheet asks for |
| `data/development-corpus.csv` | 25 architecturally enforceable obligations, with `I(o)`, cut, deficit, class and transformation |
| `data/held-out-corpus.csv` | 15 obligations from disjoint sources; predicted transformation recorded before the independent answer |
| `data/held-out-2-corpus.csv` | 12 obligations from four further disjoint sources, run against the **final** method under a pre-specified, sealed protocol |
| `data/adversary-sensitivity.csv` | 5 obligations re-classified under three adversary models, with the reasoning for each of the 15 cells |
| `data/retrodiction-cases.csv` | 14 documented-system cases: locked prediction, blind status, documented placement, D0–D4 code, rationale |
| `data/sampling-frame.csv` | The 268-item frame the corpus was drawn from, and how many each source contributed |
| `data/iso42001-frame.csv` | All 38 ISO/IEC 42001 Annex A controls, each with its Class N decision and the basis for it |
| `data/transport-recursion.csv` | All 26 transport cases across the four studies, and which the paper counts |
| `evidence/manifest.csv` | The 7 first-party vendor sources, with access dates |
| `CLAIMS.md` | Every number in the paper's evaluation section, and the file and column that produce it |
| `verify.py` | Recomputes all of them and fails if the paper and the data disagree |
| `protocols/` | The frozen selection, prediction and interpretation protocols, with their amendment history, and the held-out-2 protocol, prediction and independent passes with the hashes that seal them |
| `novelty-comparison.md` | Claim boundary against XACML/ZTA, Swiss Cheese, Koch, SARC and the antecedents of cause-keyed selection (Letier, PTaCL, usage control) |
| `expert-evaluation/` | A fifth study, **specified and not run** — see below |
| `extract.py` | Regenerates the CSVs from the protocol files |
| `manuscript-claims.md` | Snapshot of the paper's shared text (author identity removed), so the prose checks run without the paper |

## The CSVs are derived, not authored

`protocols/*.md` are the source of truth. `extract.py` reads them and writes
`data/*.csv`, checking that it recovers 25, 15, 12 and 14 rows. Re-run it after any
change so the artifact cannot drift from the analysis:

```
python3 extract.py
```

`verify.py` re-runs it too, and fails if the CSVs are not byte-identical to what
the current protocol files produce — so a hand-edit to a CSV cannot survive a
verification run.

**On the word "pre-registered".** The paper does not use it, and neither does
this README. The protocol was written, hashed, and the hash recorded before any
analysis; it was **not** deposited with a third-party registry. The seals
therefore establish that the protocol shipped here is the one the analysis was
run against — nobody can edit it after the fact and have it still verify — but
they are self-recorded and do not establish independently timestamped priority.
The file is still named `heldout-2-preregistration.md` because renaming it would
break the hash recorded in `HELDOUT2-SEAL.txt`, which is the one thing about it
that must not change.

## What the checker checks

The package is self-contained. Every file the checker reads is inside it,
including `manuscript-claims.md`, the snapshot of the paper's shared text that
the prose checks — case ids, system names, dates, spelled-out counts — are run
against. Nothing outside the extracted directory is consulted, so the result
does not depend on where it is unpacked or on what happens to sit beside it.

The checks come in three layers. Most recompute a number from a column. Others
tie the paper's *prose* to the data — the transport case numbers named in §7.5,
the systems named in §8.5, the evidence and literature-freeze dates, the counts
the paper spells out in words, and the claim that the two prediction errors fall
in different deficit causes. The last layer checks the **seals**: the SHA-256 of
the held-out-2 protocol and of each of its two analysis passes is
recomputed from the shipped file and compared with the hash recorded when it was
sealed, so a protocol that was edited after the fact cannot pass. All three
layers run from the package as shipped.

`CLAIMS.md` is the same thing in prose: one row per claim, naming the file, the
column, and how to recompute it by hand if you would rather not trust our
script. In outline:

- **Classification (n=25).** `development-corpus.csv`, column `class_norm`:
  15 T, 10 O. Per-source Class O rates come from the `source` column — 71%
  agentic, 50% rights-based legal, 17% operational.
- **Held-out set 1 (n=15).** `held-out-corpus.csv`, column `applicable`: yes in
  13. The two exceptions produced the actuation branch and the three-way
  epistemic split; both are documented in `protocols/heldout-test.md` §2.
- **Held-out set 2 (n=12).** `held-out-2-corpus.csv`, column `applicable`: yes in
  11. This is the pre-specified study of the *final* method against sources that
  played no part in producing it. `applicability` separates the 9 clean rows from
  the 2 with a recorded strain; `agreement` compares the sealed prediction with
  the sealed independent pass; `mirroring` records how far each obligation
  resembles one already analysed, which is the qualification the paper puts on
  the count. The single exception, K6, is a mediation deficit — a way of failing
  that Table 3 has no row for.
- **Retrodiction (n=14).** `retrodiction-cases.csv`, column `code_norm`: D0 5,
  D1 3, D2 3, D3 2, D4 1. The interpretation rule was fixed before the final
  coding passes and is in the paper's evaluation section, not restated here, so
  there is one normative copy.
- **Transport recursion.** `transport-recursion.csv`: seven counted development
  instances and five from held-out set 2. The file additionally records
  documented-system transport cases; the paper cites all three (P4, P12, P13)
  as its documented corroborating instances. C2PA is constructed case K4.
  The file also lists the transport cases the paper does *not* count, with the
  reason.
- **The cause ablation.** `protocols/expressiveness-ablation.md` removes one
  input from the method — why each fact is missing — and counts what it can still
  return. It authors no data: it re-tabulates the codings already in `data/`, and
  `verify.py` recomputes the counts from those files rather than reading them
  from the note. It is an ablation of our own method, **not** a comparison
  against SARC or any other published method; the note says why that distinction
  matters.
- **Adversary sensitivity (n=5).** `adversary-sensitivity.csv`: each obligation's
  class under three nested adversary models, with the reasoning per cell. The
  checker recomputes the Class T counts behind the paper's §X claim and verifies
  that no row recovers Class T under a stronger adversary — impossible under the
  definition of a cut, so a violation would mean the analysis is wrong. This is a
  sensitivity analysis, not a fifth study: it is not sealed, and its central
  property is derivable rather than empirical.
  `protocols/adversary-sensitivity.md` says so explicitly.
- **ISO Annex A scope finding.** `iso42001-frame.csv`: all 38 controls, each
  with a Class N decision. The paper claims "at least 24"; this enumeration
  reads 29. `CLAIMS.md` explains why the two differ and which controls are
  actually in dispute.

**Two columns per coded field, and why.** `class`, `match`, `code`,
`applicability`, `agreement` and `mirroring` are the frozen coding exactly as
written during the run, emphasis and qualifiers included (`**T\***`, `✓*`,
`D2 (form b)`, `A−`). Each has a plain twin — `class_norm`, `applicable`,
`code_norm`, `agreement_norm`, `mirroring_norm` — so that a tally reproduces the paper's numbers
rather than a histogram of typography. The twins are derived, never authored,
and `verify.py` recomputes each one from its frozen column, so the convenience
copy cannot drift from the record.

## Applying it to something new

Take an obligation the paper never used. Fix the scope and adversary, then work
`apply-the-method.md` top to bottom. Two failure modes are worth naming in
advance because the paper hit both:

1. **Do not read a location's attributes off its category name.** Establish what
   the component actually holds, mediates and can do, from its documentation.
   Both prediction errors in the paper came from skipping this.
2. **Do not leave the residual blank.** For a placement-obstructed obligation, an
   architecture recorded without its residual is incomplete.

## The study that was not run

`expert-evaluation/` contains a pre-specified inter-rater reproducibility study —
whether architects other than the author reach the same diagnosis. It is
**not run**: it is human-participant research and is gated on an ethics
determination, which cannot be obtained retrospectively for data already
collected. The protocol is included because a pre-specified study that has not
been run is more useful to a reader than a description of one that might be.

## Honest limits of this artifact

It makes the analysis inspectable. It does not make it independent: one
researcher produced every prediction, read every document and assigned every
code. That limitation is stated in the paper and is not repaired by publishing
the working.
