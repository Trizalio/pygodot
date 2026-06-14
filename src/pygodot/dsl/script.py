"""GDScript declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Script:
    path: str
    extends: str
    body: str = ""
    generated: bool = True
    source: str | Path | None = None

    @classmethod
    def reference(cls, path: str, *, extends: str) -> "Script":
        return cls(path=path, extends=extends, generated=False)

    @classmethod
    def from_file(cls, source: str | Path, *, path: str, extends: str) -> "Script":
        return cls(path=path, extends=extends, source=source)
