# Declarative DSL Design

The DSL should be Pythonic, explicit, typed, and IDE-friendly.

## Design principles

1. Ordinary Python object construction.
2. No mandatory context managers.
3. No metaclass-heavy API.
4. No hidden global scene stack.
5. Good autocomplete and type hints.
6. Easy composition through functions.
7. Public DSL objects are not the same as normalized compiler IR.

## MVP object model

Required public concepts:

```text
Game
Scene
Node
Script
SignalConnection
Godot value wrappers
ExternalResource
```

Node constructors/classes:

```text
Node2D
Control
Label
Button
Sprite2D later
Camera2D later
CharacterBody2D later
```

## Example scene

```python
from pathlib import Path
from pygodot import Game, Scene, Node2D, Label, Button, Script, signal

main_script = Script(
    path="res://scripts/main.gd",
    extends="Node2D",
    body="""
var counter := 0

func _ready() -> void:
    $Title.text = "Generated from Python DSL"

func _on_start_pressed() -> void:
    counter += 1
    $Title.text = "Clicked %s times" % counter
""",
)

game = Game(
    name="GeneratedGame",
    source_root=Path(__file__).parent,
    build_dir=Path(__file__).parent / "build" / "godot",
    main_scene="res://scenes/main.tscn",
)

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "Main",
            script=main_script,
            children=[
                Label("Title", text="Generated scene", position=(80, 60)),
                Button(
                    "StartButton",
                    text="Click me",
                    position=(80, 120),
                    signals=[signal("pressed", target=".", method="_on_start_pressed")],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.build()
    game.run()
```

## Node API direction

A basic node should support:

```python
Node(
    name="Main",
    type="Node2D",
    props={"position": Vec2(80, 60)},
    children=[...],
    script=Script(...),
    signals=[...],
)
```

Convenience wrappers should map to specific Godot classes:

```python
Node2D("Main", position=Vec2(10, 20))
Label("Title", text="Hello")
Button("Start", text="Start")
```

## Properties

MVP may accept keyword properties:

```python
Label("Title", text="Hello", position=(80, 60))
```

However, explicit value wrappers should be added early:

```python
Label("Title", text="Hello", position=Vec2(80, 60))
```

Do not rely forever on tuple length inference.

External resources can be referenced from properties explicitly:

```python
from pygodot import ext_resource

Node2D(
    "IconOwner",
    icon=ext_resource("res://assets/icon.svg", type="Texture2D"),
)
```

Normalization collects these references into scene external resources and replaces
the property value with an internal resource reference for the `.tscn` emitter.

## Signals

Preferred MVP syntax:

```python
Button(
    "StartButton",
    text="Start",
    signals=[
        signal("pressed", target=".", method="_on_start_pressed"),
    ],
)
```

Future syntax may allow:

```python
Button("StartButton", text="Start").on("pressed", target=".", method="_on_start_pressed")
```

But avoid hidden mutation that makes trees difficult to inspect.

## Scripts

MVP supports raw GDScript body generation:

```python
Script(
    path="res://scripts/player.gd",
    extends="CharacterBody2D",
    body="""
func _physics_process(delta: float) -> void:
    pass
""",
)
```

Future support:
- loading body from file;
- Jinja-like templates;
- generated boilerplate from structured definitions;
- manual script references without generation.

Do not implement Python-to-GDScript transpilation in MVP.

## Composition examples

The DSL should encourage normal Python functions:

```python
def menu_button(name: str, text: str, y: int, method: str) -> Button:
    return Button(
        name,
        text=text,
        position=Vec2(80, y),
        signals=[signal("pressed", target=".", method=method)],
    )
```

Scene factories are encouraged:

```python
def make_main_menu() -> Scene:
    return Scene(
        path="res://scenes/main_menu.tscn",
        root=Control("MainMenu", children=[
            Label("Title", text="Slay The Eldritch"),
            menu_button("NewGame", "New Game", 120, "_on_new_game"),
            menu_button("Exit", "Exit", 180, "_on_exit"),
        ]),
    )
```
