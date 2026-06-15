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


def style_box_flat(
    path: str,
    *,
    bg_color: Any | None = None,
    border_color: Any | None = None,
    border_width_all: int | None = None,
    corner_radius_all: int | None = None,
) -> GeneratedResource:
    props: dict[str, Any] = {}
    if bg_color is not None:
        props["bg_color"] = bg_color
    if border_color is not None:
        props["border_color"] = border_color
    if border_width_all is not None:
        props.update(
            {
                "border_width_bottom": border_width_all,
                "border_width_left": border_width_all,
                "border_width_right": border_width_all,
                "border_width_top": border_width_all,
            }
        )
    if corner_radius_all is not None:
        props.update(
            {
                "corner_radius_bottom_left": corner_radius_all,
                "corner_radius_bottom_right": corner_radius_all,
                "corner_radius_top_left": corner_radius_all,
                "corner_radius_top_right": corner_radius_all,
            }
        )
    return GeneratedResource(path=path, type="StyleBoxFlat", props=props)
