# What the cause dimension contributes — an ablation

**What this is.** An ablation of our own method, run over codings that are already published. It removes
one input — the *cause* of each deficit — and asks what the method can still return. It introduces no new
obligation, no new judgement and no new coding: every row it counts was classified in
`classification-corpus.md`, `heldout-test.md` or `heldout-2-test.md` and is already in `data/`.

**What this is not.** It is not a comparison against SARC or any other published method, and must not be
read as one. SARC places constraints among four sites in an agent execution loop and does not claim to
place obligations across a heterogeneous enterprise estate; scoring it on a problem outside its stated
scope would be a straw man. The baseline here is *our method with one dimension removed*, which is the
only baseline we can implement faithfully.

## 1. The cause-blind baseline

The ablated analyst knows everything the method knows except why a fact is missing:

- the obligation's class (N / T / O);
- the candidate locations, their available facts, their cut-scope and their actuation;
- **that** a required fact is absent at the strongest adequate cut.

From this it can distinguish exactly two situations: no deficit, in which case enforce at the cut; and a
deficit, in which case *the fact must be made available at the cut, or the obligation cannot be enforced
there*. It cannot choose among transporting the fact, transporting a verdict, approximating and
detecting, or declaring a residual, because those are keyed to the cause and to nothing else.

## 2. Result

Counting every obligation across the three corpora whose strongest adequate cut carries a deficit:

| | Count |
|---|--:|
| Obligations carrying a deficit | **35** |
| …resolved by the method to one of four transformations | **33** |
| — T2 transport (fact) | 14 |
| — T2 transport (verdict) | 9 |
| — T3 approximate and detect | 8 |
| — Terminal, declare residual | 2 |
| …returning no transformation (K6, the mediation deficit of §VIII‑D) | 1 |
| …where the deficit is minor and placement is unchanged (development item 18, T1 + residual) | 1 |

The cause-blind baseline returns one answer for all 33. The method returns four. Every one of the 33
therefore requires cause information to reach its architecture; the ablation is not a partial loss of
resolution but a total one on this axis.

## 3. Pairs the baseline cannot separate

Three pairs, each drawn from different corpora, presenting identically to the ablated analyst — a fact
the cut needs and does not have — and resolving differently.

| Pair | Both present as | Method returns | Because |
|---|---|---|---|
| dev #4 · H14 | a fact absent at the gateway | **T2 fact** · **T2 verdict** | #4's prompt flattening destroyed a representation that can be restored; H14's purpose-of-use is a judgement only the requester can render, so only the judgement may move |
| H9 · H2 | a fact absent at the cut | **T2 fact** · **T2 verdict** | H9's classification label exists upstream and can be propagated; H2's "was the intervention substantive" exists nowhere as a fact |
| dev #4 · dev #24 | a fact absent at the cut | **T2 fact** · **Terminal** | #24's predicate — whether a human has been deceived — is not computable by any party, so there is nothing to transport and the honest output is a residual |

The third pair is the one that matters most in practice. To the cause-blind analyst, "obtain this fact
from elsewhere" and "no architecture in *L* can evaluate this" are the same observation. An architect
working from deficit presence alone will keep looking for a source for a fact that does not exist.

## 4. Limits

The counts are a re-tabulation, so they inherit every limitation of the codings they count: single
analyst, purposive corpora, and the interpretive judgement in deriving `I(o)` and assigning a cause. The
ablation shows that the cause dimension is *load-bearing within this method as applied to these
obligations*. It does not show that no other formulation could reach the same architectures by another
route, and it is not evidence about any published method.
