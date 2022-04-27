#version 430

in vec2 position;
uniform mat4 mat_transformation;

out vec2 wPos;

void main() {
    wPos = position;
    gl_Position = mat_transformation * vec4(position, 0.0, 1.0);
}
