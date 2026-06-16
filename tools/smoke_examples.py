from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


ALL_EXAMPLES = (
    "minimal",
    "pong",
    "snake",
    "resources",
    "instancing",
    "timer",
    "template_script",
    "audio",
    "font",
    "animation",
    "physics",
    "flappy",
    "generated_tres",
    "ui_panel",
    "mouse_input",
    "ld49_ui_shell",
    "ld49_scene_flow",
)


@dataclass(slots=True, frozen=True)
class SmokeResult:
    example: str
    status: str
    detail: str


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    examples = ALL_EXAMPLES if args.all else _parse_examples(args.examples)
    godot_bin = os.environ.get("GODOT_BIN", "godot")

    if not _godot_available(godot_bin):
        message = f"Godot binary not found: {godot_bin!r}."
        if args.require_godot:
            print(message, file=sys.stderr)
            return 1
        print(f"SKIP {len(examples)} example(s): {message}")
        return 0

    results = run_examples(examples, frames=args.frames, godot_bin=godot_bin)
    for result in results:
        print(f"{result.status.upper()} {result.example}: {result.detail}")

    failures = [result for result in results if result.status == "fail"]
    if failures:
        print(f"{len(failures)} smoke check(s) failed.", file=sys.stderr)
        return 1

    print(f"{len(results)} smoke check(s) passed.")
    return 0


def run_examples(
    examples: Sequence[str],
    *,
    frames: int,
    godot_bin: str,
) -> list[SmokeResult]:
    results: list[SmokeResult] = []
    for example in examples:
        try:
            game = _load_game(example)
            game.godot_bin = godot_bin
            result = game.check_run(frames=frames)
        except Exception as exc:
            results.append(SmokeResult(example=example, status="fail", detail=str(exc)))
            continue

        log_lines = len(result.log_text.splitlines())
        results.append(
            SmokeResult(
                example=example,
                status="pass",
                detail=f"returncode={result.returncode}, log_lines={log_lines}",
            )
        )
    return results


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run optional Godot smoke checks for examples.")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument(
        "--examples",
        help="Comma-separated example names, such as minimal,pong,physics.",
    )
    target.add_argument("--all", action="store_true", help="Run all known examples.")
    parser.add_argument("--frames", type=int, default=20, help="Frames to run each example.")
    parser.add_argument(
        "--require-godot",
        action="store_true",
        help="Fail instead of skipping when the Godot binary is unavailable.",
    )
    args = parser.parse_args(argv)
    if args.frames <= 0:
        parser.error("--frames must be positive.")
    return args


def _parse_examples(value: str | None) -> tuple[str, ...]:
    if value is None:
        return ()
    examples = tuple(part.strip() for part in value.split(",") if part.strip())
    if not examples:
        raise SystemExit("--examples must include at least one example name.")
    unknown = sorted(set(examples) - set(ALL_EXAMPLES))
    if unknown:
        raise SystemExit(f"Unknown example(s): {', '.join(unknown)}.")
    return examples


def _godot_available(godot_bin: str) -> bool:
    path = Path(godot_bin)
    if path.is_absolute() or path.parent != Path("."):
        return path.is_file()
    return shutil.which(godot_bin) is not None


def _load_game(example: str):
    path = REPO_ROOT / "examples" / example / "game.py"
    spec = importlib.util.spec_from_file_location(f"pygodot_smoke_{example}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load example module from {path}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.game


if __name__ == "__main__":
    raise SystemExit(main())
