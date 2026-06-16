# Runtime Strategy

## Decision

Runtime is Godot 4 plus GDScript.

Python is design/build-time only. Python is not embedded in the generated game.

## Why

The project goal is to reduce Godot editor boilerplate and make project
generation declarative and repeatable. It is not to replace the Godot runtime.

Embedding Python in Godot would create export, packaging, dependency, GIL,
platform, and binding-stability problems.

## Accepted Runtime Model

```text
Python DSL/build step
  -> Generated Godot files
  -> Godot runtime executes GDScript/native engine code
```

## GDScript Role

GDScript is the gameplay glue language.

Allowed:

- generated `.gd` files;
- raw GDScript body strings in Python DSL;
- generated script bodies loaded from files under `source_root`;
- generated script bodies rendered from standard-library templates under
  `source_root`;
- user-authored manual GDScript files referenced by Python DSL;
- generated signal connections;

`Script.from_template(...)` uses Python `string.Template` only. It supports
`$name`, `${name}`, and `$$` escaping in text GDScript templates; it is not a
Python-to-GDScript compiler.

## Manual Scripts

Manual scripts are referenced explicitly:

```python
Script.reference(
    path="res://manual/player.gd",
    extends="CharacterBody2D",
)
```

Referenced scripts are emitted as external script resources in `.tscn` files,
but `Game.build()` does not write or overwrite the `.gd` file.

## Out Of Scope

- Python runtime inside Godot;
- `godot-python` dependency;
- Python GDExtension runtime;
- Python-to-GDScript transpilation;
- AST compiler from Python to GDScript;
- runtime construction of all scenes from Python descriptors.
