from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


class ExternalProjectBuildTests(unittest.TestCase):
    def test_installed_package_builds_external_project(self) -> None:
        repo_root = Path(__file__).parents[1].resolve()
        with tempfile.TemporaryDirectory(prefix="pygodot_external_") as tmp:
            temp_root = Path(tmp).resolve()
            project_dir = temp_root / "my_game"
            project_dir.mkdir()
            self.assertFalse(_is_relative_to(project_dir, repo_root))

            env = os.environ.copy()
            env.pop("PYTHONPATH", None)

            import_check = subprocess.run(
                [sys.executable, "-c", "import pygodot"],
                cwd=project_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if import_check.returncode != 0:
                self.skipTest(
                    "pygodot is not installed for this interpreter; run "
                    "`python -m pip install -e .` to exercise the external-project smoke test"
                )

            (project_dir / "game.py").write_text(
                textwrap.dedent(
                    """
                    from pathlib import Path

                    from pygodot import Color, Game, Label, Node2D, Scene, Script, label_settings


                    source_root = Path(__file__).parent
                    title_settings = label_settings(
                        "res://ui/title_label_settings.tres",
                        font_size=24,
                        font_color=Color(0.9, 0.95, 1.0),
                    )
                    script = Script(
                        path="res://scripts/main.gd",
                        extends="Node2D",
                        body='''
                    func _ready() -> void:
                        $Title.text = "Built outside the repo"
                    ''',
                    )
                    game = Game(
                        name="ExternalGame",
                        source_root=source_root,
                        build_dir=source_root / "build" / "godot",
                        main_scene="res://scenes/main.tscn",
                    )
                    game.add_scene(
                        Scene(
                            path="res://scenes/main.tscn",
                            root=Node2D(
                                "Main",
                                script=script,
                                children=[
                                    Label(
                                        "Title",
                                        text="External project",
                                        label_settings=title_settings,
                                    )
                                ],
                            ),
                        )
                    )

                    if __name__ == "__main__":
                        game.build()
                    """
                ).lstrip(),
                encoding="utf-8",
            )

            _run(
                [sys.executable, "game.py"],
                cwd=project_dir,
                env=env,
            )

            build_dir = project_dir / "build" / "godot"
            self.assertTrue((build_dir / "project.godot").is_file())
            self.assertTrue((build_dir / "scenes" / "main.tscn").is_file())
            self.assertTrue((build_dir / "scripts" / "main.gd").is_file())
            self.assertTrue((build_dir / "ui" / "title_label_settings.tres").is_file())
            manifest_path = build_dir / ".pygodot" / "manifest.json"
            self.assertTrue(manifest_path.is_file())

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["generated_files"],
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/main.tscn",
                    "scripts/main.gd",
                    "ui/title_label_settings.tres",
                ],
            )
            self.assertEqual(manifest["generated_scenes"], ["scenes/main.tscn"])
            self.assertEqual(manifest["generated_scripts"], ["scripts/main.gd"])
            self.assertEqual(manifest["generated_resources"], ["ui/title_label_settings.tres"])
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": False,
                        "id": "LabelSettings_ui_title_label_settings_tres",
                        "ownership": "generated",
                        "path": "res://ui/title_label_settings.tres",
                        "type": "LabelSettings",
                    },
                    {
                        "copied": False,
                        "id": "Script_scripts_main_gd",
                        "ownership": "generated",
                        "path": "res://scripts/main.gd",
                        "type": "Script",
                    },
                ],
            )


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(
            "Command failed:\n"
            f"command={command!r}\n"
            f"cwd={cwd}\n"
            f"returncode={result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False
