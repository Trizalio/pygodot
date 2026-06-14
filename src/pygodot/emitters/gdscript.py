"""Emitter for generated GDScript files."""

import inspect

from pygodot.ir.model import IRScript


class GdScriptEmitter:
    def emit(self, script: IRScript) -> str:
        body = script.body.strip("\n") if script.source is not None else inspect.cleandoc(script.body)
        if body:
            return f"extends {script.extends}\n\n{body}\n"
        return f"extends {script.extends}\n"
