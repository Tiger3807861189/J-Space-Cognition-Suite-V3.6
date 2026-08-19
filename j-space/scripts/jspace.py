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

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(SKILL_ROOT, "SKILL.md")

STALL_RUN = 3          # consecutive seams before a pattern is worth reporting
RESUME_GAP = 1800      # seconds after which a seam prints the fuller anchor

PREMISE_HEAD = "You do not only produce words; you also think them before"
PREMISE_TAIL = "decodable on demand."

SHIFTS = "Shift the abstraction, shift the strategy, or shift to empirics."

_anchor_cache = None


class LedgerReadError(Exception):
    """The persisted ledger cannot be read without risking state loss."""


class AnchorLoadError(Exception):
    """SKILL.md anchors could not be read."""


def read_skill_text():
    try:
        with open(SKILL_MD, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        raise AnchorLoadError("cannot read %s (%s)" % (SKILL_MD, exc)) from exc


def extract_premise(text):
    start = text.find(PREMISE_HEAD)
    if start < 0:
        raise AnchorLoadError("the premise is missing from SKILL.md")
    end = text.find(PREMISE_TAIL, start)
    if end < 0:
        raise AnchorLoadError("the premise is truncated in SKILL.md")
    return text[start : end + len(PREMISE_TAIL)]


def extract_invariants(text):
    """Read the numbered invariant list and join Markdown continuation lines."""
    heading = "## The invariants"
    start = text.find(heading)
    if start < 0:
        raise AnchorLoadError("the invariants are missing from SKILL.md")
    block = text[start + len(heading) :]
    next_heading = block.find("\n## ")
    if next_heading >= 0:
        block = block[:next_heading]

    rows = []
    current = None
    for line in block.splitlines():
        numbered = re.match(r"^\d+\.\s+(.*)$", line)
        if numbered:
            if current:
                rows.append(" ".join(current))
            current = [numbered.group(1).strip()]
        elif current is not None and line.startswith((" ", "\t")) and line.strip():
            current.append(line.strip())
        elif current is not None and line.strip():
            break
    if current:
        rows.append(" ".join(current))
    if not rows:
        raise AnchorLoadError("the invariant list is empty in SKILL.md")
    return rows


def load_anchors():
    global _anchor_cache
    if _anchor_cache is None:
        text = read_skill_text()
        _anchor_cache = (extract_premise(text), extract_invariants(text))
    return _anchor_cache


def anchor_load_help():
    return (
        "  install the complete j-space/ directory so SKILL.md sits beside scripts/"
    )


# Notation that belongs to the inner register and nowhere a person reads.
# Deliberately excludes ✓ ✗ √: they are ordinary in checklists and summaries, and
# stripping them from good writing costs more than the leak they would catch.
INNER_ONLY = ["⇒", "⟹", "⟸", "∴", "∵", "⊆", "⊇", "∋", "??", "?!", "💀"]
MARKERS = ["GRRR", "GAAAH", "PHEW", "I see meltdown", "DATA DATA", "I'M DROWNING"]
MARKDOWN_HEADING = re.compile(r"^\s{0,3}#{1,6}(?:\s|$)")
SETEXT_UNDERLINE = re.compile(r"^\s{0,3}(?:=+|-+)\s*$")
TABLE_DELIMITER = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$"
)
MARKDOWN_LIST_ITEM = re.compile(r"^\s{0,3}(?:[-+*]|\d+[.)])\s+")
MARKDOWN_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
THEMATIC_BREAK = re.compile(r"^\s{0,3}(?:(?:\*\s*){3,}|(?:-\s*){3,}|(?:_\s*){3,})$")
RESERVED_CLOSE_SUFFIX = re.compile(r" — closes: \?\d+$")
CLAIM = re.compile(
    r"(?:\b(?:verified|confirmed|validated|tested|proven)\b|"
    r"(?:已经验证|已验证|经验证|验证通过|已经确认|已确认|经确认|确认无误|"
    r"已经测试|已测试|经测试|测试通过|已经证明|已证明|经证明))",
    re.I,
)
COVERAGE = re.compile(
    r"(?:\b(?:all|each|every|cases?|inputs?|samples?|bounds?|boundaries|edges?|"
    r"random(?:ized)?|files?|modules?|sections?|lines?|scenarios?|environments?|"
    r"platforms?|datasets?|records?|routes?|commands?|branches?|ranges?|including|"
    r"through|up\s+to|Windows|Linux|macOS|Chrome|Firefox|Safari)\b|"
    r"\b(?:Python|Node(?:\.js)?)\s*\d|\bn\s*[<≤=]\s*\d|"
    r"(?:覆盖|全部|所有|每个|每条|各条|每项|逐一|逐条|边界|上下限|上限|下限|"
    r"输入|用例|文件|目录|模块|章节|区段|分段|行数|行号|场景|平台|环境|浏览器|"
    r"数据集|记录|路径|路由|命令|分支|范围|包括|包含|至多|至少|最多|最少|"
    r"随机|样本|样例|截至))",
    re.I,
)


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


