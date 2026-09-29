#!/usr/bin/env python3
"""Extract the three corpora from the frozen research notes into CSV.

The markdown files are the source of truth; these CSVs are derived. Re-run after
any change to them so the artifact cannot drift from the analysis.
"""
import csv, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
#: The shipped protocol copies, so the artifact runs standalone: unpack this
#: directory anywhere and `python3 extract.py` works with nothing else present.
#: verify.py checks these against the working originals when both are available.
ROOT = HERE / "protocols"
OUT = HERE / "data"


def rows(md_path, start_marker, ncols):
    """Pipe-table rows following a marker, excluding header and rule."""
    text = pathlib.Path(md_path).read_text(encoding="utf-8")
    i = text.index(start_marker)
    out = []
    for line in text[i:].split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            if out:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != ncols or set("".join(cells)) <= set("-: "):
            continue
        if cells[0] in ("#", "Study", "Locus", "Code"):
            continue
        out.append(cells)
    return out


def write(name, header, data):
    p = OUT / name
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)
    print(f"  {name:28s} {len(data):3d} rows")
    return len(data)


# ---------------------------------------------------------------------------
# Normalisation. The markdown cells carry emphasis and coder shorthand (**O**,
# T\*, checkmarks, "D1 (partial)"). Those are the frozen record and are kept
# verbatim; each coded column additionally gets a plain-text twin so a reviewer
# can tally the paper's numbers with `sort | uniq -c` and get the paper's
# numbers, not a histogram of typography. verify.py reads only the twins.


def plain(cell):
    """Strip markdown emphasis and escaping from a coded cell."""
    return cell.replace("**", "").replace("\\", "").strip()


#: Primary citation wins where an obligation cites two sources: #1 (AI Act
#: Art 12; ISO A.6.2.8) counts to the AI Act, #18 (NIST MG-4.1; AI Act
#: Art 14(4)) counts to NIST. This is the rule behind the per-source table in
#: classification-corpus.md §4.
SOURCES = [("EU AI Act", r"AI Act"), ("ISO/IEC 42001", r"ISO"),
           ("NIST AI 600-1", r"NIST"), ("OWASP Agentic", r"OWASP")]


def source_of(text):
    hits = [(m.start(), name) for name, pat in SOURCES
            for m in [re.search(pat, text)] if m]
    return min(hits)[1] if hits else ""


def class_of(cell):
    """T* is Class T — its facts exist and are merely unrouted, so nothing is
    destroyed. Counted as T throughout, per classification-corpus.md §3."""
    c = plain(cell).rstrip("*")
    assert c in ("T", "O"), f"unexpected class {cell!r}"
    return c


def applicable_of(cell):
    """Held-out match column. A check mark, with or without the second-deficit
    star, is an applicable case; the two exceptions are the cross and the
    tilde. See heldout-test.md §1 and §2."""
    c = plain(cell)
    return {"\u2713": "yes", "\u2713*": "yes", "\u2717": "no", "~": "no"}[c]


def applicable2_of(cell):
    """Held-out set 2 applicability column, per the sealed pre-registration §5(a):
    A applicable, A- applicable with a recorded strain, X not applicable. The
    twin folds A- into yes, because a recorded strain is a note on a row the
    method did route; only X is an exception."""
    c = plain(cell).replace("\u2212", "-")
    return {"A": "yes", "A-": "yes", "X": "no"}[c]


def agreement_of(cell):
    """Agreement between the sealed prediction and the sealed independent pass:
    full, partial, none. See heldout-2-test.md §1."""
    c = plain(cell)
    return {"\u2713": "full", "~": "partial", "\u2717": "none"}[c]


def mirroring_of(cell):
    """Structural resemblance to an obligation already analysed. The counts this
    feeds are reported separately from the headline, per §4 of the test file."""
    c = plain(cell).lower()
    assert c in ("none", "partial", "close"), f"unexpected mirroring {cell!r}"
    return c


def code_of(cell):
    """D0-D4, discarding the qualifiers ("partial", "form b") that annotate a
    code without changing it."""
    c = plain(cell)
    m = re.match(r"(D[0-4])", c)
    assert m, f"unexpected code {cell!r}"
    return m.group(1)


