"""Node declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pygodot.dsl.resources import ExternalResource
from pygodot.dsl.script import Script
from pygodot.dsl.signal import SignalConnection


@dataclass(slots=True)
class Node:
    name: str
    type: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list["Node"] = field(default_factory=list)
    script: Script | None = None
    signals: list[SignalConnection] = field(default_factory=list)
    instance: ExternalResource | None = None

    def add(self, *children: "Node") -> "Node":
        self.children.extend(children)
        return self


def node(
    name: str,
    type: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    instance: ExternalResource | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type=type,
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        instance=instance,
    )


def scene_instance(
    name: str,
    scene: ExternalResource,
    *,
    children: list[Node] | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    if scene.type != "PackedScene":
        raise ValueError(f"scene_instance requires a PackedScene resource, got {scene.type!r}.")
    return Node(
        name=name,
        type="",
        props=props,
        children=children or [],
        signals=signals or [],
        instance=scene,
    )


def Node2D(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Node2D",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
    )


def Control(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Control",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
    )


def ColorRect(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="ColorRect",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
    )


def Sprite2D(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Sprite2D",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
    )


def Label(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Label",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
    )


def Button(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Button",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
    )


def Timer(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Timer",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
    )
