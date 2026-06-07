# `pygodot` Codex Context

This is a directive bundle for starting `pygodot`: a Python 3 library for declaratively generating native Godot 4 projects.

The most important file is `AGENTS.md`. Put it at the repository root so Codex reads it as project instructions.

Recommended placement:

```text
<repo>/AGENTS.md
<repo>/README_CODEX.md
<repo>/docs/DECISIONS.md
<repo>/docs/ARCHITECTURE.md
<repo>/docs/DSL.md
<repo>/docs/GAME_API.md
<repo>/docs/EMITTERS.md
<repo>/docs/RUNTIME.md
<repo>/docs/ROADMAP.md
<repo>/docs/TESTING.md
<repo>/docs/CODING_STANDARDS.md
<repo>/docs/OPEN_QUESTIONS.md
<repo>/docs/CODEX_TASKS.md
```

Core direction:

```text
Python DSL/build-time library → typed IR → direct .tscn/.gd/project.godot emitters → normal Godot 4 runtime
```

Key constraints:
- no JSON/YAML main IR;
- no Python runtime inside Godot;
- no Python-to-GDScript transpiler in MVP;
- no metaclass/context-manager DSL magic;
- library-first API with `Game` object;
- CLI only as a thin wrapper later;
- deterministic generated output;
- snapshot tests for generated files.
