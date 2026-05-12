import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SAVE_SUMMARY = REPO_ROOT / "scripts" / "save_summary.py"


class SaveSummaryScriptTests(unittest.TestCase):
    def test_writes_stdin_to_summary_md(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            body = "# Answer\n\nLine two with **markdown**.\n"
            proc = subprocess.run(
                [sys.executable, str(SAVE_SUMMARY), str(work)],
                input=body,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = (work / "summary.md").read_text(encoding="utf-8")
            self.assertEqual(out, body)

    def test_appends_newline_when_missing(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            proc = subprocess.run(
                [sys.executable, str(SAVE_SUMMARY), str(work)],
                input="no trailing newline",
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual((work / "summary.md").read_text(encoding="utf-8"), "no trailing newline\n")

    def test_usage_error_exits_nonzero(self):
        proc = subprocess.run(
            [sys.executable, str(SAVE_SUMMARY)],
            input="",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
