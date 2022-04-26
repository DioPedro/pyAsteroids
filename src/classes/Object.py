from Element import Element

class Object:
    def __init__(self, program, elements: list()):
        self.program = program
        self.elements = elements2
    
    def addElement(self, points):
        self.elements.append(Element(points, 
                                     range(len(points)),
                                     self.program
                            ))

    def transform(self, transformation):
        loc = glGetUniformLocation(self.program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, transformation)

        for element in elements:
            element.bind()
            element.draw()