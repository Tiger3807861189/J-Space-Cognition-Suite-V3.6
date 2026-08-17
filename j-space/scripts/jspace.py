#!/usr/bin/env python3
"""jspace — an instrument for the J-Space skill.

It knows one thing you cannot know accurately: what state you were in a few seams
ago. It keeps that record and hands it back. It decides nothing, and it blocks
nothing.

    jspace.py seam                          the ledger, and what has and has not moved
    jspace.py note --next "..."             set the single next action
    jspace.py note --goal "..."             set what done means
    jspace.py note --core "name — one fact" add a hub entry
    jspace.py note --core "..." --core-slot 1  swap a live hub entry
    jspace.py note --check "..." --by "..." append a numbered verified checkpoint
    jspace.py note --open "..." --settled-by "..."   add an open question
    jspace.py note --close 2 --check "..." --by "..."  resolve question 2
    jspace.py ship draft.md                 register check on anything about to leave
    jspace.py resume                        premise, invariants and full ledger

Exit codes mean one thing only:

    0   it did what you asked
    2   it could not do what you asked

It never exits non-zero to stop you from working. The one thing it declines to do
is write a malformed entry into the ledger, because a ledger you cannot trust is
worse than no ledger — it looks like state.

Standard library only. No network. Writes exactly one directory: .jspace/

Checkpoint coverage and outgoing claims are recognised in English and Chinese.
Any other language extends the vocabulary through the environment, as literal
comma-separated terms:

    JSPACE_COVERAGE_TERMS="toutes,chaque,cas limites,couverture"
    JSPACE_CLAIM_TERMS="vérifié,confirmé"
"""

import argparse
import codecs
import json
import os
import re
import sys
import tempfile
import time

LEDGER_DIR = ".jspace"
LEDGER = os.path.join(LEDGER_DIR, "WORKSPACE.md")
HISTORY = os.path.join(LEDGER_DIR, "history.json")
SECTIONS = ("Goal", "Core", "Verified", "Open", "Next")

STALL_RUN = 3          # consecutive seams before a pattern is worth reporting
RESUME_GAP = 1800      # seconds after which a seam prints the fuller anchor

PREMISE = (
    "You do not only produce words; you also think them before — and without —\n"
    "saying them. The J-space holds what you are poised to say: concepts you can\n"
    "report on demand, hold in mind deliberately, reason with silently, and\n"
    "broadcast to many downstream computations at once. Dense on the inside,\n"
    "decodable on demand."
)

INVARIANTS = [
    "A marker fired and its move never happened — or it happened and you never settled.",
    "A sweep ran and found nothing — again.",
    "A dense line cannot be expanded back into plain words on request.",
    "Every confidence tag this session has been the same tag.",
    "A checkpoint was declared and nothing was written down.",
    "Something was called verified without stating what it covered.",
    "Dense notation appears in something a person or a task-facing tool reads.",
    "You called the task finished without reading the goal back line by line.",
]

SHIFTS = "shift the abstraction, shift the strategy, or go and measure"


class LedgerReadError(Exception):
    """The persisted ledger cannot be read without risking state loss."""

# Notation that belongs to the inner register and nowhere a person reads.
# Deliberately excludes ✓ ✗ √: they are ordinary in checklists and summaries, and
# stripping them from good writing costs more than the leak they would catch.
INNER_ONLY = ["⇒", "⟹", "⟸", "∴", "∵", "⊆", "⊇", "∋", "??", "?!", "💀"]
MARKERS = ["GRRR", "GAAAH", "PHEW", "I see meltdown", "DATA DATA", "I'M DROWNING"]

# Claim and coverage vocabularies.
#
# The checkpoint gate is deliberate: a checkpoint with no stated coverage is not
# recorded. That only holds as a gate while the vocabulary can read the language
# the coverage was written in. Where it cannot, the gate stops separating "no
# coverage stated" from "coverage stated in a language the pattern cannot read",
# and refuses a well-formed checkpoint — which is the one thing the controller
# is not supposed to do.
#
# English and Chinese are carried here because the suite is published in both.
# Any other language extends the vocabulary through the environment rather than
# by patching this file; see EXTRA_TERMS below.
CLAIM_EN = r"\b(?:verified|confirmed|validated|tested|proven)\b"
COVERAGE_EN = (
    r"\b(?:all|each|every|cases?|inputs?|samples?|bounds?|boundaries|edges?|"
    r"random(?:ized)?|files?|modules?|sections?|lines?|scenarios?|environments?|"
    r"platforms?|datasets?|records?|routes?|commands?|branches?|ranges?|including|"
    r"through|up\s+to|Windows|Linux|macOS|Chrome|Firefox|Safari)\b|"
    r"\b(?:Python|Node(?:\.js)?)\s*\d|\bn\s*[<≤=]\s*\d"
)
# Chinese is written without word separators, so \b never fires between a Han
# character and its neighbour. These alternatives are matched unanchored.
CLAIM_ZH = r"已验证|已确认|已校验|已测试|验证通过|确认无误"
COVERAGE_ZH = (
    r"全部|所有|每个|每一|逐个|逐项|覆盖|用例|边界|极端|随机|"
    r"包括|包含|全量|各个|范围|场景|分支|模块|文件|环境|平台|数据集"
)

