#!/usr/bin/env python3
"""Recompute every number the paper's evaluation section reports.

Each check names the claim, the file it is recomputed from, and the value the
paper states. Nothing here is copied from the paper's prose: the expected values
are the paper's claims, the actual values are computed from the data files, and
a disagreement is a defect in one or the other.

    python3 verify.py        # -> exit 0 if the paper matches the artifact

Run `python3 extract.py` first if the protocol files have changed; this script
also checks that the CSVs are what the current protocol files produce.

The artifact is self-contained: every file this script reads lives in this
directory, so `unzip && cd artifact && python3 verify.py` is the whole
procedure. Nothing outside the package is consulted.
"""
import csv, hashlib, json, pathlib, re, subprocess, sys
from collections import Counter

import extract  # normalisers only; importing does not rewrite the CSVs

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data"
checks = []


def load(name):
    with (DATA / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(claim, where, expected, actual):
    checks.append((claim, where, expected, actual, expected == actual))


dev, held, retro = (load("development-corpus.csv"), load("held-out-corpus.csv"),
                    load("retrodiction-cases.csv"))
held2 = load("held-out-2-corpus.csv")
adv = load("adversary-sensitivity.csv")
frame = load("sampling-frame.csv")
transport = load("transport-recursion.csv")
iso = load("iso42001-frame.csv")
manifest = list(csv.DictReader((HERE / "evidence" / "manifest.csv").open(encoding="utf-8")))

# -- VIII.A  corpus construction -------------------------------------------
check("sampling frame fixed before classification is 268 items",
      "sampling-frame.csv:items_in_frame", 268,
      sum(int(r["items_in_frame"]) for r in frame))
check("items admitted to the development corpus",
      "sampling-frame.csv:items_admitted_to_corpus", 25,
      sum(int(r["items_admitted_to_corpus"]) for r in frame))
check("NIST actions in the frame (mechanical count)",
      "sampling-frame.csv", 211,
      int(next(r["items_in_frame"] for r in frame if "NIST" in r["source"])))
check("NIST actions taken after the keyword filter",
      "sampling-frame.csv", 8,
      int(next(r["items_admitted_to_corpus"] for r in frame if "NIST" in r["source"])))
check("ISO/IEC 42001 Annex A controls in the frame",
      "sampling-frame.csv", 38,
      int(next(r["items_in_frame"] for r in frame if "ISO" in r["source"])))

# -- VIII.B  obligation classification --------------------------------------
cls = Counter(r["class_norm"] for r in dev)
check("architecturally enforceable obligations classified",
      "development-corpus.csv rows", 25, len(dev))
check("Class T (T* counted as T)", "development-corpus.csv:class_norm", 15, cls["T"])
check("Class O", "development-corpus.csv:class_norm", 10, cls["O"])
check("Class O share of the corpus (the '40% figure')",
      "development-corpus.csv:class_norm", 40, round(100 * cls["O"] / len(dev)))


def o_rate(*sources, strict=False):
    """Class O share for a source group. strict=True applies the §VI definition
    retrospectively: the T* items (coded T, but needing a transported fact)
    count as O, as the paper's 12 T / 13 O aggregate does."""
    rs = [r for r in dev if r["source"] in sources]
    def is_o(r):
        return r["class_norm"] == "O" or (strict and "*" in extract.plain(r["class"]))
    return round(100 * sum(1 for r in rs if is_o(r)) / len(rs))


check("agentic obligations Class O rate", "development-corpus.csv OWASP rows",
      71, o_rate("OWASP Agentic"))
check("rights-based legal obligations Class O rate",
      "development-corpus.csv EU AI Act rows", 50, o_rate("EU AI Act"))
check("operational controls (ISO + NIST) Class O rate",
      "development-corpus.csv ISO+NIST rows", 17,
      o_rate("ISO/IEC 42001", "NIST AI 600-1"))
check("AI Act Art 9 is coded Class N, so is absent from the 25",
      "development-corpus.csv:obligation_and_source", 0,
      sum(1 for r in dev if "Art 9" in r["obligation_and_source"]))
check("ISO A.6.2.6 is coded architecturally enforceable, so is present",
      "development-corpus.csv:obligation_and_source", 1,
      sum(1 for r in dev if "A.6.2.6" in r["obligation_and_source"]))

# -- VIII.A  the ISO Annex A scope finding ----------------------------------
# The manuscript claims "at least 24 of 38", which is what both the original
# aggregate (24) and the per-control recount (29) support. The enumeration
# below is what makes either checkable at all.
check("ISO/IEC 42001 Annex A controls enumerated individually",
      "iso42001-frame.csv", 38, len(iso))
n_class_n = sum(1 for r in iso if r["class_n"] == "yes")
check("the manuscript's 'at least 24 of 38 are Class N' holds on this enumeration",
      "iso42001-frame.csv:class_n", True, n_class_n >= 24)
check("controls that entered the development corpus are coded non-N",
      "iso42001-frame.csv vs development-corpus.csv", 0,
      sum(1 for r in iso if "development corpus" in r["basis"] and r["class_n"] != "no"))
check("every ISO obligation in the corpus appears in the Annex A enumeration",
      "development-corpus.csv vs iso42001-frame.csv", True,
      all(any(c["control_id"] in r["obligation_and_source"] for c in iso)
          for r in dev if r["source"] == "ISO/IEC 42001"))
check("the families the frozen note names are Class N without exception",
      "iso42001-frame.csv", True,
      all(r["class_n"] == "yes" for r in iso
          if r["control_id"].startswith(("A.2.", "A.3.", "A.5.", "A.8.", "A.10."))))
check("the per-control recount disagrees with the 24 aggregate, as recorded",
      "iso42001-frame.csv:class_n", 29, n_class_n)

# -- VII.E  the transport recursion -----------------------------------------
counted = [r for r in transport if r["counted_in_paper_claim"] == "yes"
           and r["study"] == "development"]
check("transport cases the paper counts (development corpus)",
      "transport-recursion.csv:counted_in_paper_claim", 7, len(counted))
check("they are exactly the items the frozen note enumerates",
      "transport-recursion.csv vs classification-corpus.md §5(e)",
      ["1", "3", "4", "19", "20", "21", "23"], [r["case_id"] for r in counted])
by_id = {d["id"]: d["transformation"] for d in dev}
check("every counted case is a T2 (transport) row of the development corpus",
      "transport-recursion.csv vs development-corpus.csv", True,
      all("T2" in by_id.get(r["case_id"], "") for r in counted))
check("development T2 cases the frozen note does not count",
      "transport-recursion.csv", ["2", "10"],
      [r["case_id"] for r in transport
       if r["study"] == "development" and r["counted_in_paper_claim"] == "no"])
check("held-out transport cases, none counted (the 3/3 is not reconstructable)",
      "transport-recursion.csv", 6,
      sum(1 for r in transport if r["study"] == "held-out"))
check("documented instances where the derived obligation is discharged",
      "transport-recursion.csv", ["P4", "P12", "P13"],
      [r["case_id"] for r in transport if r["study"] == "retrodiction"])
check("Purview, the instance the manuscript names, is one of them",
      "transport-recursion.csv", True,
      any("Purview" in r["obligation_or_system"] for r in transport
          if r["study"] == "retrodiction"))

# -- VIII.C  held-out applicability -----------------------------------------
app = Counter(r["applicable"] for r in held)
check("held-out obligations from disjoint sources",
      "held-out-corpus.csv rows", 15, len(held))
check("frozen rules applicable", "held-out-corpus.csv:applicable", 13, app["yes"])
check("exceptions, which produced the actuation and approximable branches",
      "held-out-corpus.csv:applicable", 2, app["no"])

# -- VIII.D  the pre-specified, sealed study of the final method -------------------
# Held-out set 2 tests the method as reported, against obligations that had no
# part in producing it. Its protocol was sealed before analysis; the seal file
# ships with the artifact and is checked here rather than taken on trust.
app2 = Counter(r["applicable"] for r in held2)
strain = Counter(extract.plain(r["applicability"]).replace("\u2212", "-")
                 for r in held2)
agree2 = Counter(r["agreement_norm"] for r in held2)
mirror = Counter(r["mirroring_norm"] for r in held2)

check("held-out set 2 obligations, three from each of four sources",
      "held-out-2-corpus.csv rows", 12, len(held2))
check("routed by the final method", "held-out-2-corpus.csv:applicable", 11, app2["yes"])
check("routed cleanly, with no recorded strain",
      "held-out-2-corpus.csv:applicability", 9, strain["A"])
check("routed with a recorded strain",
      "held-out-2-corpus.csv:applicability", 2, strain["A-"])
check("exceptions", "held-out-2-corpus.csv:applicability", 1, strain["X"])
check("the pre-specified bar of 9 of 12 is met",
      "held-out-2-corpus.csv vs heldout-2-preregistration.md §7", True, app2["yes"] >= 9)
check("prediction agreed with the independent pass in full",
      "held-out-2-corpus.csv:agreement_norm", 9, agree2["full"])
check("agreed in part", "held-out-2-corpus.csv:agreement_norm", 2, agree2["partial"])
check("did not agree", "held-out-2-corpus.csv:agreement_norm", 1, agree2["none"])

# The pre-specified method-level failure condition: any obligation needing a
# fifth transformation. Recomputed from the predicted column rather than taken
# from the prose, so a row that smuggled one in would fail here.
TRANSFORMS = {"T1", "T2", "T3", "Terminal"}
found = set(re.findall(r"\bT\d+\b|\bTerminal\b",
                       " ".join(r["predicted_by_frozen_method"] for r in held2)))
check("no obligation required a transformation outside the four",
      "held-out-2-corpus.csv:predicted_by_frozen_method", True, found <= TRANSFORMS)

# The exception is a mediation deficit, which is the axis Table 3 does not route.
exc = [r for r in held2 if r["applicable"] == "no"]
check("the single exception is K6", "held-out-2-corpus.csv", ["K6"],
      [r["id"] for r in exc])
check("it is an exception because no location mediates, not because a fact is missing",
      "held-out-2-corpus.csv:deficit_and_cause", True,
      bool(exc) and "mediates" in exc[0]["deficit_and_cause"])
check("and the frozen function returned nothing for it",
      "held-out-2-corpus.csv:predicted_by_frozen_method", True,
      bool(exc) and "no row" in exc[0]["predicted_by_frozen_method"])

# Mirroring. Reported separately from the headline because it bounds it.
check("rows resembling an obligation already analysed, closely",
      "held-out-2-corpus.csv:mirroring_norm", 5, mirror["close"])
check("rows resembling one partially", "held-out-2-corpus.csv:mirroring_norm",
      5, mirror["partial"])
check("rows resembling nothing in the earlier corpora",
      "held-out-2-corpus.csv:mirroring_norm", 2, mirror["none"])
check("the exception is one of the two unmirrored rows, as the paper states",
      "held-out-2-corpus.csv", True,
      bool(exc) and exc[0]["mirroring_norm"] == "none")

# Source disjointness, checked rather than asserted: no held-out-2 obligation
# may cite a development or held-out-1 source.
USED_BEFORE = ("GDPR", "AI Act", "CSA", "AICM", "800-218A", "ISO/IEC 42001",
               "AI 600-1", "OWASP", "HIPAA")
check("no held-out-2 obligation cites a source used in an earlier study",
      "held-out-2-corpus.csv:obligation_and_source", [],
      [r["id"] for r in held2
       if any(u.lower() in r["obligation_and_source"].lower() for u in USED_BEFORE)])
check("the four sources are represented three obligations each",
      "held-out-2-corpus.csv:obligation_and_source", [3, 3, 3, 3],
      [sum(1 for r in held2 if k in r["obligation_and_source"])
       for k in ("ATLAS", "C2PA", "SR 11-7", "TBS Directive")])

# The seals. A protocol that can be edited afterwards is not a pre-specification, so the
# hashes recorded at sealing time are recomputed from the shipped files.
SEAL = (HERE / "protocols" / "HELDOUT2-SEAL.txt").read_text(encoding="utf-8")
sealed_pairs = re.findall(r"file\s*:\s*(\S+)\s*\n\s*sha256\s*:\s*([0-9a-f]{64})",
                          SEAL)
check("the seal file records the protocol and both analysis passes",
      "protocols/HELDOUT2-SEAL.txt", 3, len(sealed_pairs))
for name, want in sealed_pairs:
    got = hashlib.sha256((HERE / "protocols" / name).read_bytes()).hexdigest()
    check(f"{name} is byte-identical to what was sealed",
          "protocols/HELDOUT2-SEAL.txt", want, got)

# -- VII.E  the held-out-2 transport cases ----------------------------------
h2_transport = [r for r in transport if r["study"] == "held-out-2"]
check("held-out-2 transport cases the paper counts",
      "transport-recursion.csv", ["K1", "K4", "K8", "K9", "K12"],
      [r["case_id"] for r in h2_transport if r["counted_in_paper_claim"] == "yes"])
check("held-out-2 T2 rows whose derived obligation the prediction did not name",
      "transport-recursion.csv", ["K3", "K5", "K11"],
      [r["case_id"] for r in h2_transport if r["counted_in_paper_claim"] == "no"])
check("constructed transport cases the paper now claims, across two studies",
      "transport-recursion.csv", 12,
      len(counted) + sum(1 for r in h2_transport
                         if r["counted_in_paper_claim"] == "yes"))

# -- VII.B  the cause ablation ----------------------------------------------
# Remove the cause dimension and count what the method can still return. This is
# a re-tabulation of codings already checked above, so it adds no data; it exists
# because §7.2 states the numbers and they must come from the corpora.
def _empty(cell):
    """No deficit recorded. The three corpora spell it "", "-", em dash or
    "none", so normalise the dashes before testing."""
    return (extract.plain(cell).replace("\u2014", "-").replace("\u2013", "-")
            .strip().lower() in ("", "-", "none"))


def _deficit_rows():
    """(id, transformation) for every obligation whose cut carries a deficit."""
    out = []
    for r in dev:
        if _empty(r["deficit_at_cut"]):
            continue
        out.append(("dev#" + r["id"], extract.transformation_of(r["transformation"])))
    for r in held:
        if _empty(r["cause"]):
            continue
        out.append((r["id"], extract.transformation_of(r["predicted_transformation"])))
    for r in held2:
        if extract.plain(r["deficit_and_cause"]).lower().startswith("none"):
            continue
        out.append((r["id"], extract.transformation_of(r["predicted_by_frozen_method"])))
    return out


deficit_rows = _deficit_rows()
FOUR = ("T2 fact", "T2 verdict", "T3", "Terminal")
resolved = Counter(t for _, t in deficit_rows if t in FOUR)
check("obligations across the three corpora carrying a deficit at their cut",
      "the three corpora", 35, len(deficit_rows))
check("of those, resolved to one of the four transformations",
      "the three corpora", 33, sum(resolved.values()))
check("transport a fact", "the three corpora", 14, resolved["T2 fact"])
check("transport a verdict", "the three corpora", 9, resolved["T2 verdict"])
check("approximate and detect", "the three corpora", 8, resolved["T3"])
check("terminate in a residual", "the three corpora", 2, resolved["Terminal"])
check("all four transformations are represented, so the cause dimension "
      "discriminates on every one of the 33",
      "the three corpora", 4, sum(1 for t in FOUR if resolved[t]))
check("the only row returning no transformation is K6, the mediation deficit",
      "the three corpora", ["K6"], [i for i, t in deficit_rows if t is None])

# -- X  adversary sensitivity ---# -- X  adversary sensitivity ----------------------------------------------
# Five obligations re-classified under three nested adversary models. The
# monotonicity property is not empirical: because a stronger adversary has a
# superset of paths, any location that cuts under the stronger one cuts under
# the weaker, so a row may go T -> O and never O -> T. A violation would mean
# the analysis is wrong, not that the world is surprising, so it is checked.
COLS = ("class_under_x1", "class_under_x2", "class_under_x3")
t_counts = [sum(1 for r in adv if r[c] == "T") for c in COLS]
check("obligations re-classified under three adversaries",
      "adversary-sensitivity.csv rows", 5, len(adv))
check("Class T count falls as the adversary strengthens",
      "adversary-sensitivity.csv", [4, 2, 1], t_counts)
def _recovers(seq):
    """True if Class T reappears after Class O — impossible under the definition
    of a cut, so a True here means the analysis is wrong."""
    i = seq.find("O")
    return i != -1 and "T" in seq[i:]


check("no row recovers Class T under a stronger adversary (monotonicity holds)",
      "adversary-sensitivity.csv", [],
      [r["id"] for r in adv if _recovers("".join(r[c] for c in COLS))])
check("all fifteen cells are T or O",
      "adversary-sensitivity.csv", 15,
      sum(1 for r in adv for c in COLS if r[c] in ("T", "O")))
check("one obligation is Class O under every adversary (informational obstruction)",
      "adversary-sensitivity.csv", ["O2"],
      [r["id"] for r in adv if all(r[c] == "O" for c in COLS)])
check("one is Class T under every adversary (its cut lies below them all)",
      "adversary-sensitivity.csv", ["O3"],
      [r["id"] for r in adv if all(r[c] == "T" for c in COLS)])

# -- VIII.F  documented-architecture retrodiction ---------------------------
code = Counter(r["code_norm"] for r in retro)
check("retrodiction cases coded", "retrodiction-cases.csv rows", 14, len(retro))
check("all analysed pairs are clean (predictions locked before documentation)",
      "retrodiction-cases.csv:blind_status", 14,
      sum(1 for r in retro if r["blind_status"] == "[clean]"))
check("agreement or extension (D0 + D1)", "retrodiction-cases.csv:code_norm",
      8, code["D0"] + code["D1"])
check("argued gaps (D2)", "retrodiction-cases.csv:code_norm", 3, code["D2"])
check("prediction errors (D3)", "retrodiction-cases.csv:code_norm", 2, code["D3"])
check("undetermined (D4)", "retrodiction-cases.csv:code_norm", 1, code["D4"])
check("D0/D1 dominant and D3 <= 2, so the first band of the frozen rule holds",
      "retrodiction-cases.csv:code_norm", True,
      code["D0"] + code["D1"] > code["D2"] + code["D3"] + code["D4"] and code["D3"] <= 2)
check("the result sits AT the band boundary, not inside it (D3 == 2)",
      "retrodiction-cases.csv:code_norm", True, code["D3"] == 2)
check("first-party vendor sources in the evidence manifest",
      "evidence/manifest.csv", 7, len(manifest))
check("every manifest entry carries an access date",
      "evidence/manifest.csv:accessed", 7,
      sum(1 for r in manifest if r["accessed"].strip()))
for case, code_want in (("vertexreg", "D3"), ("sagemaker", "D3")):
    check(f"the {case} case is one of the two prediction errors",
          "retrodiction-cases.csv", True,
          any(code_want == r["code_norm"] and case[:6].lower()
              in (r["platform_or_system"] + r["documented_placement"]).lower().replace(" ", "")
              for r in retro))

# -- the normalised twins agree with the frozen coded columns ---------------
# The coded columns are the frozen record; the twins are conveniences. If a CSV
# is ever hand-edited, they can drift apart, and every count above reads only
# the twin. So recompute each twin from its raw column.
check("class_norm agrees with the frozen class column for all 25",
      "development-corpus.csv", 25,
      sum(1 for r in dev if r["class_norm"] == extract.class_of(r["class"])))
check("applicable agrees with the frozen match column for all 15",
      "held-out-corpus.csv", 15,
      sum(1 for r in held if r["applicable"] == extract.applicable_of(r["match"])))
check("code_norm agrees with the frozen code column for all 14",
      "retrodiction-cases.csv", 14,
      sum(1 for r in retro if r["code_norm"] == extract.code_of(r["code"])))

# -- manuscript <-> artifact consistency -------------------------------------
# verify.py's other checks tie the paper's numbers to the data. These tie the
# paper's *prose* to it: the case ids, system names, dates and claims that are
# written out in sentences and cannot be recomputed from a column.
#
# The prose is read from manuscript-claims.md, an anonymised snapshot of the
# submitted manuscript written into this directory by the build. Nothing outside
# this directory is read, so the package verifies standalone: unzip, cd here,
# run. If the snapshot is missing the package is incomplete, and the check below
# says so rather than silently skipping the prose checks.
MANUSCRIPT = HERE / "manuscript-claims.md"
check("the anonymised manuscript snapshot ships with the artifact",
      "manuscript-claims.md", True, MANUSCRIPT.exists())
if MANUSCRIPT.exists():
    MAN = " ".join(MANUSCRIPT.read_text(encoding="utf-8").split())

    def states(pattern):
        """The manuscript asserts this, with newlines normalised away."""
        return re.search(pattern, MAN) is not None

    # §7.5 names the seven transport cases by item number.
    m = re.search(r"items ((?:\d+, )+\d+ and \d+)", MAN)
    prose_ids = re.findall(r"\d+", m.group(1)) if m else []
    check("§7.5's transport item numbers match transport-recursion.csv",
          "manuscript-claims.md §7.5", [r["case_id"] for r in counted], prose_ids)

    # §8.5 names six systems individually; each must be a coded case.
    haystack = " ".join(r["platform_or_system"] + " " + r["documented_placement"] +
                        " " + r["coding_rationale"] for r in retro)
    for name in ("VPC Service Controls", "Purview", "Model Armor",
                 "Model Registry", "SageMaker", "Foundry"):
        check(f"§8.5's named system '{name}' is a coded retrodiction case",
              "manuscript-claims.md §8.5 vs retrodiction-cases.csv", True, name in haystack)

    # The evidence date in the prose must be the date every source was read.
    accessed = {r["accessed"].strip() for r in manifest}
    check("§8.5's stated evidence date matches every manifest access date",
          "manuscript-claims.md §8.5 vs evidence/manifest.csv", True,
          states(r"read on \*\*19 August 2026\*\*") and accessed == {"2026/08/19"})

    # The literature survey and the vendor evidence are dated separately: the
    # survey was rerun on 5 September, the documentation was not re-read. The
    # paper must state both dates and say they differ, so a reader cannot take
    # the freeze date as covering the retrodiction evidence.
    check("§3.4 states the literature freeze date",
          "manuscript-claims.md §3.4", True,
          states(r"frozen\s+on 5 September 2026"))
    check("§3.4 dates the vendor evidence separately from the literature freeze",
          "manuscript-claims.md §3.4 vs §8.5", True,
          states(r"read earlier, on 19 August 2026, and is dated separately"))

    # §8.5 claims neither pre-specified failure condition was triggered.
    d3 = [r for r in retro if r["code_norm"] == "D3"]
    causes = {re.sub(r"[*_]", "", r["predicted_deficit"]).strip().lower() for r in d3}
    check("the paper's 'four or more prediction errors' threshold is not met",
          "retrodiction-cases.csv", True, len(d3) < 4)
    check("§8.5's claim that the two errors fall in different deficit causes holds",
          "retrodiction-cases.csv:predicted_deficit", len(d3), len(causes))

    # Headline counts, read out of the prose and compared with the data.
    m = re.search(r"Across (\d+) clean cases", MAN)
    check("§8.5's 'Across N clean cases' matches the coded set",
          "manuscript-claims.md §8.5", len(retro), int(m.group(1)) if m else None)
    m = re.search(r"Thirteen of the (\d+) were handled", MAN)
    check("§8.3's held-out denominator matches the corpus",
          "manuscript-claims.md §8.3", len(held), int(m.group(1)) if m else None)
    m = re.search(r"sampling frame of (\d+) items", MAN)
    check("§8.1's sampling frame matches sampling-frame.csv",
          "manuscript-claims.md §8.1", sum(int(r["items_in_frame"]) for r in frame),
          int(m.group(1)) if m else None)
    m = re.search(r"At least (\d+) of the (\d+) ISO/IEC 42001", MAN)
    check("§8.1's ISO claim is satisfied by the per-control enumeration",
          "manuscript-claims.md §8.1 vs iso42001-frame.csv", True,
          bool(m) and n_class_n >= int(m.group(1)) and len(iso) == int(m.group(2)))
    for rate, label, sources in ((86, "agentic", ("OWASP Agentic",)),
                                 (83, "rights-based", ("EU AI Act",))):
        check(f"§8.2's {rate}% {label} rate under the §VI definition is what the corpus gives",
              "manuscript-claims.md §8.2", True,
              states(rf"{rate}%") and o_rate(*sources, strict=True) == rate)
    check("§8.2's operational rate is unchanged under the §VI definition",
          "manuscript-claims.md §8.2", True,
          o_rate("ISO/IEC 42001", "NIST AI 600-1", strict=True) == 17
          and states(r"gives 86%, 83% and 17%"))
    for rate, label, sources in ((71, "agentic", ("OWASP Agentic",)),
                                 (50, "rights-based", ("EU AI Act",)),
                                 (17, "operational", ("ISO/IEC 42001", "NIST AI 600-1"))):
        check(f"§8.2's {rate}% {label} rate is what the corpus gives",
              "manuscript-claims.md §8.2", True,
              states(rf"{rate}%") and o_rate(*sources) == rate)

    # Counts the paper spells out in words rather than digits. These are the
    # ones a silent edit is most likely to leave behind, because no digit
    # changes and nothing looks wrong on the page.
    WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
             "twelve": 12, "thirteen": 13, "fifteen": 15, "twenty-five": 25}

    def spelled(word):
        return WORDS.get(word.strip().lower())

    m = re.search(r"(\S+) architecturally enforceable obligations remained: "
                  r"(\S+) Class T, (\S+) Class O", MAN)
    check("§8.2's spelled-out corpus counts match the classification",
          "manuscript-claims.md §8.2", [len(dev), cls["T"], cls["O"]],
          [spelled(m.group(1)), spelled(m.group(2)), spelled(m.group(3))] if m else None)

    m = re.search(r"(\S+) of the (\d+) were handled by those frozen rules", MAN)
    check("§8.3's spelled-out applicability count matches the held-out set",
          "manuscript-claims.md §8.3", [app["yes"], len(held)],
          [spelled(m.group(1)), int(m.group(2))] if m else None)

    m = re.search(r"documentation agreed with or extended (\S+) predictions, "
                  r"(?:\S+) of them involving no deficit; in (\S+) it was coded as "
                  r"showing a gap flagged in the prediction \([^)]*\); (\S+) "
                  r"contradicted the predicted architecture, and (\S+) could not be "
                  r"determined", MAN)
    check("§8.5's spelled-out outcome counts match the coding",
          "manuscript-claims.md §8.5", [code["D0"] + code["D1"], code["D2"],
                                  code["D3"], code["D4"]],
          [spelled(g) for g in m.groups()] if m else None)

    # The abstract reports the sealed study too, and is the sentence most
    # likely to be left behind by a later edit, since nothing else references it.
    m = re.search(r"a pre-specified test (?:on|of) (\S+) obligations from sources "
                  r"excluded from method development", MAN)
    check("the abstract's held-out-2 denominator matches the corpus",
          "manuscript-claims.md abstract", len(held2),
          spelled(m.group(1)) if m else None)
    m = re.search(r"the frozen method returned a placement for (\S+) of (\S+) obligations", MAN)
    check("the abstract's held-out-2 result matches the coding",
          "manuscript-claims.md abstract", [app2["yes"], len(held2)],
          [spelled(g) for g in m.groups()] if m else None)
    # §7.2's named result. It is stated as a principle, scoped to an adequate
    # cut, and explicitly does not fix the implementation — the three things that
    # keep it defensible given that §8.4 found a case Table 3 does not route.
    check("§7.2 instantiates the principle on a contrasting pair, not only asserts it",
          "manuscript-claims.md §7.2", True,
          states(r"a representational deficit, closed by transporting the fact")
          and states(r"an authority deficit, closed only by transporting a verdict")
          and states(r"cause is architecturally consequential"))
    check("§7.2 states the Deficit-Cause Principle",
          "manuscript-claims.md §7.2", True,
          states(r"\*\*Deficit-Cause Principle\.\*\* At an adequate cut"))
    check("the principle is scoped to the class of transformation, not the implementation",
          "manuscript-claims.md §7.2", True,
          states(r"(?:determines|selects) the \*class\* of transformation and not its implementation"))
    check("the principle defers to the exception §8.4 found",
          "manuscript-claims.md §7.2", True,
          states(r"says nothing about an obligation for\s+which no cut exists"))
    check("the paper does not overclaim the principle as a theorem, law, or unique determination",
          "manuscript-claims.md", False,
          states(r"Deficit-Cause (Theorem|Law)") or states(r"uniquely determines"))

    check("the paper claims sealing, not registry pre-registration",
          "manuscript-claims.md", False, states(r"pre-registered"))
    check("§8.4 states what the seals do and do not establish",
          "manuscript-claims.md §8.4", True,
          states(r"sealed by hash rather than deposited with a registry"))
    check("the abstract states the evaluation is four studies, as §8 does",
          "manuscript-claims.md abstract", True,
          states(r"We evaluate the method through four studies"))

    # §8.4 — the pre-specified study. Its counts are spelled out in words,
    # so nothing in the sentence changes shape when a number moves.
    m = re.search(r"(\S+) of the (\S+) were routed — (\S+) cleanly, (\S+) with a "
                  r"recorded strain", MAN)
    check("§8.4's spelled-out counts match the pre-specified study",
          "manuscript-claims.md §8.4", [app2["yes"], len(held2), strain["A"], strain["A-"]],
          [spelled(g) for g in m.groups()] if m else None)

    m = re.search(r"required at least (\S+) of (\S+) obligations to be\s+routed", MAN)
    check("§8.4's stated bar is the one the sealed protocol fixed",
          "manuscript-claims.md §8.4 vs heldout-2-preregistration.md §7", [9, 12],
          [spelled(g) for g in m.groups()] if m else None)

    m = re.search(r"(\S+) of the twelve rows structurally resemble an obligation "
                  r"already analysed; only (\S+) resemble nothing", MAN)
    check("§8.4's mirroring qualification matches the coding",
          "manuscript-claims.md §8.4 vs held-out-2-corpus.csv",
          [mirror["close"], mirror["none"]],
          [spelled(g) for g in m.groups()] if m else None)

    check("§8.4 states that the mediation row it proposes is untested here",
          "manuscript-claims.md §8.4", True,
          states(r"is untested by\s+this study"))
    check("§10 carries the mediation gap as a threat rather than only a finding",
          "manuscript-claims.md §10", True,
          states(r"Table 3 does not route every way placement can fail"))
    check("§10 records that source disjointness is not predicate disjointness",
          "manuscript-claims.md §10", True,
          states(r"source disjointness does not give predicate disjointness"))

    # §7.5's transport claim now spans two constructed studies.
    m = re.search(r"the (\S+) transport cases of the pre-specified study", MAN)
    check("§7.5's held-out-2 transport count matches transport-recursion.csv",
          "manuscript-claims.md §7.5", len([r for r in h2_transport
                                            if r["counted_in_paper_claim"] == "yes"]),
          spelled(m.group(1)) if m else None)
    m = re.search(r"(\S+) constructed cases and (\S+) documented ones do not establish", MAN)
    check("§7.5's totals match the recorded transport cases",
          "manuscript-claims.md §7.5 vs transport-recursion.csv",
          [len(counted) + len([r for r in h2_transport
                               if r["counted_in_paper_claim"] == "yes"]),
           len([r for r in transport if r["study"] == "retrodiction"])],
          [spelled(g) for g in m.groups()] if m else None)

    # §7.2 states the ablation counts; they must be the counts above.
    m = re.search(r"Of the (\d+) deficit-bearing obligations in the\s+(?:three\s+constructed\s+)?corpora(?: of\s+§VIII)?,\s+"
                  r"(\d+) (?:resolve through|require|were coded to) T2, T3 or Terminal(?:\s+\(held-out rows as\s+predicted\))?:\s+(\d+) transport a fact,\s+"
                  r"(\d+) transport a verdict,\s+(\d+) approximate and detect,\s+and\s+"
                  r"(\d+) are terminal", MAN)
    check("§7.2's ablation counts are what the corpora give",
          "manuscript-claims.md §7.2", [35, 33, 14, 9, 8, 2],
          [int(g) for g in m.groups()] if m else None)
    check("§7.2 states that obligation class alone does not separate them",
          "manuscript-claims.md §7.2", True,
          states(r"[Oo]bligation class alone does not distinguish among these\s+transformations"))

    # Table 6 reproduces the sensitivity cells; every cell must match the CSV.
    for r in adv:
        key = re.escape(r["obligation"].split(" (")[0][:32])
        row = re.search(rf"\| [^|]*{key}[^|]*\| (\w) \| (\w) \| (\w) \|", MAN)
        check(f"Table 6's row for {r['id']} matches adversary-sensitivity.csv",
              "manuscript-claims.md Table 6",
              [r["class_under_x1"], r["class_under_x2"], r["class_under_x3"]],
              list(row.groups()) if row else None)
    m = re.search(r"Class T falls from (\w+) of (\w+) to (\w+)\.", MAN)
    check("§10's stated drop in Class T matches the cells",
          "manuscript-claims.md §10", [t_counts[0], len(adv), t_counts[2]],
          [spelled(g) for g in m.groups()] if m else None)
    check("§10 states the monotonicity property and that every cell satisfies it",
          "manuscript-claims.md §10", True,
          states(r"move from T to O and never the reverse")
          and states(r"fifteen cells are consistent with that"))

    # Table 5 states each study's n and its evaluation question. The n must be
    # the row count of the corresponding data file, and every study must carry a
    # question, since the table is what tells a reviewer why there are four.
    for n, label in ((len(dev), "Development corpus"), (len(held), "Held-out refinement set"),
                     (len(held2), "Untouched test set"),
                     (len(retro), "Documented-architecture retrodiction")):
        check(f"Table 5's n for '{label}' matches its data file",
              "manuscript-claims.md Table 5", True,
              states(rf"\| {re.escape(label)} \| {n} \|"))
    check("Table 5 states one evaluation question per study",
          "manuscript-claims.md Table 5", 4,
          len(re.findall(r"\*\*EQ\d\*\*", MAN)))

    # The clean/prior separation, and that only clean pairs are reported.
    check("§8.5 states the clean/prior separation and every analysed pair is clean",
          "manuscript-claims.md §8.5 vs retrodiction-cases.csv", True,
          states(r"only clean pairs are analysed")
          and all(r["blind_status"] == "[clean]" for r in retro))

    # The frozen -> refined -> final chronology, which is what stops the held-out
    # result from looking like it was scored against rules it helped produce.
    check("§8.3 states the pre-test/refinement chronology",
          "manuscript-claims.md §8.3", True,
          states(r"The count of 13 is against the pre-test rules, not the refined ones")
          and states(r"fixed before the documented-architecture study began"))

    # §7.1's Instantiate step must stay marked as learned after the predictions.
    check("§7.1 and §8.5 agree that the predictions predate the Instantiate step",
          "manuscript-claims.md §7.1, §8.5", True,
          states(r"predictions reported there were made without it")
          and states(r"before that step existed, and none is revised"))

    # §7.5 names the documented instances by case id; they must be exactly the
    # retrodiction rows of transport-recursion.csv, and C2PA must not be
    # counted among them (it is constructed case K4).
    doc_ids = [r["case_id"] for r in transport if r["study"] == "retrodiction"]
    m = re.search(r"Three documented\s+retrodiction cases \(([^)]*)\)", MAN)
    check("§7.5 names exactly the documented cases transport-recursion.csv records",
          "manuscript-claims.md §7.5 vs transport-recursion.csv", sorted(doc_ids),
          sorted(re.findall(r"P\d+", m.group(1))) if m else None)
    check("§7.5 does not count C2PA (constructed case K4) as a documented case",
          "manuscript-claims.md §7.5", True,
          bool(m) and "C2PA" not in m.group(1) and "K4" not in m.group(1))

    # Claims the paper makes about its own corrected figures.
    check("§8.2 no longer states the superseded 25% operational rate",
          "manuscript-claims.md §8.2", False, states(r"and 25% of the operational"))
    check("§7.5 no longer claims ten transport cases",
          "manuscript-claims.md §7.5", False, states(r"ten transport cases"))

