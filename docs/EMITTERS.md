# Emitters

Emitters convert normalized IR into Godot files.

MVP emitters:
- `ProjectEmitter` for `project.godot`;
- `TscnEmitter` for `.tscn` scene files;
- `GdScriptEmitter` for `.gd` script files.

## Emitter design rules

1. Emitters consume normalized IR, not raw public DSL objects.
2. Emitters should be deterministic.
3. Emitters should not perform broad validation. Validation belongs before emission.
4. Emitters should not mutate input.
5. File writing should be separate from string generation where practical.

## `.tscn` MVP support

The direct `.tscn` emitter should support:
- `[gd_scene format=3]` header;
- `[ext_resource ...]` for scripts and later textures/resources;
- `[node ...]` sections;
- node properties;
- signal `[connection ...]` sections;
- stable resource IDs;
- deterministic property/resource ordering.

## `.tscn` example target

```text
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/main.gd" id="Script_scripts_main_gd"]

[node name="Main" type="Node2D"]
script = ExtResource("Script_scripts_main_gd")

[node name="Title" type="Label" parent="."]
text = "Generated scene"
position = Vector2(80, 60)

[node name="StartButton" type="Button" parent="."]
text = "Click me"
position = Vector2(80, 120)

[connection signal="pressed" from="StartButton" to="." method="_on_start_pressed"]
```

## Value serialization

Do not keep tuple inference as the long-term design.

MVP may support:

```python
(80, 60) -> Vector2(80, 60)
(1, 2, 3) -> Vector3(1, 2, 3)
```

But add explicit wrappers early:

```python
Vec2(80, 60)
Vec3(1, 2, 3)
Rect2(0, 0, 16, 32)
Color(1, 1, 1, 1)
NodePath("../Player")
ext_resource("res://assets/player.png", type="Texture2D")
texture("res://assets/player.png")
packed_scene("res://scenes/menu.tscn")
```

Public `ext_resource(...)` values are normalized into IR external resources and
internal resource references before emission. Identical resources are deduplicated
by `(type, path)`, so two references to the same texture share one `[ext_resource]`
entry while different Godot resource types with the same path remain distinct.

## Resource IDs

Resource IDs must be stable across runs.

Acceptable strategy for MVP:

```text
Script_scripts_main_gd
Texture2D_assets_player_png
PackedScene_scenes_menu_tscn
```

Hash-based IDs are also acceptable if deterministic and readable enough.

Avoid incremental IDs such as:

```text
Script_1
Script_2
Script_3
```

They cause noisy diffs.

## Godot-assisted emitter later

Direct text emission is good for simple scenes but can become fragile for complex resources.

Later add a Godot-assisted emitter that:
- writes a temporary GDScript generation script;
- runs Godot headless;
- asks Godot to instantiate resources/scenes;
- saves them using Godot's own resource saver.

Use this only where direct emission is too brittle.

Likely candidates:
- AnimationPlayer data;
- TileSet/TileMap resources;
- Theme resources;
- ShaderMaterial resources;
- complex imported resources;
- Mesh/ArrayMesh data.

## `project.godot` emitter

MVP fields:
- `config_version=5`;
- application name;
- main scene.
- keyboard-only input map actions.

Future fields:
- autoloads;
- display/window settings;
- rendering settings;
- physics settings;
- application icon;
- export metadata.

## GDScript emitter

MVP GDScript emission can be raw body-based:

```python
Script(path="res://scripts/main.gd", extends="Node2D", body="...")
```

Generated output:

```gdscript
extends Node2D

...
```

Future:
- templates;
- generated signal handlers;
- optional linter/formatter integration;
- manual script references.
