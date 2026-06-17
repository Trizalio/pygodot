# LD49 spell card example

This example is a narrow LD49-style spell visual slice. It uses the generic
`sub_resource(...)` API to generate a scene-local `ShaderMaterial` that
references an external `Shader`, then places it on a `ColorRect`.

The second spell visual references a source-owned `.tres` `ShaderMaterial` with
`ext_resource(...)`. The `.tres` file is copied as an external resource; nested
dependencies are declared separately when pygodot should track or copy them.
