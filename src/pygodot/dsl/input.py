"""Input action declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class InputAction:
    name: str
    keys: tuple[str, ...]
    mouse_buttons: tuple[str, ...] = ()
