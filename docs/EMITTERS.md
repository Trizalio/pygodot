# Emitters

Emitters convert normalized IR into deterministic Godot text files.

Current emitters:

- `ProjectEmitter` for `project.godot`;
- `TscnEmitter` for `.tscn` scene files;
- `GdScriptEmitter` for `.gd` script files;
- `TresEmitter` for narrow generated `.tres` resources.

## Design Rules

1. Emitters consume normalized IR, not public DSL objects.
2. Emitters produce strings and do not write files directly.
3. Emitters are deterministic: stable order, stable IDs, no timestamps.
4. Validation happens before emission.
5. Emitters do not mutate their inputs.

## `.tscn`

The direct `.tscn` emitter supports:

- `[gd_scene format=3]` headers;
- `[ext_resource ...]` entries for scripts and external resources;
- `[sub_resource ...]` entries for generated animations and simple generated
  sub-resources;
- `[node ...]` sections;
- scene instance nodes with `instance=ExtResource(...)`;
- node properties;
- signal `[connection ...]` sections;
- stable resource IDs;
- deterministic property/resource ordering.

Example:

```text
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/main.gd" id="Script_scripts_main_gd"]

[node name="Main" type="Node2D"]
script = ExtResource("Script_scripts_main_gd")

[node name="Title" type="Label" parent="."]
position = Vector2(80, 60)
text = "Generated scene"
```

Scene instances are emitted with a `PackedScene` external resource:

```text
[ext_resource type="PackedScene" path="res://scenes/gem.tscn" id="PackedScene_scenes_gem_tscn"]

[node name="GemA" parent="." instance=ExtResource("PackedScene_scenes_gem_tscn")]
position = Vector2(220, 190)
```

Generated sub-resources are emitted inside the scene and referenced by nodes:

```text
[sub_resource type="RectangleShape2D" id="RectangleShape2D_rectangle_64_64"]
size = Vector2(64, 64)

[node name="ProbeShape" type="CollisionShape2D" parent="Probe"]
shape = SubResource("RectangleShape2D_rectangle_64_64")
```

## Values

Supported values include:

- `str`, `bool`, `None`, `int`, `float`;
- `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`;
- two- and three-item tuples as temporary Vector2/Vector3 convenience;
- lists and dictionaries of supported values;
- normalized external resource references;
- normalized sub-resource references and StringName keys used by animations.

Prefer explicit value wrappers in new examples.

## Resource IDs

Resource IDs are deterministic and readable:

```text
Script_scripts_main_gd
Texture2D_assets_player_png
PackedScene_scenes_menu_tscn
CircleShape2D_circle_12
```

Avoid incremental IDs because they create noisy diffs.

## `project.godot`

The project emitter currently writes:

- `config_version=5`;
- application name;
- main scene;
- keyboard-only input map actions.
- display window size.

## GDScript

The GDScript emitter wraps generated bodies with an `extends` line:

```python
Script(path="res://scripts/main.gd", extends="Node2D", body="...")
Script.from_file(source="scripts/main.gd", path="res://scripts/main.gd", extends="Node2D")
Script.from_template(
    source="scripts/main.gd.tmpl",
    path="res://scripts/main.gd",
    extends="Node2D",
    context={"speed": 300},
)
```

Output:

```gdscript
extends Node2D

...
```

For `Script.from_file(...)`, `Game.build()` reads the body from `source_root`.
For `Script.from_template(...)`, `Game.build()` reads the template from
`source_root` and renders it with `string.Template` before passing the
normalized script to the emitter.

Manual scripts are referenced with `Script.reference(...)` and are not emitted.

## `.tres`

The `.tres` emitter is intentionally narrow. It currently supports generated
`LabelSettings` and `StyleBoxFlat` resources:

```text
[gd_resource type="LabelSettings" load_steps=2 format=3]

[ext_resource type="Font" path="res://assets/display.ttf" id="Font_assets_display_ttf"]

[resource]
font = ExtResource("Font_assets_display_ttf")
font_color = Color(1, 1, 1, 1.0)
font_size = 32
```

Generated `.tres` files are written by `Game.build()`, recorded in the manifest
under `generated_resources`, and referenced from scenes through ordinary
`ExtResource(...)` entries. A generated `.tres` can also declare its own
deterministic `[ext_resource ...]` entries for narrow supported dependencies,
currently `LabelSettings.font`.

`StyleBoxFlat` resources are emitted as direct resource properties:

```text
[gd_resource type="StyleBoxFlat" format=3]

[resource]
bg_color = Color(0.08, 0.1, 0.12, 1.0)
border_color = Color(0.3, 0.45, 0.55, 1.0)
border_width_bottom = 2
border_width_left = 2
border_width_right = 2
border_width_top = 2
corner_radius_bottom_left = 6
corner_radius_bottom_right = 6
corner_radius_top_left = 6
corner_radius_top_right = 6
```

## Godot-assisted Emission

Direct text emission is enough for current simple scenes. Add a Godot-assisted
emitter later only for resources that are brittle to write by hand, such as
TileSets, Themes, ShaderMaterials, complex Mesh data, or imported resources.
