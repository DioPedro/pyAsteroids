from OpenGL.GL import glCreateProgram, GL_VERTEX_SHADER, glLinkProgram, glGetProgramiv, glGetProgramInfoLog, GL_LINK_STATUS, glUseProgram, glClear, glClearColor, GL_COLOR_BUFFER_BIT, GL_FRAGMENT_SHADER, glBindFragDataLocation
import glfw

import json
from classes.Path import Path, curvePath, NAV_PATH, AMONG_PATH, AST_PATH
from classes.Shader import Shader
from classes.Object import Object
import classes.Transform as Transform
import numpy as np

FRAME_RATE = 60
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

t_y = 0
t_x = 0
# r = 0
s = 0.15
ss = 0.15
sll = 0.1
r_step = 0.1
s_step = 0.01

ams = 0.05
ar = 0

points: list = []

star_tuples = [
    (0.1, (2, 3)),
    (0.08, (3, -3.4)),
    (0.05, (-5, -2.6)),
    (0.15, (-3, 4)),
    (0.04, (0.14, 0.2)),
]

window: any = None
program: any = None

BASE_COLOR = [98/255, 114/255, 164/255]

with open("vShader.glsl", "r") as f:
    VERTEX_CODE = f.read()

with open("fShader.glsl", "r") as f:
    FRAGMENT_CODE = f.read()


def key_event(window, key, scancode, action, mods):
    global t_x, t_y, ss

    if scancode == 25:
        t_y += 0.01  # cima
    if scancode == 39:
        t_y -= 0.01  # baixo
    if scancode == 38:
        t_x -= 0.01  # esquerda
    if scancode == 40:
        t_x += 0.01  # direita
    if key == 45:
        ss -= s_step
    if key == 61:
        ss += s_step


def display(
        context: dict,
        window: any
):
    global ar
    glfw.poll_events()

    glClearColor(BASE_COLOR[0], BASE_COLOR[1], BASE_COLOR[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    mX, mY = glfw.get_cursor_pos(window)
    mX = min(mX, WINDOW_WIDTH)
    mX = max(mX, 0)
    mY = WINDOW_HEIGHT - min(mY, WINDOW_HEIGHT)
    mY = max(mY, 0)
    mX -= WINDOW_WIDTH/2
    mY -= WINDOW_HEIGHT/2
    mX /= WINDOW_WIDTH/2
    mY /= WINDOW_HEIGHT/2

    dx = mX - t_x
    dy = mY - t_y
    r = np.arctan2(dy, dx) - 0.5*np.pi

    for scale, pos in star_tuples:
        starTransform = Transform.stack([
            Transform.scale(scale*2, scale*2),
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
        Transform.translate(t_x, t_y),
    ])
    context['rocket'].transform(rocketTransform)

    glfw.swap_buffers(window)


def glfwInit():
    global window
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        "Amongus",
        None,
        None
    )
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
        sceneObjs["rocket"].addElement(
            element["points"],
            element["elementList"],
            element["color"] or BASE_COLOR
        )

    sceneObjs['spaceship'] = Object(
        program,
        [],
        Path(curvePath(NAV_PATH, [10]), 0)
    )
    for element in data['spaceship']["elements"]:
        sceneObjs["spaceship"].addElement(
            element["points"],
            element["elementList"],
            element["color"] or BASE_COLOR
        )

    sceneObjs['amongus'] = Object(
        program,
        [],
        Path(curvePath(AMONG_PATH, [16, 9]), 0)
    )
    for element in data['amongus']["elements"]:
        sceneObjs["amongus"].addElement(
            element["points"],
            element["elementList"],
            element["color"] or BASE_COLOR
        )

    sceneObjs['star'] = Object(program, [], None)
    for element in data['star']["elements"]:
        sceneObjs['star'].addElement(
            element["points"],
            element["elementList"],
            element["color"] or BASE_COLOR
        )

    sceneObjs['asteroid'] = Object(
        program,
        [],
        Path(curvePath(AST_PATH, [10]), 0)
    )
    for element in data['asteroid']["elements"]:
        sceneObjs['asteroid'].addElement(
            element["points"],
            element["elementList"],
            element["color"] or BASE_COLOR
        )

    return sceneObjs


def main():
    glfwInit()
    glInit()
    sceneObjs = initElements()
    lastFrame = currentFrame = glfw.get_time()
    while not glfw.window_should_close(window):
        currentFrame = glfw.get_time()
        if currentFrame - lastFrame < 1.0/FRAME_RATE:
            continue

        display(
            sceneObjs,
            window
        )
        lastFrame = currentFrame

    glfw.terminate()


main()
