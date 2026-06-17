from __future__ import annotations

import unittest

from pygodot import Color, NodePath, Rect2, StringName, Vec2, Vec3
from pygodot.emitters.values import gd_value


class ValueSerializationTests(unittest.TestCase):
    def test_serializes_common_godot_values(self) -> None:
        self.assertEqual(gd_value("hello"), '"hello"')
        self.assertEqual(gd_value(True), "true")
        self.assertEqual(gd_value(None), "null")
        self.assertEqual(gd_value((1, 2)), "Vector2(1, 2)")
        self.assertEqual(gd_value((1, 2, 3)), "Vector3(1, 2, 3)")
        self.assertEqual(gd_value(Vec2(80, 120)), "Vector2(80, 120)")
        self.assertEqual(gd_value(Vec3(1, 2, 3)), "Vector3(1, 2, 3)")
        self.assertEqual(gd_value(Rect2(1, 2, 30, 40)), "Rect2(1, 2, 30, 40)")
        self.assertEqual(gd_value(Color(1, 0.5, 0.25)), "Color(1, 0.5, 0.25, 1.0)")
        self.assertEqual(gd_value(NodePath("../Player")), 'NodePath("../Player")')
        self.assertEqual(gd_value(StringName("idle")), '&"idle"')
