from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from pygodot import Button, Game, Label, Node2D, Scene, Script, Vec2, signal


SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"


def make_scene() -> Scene:
    script = Script(
        path="res://scripts/main.gd",
        extends="Node2D",
        body="""
        var counter := 0

        func _on_start_pressed() -> void:
            counter += 1
        """,
    )
    return Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "Main",
            script=script,
            children=[
                Label("Title", text="Generated scene", position=(80, 60)),
                Button(
                    "StartButton",
                    text="Click me",
                    position=Vec2(80, 120),
                    signals=[signal("pressed", target=".", method="_on_start_pressed")],
                ),
            ],
        ),
    )


class SnapshotTestCase(unittest.TestCase):
    def assert_matches_snapshot(self, snapshot_name: str, actual: str) -> None:
        expected = (SNAPSHOTS_DIR / snapshot_name).read_text(encoding="utf-8")
        self.assertEqual(actual, expected)


def _read_generated_files(build_dir: Path) -> dict[str, str]:
    return {
        path.relative_to(build_dir).as_posix(): path.read_text(encoding="utf-8")
        for path in sorted(build_dir.rglob("*"))
        if path.is_file()
    }


def _load_example_game(name: str):
    path = Path(__file__).parents[1] / "examples" / name / "game.py"
    spec = importlib.util.spec_from_file_location(f"pygodot_example_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load example module from {path}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _find_scene(game: Game, path: str) -> Scene:
    for scene in game.scenes:
        if scene.path == path:
            return scene
    raise AssertionError(f"Missing scene: {path}")


def _build_example_script(game: Game, relative_path: str) -> str:
    return _build_example_file(game, relative_path)


def _build_example_file(game: Game, relative_path: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        build_dir = Path(tmp) / "godot_project"
        game.build_dir = build_dir
        game.build()
        return (build_dir / relative_path).read_text(encoding="utf-8")
