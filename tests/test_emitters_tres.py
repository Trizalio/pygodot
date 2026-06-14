from __future__ import annotations

import unittest

from pygodot import Color
from pygodot.emitters.tres import TresEmitter
from pygodot.ir.model import IRGeneratedResource


class TresEmitterTests(unittest.TestCase):
    def test_tres_emitter_snapshot_with_label_settings(self) -> None:
        resource = IRGeneratedResource(
            type="LabelSettings",
            path="res://ui/title_label_settings.tres",
            id="LabelSettings_ui_title_label_settings_tres",
            props={
                "font_color": Color(1, 1, 1),
                "font_size": 32,
            },
        )

        self.assertEqual(
            TresEmitter().emit(resource),
            """[gd_resource type="LabelSettings" format=3]

[resource]
font_color = Color(1, 1, 1, 1.0)
font_size = 32
""",
        )
