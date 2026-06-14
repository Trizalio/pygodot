# Emitters

Emitters convert normalized IR into deterministic Godot text files.

Current emitters:

- `ProjectEmitter` for `project.godot`;
- `TscnEmitter` for `.tscn` scene files;
- `GdScriptEmitter` for `.gd` script files.

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
- `[node ...]` sections;
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

## Values

Supported values include:

- `str`, `bool`, `None`, `int`, `float`;
- `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`;
- two- and three-item tuples as temporary Vector2/Vector3 convenience;
- lists and dictionaries of supported values;
- normalized external resource references.

Prefer explicit value wrappers in new examples.

## Resource IDs

Resource IDs are deterministic and readable:

```text
Script_scripts_main_gd
Texture2D_assets_player_png
PackedScene_scenes_menu_tscn
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

The GDScript emitter wraps raw generated bodies with an `extends` line:

```python
Script(path="res://scripts/main.gd", extends="Node2D", body="...")
```

Output:

```gdscript
extends Node2D

...
```

Manual scripts are referenced with `Script.reference(...)` and are not emitted.

## Godot-assisted Emission

Direct text emission is enough for current simple scenes. Add a Godot-assisted
emitter later only for resources that are brittle to write by hand, such as
AnimationPlayer data, TileSets, Themes, ShaderMaterials, complex Mesh data, or
imported resources.
