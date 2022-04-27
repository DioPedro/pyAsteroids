#version 430

uniform vec4 color;
in vec2 wPos;
out vec4 outColor;

void main() {
    // outColor = color * distance(vec4(wPos, 0.0, 1.0), vec4(0.0, 0.0, 0.0, 0.0));
    outColor = color * 0.1;
}
