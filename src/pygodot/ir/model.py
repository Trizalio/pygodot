"""Dataclasses for the normalized compiler IR."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class IRSignalConnection:
    signal: str
    from_path: str
    target: str
    method: str
    binds: tuple[Any, ...] = ()


@dataclass(slots=True, frozen=True)
class IRScript:
    path: str
    extends: str
    body: str
    resource_id: str
    generated: bool = True
    source: str | None = None
    template_context: dict[str, Any] | None = None


@dataclass(slots=True, frozen=True)
class IRExternalResource:
    type: str
    path: str
    id: str
    copy_if_present: bool = True


@dataclass(slots=True, frozen=True)
class IRGeneratedResource:
    type: str
    path: str
    id: str
    props: dict[str, Any] = field(default_factory=dict)
    external_resources: tuple[IRExternalResource, ...] = ()


@dataclass(slots=True, frozen=True)
class IRExternalResourceRef:
    resource_id: str


@dataclass(slots=True, frozen=True)
class IRSubResourceRef:
    resource_id: str


@dataclass(slots=True, frozen=True)
class IRStringName:
    value: str


@dataclass(slots=True, frozen=True)
class IRPackedFloat32Array:
    values: tuple[float, ...]


@dataclass(slots=True, frozen=True)
class IRSubResource:
    type: str
    id: str
    props: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class IRNode:
    name: str
    type: str
    path: str
    parent_path: str | None
    props: dict[str, Any] = field(default_factory=dict)
    children: tuple["IRNode", ...] = ()
    script: IRScript | None = None
    signals: tuple[IRSignalConnection, ...] = ()
    instance: IRExternalResourceRef | None = None
    groups: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class IRScene:
    path: str
    root: IRNode
    external_resources: tuple[IRExternalResource, ...] = ()
    sub_resources: tuple[IRSubResource, ...] = ()


@dataclass(slots=True, frozen=True)
class IRInputAction:
    name: str
    keys: tuple[str, ...]
    mouse_buttons: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class IRWindowSettings:
    width: int
    height: int
    stretch_mode: str | None = None
    stretch_aspect: str | None = None


@dataclass(slots=True, frozen=True)
class IRAutoload:
    name: str
    path: str
    resource_id: str


@dataclass(slots=True, frozen=True)
class IRProjectSetting:
    path: str
    value: Any


@dataclass(slots=True, frozen=True)
class IRProject:
    name: str
    main_scene: str
    scenes: tuple[IRScene, ...] = ()
    generated_resources: tuple[IRGeneratedResource, ...] = ()
    input_actions: tuple[IRInputAction, ...] = ()
    window: IRWindowSettings | None = None
    autoloads: tuple[IRAutoload, ...] = ()
    icon: IRExternalResource | None = None
    project_settings: tuple[IRProjectSetting, ...] = ()
