# Script Template Example

This example renders generated GDScript from a standard-library
`string.Template` file.

The template uses `$title`, `${count}`, and `$$StatusLabel`. The doubled dollar
is required when a literal Godot node shorthand such as `$StatusLabel` should
survive template rendering.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
