from .Element import Element
from .Path import Path
import numpy as np
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv, GL_TRUE
from typing import List, Tuple, Union


class Object:
    def __init__(
            self,
            program: any,
            elements: Tuple[Element, ...],
            path: Union[None, Path]):
        self.program = program
        self.elements = elements
        self.path = path

    def addElement(
            self,
            points: Tuple[Tuple[float, ...], ...],
            color: List[float]
    ):
        self.elements.append(
            Element(
                points,
                range(len(points)),
                color,
                self.program
            )
        )

    def transform(self, transformation: np.ndarray):
        loc = glGetUniformLocation(self.program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, transformation)

        for element in self.elements:
            element.bind()
            element.draw()
        
        if self.path:
            self.path.increment()
