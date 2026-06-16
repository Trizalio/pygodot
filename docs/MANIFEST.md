# Build Manifest

Every `Game.build()` writes a generated manifest at:

```text
res://.pygodot/manifest.json
```

The manifest is a readable build artifact. It records which files pygodot wrote,
which resources were copied, and which resources remain user-owned references.
It is not a persistent project database and should not be edited by hand.

## Top-Level Fields

- `generated_files`: every file written by pygodot under `build_dir`, including
  `project.godot`, generated scenes, generated scripts, generated resources,
  and `.pygodot/manifest.json`.
- `generated_scenes`: generated `.tscn` files.
- `generated_scripts`: generated `.gd` files emitted from inline, file-backed,
  or template-backed generated scripts.
- `generated_resources`: generated `.tres` resources.
- `external_resources`: Godot `ExtResource` dependencies discovered while
  normalizing scenes and generated resources.

All path lists are relative to the generated Godot project root and are sorted
deterministically.

## External Resources

Each `external_resources` entry has:

- `type`: Godot resource type, such as `Script`, `Texture2D`, `Font`, or
  `LabelSettings`.
- `path`: the `res://` path referenced by generated Godot files.
- `id`: the stable resource ID used in generated `.tscn` or `.tres` text.
- `copied`: `true` when pygodot copied a source-owned file into `build_dir`.
- `ownership`: one of the ownership values below.

External resource entries are sorted deterministically by type, path, and ID.

## Ownership Values

- `generated`: pygodot emitted the referenced resource. This includes generated
  scripts, generated scenes referenced as `PackedScene`, and generated `.tres`
  resources.
- `copied`: pygodot copied an existing file from `source_root` into `build_dir`.
  The source file remains user-owned.
- `referenced`: pygodot referenced the resource but did not write or copy it.
  This is used for manual scripts and for assets/resources managed outside the
  generated build output.

## Contract Boundaries

The manifest is generated metadata. Its current shape is useful for inspection
and tests, but source projects should keep the Python DSL, manual scripts, and
manual assets as the source of truth.

`pygodot` does not use the manifest for cleanup or pruning yet. Deleting stale
generated files remains a user or build-directory management concern.