# -- T4 extension study (preliminary; constructed cases) --------------------
# The rule, case facts and each analysis pass were sealed in order. The rule is
# re-applied here, independently of the derivation file, to every path of every
# case; a derivation that calls a path enforced when the facts do not support it
# fails the study (protocol §5, soundness).
T4SEAL = (HERE / "protocols" / "T4-SEAL.txt").read_text(encoding="utf-8")
t4_pairs = re.findall(r"file\s*:\s*(\S+)\s*\n\s*sha256\s*:\s*([0-9a-f]{64})", T4SEAL)
check("T4 seal records the protocol, the case file and three passes",
      "protocols/T4-SEAL.txt", 5, len(t4_pairs))
for name, want in t4_pairs:
    got = hashlib.sha256((HERE / "protocols" / name).read_bytes()).hexdigest()
    check(f"T4 sealed file {name} is unchanged since sealing", "protocols/T4-SEAL.txt", want, got)

t4cases = json.loads((HERE / "protocols" / "t4-cases.json").read_text(encoding="utf-8"))["cases"]


def t4_path(c, p):
    I, R, F, L = c["I"], set(c["R"]), c["facts"], c["locations"]
    def moves(f, l):
        return F[f]["source"] not in (None, l) and F[f]["may_cross"] and L[l]["can_receive"]
    for l in p["via"]:
        miss = [f for f in I if f not in L[l]["native"]]
        if R <= set(L[l]["alpha"]) and all(moves(f, l) for f in miss):
            return l, "enforced"
    for l in p["via"]:
        miss = [f for f in I if f not in L[l]["native"]]
        if (R <= set(L[l]["alpha"]) and all(moves(f, l) or F[f]["proxy"] for f in miss)
                and (p["over_approx_ok"] or (c["reversible"] and p["detect"]))):
            return l, "approximated"
    return "—", "residual"


