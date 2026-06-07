"""GDScript declarations for the public DSL."""

from dataclasses import dataclass


@dataclass(slots=True)
class Script:
    path: str
    extends: str
    body: str = ""
    generated: bool = True

    @classmethod
    def reference(cls, path: str, *, extends: str) -> "Script":
        return cls(path=path, extends=extends, generated=False)
