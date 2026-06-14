from __future__ import annotations

import unittest

from pygodot.emitters.gdscript import GdScriptEmitter
from pygodot.ir.normalize import normalize_scene
from tests.helpers import make_scene


class GdScriptEmitterTests(unittest.TestCase):
    def test_gdscript_emitter_snapshot(self) -> None:
        script = normalize_scene(make_scene()).root.script
        assert script is not None

        self.assertEqual(
            GdScriptEmitter().emit(script),
            """extends Node2D

var counter := 0

func _on_start_pressed() -> void:
    counter += 1
""",
        )
