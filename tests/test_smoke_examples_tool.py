from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


def _load_smoke_module():
    path = Path(__file__).parents[1] / "tools" / "smoke_examples.py"
    spec = importlib.util.spec_from_file_location("pygodot_smoke_examples_tool", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load smoke tool from {path}.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SmokeExamplesToolTests(unittest.TestCase):
    def test_parse_examples_rejects_unknown_names(self) -> None:
        smoke = _load_smoke_module()

        with self.assertRaisesRegex(SystemExit, "Unknown example"):
            smoke._parse_examples("minimal,missing")

    def test_main_skips_when_godot_is_missing_by_default(self) -> None:
        smoke = _load_smoke_module()

        with (
            patch.object(smoke, "_godot_available", return_value=False),
            redirect_stdout(io.StringIO()),
        ):
            result = smoke.main(["--examples", "minimal"])

        self.assertEqual(result, 0)

    def test_main_fails_when_godot_is_required_and_missing(self) -> None:
        smoke = _load_smoke_module()

        with (
            patch.object(smoke, "_godot_available", return_value=False),
            redirect_stderr(io.StringIO()),
        ):
            result = smoke.main(["--examples", "minimal", "--require-godot"])

        self.assertEqual(result, 1)

    def test_run_examples_calls_check_run_for_each_example(self) -> None:
        smoke = _load_smoke_module()
        fake_game = _FakeGame()

        with patch.object(smoke, "_load_game", return_value=fake_game):
            results = smoke.run_examples(("minimal", "physics"), frames=7, godot_bin="godot-test")

        self.assertEqual([result.status for result in results], ["pass", "pass"])
        self.assertEqual(fake_game.godot_bin, "godot-test")
        self.assertEqual(fake_game.frames, [7, 7])

    def test_run_examples_preserves_failure_diagnostics(self) -> None:
        smoke = _load_smoke_module()
        fake_game = _FailingGame()

        with patch.object(smoke, "_load_game", return_value=fake_game):
            results = smoke.run_examples(("minimal",), frames=7, godot_bin="godot-test")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        self.assertIn("command: ['godot-test']", results[0].detail)
        self.assertIn("return code: 1", results[0].detail)
        self.assertIn("stderr tail:", results[0].detail)


class _FakeGame:
    def __init__(self) -> None:
        self.godot_bin = "godot"
        self.frames: list[int] = []

    def check_run(self, *, frames: int):
        self.frames.append(frames)
        return _FakeRunResult()


class _FakeRunResult:
    returncode = 0
    log_text = "ok\n"


class _FailingGame:
    godot_bin = "godot"

    def check_run(self, *, frames: int):
        raise RuntimeError(
            "Godot command failed.\n"
            "command: ['godot-test']\n"
            "return code: 1\n"
            "stderr tail:\nboom\n"
        )


if __name__ == "__main__":
    unittest.main()
