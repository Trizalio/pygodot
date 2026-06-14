"""Public DSL objects."""

from pygodot.dsl.input import InputAction
from pygodot.dsl.nodes import (
    AudioStreamPlayer,
    Button,
    ColorRect,
    Control,
    Label,
    Node,
    Node2D,
    Sprite2D,
    Timer,
    node,
    scene_instance,
)
from pygodot.dsl.resources import (
    ExternalResource,
    audio_stream,
    ext_resource,
    external_resource,
    packed_scene,
    texture,
)
from pygodot.dsl.scene import Scene
from pygodot.dsl.settings import WindowSettings
from pygodot.dsl.script import Script
from pygodot.dsl.signal import SignalConnection, signal
from pygodot.dsl.values import Color, NodePath, Rect2, Vec2, Vec3

__all__ = [
    "AudioStreamPlayer",
    "Button",
    "Color",
    "ColorRect",
    "Control",
    "ExternalResource",
    "InputAction",
    "Label",
    "Node",
    "Node2D",
    "NodePath",
    "Rect2",
    "Scene",
    "Script",
    "SignalConnection",
    "Sprite2D",
    "Timer",
    "Vec2",
    "Vec3",
    "WindowSettings",
    "audio_stream",
    "ext_resource",
    "external_resource",
    "node",
    "packed_scene",
    "scene_instance",
    "signal",
    "texture",
]
