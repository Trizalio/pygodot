"""Scene declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass

from pygodot.dsl.nodes import Node


@dataclass(slots=True)
class Scene:
    path: str
    root: Node
