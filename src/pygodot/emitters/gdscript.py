"""Emitter for generated GDScript files."""

import inspect

from pygodot.ir.model import IRScript


class GdScriptEmitter:
    def emit(self, script: IRScript) -> str:
        body = inspect.cleandoc(script.body)
        if body:
            return f"extends {script.extends}\n\n{body}\n"
        return f"extends {script.extends}\n"
