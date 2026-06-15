"""Generated external resource declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pygodot.dsl.resources import ExternalResource


@dataclass(slots=True, frozen=True)
class GeneratedResource:
    path: str
    type: str
    props: dict[str, Any] = field(default_factory=dict)


def label_settings(
    path: str,
    *,
    font: ExternalResource | None = None,
    font_size: int | None = None,
    font_color: Any | None = None,
) -> GeneratedResource:
    props: dict[str, Any] = {}
    if font is not None:
        props["font"] = font
    if font_size is not None:
        props["font_size"] = font_size
    if font_color is not None:
        props["font_color"] = font_color
    return GeneratedResource(path=path, type="LabelSettings", props=props)
