# Claim-to-file traceability

Every quantitative claim in the paper's evaluation section, and the file that
produces it. `verify.py` recomputes all of them and exits non-zero on any
disagreement, so this table is checked rather than asserted:

```
python3 verify.py        # 172 checks, then the evaluation section recomputed
```

The column headed **recompute** is a command you can run yourself, from this
directory, without reading our code.

`verify.py` also checks the claims that are made in prose and cannot be
recomputed from a column: the seven transport item numbers in §7.5, the six
systems named individually in §8.5, the evidence date against every manifest
entry, the literature freeze date, the pre-specified failure thresholds, and the
statement that the two prediction errors fall in different deficit causes. Those
checks fail if the paper and the data drift apart. It additionally recomputes the
SHA-256 of the held-out-2 protocol and of both of its analysis passes and
compares them with the hashes recorded at sealing time, so a protocol edited
after the fact cannot pass.

## §VIII.A — corpus construction

| Claim in the paper | File | Recompute |
|---|---|---|
| Sampling frame of 268 items, fixed before classification | `data/sampling-frame.csv` | `awk -F, 'NR>1{n+=$2}END{print n}' data/sampling-frame.csv` |
| 9 AI Act · 38 ISO · 211 NIST · 10 OWASP | `data/sampling-frame.csv` | column `items_in_frame` |
| Keyword filter admitted ~40 of 211 NIST actions; 8 taken | `protocols/classification-corpus.md` §1 Filter 2 | the 16 terms are listed there verbatim; `items_admitted_to_corpus` = 8. The ~40 is as recorded in the protocol at the time; the list of matches was not retained, so it cannot be recomputed, and the paper says so |
| At least 24 of 38 ISO Annex A controls are Class N | `data/iso42001-frame.csv` | `awk -F, 'NR>1&&$3=="yes"' data/iso42001-frame.csv \| wc -l` |
| 25 obligations remained | `data/development-corpus.csv` | `tail -n +2 data/development-corpus.csv \| wc -l` |

**The ISO Annex A result, and why the paper says "at least 24".** All 38
controls are now enumerated in `data/iso42001-frame.csv` with a per-control
Class N decision and the basis for it, so the scope finding can be recounted
instead of taken on trust. Recounting does not return 24. It returns **29**.

The `basis` column says why, and separates three groups:

- **16 controls** in the families the frozen note names — A.2.x policies,
  A.3.x roles, A.5.x impact assessment, A.8.x external reporting, A.10.x
  suppliers and customers — are Class N on the original coding. Not in dispute.
- **5 controls** entered the development corpus (A.6.2.5, A.6.2.6, A.6.2.8,
  A.7.5, A.9.4) and are therefore non-N. Not in dispute.
- **17 controls** were never individually recorded. The original 24 implies 8
  of them are Class N; this recount reads 13 as Class N. That difference is the
  whole of the disagreement.

The recount is a post-hoc reconstruction by the same single coder, made after
the fact, and its control titles should be checked against a copy of the
standard before anyone leans on it. It is not presented as a correction, since
there is no per-control original coding to correct. The manuscript claims "at
least 24 of 38", which both readings support, and `verify.py` checks that the
enumeration satisfies it rather than checking for a specific number. The scope
finding — that a substantial share of the governance material examined is
not architecturally placeable — holds either way, and holds more strongly under the recount.

## §VIII.B — obligation classification

| Claim | File | Recompute |
|---|---|---|
| 15 Class T, 10 Class O | `data/development-corpus.csv` | `cut -d, -f8- data/development-corpus.csv \| ...` — or read column `class_norm` |
| The "40% figure" | same | 10/25 |
| 71% of agentic obligations are Class O | same, `source` = OWASP Agentic | 5 O of 7 |
| 50% of rights-based legal obligations | same, `source` = EU AI Act | 3 O of 6 |
| 17% of operational controls | same, `source` = ISO or NIST | 2 O of 12 |
| 86%, 83% and 17% under the §VI definition | same | T\* items 1, 3 (EU AI Act) and 21 (OWASP) count as O: 6 of 7, 5 of 6, 2 of 12. The cells are small, and were coded with the same criterion the paper then invokes |
| Art 9 and A.6.2.6 straddle Class N and were coded in opposite directions | `data/development-corpus.csv` | A.6.2.6 is row 7; Art 9 appears nowhere, being Class N |

