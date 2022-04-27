from OpenGL.GL import glGenVertexArrays, glGenBuffers, glBindVertexArray, glBindBuffer, glBufferData, GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER, GL_DYNAMIC_DRAW, glGetAttribLocation, glVertexAttribPointer, glEnableVertexAttribArray, glDrawElements, GL_LINE_LOOP, GL_UNSIGNED_INT, GL_FLOAT, GL_TRIANGLE_FAN, GL_LINE_LOOP, glGetUniformLocation, glUniform4f
import numpy as np
from typing import List, Tuple
import ctypes


class Element:
    verts: List[List[float]] = []
    elements: np.ndarray = np.array([])
    vao: any = None
    vbo: any = None
    ebo: any = None
    program: any = None
    color: List[float] = []
    BASE_COLOR = [68/255, 71/255, 90/255]

    def __init__(
            self,
            verts: Tuple[Tuple[float, ...], ...],
            elements: Tuple[int, ...],
            color: List[float],
            program: any
    ):
        self.verts = verts
        self.elements = np.array(elements, dtype=np.int32)
        self.program = program
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        self.color = color

        vertices = np.zeros(len(verts), [("position", np.float32, len(verts[0]))])
        vertices['position'] = verts

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER,
            vertices,
            GL_DYNAMIC_DRAW
        )

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.elements, GL_DYNAMIC_DRAW)

        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)

        loc = glGetAttribLocation(program, "position")
        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)
        glEnableVertexAttribArray(loc)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        pass

    def bind(self):
        glBindVertexArray(self.vao)

    def draw(self):
        loc_color = glGetUniformLocation(self.program, "color")
        glUniform4f(loc_color, self.color[0], self.color[2], self.color[2], 1.0)
        glDrawElements(
            GL_TRIANGLE_FAN,
            self.elements.size,
            GL_UNSIGNED_INT,
            None
        )

        glUniform4f(loc_color, self.BASE_COLOR[0], self.BASE_COLOR[2], self.BASE_COLOR[2], 1.0)
        glDrawElements(
            GL_LINE_LOOP,
            self.elements.size,
            GL_UNSIGNED_INT,
            None
        )

        glBindVertexArray(0)
