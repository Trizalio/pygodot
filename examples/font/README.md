# Font Resource Example

This example shows source-owned font resources copied into the generated
project and assigned to `Label` nodes.

`display_font.tres` is a small `FontVariation` resource. The
`WDXLLubrifontTC-Regular.ttf` file is a Google Fonts font under the OFL license.
`game.py` references both with `font(...)` and sets `theme_override_fonts/font`
on labels.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