def transformation_of(cell):
    """The transformation a coded cell resolves to, for the cause ablation.

    The three corpora write it differently ("T2-fact -> T1", "**T2 fact**",
    "T2 verdict x2"), so normalise once here and let verify.py count. Returns
    None where the frozen record returns no transformation at all, which is
    K6 and nothing else."""
    t = plain(cell)
    if re.search(r"no row|nothing", t, re.I):
        return None
    if re.search(r"T2[\s-]*\(?verdict", t, re.I):
        return "T2 verdict"
    if "T2" in t:
        return "T2 fact"
    if "T3" in t:
        return "T3"
    if re.search(r"terminal", t, re.I):
        return "Terminal"
    if "T1" in t:
        return "T1"
    raise AssertionError(f"unclassifiable transformation {cell!r}")


def main():
    dev = rows(ROOT / "classification-corpus.md", "| # | Obligation (source)", 7)
    dev = [r + [source_of(r[1]), class_of(r[5])] for r in dev]
    n1 = write("development-corpus.csv",
               ["id", "obligation_and_source", "key_facts_in_I_of_o", "strongest_cut",
                "deficit_at_cut", "class", "transformation",
                "source", "class_norm"], dev)

    held = rows(ROOT / "heldout-test.md", "| # | Obligation (held-out source)", 7)
    held = [r + [applicable_of(r[6])] for r in held]
    n2 = write("held-out-corpus.csv",
               ["id", "obligation_and_source", "deficit_at_strongest_cut", "cause",
                "predicted_transformation", "independent_architecture_answer", "match",
                "applicable"], held)

    held2 = rows(ROOT / "heldout-2-test.md", "| # | Obligation (held-out set 2 source)", 8)
    held2 = [r + [applicable2_of(r[5]), agreement_of(r[6]), mirroring_of(r[7])]
             for r in held2]
    n4 = write("held-out-2-corpus.csv",
               ["id", "obligation_and_source", "deficit_and_cause",
                "predicted_by_frozen_method", "independent_architecture_answer",
                "applicability", "agreement", "mirroring",
                "applicable", "agreement_norm", "mirroring_norm"], held2)

    # The retrodiction tables are interleaved across several blocks (predictions were
    # locked in three tranches, observations appended as coding proceeded), so match
    # rows by id anywhere in the file rather than by position.
    txt = (ROOT / "retrodiction-protocol.md").read_text(encoding="utf-8")


    def cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]


    pred, obs = {}, {}
    for line in txt.split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            continue
        c = cells(s)
        m = re.match(r"\*{0,2}(P\d+)\*{0,2}$", c[0])
        if not m:
            continue
        pid = m.group(1)
        if s.startswith("| **") and len(c) == 4:          # observed-placement row
            obs[pid] = c[1:]
        elif len(c) in (6, 7):                             # locked-prediction row
            pred[pid] = c[1:]

    data = []
    for pid in sorted(obs, key=lambda x: int(x[1:])):
        pr = pred.get(pid, [])
        if len(pr) == 6:      # stratum-tagged block: stratum, platform, obligation, deficit, transform, blind
            platform, obligation, deficit, transform, blind = pr[1], pr[2], pr[3], pr[4], pr[5]
        elif len(pr) == 5:    # original block: platform, obligation, deficit, transform, blind
            platform, obligation, deficit, transform, blind = pr
        else:
            platform = obligation = deficit = transform = blind = ""
        data.append([pid, platform, obligation, deficit, transform, blind,
                     obs[pid][0], obs[pid][1], obs[pid][2], code_of(obs[pid][1])])

    # -- adversary sensitivity ----------------------------------------------
    # Five obligations re-classified under three nested adversary models. The
    # analysis file is the source of truth; this parses its results table so the
    # CSV, the paper's Table 6 and the prose cannot drift apart.
    adv_md = (ROOT / "adversary-sensitivity.md").read_text(encoding="utf-8")
    adv = []
    for line in adv_md[adv_md.index("## 4. Results"):].split("\n"):
        t = line.strip()
        if not t.startswith("|"):
            if adv:
                break
            continue
        c = [x.strip() for x in t.strip("|").split("|")]
        if len(c) != 6 or not re.match(r"^O\d+$", plain(c[0])):
            continue
        adv.append([plain(c[0]), c[1], plain(c[2]), plain(c[3]), plain(c[4]), c[5]])
    for r in adv:
        for cell in r[2:5]:
            assert cell in ("T", "O"), f"unexpected class {cell!r} in {r[0]}"
    write("adversary-sensitivity.csv",
          ["id", "obligation", "class_under_x1", "class_under_x2",
           "class_under_x3", "rationale"], adv)

    # -- transport recursion -------------------------------------------------
    # Every T2 spawns a derived integrity obligation ("this transported fact or
    # verdict must be unforgeable by X") which must itself be placed. The claim
    # under test is that it terminates in one step. The frozen record enumerates
    # the development instances by item number in classification-corpus.md
    # §5(e); we parse that sentence rather than retyping the ids, so the CSV
    # cannot disagree with the note that established them.
    corpus_md = (ROOT / "classification-corpus.md").read_text(encoding="utf-8")
    m = re.search(r"Move-Context recursion held on every instance\.\*\* Items "
                  r"([\d, ]+?) each spawned", corpus_md)
    assert m, "the frozen seven-item sentence has moved or changed wording"
    frozen_seven = [i.strip() for i in m.group(1).split(",") if i.strip()]

    tr = []
    for r in dev:
        if "T2" not in r[6]:
            continue
        counted = r[0] in frozen_seven
        tr.append(["development", r[0], r[1], r[6], "yes" if counted else "no",
                   "enumerated in classification-corpus.md §5(e): Class T, closed "
                   "by T1 at the identity or signing layer, no second recursion"
                   if counted else
                   "T2 case, but not among the seven the frozen note enumerates; "
                   "both carry a residual alongside the transport"])
    for r in held:
        if "T2" not in r[4]:
            continue
        tr.append(["held-out", r[0], r[1], plain(r[4]), "no",
                   "heldout-test.md §3 claims 3/3 termination for this study but "
                   "does not say which three of these six; not reconstructable, "
                   "so excluded from the paper's count"])
    # The prediction pass names a derived integrity obligation in five of the
    # eight T2 rows; the sentence that enumerates them is parsed rather than
    # retyped, so the CSV cannot disagree with the frozen note.
    h2_md = (ROOT / "heldout-2-test.md").read_text(encoding="utf-8")
    m2 = re.search(r"prediction recorded a derived integrity obligation — "
                   r"((?:K\d+, )+K\d+)", h2_md)
    assert m2, "the five-case sentence in heldout-2-test.md has moved or changed"
    frozen_five = [i.strip() for i in m2.group(1).split(",")]
    for r in held2:
        if "T2" not in r[3]:
            continue
        counted = r[0] in frozen_five
        tr.append(["held-out-2", r[0], r[1], plain(r[3])[:60],
                   "yes" if counted else "no",
                   "the sealed prediction names a derived integrity obligation "
                   "closing by T1 at the identity or signing layer"
                   if counted else
                   "T2 row whose derived integrity obligation the sealed "
                   "prediction pass did not name; not counted"])

    for r in data:
        if "derived" not in r[8].lower():
            continue
        tr.append(["retrodiction", r[0], r[1], plain(r[4])[:60], "documented",
                   "the derived integrity obligation is discharged in the "
                   "documented design, observed rather than reasoned"])

    write("transport-recursion.csv",
          ["study", "case_id", "obligation_or_system", "transformation",
           "counted_in_paper_claim", "basis"], tr)

    n3 = write("retrodiction-cases.csv",
               ["id", "platform_or_system", "obligation", "predicted_deficit",
                "predicted_transformation", "blind_status", "documented_placement",
                "code", "coding_rationale", "code_norm"], data)

    print(f"\nexpected 25 / 15 / 12 / 14 — got {n1} / {n2} / {n4} / {n3}")
    assert len(adv) == 5, f"expected 5 sensitivity rows, got {len(adv)}"


if __name__ == "__main__":
    main()