t4_rec = {(r["case"], r["path"]): (r["assigned"], r["outcome"]) for r in load("t4-paths.csv")}
t4_mismatch, t4_case = [], {}
for c in t4cases:
    vias = [set(p["via"]) for p in c["paths"].values()]
    check(f"T4 case {c['id']} has no single adequate cut", "protocols/t4-cases.json",
          set(), set.intersection(*vias))
    outs = []
    for pid, p in c["paths"].items():
        got = t4_path(c, p); outs.append(got[1])
        if t4_rec.get((c["id"], pid)) != got:
            t4_mismatch.append((c["id"], pid))
    t4_case[c["id"]] = "U" if "residual" in outs else ("A" if "approximated" in outs else "F")
check("T4 soundness: every recorded per-path outcome is what the rule returns",
      "t4-paths.csv vs t4-cases.json", [], t4_mismatch)
check("T4 per-path outcomes recorded", "t4-paths.csv", 18, len(t4_rec))
t4c = load("t4-cases.csv")
check("T4 case outcomes in the coding match the rule", "t4-cases.csv vs t4-cases.json", True,
      all(t4_case[r["case"]] == r["t4_outcome"] for r in t4c))
t4_count = Counter(r["t4_outcome"] for r in t4c)
check("T4 test cases by outcome (F, A, U)", "t4-cases.csv", [4, 2, 2],
      [t4_count["F"], t4_count["A"], t4_count["U"]])
