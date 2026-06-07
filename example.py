from pathlib import Path

from pygodot import Button, Game, Label, Node2D, Scene, Script, signal

ROOT = Path(__file__).parent

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
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=r"C:\godot\Godot_v4.6.3\Godot_v4.6.3-stable_win64.exe",
)

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "Main",
            script=main_script,
            children=[
                Label(
                    "Title",
                    text="Generated scene",
                    position=(80, 60),
                ),
                Button(
                    "StartButton",
                    text="Click me",
                    position=(80, 120),
                    signals=[
                        signal("pressed", target=".", method="_on_start_pressed"),
                    ],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
