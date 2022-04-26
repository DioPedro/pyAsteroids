import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

from classes.Object import Object
from classes.Shader import Shader, VERTEX_CODE, FRAG_CODE
from classes.Element import Element

NAV_PATH = lambda x: (np.sin(2 * x) + (np.sin(6 * x) / 4)) 
t_x = 0
t_y = 0
r = 0
r_step = 0.05

def curvePath(amplitude, equation)
    rads = np.arange(0, (2 * np.pi), 0.01)
    amplitude = 10
    
    points = []
    for rad in rads:
        r = amplitude * equation(rad)
        points.append([r * np.cos(rad), r * np.sin(rad)])
    
    return points


def key_event(window,key,scancode,action,mods):
    global t_x, t_y, r
    
    if key == 87:
        t_y += 0.01 #cima
        r = 0
    if key == 83:
        t_y -= 0.01 #baixo
        r = r_step * 64
    if key == 65:
        t_x -= 0.01 #esquerda
        r = r_step * 32
    if key == 68:
        t_x += 0.01 #direita
        r = -r_step * 32
    if key == 69: # diagonal superior direita (1° quadrante)
        t_y += 0.01
        t_x += 0.01
        r = -r_step * 16
    if key == 81: # diagonal superior esquerda (2° quadrante)
        t_y += 0.01
        t_x -= 0.01
        r = r_step * 16
    if key == 90: # diagonal inferior esquerda (3° quadrante)
        t_y -= 0.01
        t_x -= 0.01
        r = r_step * 48
    if key == 67: # diagonal inferior direita (4° quadrante)
        t_y -= 0.01
        t_x += 0.01
        r = -r_step * 48
    if scancode == 24: r += r_step
    if scancode == 26: r -= r_step
    
    glfw.set_key_callback(window,key_event)

def display(rocket, spaceship, amongus):
    glfw.poll_events() 
    
    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(0.15625, 0.1640625, 0.2109375, 1.0)                            
    
    rocketTransform = Transform.stack([
        Transform.translate(t_x, t_y),
        Transform.scale(s, s),
        Transform.rotate(r)
    ])
    rocket.transform(rocketTransform)
    
    spaceshipTransform = Transform.stack([
        Transform.translate(points[sp_idx][0], points[sp_idx][1]),
        Transform.scale(sll, sll)
    ])
    spaceship.transform(spaceshipTransform)

    amongusTranform = Transform.stack([
        Transform.translate(ax[am_idx], ay[am_idx]),
        Transform.scale(ams, ams),
        Transform.rotate(ar)
    ])

    amongus.transform(amongusTranform)

    if am_idx + 1 < len(ax):
        am_idx += 1
        ar += 0.01

    if sp_idx + 1 == max_size:
        sp_idx = 0
    sp_idx += 1

    glfw.swap_buffers(window)

def main():
    # Starting Window
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(600, 600, "Cores", None, None)
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    glfw.window_hint(glfw.MAXIMIZED, glfw.FALSE)
    glfw.make_context_current(window)

    program  = glCreateProgram()
    vertexShader = Shader(VERTEX_CODE, GL_VERTEX_SHADER)
    fragShader = Shader(VERTEX_CODE, GL_VERTEX_SHADER)

    vertexShader.attach(program);
    fragShader.attach(program);

    # Build program
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')

    # Make program the default program
    glUseProgram(program)

    del vertexShader
    del fragShader

    rocket = Object()
    rocket.addElement(
        points = [
            (0.0, +0.5),  # vertice 0
            (-0.5, -0.5),  # vertice 1
            (0, -0.25),  # vertice 2
            (+0.5, -0.5),  # vertice 3
        ]
    )
    rocket.addElement(
        points =  [
            (+0.5, -0.5),  # vertice 2
            (-0.5, -0.5),  # vertice 1
            (0, -0.25),  # vertice 3
            (0.0, +0.5),  # vertice 0
        ]
    )

    spaceship = Object()
    spaceship.addElement(
        points = [
            (-1.0, 0.0),  # vertice 0
            (-0.7, 0.5),  # vertice 1
            (0.7, 0.5),  # vertice 2
            (1.0, 0.0),  # vertice 3
            (0.5, -0.5),  # vertice 4
            (-0.5, -0.5),  # vertice 5
        ]
    )
    spaceship.addElement( 
        points = [
            (-1.0, 0.0),  # vertice 0
            (1.0, 0.0),  # vertice 1
        ]
    )
    spaceship.addElement(
            points = [
                (-0.5, 0.5),  # vertice 0
                (-0.4, 0.7),  # vertice 1
                (-0.2, 0.8),  #vertice 2
                (0, 0.85),  # vertice 3
                (0.2, 0.8),  # vertice 4
                (0.4, 0.7),  # vertice 5
                (0.5, 0.5)  #vertice 6
        ]
    )

    amongus = Object()
    amongus.addElement(
        points = [
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
        ]
    )
    amongus.addElement(
        points = [
            (-0.18, -1.99),
            (-0.21, -0.79)
        ]
    )
    amongus.addElement(
        points = [
            (0.8, -1.29),
            (1.42, -1.29),
            (1.77, -0.78),
            (1.74, 0.19),
            (1.42, 0.7),
            (0.78, 0.78)
        ]
    )

    loc_color = glGetUniformLocation(program, "color")
    R = 0.96875
    G = 0.96875
    B = 0.9453125

    display(rocket, spaceship, amogos)
    glfw.show_window(window)


