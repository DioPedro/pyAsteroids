from OpenGL.GL import glCreateProgram, GL_VERTEX_SHADER, glLinkProgram, glGetProgramiv, glGetProgramInfoLog, GL_LINK_STATUS, glUseProgram, glClear, glClearColor, GL_COLOR_BUFFER_BIT, GL_FRAGMENT_SHADER, glBindFragDataLocation
import glfw

import json
from classes.Path import Path, curvePath, NAV_PATH, AMONG_PATH, AST_PATH
from classes.Shader import Shader
from classes.Object import Object
import classes.Transform as Transform
import numpy as np

t_y = 0
t_x = 0
r = 0
s = 0.15
ss = 0.15
sll = 0.1
r_step = 0.05
s_step = 0.01

ams = 0.05
ar = 0

points: list = []

star_tuples = [
    (0.1, (3, 3)),
    (0.08, (3, -3)),
    (0.05, (-3, -3)),
    (0.15, (-3, 3)),
]

window: any = None
program: any = None

BASE_COLOR = [98/255, 114/255, 164/255]

with open("vShader.glsl", "r") as f:
    VERTEX_CODE = f.read()

with open("fShader.glsl", "r") as f:
    FRAGMENT_CODE = f.read()


def key_event(window, key, scancode, action, mods):
    global t_x, t_y, r, ss

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
    if key == 45:
        ss -= s_step
    if key == 61:
        ss += s_step

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
            Transform.scale(ss, ss)
        ])
        context['star'].transform(starTransform)

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
        Transform.scale(0.3, 0.3),
        Transform.translate(*context['asteroid'].path.atPosition()),
        Transform.scale(s, s)
    ])
    context['asteroid'].transform(asteroidTransform)

    rocketTransform = Transform.stack([
        Transform.scale(s, s),
        Transform.rotate(r),
        Transform.translate(t_x, t_y)
    ])
    context['rocket'].transform(rocketTransform)

    glfw.swap_buffers(window)


def glfwInit():
    global window
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(600, 600, "Cores", None, None)
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    glfw.window_hint(glfw.MAXIMIZED, glfw.FALSE)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
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

    glBindFragDataLocation(program, 0, "outColor")
    glUseProgram(program)

    del vertexShader, fragShader


def initElements():
    sceneObjs = dict()
    data = None

    with open('./objects.json', 'r') as fp:
        data = json.load(fp)
    sceneObjs['rocket'] = Object(program, [], None)
    for element in data['rocket']['elements']:
        sceneObjs["rocket"].addElement(element["points"], element["color"] or BASE_COLOR)

    sceneObjs['spaceship'] = Object(program, [], Path(curvePath(NAV_PATH, [10]), 0))
    for element in data['spaceship']["elements"]:
        sceneObjs["spaceship"].addElement(element["points"], element["color"])

    sceneObjs['amongus'] = Object(program, [], Path(curvePath(AMONG_PATH, [16, 9]), 0))
    for element in data['amongus']["elements"]:
        sceneObjs["amongus"].addElement(element["points"], element["color"])

    sceneObjs['star'] = Object(program, [], None)
    for element in data['star']["elements"]:
        sceneObjs['star'].addElement(element["points"], element["color"])

    sceneObjs['asteroid'] = Object(program, [], Path(curvePath(AST_PATH, [5]), 0))
    for element in data['asteroid']["elements"]:
        sceneObjs['asteroid'].addElement(element["points"], element["color"])

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
