"""Generated scene sub-resource declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class SubResource:
    type: str
    id_hint: str
    props: dict[str, Any] = field(default_factory=dict)


def sub_resource(type: str, *, id_hint: str, **props: Any) -> SubResource:
    return SubResource(type=type, id_hint=id_hint, props=props)
