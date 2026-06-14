# Timer Example

This example shows a built-in Godot `Timer` node connected through the regular
signal DSL.

`PulseTimer.timeout` calls `_on_pulse_timer_timeout()` on the root script. The
script increments a counter and changes a `ColorRect`, demonstrating that timer
nodes, generated signal connections, and file-backed GDScript work together.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