def next_open_number(book):
    """Allocate an Open id that remains retired after its question closes."""
    numbers = []
    active = re.compile(r"^\?(\d+)\b")
    closed = re.compile(r" — closes: \?(\d+)$")
    for row in book["Open"]:
        match = active.match(row)
        if match:
            numbers.append(int(match.group(1)))
    for row in book["Verified"]:
        match = closed.search(row)
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
    open_rows = book["Open"]
    for row in open_rows[:2]:
        print("Open:     " + row)
    if len(open_rows) > 2:
        print("          (+%d more in the ledger — run `resume` for the full list)" % (len(open_rows) - 2))
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
    try:
        premise, inv = load_anchors()
    except AnchorLoadError as exc:
        print("CANNOT: %s." % exc)
        print(anchor_load_help())
        return False
    print(heading)
    print(premise)
    print()
    print_full_ledger(book)
    print()
    print("The invariants:")
    for n, text in enumerate(inv, 1):
        print("  %d. %s" % (n, text))
    print()
    print(
        "State the pass you are on in the inner or ledger register, and make `Next` "
        "name the first action back."
    )
    return True


def mode_seam(book):
    hist = read_history()
    gap = int(time.time()) - hist[-1]["t"] if hist else 0
    if gap > RESUME_GAP:
        if not print_reentry(
            book,
            "── j-space ─ seam (long gap: %d minutes since the last one)" % (gap // 60),
        ):
            return 2
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
        print("  " + SHIFTS)
    if not one(book, "Next"):
        print()
        print("`Next` is never empty. A ledger with no next action is a ledger you have stopped using.")
    return 0


def mode_resume(book):
    if not print_reentry(book, "── j-space ─ resume"):
        return 2
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
                    "Mentioning is not loading.",
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
                changed = changed or displaced != args.core
    elif args.core_slot is not None:
        refused.append(("--core-slot requires --core.", '--core "name — defining fact" --core-slot 1'))

    try:
        inv = load_anchors()[1]
    except AnchorLoadError as exc:
        print("CANNOT: %s." % exc)
        print(anchor_load_help())
        return 2

    check_recorded = False
    check_index = None
    if args.check:
        if not args.by:
            refused.append(
                (
                    inv[4],
                    '--check "what now holds" --by "what verified it"',
                )
            )
        elif RESERVED_CLOSE_SUFFIX.search(args.by):
            refused.append(
                (
                    "checkpoint evidence ends with the controller-reserved closure suffix.",
                    "remove `— closes: ?NN`; the controller records it only after --close succeeds",
                )
            )
        elif not COVERAGE.search(args.by):
            refused.append(
                (
                    inv[5],
                    '--by "brute force, n ≤ 6, including empty and maximum"',
                )
            )
        else:
            num = next_number(book["Verified"], "✓")
            book["Verified"].append(
                "✓%02d %s — verified by: %s" % (num, args.check, args.by)
            )
            check_index = len(book["Verified"]) - 1
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
            num = next_open_number(book)
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
                ("no open question numbered %d." % args.close, "run `resume` to see the full list")
            )
        elif not check_recorded:
            refused.append(
                (
                    "An `Open` entry closes only against a recorded checkpoint, and its number is never reused.",
                    '--close %d --check "what now holds" --by "verifier and coverage"' % args.close,
                )
            )
        else:
            rows.pop(idx)
            book["Verified"][check_index] += " — closes: " + target
            changed = True

    if args.next:
        book["Next"] = [args.next]
        changed = True

    if changed:
        problem = write_ledger(book)
        if problem:
            print("CANNOT: cannot write the ledger — " + problem)
            print("  No filesystem? The ledger lives in the conversation. Restate the five lines")
            print("  at each seam. Same discipline, different medium.")
            return 2
    for message, fix in refused:
        declined(message, fix)
    if refused:
        if changed:
            print("  (everything else in this call was recorded.)")
        return 2
    print_ledger(book)
    return 0


def markdown_fenced_lines(lines):
    """Return zero-based lines inside Markdown fenced code blocks, including their fences."""
    fenced = set()
    fence_char = None
    fence_size = 0
    for index, line in enumerate(lines):
        if fence_char is None:
            match = MARKDOWN_FENCE.match(line)
            if not match:
                continue
            token = match.group(1)
            fence_char = token[0]
            fence_size = len(token)
            fenced.add(index)
            continue

        fenced.add(index)
        closing = r"^\s{0,3}%s{%d,}\s*$" % (re.escape(fence_char), fence_size)
        if re.match(closing, line):
            fence_char = None
            fence_size = 0
    return fenced


