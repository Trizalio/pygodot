# Declarative DSL

The DSL is ordinary Python object construction. It should be explicit, typed
where useful, IDE-friendly, and easy to compose with functions.

## Principles

1. No mandatory context managers.
2. No metaclass-heavy public API.
3. No hidden global scene stack.
4. Public DSL objects are separate from normalized compiler IR.
5. Prefer small helpers that examples actually need.

## Public Concepts

Current public concepts:

- `Game`;
- `Scene`;
- `Node`;
- `Script`;
- `SignalConnection`;
- `InputAction`;
- `Animation`;
- generated sub-resources;
- generated external resources;
- Godot value wrappers;
- external resource references;
- scene instances.

Node constructors/helpers:

- `node(name, type, ...)` for arbitrary Godot node classes;
- `Node2D`;
- `Control`;
- `MarginContainer`;
- `Panel`;
- `VBoxContainer`;
- `HBoxContainer`;
- `GridContainer`;
- `CenterContainer`;
- `ColorRect`;
- `TextureRect`;
- `RichTextLabel`;
- `HSeparator`;
- `Sprite2D`;
- `Label`;
- `Button`;
- `Timer`;
- `AnimationPlayer`;
- `AudioStreamPlayer`;
- `Area2D`;
- `CollisionShape2D`.

## Example Scene

```python
from pathlib import Path
from pygodot import Button, Game, Label, Node2D, Scene, Script, Vec2, signal

script = Script(
    path="res://scripts/main.gd",
    extends="Node2D",
    body="""
var counter := 0

func _on_start_pressed() -> void:
    counter += 1
    $Title.text = "Clicked %s times" % counter
""",
)

game = Game(
    name="GeneratedGame",
    source_root=Path(__file__).parent,
    build_dir=Path(__file__).parent / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
)

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "Main",
            script=script,
            children=[
                Label("Title", text="Generated scene", position=Vec2(80, 60)),
                Button(
                    "StartButton",
                    text="Click me",
                    position=Vec2(80, 120),
                    signals=[signal("pressed", target=".", method="_on_start_pressed")],
                ),
            ],
        ),
    )
)
```

## Nodes

Use `node(...)` for Godot classes that do not have a convenience constructor:

```python
node(
    "CustomNode",
    "SomeGodotClass",
    position=Vec2(10, 20),
)
```

Use convenience constructors when they exist:

```python
Node2D("Main")
ColorRect("Panel", color=Color(1, 1, 1), size=Vec2(200, 80))
Sprite2D("Logo", texture=texture("res://assets/logo.svg"))
Label("Title", text="Hello")
Button("Start", text="Start")
Timer("PulseTimer", wait_time=0.5, autostart=True)
AnimationPlayer("Animator", autoplay="pulse", animations=[pulse_animation])
AudioStreamPlayer("Player", stream=audio_stream("res://assets/tone.wav"))
Area2D("Trigger", children=[CollisionShape2D("Hitbox", shape=hitbox_shape)])
```

LD49-style UI scenes can use thin Control/container constructors:

```python
MarginContainer(
    "Main",
    children=[
        Panel(
            "Panel",
            children=[
                VBoxContainer(
                    "Menu",
                    children=[
                        TextureRect("Banner", texture=texture("res://assets/banner.svg")),
                        CenterContainer("Center", children=[Button("Start", text="Start")]),
                    ],
                )
            ],
        )
    ],
)
```

Nodes can be assigned to Godot groups with the `groups` keyword. This is
available on `Node`, `node(...)`, `scene_instance(...)`, and existing node
constructors:

```python
Node2D("Player", groups=["actors", "restartable"])
node("MarkerLayer", "Node", groups=["debug"])
```

Do not add broad wrappers for the whole Godot API. Add small constructors only
when examples show repeated pain.

## Values and Resources

Prefer explicit wrappers:

```python
Vec2(80, 60)
Vec3(1, 2, 3)
Rect2(0, 0, 16, 32)
Color(1, 1, 1)
NodePath("../Player")
StringName("idle")
```

Temporary tuple inference exists for simple vectors, but new examples should use
explicit wrappers.

External resources are referenced explicitly:

```python
Sprite2D("Logo", texture=texture("res://assets/logo.svg"))
AudioStreamPlayer("Player", stream=audio_stream("res://assets/tone.wav"))
Node(
    name="Title",
    type="Label",
    props={"theme_override_fonts/font": font("res://assets/display_font.tres")},
)
ColorRect("Spell", material=ext_resource("res://materials/spell_edge.tres", type="ShaderMaterial"))
Node2D("Other", resource=ext_resource("res://assets/data.tres", type="Resource"))
```

Normalization collects external resources into scene resource tables and
deduplicates them by `(type, path)`. During `Game.build()`, existing source
files under `Game.source_root` are copied to matching `res://` paths under
`build_dir` and recorded in the manifest with `ownership="copied"`. Missing
external resources remain soft references: they are not copied, they appear in
`BuildResult.referenced_resources`, and the manifest records them with
`ownership="referenced"`.

