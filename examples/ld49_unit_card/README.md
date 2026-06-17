# LD49 unit card example

This example is a narrow LD49-style unit scene slice. It uses generic
`sub_resource(...)` declarations for `AtlasTexture` frames and a `SpriteFrames`
resource, then attaches those frames to an `AnimatedSprite2D` node declared with
`node(...)`.

The spawn/death audio players use copied source assets. Runtime behavior remains
ordinary file-backed GDScript.
