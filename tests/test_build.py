from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pygodot import Game, Label, Node2D, Scene, Script, Vec2, texture
from pygodot.errors import BuildError
from pygodot.godot_cli import check_project_run
from tests.helpers import _read_generated_files, make_scene


class BuildTests(unittest.TestCase):
    def test_game_build_writes_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(make_scene())

            result = game.build()

            self.assertEqual(result.project_dir, build_dir)
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [".pygodot/manifest.json", "project.godot", "scenes/main.tscn", "scripts/main.gd"],
            )
            self.assertTrue((build_dir / "project.godot").exists())
            self.assertTrue((build_dir / "scenes" / "main.tscn").exists())
            self.assertTrue((build_dir / "scripts" / "main.gd").exists())
            self.assertEqual(result.manifest_path, build_dir / ".pygodot" / "manifest.json")

    def test_game_build_output_is_stable_across_repeated_builds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(make_scene())

            game.build()
            first = _read_generated_files(build_dir)
            game.build()
            second = _read_generated_files(build_dir)

            self.assertEqual(second, first)

    def test_game_build_does_not_write_referenced_manual_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manual_script = Path(tmp) / "manual" / "player.gd"
            manual_script.parent.mkdir(parents=True)
            manual_script.write_text("extends Node2D\n", encoding="utf-8")
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.reference(
                            "res://manual/player.gd",
                            extends="Node2D",
                        ),
                    ),
                )
            )

            result = game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [".pygodot/manifest.json", "project.godot", "scenes/main.tscn"],
            )
            self.assertEqual(result.generated_scripts, [])
            self.assertFalse((build_dir / "manual" / "player.gd").exists())
            self.assertIn(
                'path="res://manual/player.gd"',
                (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8"),
            )

    def test_game_build_writes_generated_script_from_source_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            source_script = source_root / "scripts" / "player.gd"
            source_script.parent.mkdir(parents=True)
            source_script.write_text(
                "func _ready() -> void:\n    $Label.text = \"Loaded from file\"\n",
                encoding="utf-8",
            )
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=source_root,
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_file(
                            source="scripts/player.gd",
                            path="res://scripts/player.gd",
                            extends="Node2D",
                        ),
                    ),
                )
            )

            result = game.build()

            generated_script = build_dir / "scripts" / "player.gd"
            self.assertEqual(result.generated_scripts, [generated_script])
            self.assertEqual(
                generated_script.read_text(encoding="utf-8"),
                """# Generated by pygodot. Do not edit by hand.

extends Node2D

func _ready() -> void:
    $Label.text = "Loaded from file"
""",
            )

    def test_game_build_writes_generated_script_from_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            template = source_root / "scripts" / "player.gd.tmpl"
            template.parent.mkdir(parents=True)
            template.write_text(
                "const SPEED := $speed\n\nfunc _ready() -> void:\n    $$Label.text = \"$title\"\n",
                encoding="utf-8",
            )
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=source_root,
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_template(
                            source="scripts/player.gd.tmpl",
                            path="res://scripts/player.gd",
                            extends="Node2D",
                            context={"speed": 300, "title": "Templated"},
                        ),
                    ),
                )
            )

            result = game.build()

            generated_script = build_dir / "scripts" / "player.gd"
            self.assertEqual(result.generated_scripts, [generated_script])
            self.assertEqual(
                generated_script.read_text(encoding="utf-8"),
                """# Generated by pygodot. Do not edit by hand.

extends Node2D

const SPEED := 300

func _ready() -> void:
    $Label.text = "Templated"
""",
            )

    def test_game_build_rejects_missing_generated_script_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_file(
                            source="scripts/missing.gd",
                            path="res://scripts/main.gd",
                            extends="Node2D",
                        ),
                    ),
                )
            )

            with self.assertRaisesRegex(BuildError, "source file does not exist"):
                game.build()

    def test_game_build_rejects_missing_generated_script_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_template(
                            source="scripts/missing.gd.tmpl",
                            path="res://scripts/main.gd",
                            extends="Node2D",
                            context={},
                        ),
                    ),
                )
            )

            with self.assertRaisesRegex(BuildError, "template file does not exist"):
                game.build()

    def test_game_build_rejects_missing_script_template_variable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            template = source_root / "scripts" / "player.gd.tmpl"
            template.parent.mkdir(parents=True)
            template.write_text("const SPEED := $speed\nconst NAME := $name\n", encoding="utf-8")
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=source_root,
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_template(
                            source="scripts/player.gd.tmpl",
                            path="res://scripts/main.gd",
                            extends="Node2D",
                            context={"speed": 300},
                        ),
                    ),
                )
            )

            with self.assertRaisesRegex(BuildError, "key='name'"):
                game.build()

    def test_game_build_rejects_unsafe_generated_script_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_file(
                            source="../outside.gd",
                            path="res://scripts/main.gd",
                            extends="Node2D",
                        ),
                    ),
                )
            )

            with self.assertRaisesRegex(BuildError, "cannot leave source root"):
                game.build()

    def test_game_build_rejects_unsafe_generated_script_template_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_template(
                            source="../outside.gd.tmpl",
                            path="res://scripts/main.gd",
                            extends="Node2D",
                            context={},
                        ),
                    ),
                )
            )

            with self.assertRaisesRegex(BuildError, "cannot leave source root"):
                game.build()

    def test_game_build_copies_existing_external_assets_and_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            build_dir = Path(tmp) / "godot_project"
            asset_path = source_root / "assets" / "icon.svg"
            asset_path.parent.mkdir(parents=True)
            asset_path.write_text("<svg></svg>\n", encoding="utf-8")

            game = Game(
                name="GeneratedGame",
                source_root=source_root,
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        icon=texture("res://assets/icon.svg"),
                    ),
                )
            )

            result = game.build()

            copied_asset = build_dir / "assets" / "icon.svg"
            self.assertEqual(result.copied_resources, [copied_asset])
            self.assertEqual(copied_asset.read_text(encoding="utf-8"), "<svg></svg>\n")

            manifest_path = build_dir / ".pygodot" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(result.manifest_path, manifest_path)
            self.assertIn(".pygodot/manifest.json", manifest["generated_files"])
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": True,
                        "id": "Texture2D_assets_icon_svg",
                        "path": "res://assets/icon.svg",
                        "type": "Texture2D",
                    }
                ],
            )

    def test_game_build_rejects_unsafe_res_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://../main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://../main.tscn",
                    root=Node2D("Main"),
                )
            )

            with self.assertRaisesRegex(
                BuildError,
                "Unsafe res:// path cannot leave project root: path='res://../main.tscn'",
            ):
                game.build()

    def test_check_project_run_builds_headless_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "pygodot_check_run.log").write_text(
                "Loading resource: res://scenes/main.tscn\n",
                encoding="utf-8",
            )

            with patch("pygodot.godot_cli.subprocess.run") as run:
                run.return_value = subprocess.CompletedProcess(
                    args=[],
                    returncode=0,
                    stdout="fake godot ok\n",
                    stderr="",
                )

                result = check_project_run(
                    project_dir,
                    godot_bin="godot",
                    scene="res://scenes/main.tscn",
                    frames=3,
                )

            self.assertEqual(result.returncode, 0)
            self.assertIn("--headless", result.command)
            self.assertIn("--scene", result.command)
            self.assertIn("res://scenes/main.tscn", result.command)
            self.assertIn("--quit-after", result.command)
            self.assertIn("3", result.command)
            self.assertIn("fake godot ok", result.stdout)
            self.assertIn("Loading resource", result.log_text)
