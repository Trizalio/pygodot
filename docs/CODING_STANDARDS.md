# Coding Standards

## Python version

Use Python 3.11+ style.

Preferred typing:

```python
def foo(value: int | None) -> list[str]: ...
```

Prefer built-in generics:

```python
list[str]
dict[str, int]
```

Avoid old style unless compatibility requires it:

```python
Optional[int]
List[str]
Dict[str, int]
```

## Data models

Start with `dataclasses` for public DSL and IR unless there is a clear reason to add a heavier dependency.

Recommended:

```python
@dataclass(slots=True)
class Scene:
    path: str
    root: Node
```

Use frozen dataclasses for normalized IR if mutation becomes a problem.

## Dependencies

Keep dependencies minimal.

Current tests use `unittest` and do not require extra dependencies.

Possible later dependencies:
- `typer` only if/when CLI becomes useful;
- `ruff` for lint/format if the project adopts it.

Do not add Pydantic unless validation requirements justify it.

## Public API

Prefer explicit constructors and functions.

Avoid:
- metaclass-based DSL;
- mandatory context manager DSL;
- global implicit scene stacks;
- import-time side effects;
- monkey-patching user modules.

## Error handling

Create project-specific exceptions:

```python
class PyGodotError(Exception): ...
class ValidationError(PyGodotError): ...
class EmitError(PyGodotError): ...
class GodotCliError(PyGodotError): ...
```

Errors should include scene path and node path where possible.
For property/resource/script errors, include the smallest useful context:
scene path, node path, property name, resource path, script path, and value type
where relevant.

Bad:

```text
Unsupported value
```

Better:

```text
Unsupported value for property 'position' at res://scenes/main.tscn:Main/Title: <value repr>
```

Current style:

```text
Unsupported value for property 'position': scene='res://scenes/main.tscn', node='Title', value=<...>, value_type=...
```

## Generated files

Generated files should include a marker/header where the target format supports comments.

Generated writer should refuse to overwrite files that lack the marker unless explicitly configured.

## Formatting generated text

Generated output should be readable and deterministic.

Rules:
- stable section order;
- stable property order;
- stable resource order;
- final newline at end of file;
- avoid trailing whitespace;
- avoid timestamps in generated files.

## Module boundaries

Do not put all compiler logic in `Game`.

`Game` orchestrates. Emitters emit. Validators validate. Normalizers normalize.
