from OpenGL.GL import *
import numpy as np
from typing import List

class Element:
	verts: List[List[float]] = []
	elements: np.ndarray = np.array([])
	vao: any = None
	vbo: any = None
	ebo: any = None
	program: any = None

	def __init__(self, verts: List[List[float]], elements: List[int], program: any) -> None:
		self.verts = verts
		self.elements = np.array(elements)
		self.program = program
		self.vao = glGenVertexArrays(1)
		self.vbo = glGenBuffers(1)
		self.ebo = glGenBuffers(1)

		glBindVertexArray(self.vao)

		# preparando espaço para 3 vértices usando 2 coordenadas (x,y)
		vertices = np.zeros(len(verts), [("position", np.float32, len(verts[0]))])

		# preenchendo as coordenadas de cada vértice
		vertices['position'] = verts

		# Upload data
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.elements.nbytes, self.elements, GL_STATIC_DRAW)

		# Bind the position attribute
		# --------------------------------------
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
		glDrawArrays(GL_LINE_LOOP, 0, self.elements.size)
		glBindVertexArray(0)
