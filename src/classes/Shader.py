from OpenGL.GL import glShaderSource, glCreateShader, GL_COMPILE_STATUS, glGetShaderInfoLog, glAttachShader, glGetShaderiv, glCompileShader, glDeleteShader


class Shader:
    def __init__(self, sourceCode, shaderType):
        self.sourceCode = sourceCode
        self.shader = glCreateShader(shaderType)

        glShaderSource(self.shader, sourceCode)
        glCompileShader(self.shader)

        if not glGetShaderiv(self.shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(self.shader).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Shader")

    def attach(self, program):
        glAttachShader(program, self.shader)

    def __del__(self):
        glDeleteShader(self.shader)
