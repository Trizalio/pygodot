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

__scene__ = Scene(
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
                    signal("pressed", target=".", method="_on_start_pressed")
                ],
            ),
        ],
    ),
)