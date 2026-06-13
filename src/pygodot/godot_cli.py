"""Godot binary invocation helpers."""

from dataclasses import dataclass
from pathlib import Path
import subprocess

from pygodot.errors import GodotCliError


@dataclass(slots=True, frozen=True)
class GodotRunResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    log_text: str = ""


def run_project(project_dir: Path, *, godot_bin: str = "godot", scene: str | None = None) -> None:
    command = [godot_bin, "--path", str(project_dir)]
    if scene is not None:
        command.extend(["--scene", scene])
    _run(command)


def import_project(project_dir: Path, *, godot_bin: str = "godot") -> None:
    _run([godot_bin, "--headless", "--path", str(project_dir), "--import"])


def check_project_run(
    project_dir: Path,
    *,
    godot_bin: str = "godot",
    scene: str | None = None,
    frames: int = 20,
    log_file: str = "pygodot_check_run.log",
) -> GodotRunResult:
    command = [
        godot_bin,
        "--headless",
        "--verbose",
        "--path",
        str(project_dir),
    ]
    if scene is not None:
        command.extend(["--scene", scene])
    command.extend(["--quit-after", str(frames), "--log-file", log_file])

    result = _run_capture(command, project_dir=project_dir, log_file=log_file)
    combined_output = "\n".join([result.stdout, result.stderr, result.log_text])
    if _has_godot_error(combined_output):
        raise GodotCliError(
            f"Godot check run reported errors: command={command!r}\n"
            f"{_tail(combined_output)}"
        )
    return result


def _run(command: list[str]) -> None:
    try:
        subprocess.run(command, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise GodotCliError(f"Godot command failed: {command!r}") from exc


def _run_capture(command: list[str], *, project_dir: Path, log_file: str) -> GodotRunResult:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise GodotCliError(f"Godot command failed: {command!r}") from exc

    log_text = _read_log(project_dir, log_file)
    result = GodotRunResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        log_text=log_text,
    )
    if completed.returncode != 0:
        combined_output = "\n".join([completed.stdout, completed.stderr, log_text])
        raise GodotCliError(
            f"Godot command failed with exit code {completed.returncode}: command={command!r}\n"
            f"{_tail(combined_output)}"
        )
    return result


def _read_log(project_dir: Path, log_file: str) -> str:
    path = Path(log_file)
    if not path.is_absolute():
        path = project_dir / path
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _has_godot_error(output: str) -> bool:
    error_markers = (
        "SCRIPT ERROR:",
        "ERROR:",
        "Parse Error:",
        "Failed to load script",
    )
    return any(marker in output for marker in error_markers)


def _tail(output: str, *, lines: int = 40) -> str:
    return "\n".join(output.splitlines()[-lines:])
