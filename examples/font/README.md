# Font Resource Example

This example shows a source-owned Godot font resource copied into the generated
project and assigned to a `Label`.

`display_font.tres` is a small `FontVariation` resource under
`examples/font/assets`. `game.py` references it with `font(...)` and sets
`theme_override_fonts/font` on the title label.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
