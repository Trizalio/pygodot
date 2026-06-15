from __future__ import annotations

import unittest

from pygodot import (
    AnimationPlayer,
    Area2D,
    AudioStreamPlayer,
    Button,
    CircleShape2D,
    Color,
    ColorRect,
    CollisionShape2D,
    Label,
    Node2D,
    Rect2,
    RectangleShape2D,
    Scene,
    Script,
    Sprite2D,
    SubResource,
    Timer,
    Vec2,
    audio_stream,
    animation,
    circle_shape_2d,
    font,
    key,
    label_settings,
    node,
    packed_scene,
    rectangle_shape_2d,
    scene_instance,
    signal,
    style_box_flat,
    sub_resource,
    texture,
    value_track,
)


class DslNodeTests(unittest.TestCase):
    def test_animation_player_constructor_creates_animation_player_node(self) -> None:
        pulse = animation(
            "pulse",
            length=1.0,
            loop=True,
            tracks=[
                value_track(
                    "Target:scale",
                    keys=[
                        key(0.0, Vec2(1, 1)),
                        key(1.0, Vec2(2, 2)),
                    ],
                )
            ],
        )
        player = AnimationPlayer("Animator", autoplay="pulse", animations=[pulse])

        self.assertEqual(player.name, "Animator")
        self.assertEqual(player.type, "AnimationPlayer")
        self.assertEqual(player.props, {"autoplay": "pulse"})
        self.assertEqual(player.animations, [pulse])

    def test_audio_stream_player_constructor_creates_audio_node(self) -> None:
        player = AudioStreamPlayer(
            "Player",
            stream=audio_stream("res://assets/tone.wav"),
            volume_db=-8,
        )

        self.assertEqual(player.name, "Player")
        self.assertEqual(player.type, "AudioStreamPlayer")
        self.assertEqual(
            player.props,
            {
                "stream": audio_stream("res://assets/tone.wav"),
                "volume_db": -8,
            },
        )

    def test_area_and_collision_shape_constructors_create_physics_nodes(self) -> None:
        shape = rectangle_shape_2d(size=Vec2(32, 48))
        collision = CollisionShape2D("Hitbox", shape=shape)
        area = Area2D(
            "Trigger",
            position=Vec2(10, 20),
            signals=[signal("area_entered", target=".", method="_on_area_entered")],
            children=[collision],
        )

        self.assertEqual(shape, RectangleShape2D(size=Vec2(32, 48)))
        self.assertEqual(collision.name, "Hitbox")
        self.assertEqual(collision.type, "CollisionShape2D")
        self.assertEqual(collision.props, {"shape": shape})
        self.assertEqual(area.name, "Trigger")
        self.assertEqual(area.type, "Area2D")
        self.assertEqual(area.props, {"position": Vec2(10, 20)})
        self.assertEqual(area.signals[0].signal, "area_entered")
        self.assertEqual(area.children, [collision])

    def test_sub_resource_helpers_create_generated_resources(self) -> None:
        generic = sub_resource(
            "RectangleShape2D",
            id_hint="player_hitbox",
            size=Vec2(24, 32),
        )
        circle = circle_shape_2d(radius=12)

        self.assertEqual(
            generic,
            SubResource(
                type="RectangleShape2D",
                id_hint="player_hitbox",
                props={"size": Vec2(24, 32)},
            ),
        )
        self.assertEqual(circle, CircleShape2D(radius=12))
        self.assertEqual(
            circle.as_sub_resource(),
            SubResource(
                type="CircleShape2D",
                id_hint="circle_12",
                props={"radius": 12},
            ),
        )

    def test_label_settings_helper_creates_generated_resource(self) -> None:
        settings = label_settings(
            "res://ui/title_label_settings.tres",
            font=font("res://assets/display.ttf"),
            font_size=32,
            font_color=Color(1, 1, 1),
        )

        self.assertEqual(settings.path, "res://ui/title_label_settings.tres")
        self.assertEqual(settings.type, "LabelSettings")
        self.assertEqual(
            settings.props,
            {
                "font": font("res://assets/display.ttf"),
                "font_size": 32,
                "font_color": Color(1, 1, 1),
            },
        )

    def test_style_box_flat_helper_creates_generated_resource(self) -> None:
        style = style_box_flat(
            "res://ui/panel_style.tres",
            bg_color=Color(0.1, 0.2, 0.3),
            border_color=Color(0.4, 0.5, 0.6),
            border_width_all=2,
            corner_radius_all=6,
        )

        self.assertEqual(style.path, "res://ui/panel_style.tres")
        self.assertEqual(style.type, "StyleBoxFlat")
        self.assertEqual(
            style.props,
            {
                "bg_color": Color(0.1, 0.2, 0.3),
                "border_color": Color(0.4, 0.5, 0.6),
                "border_width_bottom": 2,
                "border_width_left": 2,
                "border_width_right": 2,
                "border_width_top": 2,
                "corner_radius_bottom_left": 6,
                "corner_radius_bottom_right": 6,
                "corner_radius_top_left": 6,
                "corner_radius_top_right": 6,
            },
        )

    def test_node_helper_creates_generic_node(self) -> None:
        script = Script(
            path="res://scripts/panel.gd",
            extends="Control",
            body="func _ready() -> void:\n    pass",
        )
        signals = [signal("pressed", target=".", method="_on_pressed")]
        child = Label("Title", text="Hello")

        generic = node(
            "Panel",
            "Control",
            children=[child],
            script=script,
            signals=signals,
            position=Vec2(12, 24),
            visible=True,
        )

        self.assertEqual(generic.name, "Panel")
        self.assertEqual(generic.type, "Control")
        self.assertEqual(generic.props, {"position": Vec2(12, 24), "visible": True})
        self.assertEqual(generic.children, [child])
        self.assertIs(generic.script, script)
        self.assertEqual(generic.signals, signals)

    def test_color_rect_constructor_creates_color_rect_node(self) -> None:
        rect = ColorRect(
            "Panel",
            position=Vec2(10, 20),
            size=Vec2(200, 80),
            color=Color(0.1, 0.2, 0.3),
        )

        self.assertEqual(rect.name, "Panel")
        self.assertEqual(rect.type, "ColorRect")
        self.assertEqual(
            rect.props,
            {
                "position": Vec2(10, 20),
                "size": Vec2(200, 80),
                "color": Color(0.1, 0.2, 0.3),
            },
        )

    def test_sprite2d_constructor_creates_sprite_node(self) -> None:
        sprite = Sprite2D(
            "Logo",
            texture=texture("res://assets/logo.svg"),
            position=Vec2(100, 120),
        )

        self.assertEqual(sprite.name, "Logo")
        self.assertEqual(sprite.type, "Sprite2D")
        self.assertEqual(
            sprite.props,
            {
                "texture": texture("res://assets/logo.svg"),
                "position": Vec2(100, 120),
            },
        )

    def test_scene_instance_constructor_creates_instance_node(self) -> None:
        resource = packed_scene("res://scenes/gem.tscn")
        instance = scene_instance("GemA", resource, position=Vec2(220, 190))

        self.assertEqual(instance.name, "GemA")
        self.assertEqual(instance.type, "")
        self.assertIs(instance.instance, resource)
        self.assertEqual(instance.props, {"position": Vec2(220, 190)})

    def test_scene_as_packed_scene_returns_packed_scene_resource(self) -> None:
        scene = Scene(path="res://scenes/gem.tscn", root=Node2D("Gem"))

        self.assertEqual(scene.as_packed_scene(), packed_scene("res://scenes/gem.tscn"))

    def test_scene_instance_requires_packed_scene_resource(self) -> None:
        with self.assertRaisesRegex(ValueError, "PackedScene"):
            scene_instance("Logo", texture("res://assets/logo.svg"))

    def test_timer_constructor_creates_timer_node(self) -> None:
        timer = Timer(
            "PulseTimer",
            wait_time=0.5,
            autostart=True,
            signals=[signal("timeout", target=".", method="_on_timeout")],
        )

        self.assertEqual(timer.name, "PulseTimer")
        self.assertEqual(timer.type, "Timer")
        self.assertEqual(timer.props, {"wait_time": 0.5, "autostart": True})
        self.assertEqual(timer.signals[0].signal, "timeout")

    def test_script_from_file_declares_generated_source(self) -> None:
        script = Script.from_file(
            source="scripts/player.gd",
            path="res://scripts/player.gd",
            extends="Node2D",
        )

        self.assertEqual(script.source, "scripts/player.gd")
        self.assertEqual(script.path, "res://scripts/player.gd")
        self.assertEqual(script.extends, "Node2D")
        self.assertEqual(script.body, "")
        self.assertTrue(script.generated)

    def test_script_from_template_declares_generated_template(self) -> None:
        script = Script.from_template(
            source="scripts/player.gd.tmpl",
            path="res://scripts/player.gd",
            extends="Node2D",
            context={"speed": 300},
        )

        self.assertEqual(script.source, "scripts/player.gd.tmpl")
        self.assertEqual(script.path, "res://scripts/player.gd")
        self.assertEqual(script.extends, "Node2D")
        self.assertEqual(script.body, "")
        self.assertEqual(script.template_context, {"speed": 300})
        self.assertTrue(script.generated)