**On the two class columns.** `class` is the frozen coding exactly as written
during the run, including `**T\***` — Class T whose facts exist but are not
routed to the cut. `class_norm` is its plain twin, with `T*` folded into `T`
because nothing is destroyed, only unrouted. The paper's 15 counts T\* as T.
`verify.py` checks the twin against the frozen column for every row, so the
convenience column cannot quietly disagree with the record.

**One correction is recorded, not silently applied.** The per-source table in
`protocols/classification-corpus.md` §4 read NIST 6 T / 2 O until 31 August
2026; the row-level coding gives 7 T / 1 O, and the derived table was corrected
to match the frozen coding. The correction moved the operational-controls rate
from 25% to 17%, which sharpens rather than softens the paper's contrast with
71%. The note in §4 gives the probable origin of the slip.

## §VII.E — the transport recursion

`data/transport-recursion.csv` lists all 26 transport (T2) cases across the four
studies, with whether the paper counts each one and why.

| Claim | File | Recompute |
|---|---|---|
| Seven development cases, items 1, 3, 4, 19, 20, 21, 23 | `data/transport-recursion.csv` | `study` = development, `counted_in_paper_claim` = yes |
| Five held-out-2 cases, K1, K4, K8, K9, K12 | same | `study` = held-out-2, `counted_in_paper_claim` = yes |
| Twelve constructed cases in total | same | both of the above |
| Each derived obligation closed by T1 in one step | `protocols/classification-corpus.md` §5(e) and `protocols/heldout-2-predictions.md` | the ids in both are parsed by `extract.py`, not retyped |
| Three documented instances: P4 (Azure AI), P12 (Progent), P13 (Purview) | `data/transport-recursion.csv` rows with `study` = retrodiction | `coding_rationale` in `data/retrodiction-cases.csv`. C2PA's claim signature is constructed case K4, not a documented case (corrected 29 Sep 2026; the paper previously counted it as documented) |

**This claim was corrected on 31 August 2026.** The manuscript previously read
"the ten transport cases analysed in §8". The ten came from a working note in
`protocols/heldout-test.md` §3 — "7/7 in development, 3/3 here, 10/10 overall"
— and the three held-out cases are named nowhere. This study has **six** T2
obligations (H1, H2, H3, H9, H13, H14) and only H13 names its derived
obligation, so no three of them can be identified as the ones counted. The
number is not reconstructable and has been retired rather than guessed at.

The paper claims the seven development instances, enumerated by item number in
the frozen note, and the five held-out-2 instances, enumerated in the sealed
prediction pass, alongside three documented ones (P4, P12, P13). Both constructed sets are counted
from a sentence that names their ids, parsed rather than retyped, so neither can
drift from the note that established it. Three T2 rows in held-out set 2 — K3, K5
and K11 — carry no named derived obligation and are recorded as uncounted, on the
same basis as the two uncounted development cases.

## §VIII.C — held-out applicability

| Claim | File | Recompute |
|---|---|---|
| 15 obligations from disjoint sources (GDPR, CSA AICM, SP 800-218A, AI Act Ch. V) | `data/held-out-corpus.csv` | column `obligation_and_source` |
| Applicable to 13 | same | column `applicable` = yes |
| 2 exceptions, which produced the actuation branch and the epistemic split | same | `applicable` = no → H4 (actuation) and H5 (approximable) |
| Prediction recorded before the independent answer | `protocols/heldout-test.md` §1 | the predicted and answer columns are separate and the file is dated |

`✓*` in the frozen `match` column means the predicted transformation was right
but the obligation carried a *second* deficit cause the single-valued
prediction missed (H3, H12). Those are applicable cases, and the paper counts
them in the 13; they are also what motivated per-fact composition.

## §VIII.D — held-out set 2, the final method

The pre-specified study. Sources, selection rule, obligations, frozen method,
architecture and adversary models, coding scheme and pass criterion were fixed in
`protocols/heldout-2-preregistration.md` and sealed before analysis; the
prediction pass and the independent pass were each sealed before the next began.
`protocols/HELDOUT2-SEAL.txt` carries the three hashes and `verify.py` recomputes
all of them.

