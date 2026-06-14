"""Public DSL objects."""

from pygodot.dsl.animation import (
    Animation,
    AnimationKey,
    ValueTrack,
    animation,
    key,
    value_track,
)
from pygodot.dsl.input import InputAction
from pygodot.dsl.nodes import (
    Area2D,
    AudioStreamPlayer,
    AnimationPlayer,
    Button,
    CollisionShape2D,
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
    font,
    packed_scene,
    texture,
)
from pygodot.dsl.scene import Scene
from pygodot.dsl.settings import WindowSettings
from pygodot.dsl.shapes import (
    CircleShape2D,
    RectangleShape2D,
    circle_shape_2d,
    rectangle_shape_2d,
)
from pygodot.dsl.script import Script
from pygodot.dsl.signal import SignalConnection, signal
from pygodot.dsl.subresources import SubResource, sub_resource
from pygodot.dsl.values import Color, NodePath, Rect2, Vec2, Vec3

__all__ = [
    "Animation",
    "AnimationKey",
    "AnimationPlayer",
    "Area2D",
    "AudioStreamPlayer",
    "Button",
    "CircleShape2D",
    "CollisionShape2D",
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
    "RectangleShape2D",
    "Scene",
    "Script",
    "SignalConnection",
    "Sprite2D",
    "SubResource",
    "Timer",
    "ValueTrack",
    "Vec2",
    "Vec3",
    "WindowSettings",
    "audio_stream",
    "animation",
    "circle_shape_2d",
    "ext_resource",
    "external_resource",
    "font",
    "key",
    "node",
    "packed_scene",
    "rectangle_shape_2d",
    "scene_instance",
    "signal",
    "sub_resource",
    "texture",
    "value_track",
]
