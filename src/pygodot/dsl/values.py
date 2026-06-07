"""Typed Godot value wrappers for the public DSL."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Vec2:
    x: float
    y: float


@dataclass(slots=True, frozen=True)
class Vec3:
    x: float
    y: float
    z: float


@dataclass(slots=True, frozen=True)
class Color:
    r: float
    g: float
    b: float
    a: float = 1.0


@dataclass(slots=True, frozen=True)
class NodePath:
    path: str
