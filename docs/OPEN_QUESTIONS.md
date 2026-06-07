# Open Questions

These are not settled yet. Do not implement large irreversible designs for them without an explicit decision.

## Q001 — Generated path policy

Options:

1. Generate directly into normal Godot paths:
   - `res://scenes/main.tscn`
   - `res://scripts/main.gd`

2. Generate into `.generated`:
   - `res://.generated/scenes/main.tscn`
   - `res://.generated/scripts/main.gd`

3. Generate into a temporary/build-only Godot project.

Current leaning:
- for MVP, generate a whole build directory project;
- later support generating into a persistent Godot project with strict overwrite markers.

## Q002 — Public node wrappers as functions or classes

Options:
- `Node2D(...)` as a function returning `Node`;
- `Node2D` as a dataclass subclass;
- generated typed wrappers from Godot API dump.

Current leaning:
- start with simple functions/classes;
- do not overbuild typed wrappers before the emitter and validation architecture is stable.

## Q003 — Property name mapping

Godot properties use names like `position`, `text`, `disabled`.

Question:
- should Python DSL preserve exact Godot property names;
- or provide Python aliases for awkward names?

Current leaning:
- preserve exact Godot property names in MVP;
- add aliases only with clear value.

## Q004 — Script ownership

How should scripts be represented?

Options:
- generated raw body;
- template-generated body;
- manual existing file reference;
- hybrid file with generated regions.

Current leaning:
- support generated raw body and manual references early;
- avoid generated regions until needed.

## Q005 — Godot version target

MVP should target Godot 4.x, likely current stable Godot 4.

Need to decide:
- minimum supported Godot 4 version;
- whether to support multiple `.tscn` variants;
- how to test compatibility.

## Q006 — Asset import strategy

Options:
- copy assets into build dir and run Godot import;
- reference assets already in a persistent Godot project;
- maintain an asset manifest.

Current leaning:
- for build-directory output, copy resources that exist under `source_root`;
- keep missing resources as references and record `copied=false` in the manifest;
- evolve the manifest before supporting persistent project cleanup.

## Q007 — Godot API validation

Should the project ingest Godot API dumps to validate properties/signals/types?

Current leaning:
- not in MVP;
- add later after direct emitter works.

## Q008 — CLI shape

Potential CLI:

```bash
pygodot build package.module:game
pygodot run package.module:game
pygodot editor package.module:game
```

But CLI is secondary to `Game` methods.