EXTRA_CLAIM_ENV = "JSPACE_CLAIM_TERMS"
EXTRA_COVERAGE_ENV = "JSPACE_COVERAGE_TERMS"


def extra_terms(name):
    """Literal comma-separated terms from the environment, escaped for regex use."""
    raw = os.environ.get(name) or ""
    return [re.escape(term) for term in (part.strip() for part in raw.split(",")) if term]


def vocabulary(*groups):
    """One case-insensitive pattern over every non-empty alternative group."""
    alternatives = [group for group in groups if group]
    return re.compile("(?:" + "|".join(alternatives) + ")", re.I)


CLAIM = vocabulary(CLAIM_EN, CLAIM_ZH, *extra_terms(EXTRA_CLAIM_ENV))
COVERAGE = vocabulary(COVERAGE_EN, COVERAGE_ZH, *extra_terms(EXTRA_COVERAGE_ENV))


# ------------------------------------------------------------------------- ledger


def read_ledger():
    book = {k: [] for k in SECTIONS}
    if not os.path.exists(LEDGER):
        return book
    current = None
    try:
        with open(LEDGER, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeError) as exc:
        raise LedgerReadError("%s (%s)" % (LEDGER, exc)) from exc
    for line in lines:
        head = line.strip()
        if head.startswith("## "):
            name = head[3:].strip()
            current = name if name in book else None
            continue
        if current and head:
            if current in ("Goal", "Next"):
                book[current].append(head.rstrip())
            else:
                book[current].append(head[2:].rstrip() if head.startswith("- ") else head.rstrip())
    return book


def ensure_dir():
    """Make the ledger directory. Returns an error string, or None on success."""
    try:
        os.makedirs(LEDGER_DIR, exist_ok=True)
    except OSError as exc:
        return "%s (%s)" % (LEDGER_DIR, exc.strerror or "cannot create")
    if not os.path.isdir(LEDGER_DIR):
        return "%s exists but is not a directory" % LEDGER_DIR
    return None


def atomic_write_text(path, text):
    """Replace a UTF-8 text file atomically. Returns an error string or None."""
    problem = ensure_dir()
    if problem:
        return problem
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=LEDGER_DIR, prefix=".jspace-", delete=False
        ) as fh:
            temp_path = fh.name
            fh.write(text)
        os.replace(temp_path, path)
    except OSError as exc:
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        return "%s (%s)" % (path, exc.strerror or "cannot write")
    return None


def write_ledger(book):
    out = ["# J-Space Workspace Ledger", ""]
    for name in SECTIONS:
        out.append("## " + name)
        rows = book[name]
        if name in ("Goal", "Next"):
            out.append(rows[0] if rows else "")
        else:
            out.extend("- " + r for r in rows)
        out.append("")
    return atomic_write_text(LEDGER, "\n".join(out).rstrip() + "\n")


def one(book, key):
    return book[key][0] if book[key] else ""


def declined(message, fix):
    print("NOT RECORDED: " + message)
    print("  " + fix)
    return 2


def clean_scalar(value):
    """Return a safe one-line scalar and an error, if any."""
    if value is None:
        return None, None
    if "\r" in value or "\n" in value:
        return None, "must be one line"
    value = value.strip()
    if not value:
        return None, "must not be empty"
    return value, None


def next_number(rows, prefix):
    numbers = []
    pattern = re.compile(r"^%s(\d+)\b" % re.escape(prefix))
    for row in rows:
        match = pattern.match(row)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


# ------------------------------------------------------------------------ history