| Claim | File | Recompute |
|---|---|---|
| 12 obligations, 3 each from ATLAS, C2PA, SR 11-7 and the TBS Directive | `data/held-out-2-corpus.csv` | column `obligation_and_source` |
| No source was used in an earlier study | same | grep the `obligation_and_source` column for GDPR, AI Act, CSA, AICM, 800-218A, ISO/IEC 42001, AI 600-1, OWASP or HIPAA; none appears |
| 11 of 12 routed by the frozen final method | same | column `applicable` = yes |
| 9 clean, 2 with a recorded strain | same | column `applicability`: `A`, `A−` |
| 1 exception, on the mediation axis | same | `applicability` = `**X**` → K6 |
| No obligation required a fifth transformation | same | `predicted_by_frozen_method` contains only T1, T2, T3 and Terminal |
| Prediction agreed with the independent pass in 9 of 12 | same | column `agreement`: `✓` 9, `~` 2, `✗` 1 |
| 5 rows closely resemble an obligation already analysed; 2 resemble none | same | column `mirroring` |
| The pre-specified bar was 9 of 12 | `protocols/heldout-2-preregistration.md` §7 | stated there, before analysis |

**Why `mirroring` is in the data rather than the discussion.** A count of 11 of
12 means less if the twelve look like obligations the method was built on. The
column records that judgement per row so a reader can discount the headline
themselves: only K1 and K6 resemble nothing in the earlier corpora, and K6 is the
exception. The paper says so in §8.4 and §10, and `verify.py` checks that the
prose and the column agree.

**Refinement 4 is recorded, not applied.** K6 exposed that Table 3 routes
decision and actuation deficits but not mediation deficits. The symmetric repair
is written down in `protocols/heldout-2-test.md` §2 and named in the paper as a
finding. It is *not* in Table 3, because it was derived from the case that
exposed it and this study does not test it.

## §VII.B — the cause ablation

The counts §VII‑B states for the ablation. Nothing here is authored: every row
counted was coded in one of the three corpora and checked above.

| Claim | File | Recompute |
|---|---|---|
| 35 obligations carry a deficit at their strongest cut | the three corpus CSVs | rows whose deficit/cause column is not empty, `-`, an em dash, or `none` |
| 33 of them resolve to one of four transformations | same | `verify.py` normalises each transformation cell once, then tallies |
| 14 fact, 9 verdict, 8 approximate-and-detect, 2 terminal | same | the tally |
| The one row returning no transformation is K6 | `held-out-2-corpus.csv` | the mediation deficit of §VIII‑D |
| §VII‑B's stated counts match | `manuscript-claims.md` vs the tally | `verify.py` reads the numbers out of the prose |

**Counting rules** (the paper states these in one sentence and points here):

- *Scope.* The development, held-out and untouched corpora only; the 14
  retrodiction cases are not counted.
- *Which coding.* Development rows as coded. Held-out rows use
  `predicted_transformation`, the pre-test prediction; untouched rows use
  `predicted_by_frozen_method`, the sealed prediction. Two held-out rows read
  differently under the method as now presented: H4 (erasure) is recorded with
  no deficit at Z1, so it is not among the 35, although the method now treats it
  as an actuation deficit (the total would be 36); H5 (explanation) counts as
  Terminal, as predicted, although it later proved approximable (T3 would be 9,
  Terminal 1).
- *One transformation per obligation.* Four obligations combine two or more of
  T2 fact, T2 verdict, T3 and Terminal (development 2; K3, K8, K11), and four
  pair one of them with local T1 enforcement (development 25; K1, K5, K10).
  (Before 1 Oct 2026 this line read "seven", omitting K1, which is coded
  `T2 fact + T1` like K5 and K10.) Each is counted once by
  precedence: T2 verdict, then T2 fact, then T3, then Terminal, then T1
  (`extract.transformation_of`).
- *What it shows.* The tally re-tabulates the researcher's own codings, so it
  shows that the cause dimension separates the obligations, not that each
  separation is correct.

The remaining row of the 35 is development item 18, whose deficit is minor and
leaves placement unchanged (`T1 + minor residual`). It is counted in the 35 and
excluded from the 33, and `protocols/expressiveness-ablation.md` §2 says so
rather than quietly dropping it.

**What the ablation is not.** It is not a baseline comparison. SARC places
constraints among four sites in an agent execution loop and does not claim to
place obligations across a heterogeneous enterprise estate; scoring it outside
its stated scope would be a straw man. The baseline is our own method with the
cause dimension removed, which is the only one we can implement faithfully.

## §X — adversary sensitivity

Not a study. A re-analysis of five obligations already classified elsewhere in
the paper, under three nested adversary models, to put a number on a claim the
paper otherwise asserts.

