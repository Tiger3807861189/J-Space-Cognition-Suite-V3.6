"""Regression tests for the optional J-Space runtime controller."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / "j-space" / "scripts" / "jspace.py"


class JSpaceControllerTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.workspace.cleanup()

    @property
    def ledger(self):
        return Path(self.workspace.name) / ".jspace" / "WORKSPACE.md"

    @property
    def history(self):
        return Path(self.workspace.name) / ".jspace" / "history.json"

    def run_controller(self, *args, stdin=None):
        return subprocess.run(
            [sys.executable, str(CONTROLLER), *args],
            cwd=self.workspace.name,
            input=stdin,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def open_ledger(self, goal="Ship verified output", next_action="Inspect inputs"):
        result = self.run_controller(
            "note", "--goal", goal, "--next", next_action
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_documented_loop_lifecycle(self):
        self.open_ledger()
        for entry in (
            "constraints — preserve public behavior",
            "evidence — cover all affected files",
        ):
            result = self.run_controller("note", "--core", entry)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        swap = self.run_controller(
            "note",
            "--core",
            "delivery — keep the outer register clean",
            "--core-slot",
            "1",
        )
        self.assertEqual(swap.returncode, 0, swap.stdout + swap.stderr)

        opened = self.run_controller(
            "note",
            "--open",
            "Does the parser preserve state?",
            "--settled-by",
            "controller tests over all ledger sections",
        )
        self.assertEqual(opened.returncode, 0, opened.stdout + opened.stderr)

        refused = self.run_controller("note", "--close", "1")
        self.assertEqual(refused.returncode, 2)
        self.assertIn("requires a checkpoint", refused.stdout)

        closed = self.run_controller(
            "note",
            "--close",
            "1",
            "--check",
            "the parser preserves state",
            "--by",
            "unittest over all ledger sections and edge inputs",
            "--next",
            "Prepare delivery",
        )
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)

        seam = self.run_controller("seam")
        self.assertEqual(seam.returncode, 0, seam.stdout + seam.stderr)
        self.assertIn("Goal:     Ship verified output", seam.stdout)
        self.assertIn("Next:     Prepare delivery", seam.stdout)

        resume = self.run_controller("resume")
        self.assertEqual(resume.returncode, 0, resume.stdout + resume.stderr)
        self.assertIn("Not working if:", resume.stdout)
        self.assertIn("[live] delivery", resume.stdout)

    def test_long_gap_prints_full_reentry(self):
        self.open_ledger()
        self.history.parent.mkdir(exist_ok=True)
        self.history.write_text(
            json.dumps(
                [
                    {
                        "t": int(time.time()) - 3601,
                        "next": "Inspect inputs",
                        "verified": 0,
                        "open": 0,
                    }
                ]
            ),
            encoding="utf-8",
        )

        result = self.run_controller("seam")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("long gap", result.stdout)
        self.assertIn("Not working if:", result.stdout)

    def test_scalar_values_round_trip_and_section_heading_is_refused(self):
        self.open_ledger(goal="- preserve leading punctuation")
        seam = self.run_controller("seam")
        self.assertEqual(seam.returncode, 0, seam.stdout + seam.stderr)
        self.assertIn("Goal:     - preserve leading punctuation", seam.stdout)

        refused = self.run_controller("note", "--goal", "## Verified")
        self.assertEqual(refused.returncode, 2)
        self.assertIn("must not begin with a ledger section heading", refused.stdout)

        unchanged = self.run_controller("seam")
        self.assertEqual(unchanged.returncode, 0, unchanged.stdout + unchanged.stderr)
        self.assertIn("Goal:     - preserve leading punctuation", unchanged.stdout)

    def test_unreadable_ledger_is_declined_without_traceback(self):
        self.ledger.parent.mkdir()
        self.ledger.write_bytes(b"\xff\xfe\x00\x80")

        result = self.run_controller("seam")
        self.assertEqual(result.returncode, 2)
        self.assertIn("ledger was unreadable", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_ship_skips_section_headings_but_flags_claims(self):
        heading = self.run_controller("ship", "-", stdin="## Verified\n")
        self.assertEqual(heading.returncode, 0, heading.stdout + heading.stderr)
        self.assertIn("clean", heading.stdout)

        claimed = self.run_controller(
            "ship", "-", stdin="## Verified\nResult verified by intuition\n"
        )
        self.assertEqual(claimed.returncode, 0, claimed.stdout + claimed.stderr)
        self.assertIn('"verified" with no stated coverage', claimed.stdout)

    def test_chinese_coverage_is_accepted(self):
        self.open_ledger()
        accepted = self.run_controller(
            "note",
            "--check",
            "结构核对完成",
            "--by",
            "直接取证, 覆盖: 所有文件与目录",
        )
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        self.assertIn("✓01", accepted.stdout)

        refused = self.run_controller(
            "note",
            "--check",
            "结构核对完成",
            "--by",
            "grep 输出",
        )
        self.assertEqual(refused.returncode, 2)
        self.assertIn("without stated coverage", refused.stdout)

    def test_history_recovery_and_register_inspection(self):
        self.open_ledger()
        self.history.write_text("{}", encoding="utf-8")
        seam = self.run_controller("seam")
        self.assertEqual(seam.returncode, 0, seam.stdout + seam.stderr)
        self.assertIn("invalid shape", seam.stderr)

        clean = self.run_controller("ship", "-", stdin="Verified all files by full scan.")
        self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)
        self.assertIn("clean", clean.stdout)

        outgoing = Path(self.workspace.name) / "outgoing.txt"
        outgoing.write_text("I see meltdown ⇒ retry", encoding="utf-16")
        reported = self.run_controller("ship", os.fspath(outgoing))
        self.assertEqual(reported.returncode, 0, reported.stdout + reported.stderr)
        self.assertIn("inner-register notation", reported.stdout)
        self.assertIn("state markers", reported.stdout)

        outgoing.write_bytes(b"\x81\x82\x83")
        declined = self.run_controller("ship", os.fspath(outgoing))
        self.assertEqual(declined.returncode, 2)
        self.assertIn("cannot decode safely", declined.stdout)


if __name__ == "__main__":
    unittest.main()
