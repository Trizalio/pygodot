"""Shape resource declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass

from pygodot.dsl.values import Vec2


@dataclass(slots=True, frozen=True)
class RectangleShape2D:
    size: Vec2


def rectangle_shape_2d(*, size: Vec2) -> RectangleShape2D:
    return RectangleShape2D(size=size)
