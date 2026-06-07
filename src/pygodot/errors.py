"""Project-specific exceptions."""


class PyGodotError(Exception):
    """Base class for pygodot errors."""


class ValidationError(PyGodotError):
    """Raised when DSL or IR validation fails."""


class EmitError(PyGodotError):
    """Raised when a Godot file cannot be emitted."""


class BuildError(PyGodotError):
    """Raised when build orchestration fails."""


class GodotCliError(PyGodotError):
    """Raised when invoking the Godot CLI fails."""
