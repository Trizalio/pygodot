"""Node declarations for the public DSL."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pygodot.dsl.animation import Animation
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
    animations: list[Animation] = field(default_factory=list)
    groups: list[str] = field(default_factory=list)

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
    groups: list[str] | None = None,
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
        groups=groups or [],
    )


def scene_instance(
    name: str,
    scene: ExternalResource,
    *,
    children: list[Node] | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
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
        groups=groups or [],
    )


def Node2D(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Node2D",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def Area2D(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Area2D",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def CollisionShape2D(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="CollisionShape2D",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def Control(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Control",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def MarginContainer(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="MarginContainer",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def Panel(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Panel",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def VBoxContainer(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="VBoxContainer",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def HBoxContainer(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="HBoxContainer",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def GridContainer(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="GridContainer",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def CenterContainer(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="CenterContainer",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def TextureRect(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="TextureRect",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def RichTextLabel(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="RichTextLabel",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def HSeparator(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="HSeparator",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def ColorRect(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="ColorRect",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def Sprite2D(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Sprite2D",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def Label(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Label",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def Button(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Button",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def Timer(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="Timer",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def AudioStreamPlayer(
    name: str,
    *,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="AudioStreamPlayer",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        groups=groups or [],
    )


def AnimationPlayer(
    name: str,
    *,
    animations: list[Animation] | None = None,
    children: list[Node] | None = None,
    script: Script | None = None,
    signals: list[SignalConnection] | None = None,
    groups: list[str] | None = None,
    **props: Any,
) -> Node:
    return Node(
        name=name,
        type="AnimationPlayer",
        props=props,
        children=children or [],
        script=script,
        signals=signals or [],
        animations=animations or [],
        groups=groups or [],
    )