Copied `.tres` resources are treated as source-owned files. `pygodot` does not
parse them to discover nested dependencies; declare those dependencies directly
when pygodot should copy or track them.

Generated `.tres` resources are intentionally narrow. The current public helper
is `label_settings(...)`, which writes a native Godot `LabelSettings` resource
and references it from scenes as an `ExtResource`:

```python
title_settings = label_settings(
    "res://ui/title_label_settings.tres",
    font=font("res://assets/display.ttf"),
    font_size=32,
    font_color=Color(1, 1, 1),
)

Label(
    "Title",
    text="Generated .tres",
    label_settings=title_settings,
)
```

The optional `font` argument accepts the same `font("res://...")` external
resource helper used by node properties. `Game.build()` copies an existing font
file from `source_root` when the font is referenced only from the generated
`.tres` file, and the `.tres` file declares it as an internal `ExtResource`.
If that font file is not present under `source_root`, it is recorded as a
referenced external resource instead of failing the build.

Use source-owned copied `.tres` files with `ext_resource(...)` or typed helpers
when pygodot should not generate the resource content.

Shader files can be referenced with `shader("res://...")`, which is a small
typed helper around `ext_resource(..., type="Shader")`. Generated scene
sub-resources can use it for narrow `ShaderMaterial` cases:

```python
spell_material = sub_resource(
    "ShaderMaterial",
    id_hint="arcane_burst",
    shader=shader("res://shaders/spell_pulse.gdshader"),
    **{
        "shader_parameter/pulse": 0.65,
        "shader_parameter/tint": Color(0.2, 0.85, 1.0),
    },
)

ColorRect("Spell", material=spell_material, size=Vec2(96, 96))
```

Use source-owned `.tres` materials through `ext_resource(...,
type="ShaderMaterial")` when the material content should remain manual.

Generated `StyleBoxFlat` resources are available for small reusable UI styles:

```python
panel_style = style_box_flat(
    "res://ui/panel_style.tres",
    bg_color=Color(0.08, 0.10, 0.12),
    border_color=Color(0.30, 0.45, 0.55),
    border_width_all=2,
    corner_radius_all=6,
)

node(
    "Panel",
    "Panel",
    theme_override_styles={"panel": panel_style},
)
```

The helper intentionally supports only a small property set. Use
`ext_resource(...)` for manual style resources that need broader Godot support.

Generated scenes can also be reused as `PackedScene` instances:

```python
gem_scene = Scene(
    path="res://scenes/gem.tscn",
    root=Node2D("Gem"),
)

Node2D(
    "Main",
    children=[
        scene_instance("GemA", gem_scene.as_packed_scene(), position=Vec2(220, 190)),
        scene_instance("GemB", gem_scene.as_packed_scene(), position=Vec2(320, 150)),
    ],
)
```

`scene_instance(...)` expects a `PackedScene` resource. For generated scenes,
prefer `scene.as_packed_scene()` so the resource path stays attached to the
scene declaration. `packed_scene(...)` remains available for manual or external
scene references.

Simple generated scene sub-resources can be declared directly:

```python
shape = sub_resource(
    "RectangleShape2D",
    id_hint="player_hitbox",
    size=Vec2(64, 64),
)

CollisionShape2D("ProbeShape", shape=shape)
```

`id_hint` is combined with the resource type to produce deterministic resource
IDs such as `RectangleShape2D_player_hitbox`.

Generic sub-resources can also model narrow resource shapes before a typed
helper exists. For example, `examples/ld49_unit_card` uses `AtlasTexture` and
`SpriteFrames` resources directly:

```python
frame = sub_resource(
    "AtlasTexture",
    id_hint="unit_idle_0",
    atlas=texture("res://assets/unit_atlas.svg"),
    region=Rect2(0, 0, 32, 32),
)

frames = sub_resource(
    "SpriteFrames",
    id_hint="unit_frames",
    animations=[
        {
            "frames": [{"duration": 1.0, "texture": frame}],
            "loop": True,
            "name": StringName("idle"),
            "speed": 5.0,
        }
    ],
)
```

Typed shape helpers are available for common collision shapes:

```python
hitbox_shape = rectangle_shape_2d(size=Vec2(64, 64))
sensor_shape = circle_shape_2d(radius=12)

Area2D(
    "Probe",
    signals=[signal("area_entered", target=".", method="_on_probe_area_entered")],
    children=[
        CollisionShape2D("ProbeShape", shape=hitbox_shape),
    ],
)
```

The current shape DSL intentionally covers only `RectangleShape2D` and
`CircleShape2D`, generated as scene sub-resources. Use `sub_resource(...)` for
other simple sub-resources before adding a new typed helper.

## Animations

Generated `AnimationPlayer` nodes can contain value-track animations:

```python
pulse_animation = animation(
    "pulse",
    length=1.2,
    loop=True,
    tracks=[
        value_track(
            "Pulse:scale",
            keys=[
                key(0.0, Vec2(1, 1)),
                key(0.6, Vec2(1.35, 1.35)),
                key(1.2, Vec2(1, 1)),
            ],
        ),
    ],
)

AnimationPlayer("Animator", autoplay="pulse", animations=[pulse_animation])
```

