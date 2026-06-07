"""GDScript declarations for the public DSL."""

from dataclasses import dataclass


@dataclass(slots=True)
class Script:
    path: str
    extends: str
    body: str
