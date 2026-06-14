# Open Questions

These questions remain open. Do not implement large irreversible designs for
them without an explicit decision.

## Q001 - Persistent Godot Project Output

Current builds generate a complete project under `Game.build_dir`.

Open question:

- should pygodot also support writing generated files into a persistent
  hand-edited Godot project?

If yes, generated paths, cleanup behavior, and overwrite policy need stronger
rules than the current build-directory workflow.

## Q002 - Godot API Validation

Should pygodot ingest Godot API dumps to validate property names, property
types, signal names, and resource types?

Current answer:

- not yet;
- examples and direct emitter stability come first.

## Q003 - Script Template Ergonomics

Raw GDScript bodies inside Python strings and `Script.from_file(...)` work for
current examples.

Open options:

- simple templates;
- generated helper snippets;
- better smoke-check error presentation.

Do not build a Python-to-GDScript transpiler.

## Q004 - Complex Resource Strategy

Direct text emission is fine for current scenes.

Open question:

- when should pygodot introduce direct `.tres` emission or a Godot-assisted
  emitter?

Likely trigger examples include physics shapes, TileSet, Theme, ShaderMaterial,
or Mesh data.

## Q005 - CLI Shape

The public workflow is library-first.

A future CLI could look like:

```bash
pygodot build package.module:game
pygodot run package.module:game
pygodot check package.module:game
```

The CLI should remain a thin wrapper around imported `Game` objects.

## Q006 - Supported Godot Versions

The current project is tested manually against Godot 4.6.x.

Open question:

- what minimum Godot 4 version should be supported?
- should snapshots or smoke checks vary by Godot version?
