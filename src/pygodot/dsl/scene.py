"""Scene declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass

from pygodot.dsl.nodes import Node
from pygodot.dsl.resources import ExternalResource, packed_scene


@dataclass(slots=True)
class Scene:
    path: str
    root: Node

    def as_packed_scene(self) -> ExternalResource:
        return packed_scene(self.path)