check("T4 never codes enforceable what the independent pass codes U (EQ5b)", "t4-cases.csv", True,
      all(r["t4_outcome"] == "U" for r in t4c if r["independent_outcome"] == "U"))
t4_agree = sum(1 for r in t4c if r["agreement_norm"] in ("agree", "partial"))
check("T4 agreement meets the sealed threshold (at least 6 of 8)", "t4-cases.csv", True, t4_agree >= 6)

# -- artifact integrity ------------------------------------------------------
before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(DATA.glob("*.csv")) if p.name != "sampling-frame.csv"}
subprocess.run([sys.executable, str(HERE / "extract.py")], check=True,
               stdout=subprocess.DEVNULL)
after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
         for p in sorted(DATA.glob("*.csv")) if p.name != "sampling-frame.csv"}
check("CSVs are exactly what the current protocol files produce (no drift)",
      "extract.py re-run", before, after)

# -- the paper's evaluation section, recomputed ------------------------------
# Printed after the checks so that a reader who wants the paper's numbers rather
# than a pass/fail list gets them from the data, in the order the paper reports
# them. Every value here is computed above; nothing is transcribed from prose.
def paper_summary():
    o = o_rate
    return [
        ("VIII.A  sampling frame, fixed before classification",
         f"{sum(int(r['items_in_frame']) for r in frame)} items; "
         f"{sum(int(r['items_admitted_to_corpus']) for r in frame)} admitted"),
        ("VIII.A  ISO/IEC 42001 Annex A controls that are Class N",
         f"{n_class_n} of {len(iso)} (the paper claims at least 24)"),
        ("VIII.B  classification of the development corpus",
         f"{cls['T']} Class T, {cls['O']} Class O of {len(dev)}"),
        ("VIII.B  Class O rate by source",
         f"agentic {o('OWASP Agentic')}%, rights-based {o('EU AI Act')}%, "
         f"operational {o('ISO/IEC 42001', 'NIST AI 600-1')}%"),
        ("VIII.B  the same under the §VI definition",
         f"agentic {o_rate('OWASP Agentic', strict=True)}%, "
         f"rights-based {o_rate('EU AI Act', strict=True)}%, "
         f"operational {o_rate('ISO/IEC 42001', 'NIST AI 600-1', strict=True)}%"),
        ("VIII.C  held-out set 1, the pre-test rules",
         f"{app['yes']} of {len(held)} handled; {app['no']} exceptions"),
        ("VIII.D  held-out set 2, the final method, pre-specified",
         f"{app2['yes']} of {len(held2)} routed "
         f"({strain['A']} clean, {strain['A-']} strained); {strain['X']} exception"),
        ("VIII.D  mirroring of held-out set 2 against earlier corpora",
         f"{mirror['close']} close, {mirror['partial']} partial, {mirror['none']} none"),
        ("VIII.F  documented-architecture retrodiction",
         f"D0+D1 {code['D0'] + code['D1']}, D2 {code['D2']}, "
         f"D3 {code['D3']}, D4 {code['D4']} of {len(retro)}"),
        ("VII.E   transport recursion, one-step terminations",
         f"{len(counted) + sum(1 for r in h2_transport if r['counted_in_paper_claim'] == 'yes')}"
         f" constructed, {sum(1 for r in transport if r['study'] == 'retrodiction')} documented"),
        ("VII.B   cause ablation, deficit-bearing obligations",
         f"{sum(resolved.values())} of {len(deficit_rows)} across "
         f"{sum(1 for t in FOUR if resolved[t])} transformations"),
        ("X       adversary sensitivity, Class T by adversary",
         f"{t_counts[0]} of {len(adv)} (X1), {t_counts[1]} of {len(adv)} (X2), "
         f"{t_counts[2]} of {len(adv)} (X3)"),
        ("VIII.G  T4 extension (constructed cases, preliminary)",
         f"F {t4_count['F']}, A {t4_count['A']}, U {t4_count['U']} of {len(t4c)}; "
         f"agreement {t4_agree}/{len(t4c)}; soundness {18 - len(t4_mismatch)}/18"),
    ]


# -- report ------------------------------------------------------------------
width = max(len(c[0]) for c in checks)
failed = 0
for claim, where, expected, actual, ok in checks:
    if isinstance(expected, dict):
        expected = actual = "regenerates identically" if ok else "DRIFTED"
    print(f"{'PASS' if ok else 'FAIL'}  {claim:<{width}}  "
          f"expected {expected!s:<6} got {actual!s:<6}  [{where}]")
    failed += not ok
print(f"\n{len(checks) - failed}/{len(checks)} checks passed")
print("\nThe paper's evaluation section, recomputed from the data files:\n")
for where, value in paper_summary():
    print(f"  {where:<58s} {value}")
print()
if failed:
    print(f"{failed} FAILED — the paper and the artifact disagree.")
sys.exit(1 if failed else 0)
