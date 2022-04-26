from OpenGL.GL import *
import OpenGL.GL.shaders

VERTEX_CODE = """
        attribute vec2 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,0.0,1.0);
        }
    """

FRAG_CODE = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
    """

class Shader:
    def __init__(self, sourceCode, shaderType):
        self.sourceCode = sourceCode;
        self.shader = glCreateShader(shaderType);

        glShaderSource(self.shader, sourceCode);
        glCompileShader(self.shader);

        if not glGetShaderiv(self.shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(self.shader).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Shader")

    def attach(self, program):
        glAttachShader(program, self.shader)

    def __del__(self):
        glDeleteShader(self.shader)
