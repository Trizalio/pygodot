"""Project settings declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pygodot.dsl.values import Vec2


@dataclass(slots=True, frozen=True)
class WindowSettings:
    size: Vec2
    stretch_mode: str | None = None
    stretch_aspect: str | None = None


@dataclass(slots=True, frozen=True)
class Autoload:
    name: str
    path: str


@dataclass(slots=True, frozen=True)
class ProjectSetting:
    path: str
    value: Any
