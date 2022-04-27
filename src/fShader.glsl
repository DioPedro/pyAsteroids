#version 430

uniform vec4 color;
in vec2 wPos;
out vec4 outColor;

void main() {
    outColor = color;
}