def read_history():
    if not os.path.exists(HISTORY):
        return []
    try:
        with open(HISTORY, encoding="utf-8") as fh:
            hist = json.load(fh)
    except (ValueError, OSError) as exc:
        print("WARNING: history was unreadable and has been restarted (%s)." % exc, file=sys.stderr)
        return []
    valid = isinstance(hist, list)
    if valid:
        for row in hist:
            valid = (
                isinstance(row, dict)
                and isinstance(row.get("t"), int)
                and not isinstance(row.get("t"), bool)
                and isinstance(row.get("next"), str)
                and isinstance(row.get("verified"), int)
                and not isinstance(row.get("verified"), bool)
                and isinstance(row.get("open"), int)
                and not isinstance(row.get("open"), bool)
            )
            if not valid:
                break
    if not valid:
        print("WARNING: history had an invalid shape and has been restarted.", file=sys.stderr)
        return []
    return hist


def append_history(book):
    hist = read_history()
    hist.append(
        {
            "t": int(time.time()),
            "next": one(book, "Next"),
            "verified": len(book["Verified"]),
            "open": len(book["Open"]),
        }
    )
    hist = hist[-20:]
    problem = atomic_write_text(HISTORY, json.dumps(hist))
    if problem:
        print("WARNING: recent seam history was not saved — " + problem, file=sys.stderr)
    return hist


def observations(hist):
    """Facts about recent state. Facts only — the judgement is not the script's."""
    if len(hist) < STALL_RUN:
        return []
    run = hist[-STALL_RUN:]
    found = []
    if len({h["next"] for h in run}) == 1 and run[0]["next"]:
        found.append(
            "Your next action has been the same for %d seams." % STALL_RUN
        )
    if run[0]["verified"] == run[-1]["verified"]:
        found.append(
            "Nothing new has been verified across those %d seams." % STALL_RUN
        )
    opens = [h["open"] for h in run]
    if all(b > a for a, b in zip(opens, opens[1:])) and len(opens) > 1:
        found.append("Open-question count increased at every seam.")
    if run[0]["verified"] != run[-1]["verified"] and len({h["next"] for h in run}) == 1:
        found.append(
            "Verified entries are growing but the next action has not changed."
        )
    return found


# -------------------------------------------------------------------------- modes


def print_ledger(book):
    print("Goal:     " + (one(book, "Goal") or "(not set)"))
    core = book["Core"] or ["(empty)"]
    print("Core:     " + core[0])
    for extra in core[1:2]:
        print("          " + extra)
    if len(core) > 2:
        print("          (+%d more in the ledger — two live at a time)" % (len(core) - 2))
    verified = book["Verified"]
    print("Verified: " + (verified[-1] if verified else "(none yet)"))
    if len(verified) > 1:
        print("          (%d earlier, in the ledger)" % (len(verified) - 1))
    for row in book["Open"][:2]:
        print("Open:     " + row)
    print("Next:     " + (one(book, "Next") or "(not set)"))


def print_full_ledger(book):
    print("Goal: " + (one(book, "Goal") or "(not set)"))
    print("Core:")
    if book["Core"]:
        for index, row in enumerate(book["Core"]):
            state = "live" if index < 2 else "parked"
            print("  [%s] %s" % (state, row))
    else:
        print("  (empty)")
    print("Verified:")
    if book["Verified"]:
        for row in book["Verified"]:
            print("  " + row)
    else:
        print("  (none yet)")
    print("Open:")
    if book["Open"]:
        for row in book["Open"]:
            print("  " + row)
    else:
        print("  (none)")
    print("Next: " + (one(book, "Next") or "(not set)"))


def print_reentry(book, heading):
    print(heading)
    print(PREMISE)
    print()
    print_full_ledger(book)
    print()
    print("Not working if:")
    for n, text in enumerate(INVARIANTS, 1):
        print("  %d. %s" % (n, text))
    print()
    print("State the current pass, then make Next name the first action back.")