def markdown_structural_lines(lines):
    """Return zero-based lines whose words are Markdown structure, not prose claims."""
    structural = markdown_fenced_lines(lines)
    for index, line in enumerate(lines):
        if index in structural:
            continue
        if MARKDOWN_HEADING.match(line) or THEMATIC_BREAK.match(line):
            structural.add(index)
        if (
            index + 1 < len(lines)
            and index + 1 not in structural
            and line.strip()
            and SETEXT_UNDERLINE.match(lines[index + 1])
        ):
            structural.update((index, index + 1))
        if TABLE_DELIMITER.match(line):
            start = index - 1
            while (
                start >= 0
                and start not in structural
                and lines[start].strip()
                and "|" in lines[start]
            ):
                structural.add(start)
                start -= 1
            end = index
            while (
                end < len(lines)
                and end not in structural
                and lines[end].strip()
                and "|" in lines[end]
            ):
                structural.add(end)
                end += 1
    return structural


def claim_without_coverage(lines):
    """Return the first uncovered claim line, joining soft-wrapped paragraphs."""
    structural = markdown_structural_lines(lines)

    paragraph = []

    def flush():
        if not paragraph:
            return None
        joined = " ".join(line.strip() for _, line in paragraph)
        if not CLAIM.search(joined) or COVERAGE.search(joined):
            return None
        return next(number for number, line in paragraph if CLAIM.search(line))

    for index, line in enumerate(lines):
        stripped = line.strip()
        if (
            not stripped
            or index in structural
        ):
            uncovered = flush()
            if uncovered:
                return uncovered
            paragraph = []
            continue

        if MARKDOWN_LIST_ITEM.match(line):
            uncovered = flush()
            if uncovered:
                return uncovered
            paragraph = [(index + 1, line)]
        elif "|" in line:
            uncovered = flush()
            if uncovered:
                return uncovered
            paragraph = [(index + 1, line)]
            uncovered = flush()
            if uncovered:
                return uncovered
            paragraph = []
        else:
            paragraph.append((index + 1, line))

    return flush()


def mode_ship(text):
    """Report inner-register leakage in outgoing text.

    A report, not a gate: it exits 0 whether or not it finds anything, because
    the caller asked it to look and it looked.
    """
    try:
        inv = load_anchors()[1]
    except AnchorLoadError as exc:
        print("CANNOT: %s." % exc)
        print(anchor_load_help())
        return 2

    findings = []
    lines = text.splitlines()
    structural = markdown_structural_lines(lines)
    prose = "\n".join(line for index, line in enumerate(lines) if index not in structural)

    leaked = sorted({s for s in INNER_ONLY if s in prose})
    if leaked:
        findings.append(inv[6] + " Found: " + " ".join(leaked))

    hot = sorted({m for m in MARKERS if m.lower() in prose.lower()})
    if hot:
        findings.append("state markers in outgoing text: " + ", ".join(hot))

    uncovered = claim_without_coverage(lines)
    if uncovered:
        findings.append("line %d: %s" % (uncovered, inv[5]))

    run = 1
    for index, (a, b) in enumerate(zip(lines, lines[1:])):
        if index in structural or index + 1 in structural:
            run = 1
            continue
        run = run + 1 if a.strip() and a.strip() == b.strip() else 1
        if run >= 3:
            findings.append("repetition loop: a line repeats three times or more")
            break

    for index, line in enumerate(lines):
        if index not in structural and re.search(r"([.…\-'])\1{20,}", line):
            findings.append("repetition loop: a character run of 20 or more")
            break

    if not findings:
        print("clean — the outgoing register holds.")
        return 0
    print("── j-space ─ ship")
    for f in findings[:7]:
        print("· " + f)
    print()
    print("Expand the whole span into clean language before it ships. The switch is total, never cosmetic.")
    return 0


def decode_outgoing(data, label):
    """Decode outgoing bytes without silently accepting an unknown encoding."""
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
        return None, "%s (cannot decode safely: %s)" % (label, exc)
    return text, None


def read_outgoing(path):
    """Read and decode outgoing text from a file."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return None, "%s (%s)" % (path, exc.strerror or "unreadable")
    return decode_outgoing(data, path)


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
            try:
                stream = getattr(sys.stdin, "buffer", None)
                data = stream.read() if stream is not None else sys.stdin.read().encode("utf-8")
            except OSError as exc:
                text, problem = None, "stdin (%s)" % (exc.strerror or "unreadable")
            else:
                text, problem = decode_outgoing(data, "stdin")
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