| Claim | File | Recompute |
|---|---|---|
| Class T falls from 4 of 5 to 1 of 5 as the adversary strengthens | `data/adversary-sensitivity.csv` | count `T` in `class_under_x1`, `class_under_x2`, `class_under_x3` |
| No obligation recovers Class T under a stronger adversary | same | no row has a `T` at or after its first `O` |
| Purpose limitation is Class O under all three | same | row `O2` |
| Unsanctioned code execution is Class T under all three | same | row `O3` |
| The paper's Table 6 reproduces these cells | `manuscript-claims.md` vs the CSV | `verify.py` matches every row |

**Why monotonicity is checked rather than reported as a finding.** If the paths
available to a stronger adversary are a superset, every location that cuts under
the stronger one cuts under the weaker, so feasible sets shrink and a row can
only go T → O. That is a consequence of the definition, not an observation. The
check exists to catch an error in the analysis; the informative part of the table
is *how far* classification moves, which the definition does not predict.

## §VIII.E — documented-architecture retrodiction

| Claim | File | Recompute |
|---|---|---|
| 14 clean cases | `data/retrodiction-cases.csv` | `blind_status` is `[clean]` in all 14 |
| 8 agreement or extension | same | `code_norm` D0 (5) + D1 (3) |
| 3 argued gaps | same | `code_norm` D2 |
| 2 prediction errors | same | `code_norm` D3 — P17 Vertex AI Model Registry, P19 SageMaker Model Monitor |
| 1 undetermined | same | `code_norm` D4 |
| Result is at the boundary of the agreement band, not inside it | `protocols/retrodiction-protocol.md` §3, and the decision rule | the rule permits D3 ≤ 2; D3 = 2 |
| 7 first-party vendor sources, all read 19 August 2026 | `evidence/manifest.csv` | column `accessed` |

`code` carries the coder's qualifiers (`D1 (partial)`, `D2 (form b)`);
`code_norm` is the bare code. A qualifier annotates a code, it does not change
it, so both tally to the same 5/3/3/2/1.

**Why the counts are stated per code and never aggregated with the other three
studies.** The four studies differ in independence, not only in size. Only
retrodiction has an external reference, and even it was coded by one researcher;
the two held-out sets test different versions of the method and cannot be summed.
The paper reports them separately for that reason and this artifact keeps them in
four separate files.

## What this artifact cannot establish

`verify.py` passing means the paper's numbers are the numbers in the data. It
does not mean the codings are correct. One researcher selected every case, made
every prediction, read every document and assigned every code. The seals on the
held-out-2 protocol fix *when* each claim was made, which is a different thing
from fixing whether it is right. The coding rationale is published for each
retrodiction case (`coding_rationale`), the prediction and independent passes are
published separately for held-out set 2, and the `mirroring` column publishes the
study's own main limitation — so a reader can disagree with a specific code and
see exactly what it would change, which is the strongest form of checking a
single-coder study supports.


## §VIII‑G — T4 extension (arXiv version; preliminary, constructed cases)

| Claim | File | Recompute |
|---|---|---|
| Rule, cases and passes sealed in order | `protocols/T4-SEAL.txt` | `shasum -a 256` each listed file |
| No test case has a single adequate cut | `protocols/t4-cases.json` | intersection of each case's path `via` sets is empty |
| 18 of 18 per-path outcomes are what the rule returns | `data/t4-paths.csv` vs `protocols/t4-cases.json` | `verify.py` re-applies protocol §2 |
| 4 F, 2 A, 2 U of 8 test cases | `data/t4-cases.csv` | column `t4_outcome` |
| Independent pass agrees in 8 of 8 | same | column `agreement_norm` |
| K6 (D0) is diagnostic only | `protocols/t4-cases.json` | `role` = diagnostic; excluded from every count |


## Notes on the recorded evidence (added 29 Sep 2026)

- `protocols/retrodiction-protocol.md` §5 says "The eight `[prior]` pairs remain uncoded". That line was
  written at an interim stage; the final record has **seven** `[prior]` pairs (P1–P3, P7, P8, P10, P11),
  as the paper states. The protocol text is kept as written.
- The P5 row of `data/retrodiction-cases.csv` places "examines the assembled prompt and complete response
  without distinguishing between segments by provenance" in quotation marks. It is a paraphrase of the
  Model Armor documentation, not a verbatim quotation; the paper quotes only the page's own wording
  ("inspects each prompt and response independently as a single-turn request").
- The cause tally is reported in §VIII‑D of the paper; the labels "§7.2" and "VII.B" in `verify.py`
  are the section numbers it had when the checks were written.