def mode_seam(book):
    hist = read_history()
    gap = int(time.time()) - hist[-1]["t"] if hist else 0
    if gap > RESUME_GAP:
        print_reentry(
            book,
            "── j-space ─ seam (long gap: %d minutes since the last one)" % (gap // 60),
        )
    else:
        print("── j-space ─ seam")
        print_ledger(book)
    hist = append_history(book)
    found = observations(hist)
    if found:
        print()
        for f in found:
            print("· " + f)
        print()
        print("You would not have noticed that; I keep the record, so here it is.")
        print("If that is depth, carry on. If it is a stall, the moves open to you are:")
        print("  " + SHIFTS + ".")
    if not one(book, "Next"):
        print()
        print("There is no next action recorded. The ledger stops being state at that point.")
    return 0


def mode_resume(book):
    print_reentry(book, "── j-space ─ resume")
    append_history(book)
    return 0


def mode_note(book, args):
    """Apply valid edits; decline malformed ones without dropping independent edits.

    Initial creation is atomic because Goal and Next are both required. After that,
    a declined independent edit must not cost an accepted one, or mixed calls never
    converge.
    """
    changed = False
    refused = []
    invalid = set()

    for name, flag in (
        ("goal", "--goal"),
        ("core", "--core"),
        ("next", "--next"),
        ("check", "--check"),
        ("by", "--by"),
        ("open", "--open"),
        ("settled_by", "--settled-by"),
    ):
        value, problem = clean_scalar(getattr(args, name))
        if value is not None and not problem and name in ("goal", "next") and value.startswith("## "):
            problem = "must not begin with a ledger section heading ('## ')"
            value = None
        setattr(args, name, value)
        if problem:
            invalid.add(name)
            refused.append(("%s %s." % (flag, problem), "%s \"one-line value\"" % flag))

    if not (one(book, "Goal") or args.goal) or not (one(book, "Next") or args.next):
        refused.append(
            (
                "opening the ledger requires both Goal and Next.",
                'note --goal "what done means" --next "the first action"',
            )
        )
        for message, fix in refused:
            declined(message, fix)
        return 2

    if args.goal:
        book["Goal"] = [args.goal]
        changed = True

    if args.core:
        if "—" not in args.core and " - " not in args.core:
            refused.append(
                (
                    "a core entry without its defining fact is a mention, not a load.",
                    '--core "name — the one fact that makes it matter"',
                )
            )
        elif args.core_slot is None:
            if args.core not in book["Core"]:
                book["Core"].append(args.core)
                changed = True
        else:
            live = book["Core"][:2]
            parked = book["Core"][2:]
            idx = args.core_slot - 1
            if idx > len(live):
                refused.append(
                    (
                        "live core slot %d does not exist." % args.core_slot,
                        "use the next available slot or add the entry without --core-slot",
                    )
                )
            elif args.core in live and (idx >= len(live) or live[idx] != args.core):
                refused.append(
                    ("that core entry is already live.", "choose the slot that should actually change")
                )
            elif idx == len(live):
                live.append(args.core)
                book["Core"] = live + parked
                changed = True
            else:
                displaced = live[idx]
                live[idx] = args.core
                parked = [row for row in parked if row != args.core]
                if displaced != args.core:
                    parked.insert(0, displaced)
                book["Core"] = live + parked
                changed = displaced != args.core
    elif args.core_slot is not None:
        refused.append(("--core-slot requires --core.", '--core "name — defining fact" --core-slot 1'))

    check_recorded = False
    if args.check:
        if not args.by:
            refused.append(
                (
                    "a checkpoint with no record is not a checkpoint.",
                    '--check "what now holds" --by "what verified it"',
                )
            )
        elif not COVERAGE.search(args.by):
            refused.append(
                (
                    "verified without stated coverage is a mood, not a result.",
                    '--by "brute force, n ≤ 6, including empty and maximum"',
                )
            )
        else:
            num = next_number(book["Verified"], "✓")
            book["Verified"].append(
                "✓%02d %s — verified by: %s" % (num, args.check, args.by)
            )
            changed = True
            check_recorded = True
    else:
        if args.by and "check" not in invalid:
            refused.append(("--by requires --check.", '--check "what now holds" --by "verifier and coverage"'))

    if args.open:
        settle = args.settled_by or ""
        if not settle:
            refused.append(
                (
                    "an open question with nothing that would settle it cannot be closed.",
                    '--open "the question" --settled-by "the cheapest test that could refute it"',
                )
            )
        else:
            num = next_number(book["Open"], "?")
            book["Open"].append("?%02d %s — settled by: %s" % (num, args.open, settle))
            changed = True
    elif args.settled_by and "open" not in invalid:
        refused.append(("--settled-by requires --open.", '--open "question" --settled-by "test"'))

    if args.close is not None:
        rows = book["Open"]
        target = "?%02d" % args.close
        idx = next((i for i, row in enumerate(rows) if row.startswith(target + " ")), None)
        if idx is None:
            refused.append(
                ("no open question numbered %d." % args.close, "run `seam` to see the list")
            )
        elif not check_recorded:
            refused.append(
                (
                    "closing an open question requires a checkpoint in the same call.",
                    '--close %d --check "what now holds" --by "verifier and coverage"' % args.close,
                )
            )
        else:
            rows.pop(idx)
            changed = True

    if args.next:
        book["Next"] = [args.next]
        changed = True

    if changed:
        problem = write_ledger(book)
        if problem:
            print("CANNOT: cannot write the ledger — " + problem)
            print("  free the path, or work without the file: keep the five lines in the")
            print("  conversation and restate them at each seam.")
            return 2
    for message, fix in refused:
        declined(message, fix)
    if refused:
        if changed:
            print("  (everything else in this call was recorded.)")
        return 2
    print_ledger(book)
    return 0


def mode_ship(text):
    """Report inner-register leakage in outgoing text.

    A report, not a gate: it exits 0 whether or not it finds anything, because
    the caller asked it to look and it looked.
    """
    findings = []
    lines = text.splitlines()

    leaked = sorted({s for s in INNER_ONLY if s in text})
    if leaked:
        findings.append("inner-register notation in outgoing text: " + " ".join(leaked))

    hot = sorted({m for m in MARKERS if m.lower() in text.lower()})
    if hot:
        findings.append("state markers in outgoing text: " + ", ".join(hot))

    for n, line in enumerate(lines, 1):
        if CLAIM.search(line) and not COVERAGE.search(line):
            findings.append('line %d: "verified" with no stated coverage' % n)
            break

    run = 1
    for a, b in zip(lines, lines[1:]):
        run = run + 1 if a.strip() and a.strip() == b.strip() else 1
        if run >= 3:
            findings.append("repetition loop: a line repeats three times or more")
            break

    if re.search(r"([.…\-'\s])\1{20,}", text):
        findings.append("repetition loop: a character run of 20 or more")

    if not findings:
        print("clean — the outgoing register holds.")
        return 0
    print("── j-space ─ ship")
    for f in findings[:7]:
        print("· " + f)
    print()
    print("The switch is total: expand the span into clean language before it goes.")
    return 0


def decode_outgoing(data, origin):
    """Decode outgoing bytes without silently accepting an unknown or binary encoding."""
    try:
        if data.startswith(codecs.BOM_UTF8):
            text = data.decode("utf-8-sig")
        elif data.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
            text = data.decode("utf-32")
        elif data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
            text = data.decode("utf-16")
        else:
            text = data.decode("utf-8")
            if "\x00" in text:
                raise UnicodeError("NUL bytes suggest an unsupported encoding")
    except UnicodeError as exc:
        return None, "%s (cannot decode safely: %s)" % (origin, exc)
    return text, None


def read_outgoing(path):
    """Read outgoing text from a file, decoded the same way for every source."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return None, "%s (%s)" % (path, exc.strerror or "unreadable")
    return decode_outgoing(data, path)


def read_outgoing_stdin():
    """Read outgoing text from stdin as bytes.

    Reading the text stream instead would decode through the ambient locale, so
    the same UTF-8 input inspected as a file and piped through `-` would not
    produce the same findings.
    """
    stream = getattr(sys.stdin, "buffer", None)
    if stream is None:
        return sys.stdin.read(), None
    return decode_outgoing(stream.read(), "stdin")


def configure_streams():
    """Keep controller output deterministic on Windows consoles and redirected streams."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


# --------------------------------------------------------------------------- main


def main(argv=None):
    """Parse the subcommand and run it. Returns the process exit code."""
    configure_streams()
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("seam", help="the ledger, and what has and has not moved")
    sub.add_parser("resume", help="premise, invariants and full ledger, after a gap")

    n = sub.add_parser("note", help="record something in the ledger")
    n.add_argument("--goal")
    n.add_argument("--core")
    n.add_argument("--core-slot", dest="core_slot", type=int, choices=(1, 2))
    n.add_argument("--next")
    n.add_argument("--check")
    n.add_argument("--by")
    n.add_argument("--open")
    n.add_argument("--settled-by", dest="settled_by")
    n.add_argument("--close", type=int)

    s = sub.add_parser("ship", help="register check on anything about to leave")
    s.add_argument("file", help="path, or - for stdin")

    args = p.parse_args(argv)

    if args.cmd == "ship":
        if args.file == "-":
            text, problem = read_outgoing_stdin()
        else:
            text, problem = read_outgoing(args.file)
        if problem:
            print("CANNOT: " + problem + ".")
            print("  pass a readable file, or - to read stdin")
            return 2
        return mode_ship(text)

    try:
        book = read_ledger()
    except LedgerReadError as exc:
        print("CANNOT: ledger was unreadable — %s." % exc)
        print("  repair or remove .jspace/WORKSPACE.md before recording more state")
        return 2
    if args.cmd == "seam":
        return mode_seam(book)
    if args.cmd == "resume":
        return mode_resume(book)
    return mode_note(book, args)


if __name__ == "__main__":
    sys.exit(main())
