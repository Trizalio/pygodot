from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the generated LD49 pygodot build output.")
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path("ld49_pygodot/build/godot_project"),
        help="Generated Godot project directory to validate.",
    )
    args = parser.parse_args(argv)

    from ld49_pygodot.validation import validate_build

    issues = validate_build(args.project_dir)
    if issues:
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print(f"LD49 pygodot validation passed: {args.project_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
