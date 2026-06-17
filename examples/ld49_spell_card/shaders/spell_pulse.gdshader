shader_type canvas_item;

uniform vec4 tint : source_color = vec4(0.4, 0.85, 1.0, 1.0);
uniform float pulse = 0.5;

void fragment() {
    vec2 centered_uv = UV - vec2(0.5);
    float ring = smoothstep(0.40, 0.25, length(centered_uv));
    float shimmer = 0.75 + 0.25 * sin((UV.x + UV.y + pulse) * 12.0);
    COLOR = vec4(tint.rgb * shimmer, tint.a * ring);
}
