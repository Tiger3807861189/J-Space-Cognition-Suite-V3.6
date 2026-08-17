#!/usr/bin/env python3
"""verify_suite — authoring-time integrity check for the J-Space skill.

Run from anywhere:  python3 <skill-root>/scripts/verify_suite.py

Checks, in order of how badly each one breaks the suite:

  1. Exactly one file in the tree carries skill frontmatter. More than one and the
     harness registers more than one command.
  2. The J-Space Premise is byte-identical in SKILL.md and in all nine modules.
     Verbatim recurrence is the repetition schedule; a paraphrase silently
     disables it.
  3. Every module and reference is present and reachable from the entry file.
  4. No version talk anywhere in the skill text. The text addresses the model,
     never the maintainer.
  5. Every module carries a drill with a pass and a fail criterion.
  6. All nine modules carry the same backbone sections, in the same order.
     Extra sections between them are allowed and expected — that is where a
     module says what it is rather than what to do. What must not vary is the
     spine, so every module is navigable the same way.

Exit 0 clean, 1 with findings. Standard library only.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MODULES = [
    "introspection",
    "directed-focus",
    "deep-reasoning",
    "broadcast",
    "capacity",
    "self-monitoring",
    "shorthand",
    "markers",
    "empirics",
]
REFERENCES = ["j-space-science", "induction-playbook", "exemplars", "problem-model"]

PREMISE_HEAD = "You do not only produce words; you also think them before"
PREMISE_TAIL = "decodable on demand."

VERSION_TALK = re.compile(
    r"\b(version\s+v?\d+(?:\.\d+)*|v\d+(?:\.\d+)+|old version|new version|"
    r"previous version|earlier version|compared to|now adds|newly added|this release|"
    r"changelog|upgrade[ds]? from)",
    re.I,
)
FRONTMATTER_KEYS = {"name", "description"}

findings = []


def fail(where, what):
    findings.append("%s: %s" % (where, what))


def read(path):
    return open(path, encoding="utf-8").read()


def extract_premise(text, where):
    start = text.find(PREMISE_HEAD)
    if start < 0:
        fail(where, "the premise is missing")
        return None
    end = text.find(PREMISE_TAIL, start)
    if end < 0:
        fail(where, "the premise is truncated")
        return None
    return text[start : end + len(PREMISE_TAIL)]


def main():
    """Run every check, print the findings, and return the exit code."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass

    entry = os.path.join(ROOT, "SKILL.md")
    if not os.path.exists(entry):
        print("SKILL.md not found at " + entry)
        return 1

    # 1 — exactly one frontmatter in the tree
    fronted = []
    for base, _, names in os.walk(ROOT):
        for name in names:
            if not name.endswith(".md"):
                continue
            path = os.path.join(base, name)
            if read(path).startswith("---\n"):
                fronted.append(os.path.relpath(path, ROOT))
    if fronted != ["SKILL.md"]:
        fail("tree", "frontmatter must appear only in SKILL.md, found: %s" % ", ".join(sorted(fronted)))

    # 2 & 3 & 5 — presence, premise, drills
    entry_text = read(entry)
    if entry_text.startswith("---\n"):
        frontmatter = entry_text.split("---\n", 2)[1]
        keys = {
            line.split(":", 1)[0].strip()
            for line in frontmatter.splitlines()
            if ":" in line and not line.lstrip().startswith("#")
        }
        unsupported = sorted(keys - FRONTMATTER_KEYS)
        if unsupported:
            fail("SKILL.md", "unsupported frontmatter keys: %s" % ", ".join(unsupported))
    canonical = extract_premise(entry_text, "SKILL.md")

    for name in MODULES:
        rel = os.path.join("modules", name + ".md")
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            fail(rel, "missing")
            continue
        text = read(path)
        block = extract_premise(text, rel)
        if canonical and block and block != canonical:
            fail(rel, "the premise differs from SKILL.md — it must be byte-identical")
        if "## Drill" not in text:
            fail(rel, "no drill")
        else:
            drill = text.split("## Drill", 1)[1].split("## ", 1)[0]
            if "**Pass:**" not in drill or "**Fail:**" not in drill:
                fail(rel, "the drill has no pass/fail criterion")
        if rel not in entry_text and (name + ".md") not in entry_text:
            fail(rel, "not routed to from SKILL.md")

    for name in REFERENCES:
        rel = os.path.join("references", name + ".md")
        if not os.path.exists(os.path.join(ROOT, rel)):
            fail(rel, "missing")
        elif rel.replace(os.sep, "/") not in entry_text and (name + ".md") not in entry_text:
            fail(rel, "not reachable from SKILL.md")

    # 6 — the same backbone, in the same order, in every module
    backbone = [
        "## The J-Space Premise",
        "## Grounding",
        "## Drills",
        "## Protocol",
        "## Failure modes",
        "## Hand-off",
    ]
    for name in MODULES:
        rel = os.path.join("modules", name + ".md")
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        heads = [l.strip() for l in read(path).splitlines() if l.startswith("## ")]
        missing = [h for h in backbone if h not in heads]
        if missing:
            fail(rel, "backbone sections missing: %s" % ", ".join(missing))
            continue
        order = [heads.index(h) for h in backbone]
        if order != sorted(order):
            fail(rel, "backbone sections are out of order")

    # 4 — no version talk in anything the model reads
    for base, _, names in os.walk(ROOT):
        for name in sorted(names):
            if not name.endswith(".md"):
                continue
            path = os.path.join(base, name)
            rel = os.path.relpath(path, ROOT)
            for n, line in enumerate(read(path).splitlines(), 1):
                hit = VERSION_TALK.search(line)
                if hit:
                    fail(rel, 'line %d: version talk "%s"' % (n, hit.group(0)))

    if findings:
        print("verify_suite: %d finding(s)" % len(findings))
        for f in findings:
            print("  ✗ " + f)
        return 1
    print("verify_suite: clean — one entry, one premise, nine modules, no version talk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
