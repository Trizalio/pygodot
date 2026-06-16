from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pygodot.errors import GodotCliError
from pygodot.godot_cli import GodotRunResult, check_project_run


class GodotCliTests(unittest.TestCase):
    def test_run_result_diagnostic_summary_includes_separate_tails(self) -> None:
        result = GodotRunResult(
            command=["godot", "--headless"],
            returncode=7,
            stdout="stdout one\nstdout two\nstdout three\n",
            stderr="stderr one\nstderr two\n",
            log_text="log one\nlog two\nlog three\n",
        )

        summary = result.diagnostic_summary(tail_lines=2)

        self.assertIn("command: ['godot', '--headless']", summary)
        self.assertIn("return code: 7", summary)
        self.assertIn("stdout tail:\nstdout two\nstdout three", summary)
        self.assertIn("stderr tail:\nstderr one\nstderr two", summary)
        self.assertIn("Godot log tail:\nlog two\nlog three", summary)

    def test_check_project_run_failure_includes_command_returncode_and_output_tails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "pygodot_check_run.log").write_text(
                "log first\nlog second\nlog third\n",
                encoding="utf-8",
            )

            with patch("pygodot.godot_cli.subprocess.run") as run:
                run.return_value = subprocess.CompletedProcess(
                    args=[],
                    returncode=2,
                    stdout="stdout first\nstdout second\n",
                    stderr="stderr first\nstderr second\n",
                )

                with self.assertRaises(GodotCliError) as raised:
                    check_project_run(
                        project_dir,
                        godot_bin="godot-test",
                        scene="res://scenes/main.tscn",
                        frames=4,
                    )

            message = str(raised.exception)
            self.assertIn("Godot command failed.", message)
            self.assertIn("command: ['godot-test'", message)
            self.assertIn("return code: 2", message)
            self.assertIn("stdout tail:\nstdout first\nstdout second", message)
            self.assertIn("stderr tail:\nstderr first\nstderr second", message)
            self.assertIn("Godot log tail:\nlog first\nlog second\nlog third", message)

    def test_check_project_run_godot_error_marker_includes_log_tail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "pygodot_check_run.log").write_text(
                "Loading scene\nSCRIPT ERROR: bad script\n",
                encoding="utf-8",
            )

            with patch("pygodot.godot_cli.subprocess.run") as run:
                run.return_value = subprocess.CompletedProcess(
                    args=[],
                    returncode=0,
                    stdout="",
                    stderr="",
                )

                with self.assertRaises(GodotCliError) as raised:
                    check_project_run(project_dir, godot_bin="godot-test", frames=3)

            message = str(raised.exception)
            self.assertIn("Godot check run reported errors.", message)
            self.assertIn("return code: 0", message)
            self.assertIn("stdout tail:\n(empty)", message)
            self.assertIn("stderr tail:\n(empty)", message)
            self.assertIn("Godot log tail:\nLoading scene\nSCRIPT ERROR: bad script", message)


if __name__ == "__main__":
    unittest.main()
