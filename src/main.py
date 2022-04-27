from OpenGL.GL import glCreateProgram, GL_VERTEX_SHADER, glLinkProgram, glGetProgramiv, glGetProgramInfoLog, GL_LINK_STATUS, glUseProgram, glClear, glClearColor, GL_COLOR_BUFFER_BIT, GL_FRAGMENT_SHADER
import glfw

from classes.Path import Path, curvePath, NAV_PATH, AMONG_PATH
from classes.Shader import Shader
from classes.Object import Object
import classes.Transform as Transform
import numpy as np

t_y = 0
t_x = 0
r = 0
s = 0.15
sll = 0.1
r_step = 0.05
s_step = 0.01

ams = 0.05
ax = [i/1000 for i in range(-50000, 51000, 50)]
ay = [i/1000 for i in range(50000, -51000, -50)]
ar = 0

points: list = []

star_tuples = [
    (0.1, (3, 3)),
    (0.3, (3, -3)),
    (0.05, (-3, -3)),
    (0.15, (-3, 3))
]

window: any = None
program: any = None

BASE_COLOR = [98/255, 114/255, 164/255]

VERTEX_CODE = """
attribute vec2 position;
uniform mat4 mat_transformation;

void main() {
    gl_Position = mat_transformation * vec4(position, 0.0, 1.0);
}
"""

FRAGMENT_CODE = """
uniform vec4 color;

void main() {
    gl_FragColor = color;
}
"""


def key_event(window, key, scancode, action, mods):
    global t_x, t_y, r

    if key == 87:
        t_y += 0.01  # cima
        r = 0
    if key == 83:
        t_y -= 0.01  # baixo
        r = r_step * 64
    if key == 65:
        t_x -= 0.01  # esquerda
        r = r_step * 32
    if key == 68:
        t_x += 0.01  # direita
        r = -r_step * 32
    if key == 69:  # diagonal superior direita (1° quadrante)
        t_y += 0.01
        t_x += 0.01
        r = -r_step * 16
    if key == 81:  # diagonal superior esquerda (2° quadrante)
        t_y += 0.01
        t_x -= 0.01
        r = r_step * 16
    if key == 90:  # diagonal inferior esquerda (3° quadrante)
        t_y -= 0.01
        t_x -= 0.01
        r = r_step * 48
    if key == 67:  # diagonal inferior direita (4° quadrante)
        t_y -= 0.01
        t_x += 0.01
        r = -r_step * 48
    if scancode == 24:
        r += r_step
    if scancode == 26:
        r -= r_step


def multiplica_matriz(a: np.ndarray, b: np.ndarray):
    m_a = a.reshape(4, 4)
    m_b = b.reshape(4, 4)
    m_c = np.dot(m_a, m_b)
    c = m_c.reshape(1, 16)
    return c