The current animation DSL is intentionally narrow: generated `Animation` and
`AnimationLibrary` sub-resources, value tracks, and explicit keyframes.

## Signals

Signals are explicit connection objects:

```python
Button(
    "StartButton",
    text="Start",
    signals=[
        signal("pressed", target=".", method="_on_start_pressed"),
    ],
)
```

Signal connections can include Godot bind arguments:

```python
Button(
    "LeftButton",
    text="Left",
    signals=[
        signal("pressed", target=".", method="_on_direction_pressed", binds=["left"]),
    ],
)
```

Built-in node signals use the same connection form:

```python
Timer(
    "PulseTimer",
    wait_time=0.5,
    autostart=True,
    signals=[
        signal("timeout", target=".", method="_on_pulse_timer_timeout"),
    ],
)
```

## Scripts

Generated scripts use raw GDScript bodies:

```python
Script(
    path="res://scripts/player.gd",
    extends="Node2D",
    body="""
func _ready() -> void:
    print("ready")
""",
)
```

Generated script bodies can also come from source files under
`Game.source_root`:

```python
Script.from_file(
    source="scripts/player.gd",
    path="res://scripts/player.gd",
    extends="Node2D",
)
```

`source` is user-owned input. `path` is the generated Godot project destination.
The source file should contain the script body; `extends` is still declared in
Python and emitted by pygodot.

Generated scripts can also use standard-library `string.Template` files:

```python
Script.from_template(
    source="scripts/player.gd.tmpl",
    path="res://scripts/player.gd",
    extends="Node2D",
    context={"speed": 300, "title": "Pilot"},
)
```

Template files are plain GDScript body files rendered with Python's
standard-library `string.Template`:

- `$name` inserts `context["name"]`;
- `${name}` is the braced form, useful next to identifier characters;
- `$$` emits a literal `$`.

Literal Godot node shorthand such as `$Player` must be escaped as `$$Player`
inside template files:

```gdscript
const SPEED := ${speed}

func _ready() -> void:
    $$Title.text = "$title"
```

Context values are converted by `string.Template` during substitution, so simple
numbers such as `300` can be passed directly. Missing or invalid placeholders
raise `BuildError` with the script path, template source, and missing key or
template parse error.

Templates are text substitution only. They are not Python-to-GDScript
transpilation, do not add control flow, and do not parse Python functions or
classes.

Manual scripts are referenced without generation:

```python
Script.reference("res://manual/player.gd", extends="CharacterBody2D")
```

Referenced manual scripts are included in generated `.tscn` files as external
script resources, but `Game.build()` does not write the `.gd` file.

## Project Settings And Autoloads

Autoload singletons are declared on `Game` and emitted into `project.godot`:

```python
game.add_autoload("GameState", "res://scripts/singletons/game_state.gd")
game.add_autoload("SceneChanger", "res://scripts/singletons/scene_changer.gd")
```

Autoload paths are script resources. If the `.gd` file exists under
`source_root`, `Game.build()` copies it into `build_dir` and records it with
`ownership="copied"`. If it is missing or managed elsewhere, the manifest records
it with `ownership="referenced"`.

Focused project settings are available for the LD49-style project shell:

```python
game.set_icon("res://resources/icon.png")
game.set_display(size=Vec2(540, 750), stretch_mode="canvas_items", stretch_aspect="expand")
game.set_project_setting("audio/output_latency/web", 200)
game.set_project_setting("physics/common/enable_pause_aware_picking", True)
```

`set_project_setting(...)` is intentionally narrow: it accepts a Godot project
setting path such as `section/key/path` and a value supported by pygodot's Godot
value emitter. It is not a full `ProjectSettings` wrapper.

## Input Actions

Input actions are declared on `Game` and emitted into `project.godot`:

```python
game.add_input_action("left_up", keys=["W"])
game.add_input_action("right_up", keys=["UP"])
game.add_input_action("restart", keys=["SPACE"])
game.add_input_action("place_marker", mouse_buttons=["LEFT"])
```

Generated GDScript should use Godot's InputMap APIs:

```gdscript
Input.is_action_pressed("left_up")
Input.is_action_just_pressed("restart")
Input.is_action_just_pressed("place_marker")
```

The current InputMap DSL intentionally covers keyboard keys and mouse buttons
only. It does not cover gamepads, touch, gestures, or arbitrary Godot input
event types yet.

## Window Settings

Generated project window size is declared on `Game`:

```python
game.set_window(size=Vec2(800, 600))
```

The current settings DSL intentionally covers only viewport width and height.

## Composition

Use normal Python functions for reusable scene fragments:

```python
def menu_button(name: str, text: str, y: int, method: str) -> Button:
    return Button(
        name,
        text=text,
        position=Vec2(80, y),
        signals=[signal("pressed", target=".", method=method)],
    )
```
