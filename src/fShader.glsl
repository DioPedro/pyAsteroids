#version 430

uniform vec4 color;
in wPos;

void main() {
    gl_FragColor = color * distance(vec4(wPos, 0.0, 1.0), vec4(0.0, 0.0, 0.0, 0.0));
}