def display(
        context: dict,
        window: any
):
    global ar
    glfw.poll_events()

    glClearColor(BASE_COLOR[0], BASE_COLOR[1], BASE_COLOR[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    for scale, pos in star_tuples:
        starTransform = Transform.stack([
            Transform.scale(scale, scale),
            Transform.translate(*pos),
            Transform.scale(s, s)
        ])
        context['star'].transform(starTransform)

    rocketTransform = Transform.stack([
        Transform.scale(s, s),
        Transform.rotate(r),
        Transform.translate(t_x, t_y)
    ])
    context['rocket'].transform(rocketTransform)

    spaceshipTransform = Transform.stack([
        Transform.translate(*context['spaceship'].path.atPosition()),
        Transform.scale(sll, sll)
    ])
    context['spaceship'].transform(spaceshipTransform)

    amongusTransform = Transform.stack([
        Transform.rotate(ar),
        Transform.translate(*context['amongus'].path.atPosition()),
        Transform.scale(ams, ams)
    ])
    context['amongus'].transform(amongusTransform)
    ar += 0.02

    asteroidTransform = Transform.stack([
        Transform.translate(0.5, 0.5),
        Transform.scale(s, s)
    ])
    context['asteroid'].transform(asteroidTransform)

    glfw.swap_buffers(window)


def glfwInit():
    global window
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(600, 600, "Cores", None, None)
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    glfw.window_hint(glfw.MAXIMIZED, glfw.FALSE)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_event)
    glfw.show_window(window)


def glInit():
    global program
    program = glCreateProgram()
    vertexShader = Shader(VERTEX_CODE, GL_VERTEX_SHADER)
    fragShader = Shader(FRAGMENT_CODE, GL_FRAGMENT_SHADER)
    vertexShader.attach(program)
    fragShader.attach(program)

    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')

    glUseProgram(program)

    del vertexShader, fragShader


def initElements():
    sceneObjs = dict()

    # Paleta de cores: https://github.com/dracula/dracula-theme
    sceneObjs['rocket'] = Object(program, [], None)
    sceneObjs['rocket'].addElement([
        (0.0, +0.5),
        (-0.5, -0.5),
        (0, -0.25),
        (+0.5, -0.5),
    ], BASE_COLOR)
    sceneObjs['rocket'].addElement([
        (+0.5, -0.5),
        (-0.5, -0.5),
        (0, -0.25),
        (0.0, +0.5),
    ], [1, 121/255, 198/255])

    sceneObjs['spaceship'] = Object(
        program,
        [],
        Path(curvePath(NAV_PATH, [10]), 0)
    )
    sceneObjs['spaceship'].addElement([
        (-1.0, 0.0),
        (-0.7, 0.5),
        (0.7, 0.5),
        (1.0, 0.0),
        (0.5, -0.5),
        (-0.5, -0.5),
    ], [0.38431, 0.44705, 0.64313])
    sceneObjs['spaceship'].addElement([
        (-0.5, 0.5),
        (-0.4, 0.7),
        (-0.2, 0.8),
        (0, 0.85),
        (0.2, 0.8),
        (0.4, 0.7),
        (0.5, 0.5),
    ], [80/255, 250/255, 123/255])

    sceneObjs['amongus'] = Object(
        program,
        [],
        Path(curvePath(AMONG_PATH, [16, 9]), 0)
    )
    sceneObjs['amongus'].addElement([
        (-1.37, 1.02),
        (-1.15, 1.44),
        (-0.83, 1.79),
        (0, 1.79),
        (0.5, 1.4),
        (0.78, 0.78),
        (0.82, -1.97),
        (0.6, -2.2),
        (0.18, -2.2),
        (-0.18, -1.99),
        (-0.6, -2.19),
        (-1.03, -2.22),
        (-1.29, -2),
        (-1.38, 0),
        (-0.63, 0.13),
        (-0.41, 0.61),
        (-0.75, 0.97),
        (-1.37, 1.02),
        (-1.83, 0.99),
        (-2.12, 0.64),
        (-1.97, 0.18),
        (-1.38, 0),
        (-0.63, 0.13),
        (-0.41, 0.61),
        (-0.75, 0.97),
        (-1.37, 1.02)
    ], [1, 0.3333, 0.333])  # Corpo
    sceneObjs['amongus'].addElement([
        (-1.38, 0),
        (-0.63, 0.13),
        (-0.41, 0.61),
        (-0.75, 0.97),
        (-1.37, 1.02),
        (-1.83, 0.99),
        (-2.12, 0.64),
        (-1.97, 0.18),
        (-1.38, 0)
    ], [0.38431, 0.44705, 0.64313])  # Visor
    sceneObjs['amongus'].addElement([
        (0.8, -1.29),
        (1.42, -1.29),
        (1.77, -0.78),
        (1.74, 0.19),
        (1.42, 0.7),
        (0.78, 0.78)
    ], [68/255, 71/255, 90/255])  # Backpack

    sceneObjs['star'] = Object(program, [], None)
    sceneObjs['star'].addElement([
        (-2, 0),
        (0, 4),
        (2, 0),
        (0, -4)
    ], [241/255, 250/255, 140/255])  # Star

    sceneObjs['asteroid'] = Object(program, [], None)
    sceneObjs['asteroid'].addElement([
        (-4, 0),
        (-3.62, -0.88),
        (-2.94, -1.6),
        (-1.52, -2.42),
        (-0.32, -2.5),
        (0.84, -2.16),
        (1.74, -1.58),
        (1.6, -0.76),
        (2.18, -0.34),
        (2.54, 0.62),
        (2.14, 1.3),
        (1.66, 2.02),
        (1.46, 2.92),
        (0.48, 3.34),
        (-0.22, 2.78),
        (-1, 3),
        (-1.64, 3.32),
        (-2.2, 2.76),
        (-2, 2),
        (-2.9, 2.26),
        (-3.66, 1.82),
        (-3.68, 1.2),
        (-3.32, 0.4)
    ], [68/255, 71/255, 90/255])  # Asteroid

    return sceneObjs


def main():
    glfwInit()
    glInit()
    sceneObjs = initElements()
    while not glfw.window_should_close(window):
        display(
            sceneObjs,
            window
        )

    glfw.terminate()


main()
