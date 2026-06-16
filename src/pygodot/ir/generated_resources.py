"""Supported generated .tres resource type definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GeneratedResourceSpec:
    type: str


SUPPORTED_GENERATED_RESOURCE_TYPES: dict[str, GeneratedResourceSpec] = {
    "LabelSettings": GeneratedResourceSpec(type="LabelSettings"),
    "StyleBoxFlat": GeneratedResourceSpec(type="StyleBoxFlat"),
}


def generated_resource_spec(resource_type: str) -> GeneratedResourceSpec:
    try:
        return SUPPORTED_GENERATED_RESOURCE_TYPES[resource_type]
    except KeyError as exc:
        raise TypeError(f"Unsupported generated .tres resource type: {resource_type!r}.") from exc


def supported_generated_resource_types() -> frozenset[str]:
    return frozenset(SUPPORTED_GENERATED_RESOURCE_TYPES)
