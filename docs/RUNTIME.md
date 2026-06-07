# Runtime Strategy

## Decision

Runtime is Godot 4 + GDScript.

Python is not part of the game runtime in MVP.

## Why

The project goal is to reduce Godot editor boilerplate and make scene/project construction declarative and repeatable. It is not to replace the Godot runtime.

Using Python inside Godot would create large problems:
- export complexity;
- platform-specific packaging;
- dependency management inside game builds;
- CPython runtime overhead;
- GIL concerns;
- binding stability issues;
- harder debugging;
- less native Godot workflow.

## Accepted runtime model

```text
Python DSL/build step
    ↓
Generated Godot files
    ↓
Godot runtime executes GDScript/native engine code
```

## GDScript role

GDScript is the primary gameplay glue language.

Allowed:
- generated `.gd` files;
- raw GDScript body strings in Python DSL;
- template-generated scripts later;
- user-authored manual GDScript scripts referenced by Python DSL;
- generated signal connections.

## GDExtension role

GDExtension is not part of MVP.

Future use:
- heavy simulation;
- pathfinding;
- procedural generation hot paths;
- combat calculations;
- geometry/mesh processing;
- Rust/C++ acceleration.

Python should not be routed through GDExtension for runtime.

## Explicitly out of scope for MVP

- Python GDExtension runtime;
- godot-python dependency;
- Python subset transpilation to GDScript;
- AST compiler from Python to GDScript;
- runtime construction of all scenes from Python-like descriptors;
- Python scripting inside exported games.

## Script generation strategy

Start simple:

```python
Script(
    path="res://scripts/main.gd",
    extends="Node2D",
    body="""
func _ready() -> void:
    print("ready")
""",
)
```

Then add:
- `Script.from_file(...)`;
- `Script.template(...)`;
- `Script.reference(...)` for manual scripts that should not be generated.

Do not build a Python-to-GDScript transpiler unless a later explicit decision reverses this.
