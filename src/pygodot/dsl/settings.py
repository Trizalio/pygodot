"""Project settings declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass

from pygodot.dsl.values import Vec2


@dataclass(slots=True, frozen=True)
class WindowSettings:
    size: Vec2
