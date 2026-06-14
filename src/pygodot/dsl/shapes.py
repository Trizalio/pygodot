"""Shape resource declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass

from pygodot.dsl.subresources import SubResource, sub_resource
from pygodot.dsl.values import Vec2


@dataclass(slots=True, frozen=True)
class RectangleShape2D:
    size: Vec2

    def as_sub_resource(self) -> SubResource:
        return sub_resource(
            "RectangleShape2D",
            id_hint=f"rectangle_{self.size.x}_{self.size.y}",
            size=self.size,
        )


@dataclass(slots=True, frozen=True)
class CircleShape2D:
    radius: float

    def as_sub_resource(self) -> SubResource:
        return sub_resource(
            "CircleShape2D",
            id_hint=f"circle_{self.radius}",
            radius=self.radius,
        )


def rectangle_shape_2d(*, size: Vec2) -> RectangleShape2D:
    return RectangleShape2D(size=size)


def circle_shape_2d(*, radius: float) -> CircleShape2D:
    return CircleShape2D(radius=radius)
