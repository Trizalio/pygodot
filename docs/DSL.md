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
- Godot value wrappers;
- external resource references;
- scene instances.

Node constructors/helpers:

- `node(name, type, ...)` for arbitrary Godot node classes;
- `Node2D`;
- `Control`;
- `ColorRect`;
- `Sprite2D`;
- `Label`;
- `Button`;
- `Timer`.

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
```

Temporary tuple inference exists for simple vectors, but new examples should use
explicit wrappers.

External resources are referenced explicitly:

```python
Sprite2D("Logo", texture=texture("res://assets/logo.svg"))
Node2D("Other", resource=ext_resource("res://assets/data.tres", type="Resource"))
```

Normalization collects external resources into scene resource tables and
deduplicates them by `(type, path)`. During `Game.build()`, existing source
files under `Game.source_root` are copied to matching `res://` paths under
`build_dir` and recorded in the manifest.

Generated scenes can also be reused as `PackedScene` instances:

```python
gem_scene = packed_scene("res://scenes/gem.tscn")

Node2D(
    "Main",
    children=[
        scene_instance("GemA", gem_scene, position=Vec2(220, 190)),
        scene_instance("GemB", gem_scene, position=Vec2(320, 150)),
    ],
)
```

`scene_instance(...)` expects a `PackedScene` resource, normally created with
`packed_scene(...)`.

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

Manual scripts are referenced without generation:

```python
Script.reference("res://manual/player.gd", extends="CharacterBody2D")
```

Referenced manual scripts are included in generated `.tscn` files as external
script resources, but `Game.build()` does not write the `.gd` file.

## Input Actions

Keyboard input actions are declared on `Game` and emitted into `project.godot`:

```python
game.add_input_action("left_up", keys=["W"])
game.add_input_action("right_up", keys=["UP"])
game.add_input_action("restart", keys=["SPACE"])
```

Generated GDScript should use Godot's InputMap APIs:

```gdscript
Input.is_action_pressed("left_up")
Input.is_action_just_pressed("restart")
```

The current InputMap DSL is keyboard-only.

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
