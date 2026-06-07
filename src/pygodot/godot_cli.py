"""Godot binary invocation helpers."""

from pathlib import Path
import subprocess

from pygodot.errors import GodotCliError


def run_project(project_dir: Path, *, godot_bin: str = "godot", scene: str | None = None) -> None:
    command = [godot_bin, "--path", str(project_dir)]
    if scene is not None:
        command.append(scene)
    _run(command)


def import_project(project_dir: Path, *, godot_bin: str = "godot") -> None:
    _run([godot_bin, "--headless", "--path", str(project_dir), "--import"])


def _run(command: list[str]) -> None:
    try:
        subprocess.run(command, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise GodotCliError(f"Godot command failed: {command!r}") from exc
