# Modified from
# https://github.com/tartley/gltutpy/blob/master/t01.hello-triangle/HelloTriangle.py

import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL.ARB import vertex_array_object
from os.path import dirname, join

# Number of bytes in a GLFloat
sizeOfFloat = 4
sizeOfUshort = 2

class GameObject:
    def __init__(self, vertices, colours, indices):
        self.vertexPositions = vertices
        self.vertexComponents = 4
        self.vertexColours = colours
        self.colourComponents = 4
        self.indices = indices
        self.vertexArrayObject = glGenVertexArrays(1)
        self.positionBufferObject, self.colourBufferObject = self.initialize_vertex_buffers()
        self.indexBufferObject = self.initialize_index_buffer()

    def initialize_vertex_buffers(self):
        glBindVertexArray(self.vertexArrayObject)
        positionBufferObject = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, positionBufferObject)
        array_type = (GLfloat * len(self.vertexPositions))
        glBufferData(
            GL_ARRAY_BUFFER, len(self.vertexPositions) * sizeOfFloat,
            array_type(*self.vertexPositions), GL_STATIC_DRAW
        )
        colourBufferObject = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, colourBufferObject)
        array_type = (GLfloat * len(self.vertexColours))
        glBufferData(
            GL_ARRAY_BUFFER, len(self.vertexColours) * sizeOfFloat,
            array_type(*self.vertexColours), GL_STATIC_DRAW
        )
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        return positionBufferObject, colourBufferObject

    def initialize_index_buffer(self):
        glBindVertexArray(self.vertexArrayObject)
        indexBufferObject = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexBufferObject)
        array_type = (GLushort * len(self.indices))
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER, len(self.indices) * sizeOfUshort,
            array_type(*self.indices), GL_STATIC_DRAW
        )
        glBindVertexArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        return indexBufferObject

class ShaderProgram:
    def __init__(self, gameObjects, vShaderFilename, fShaderFilename):
        self.gameObjects = gameObjects
        glBindVertexArray(gameObjects[0].vertexArrayObject)
        self.shaderProgram = compileProgram(
            compileShader(
                loadFile(vShaderFilename), GL_VERTEX_SHADER),
            compileShader(
                loadFile(fShaderFilename), GL_FRAGMENT_SHADER)
        )
        glBindVertexArray(0)
        self.setup_attributes()

    def setup_attributes(self):
        for go in self.gameObjects:
            glBindVertexArray(go.vertexArrayObject)
            glBindBuffer(GL_ARRAY_BUFFER, go.positionBufferObject)
            positionLocation= glGetAttribLocation(self.shaderProgram, b'position')
            glEnableVertexAttribArray(positionLocation)
            glVertexAttribPointer(positionLocation, go.vertexComponents, GL_FLOAT, False, 0, None)
            glBindBuffer(GL_ARRAY_BUFFER, go.colourBufferObject)
            colourLocation = glGetAttribLocation(self.shaderProgram, b'colour_in')
            glEnableVertexAttribArray(colourLocation)
            glVertexAttribPointer(colourLocation, go.colourComponents, GL_FLOAT, False, 0, None)
            glBindVertexArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    def drawGameObjects(self):
        glUseProgram(self.shaderProgram)
        for go in self.gameObjects:
            glBindVertexArray(go.vertexArrayObject)
            glDrawElements(GL_TRIANGLES, len(go.indices), GL_UNSIGNED_SHORT, None)
            glBindVertexArray(0)
        glUseProgram(0)

def main():
    global triangleShader

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_3_2_CORE_PROFILE | GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(720, 480)

    glutCreateWindow(b'Hello Triangle Organized')

    glutDisplayFunc(display)
    glutKeyboardFunc(onKeyEvent)

    printSystemGLInfo()

    glClearColor (0.1, 0.2, 0.3, 1.0)

    # Three vertices, with an x,y,z & w for each.
    vertexPositions = [
        0.0, 0.0,  0.0,  1.0,
        0.5, 0.0,  0.0,  1.0,
        0.0, 0.5,  0.0,  1.0,
    ]

    vertexColours = [
        0.0, 0.8, 0.0, 1.0,
        0.0, 0.5, 0.0, 1.0,
        0.0, 0.2, 0.0, 1.0,
    ]

    indices = [
        0,1,2
    ]
    
    triangle = GameObject(vertexPositions, vertexColours, indices)
    triangleShader = ShaderProgram([triangle], 'simpleVAO.vert', 'simpleVAO.frag')

    # Run the GLUT main loop until the user closes the window.
    glutMainLoop()


def printSystemGLInfo():
    print('Vendor: %s' % (glGetString(GL_VENDOR)).decode("utf-8") )
    print('Opengl version: %s' % (glGetString(GL_VERSION).decode("utf-8") ))
    print('GLSL Version: %s' % (glGetString(GL_SHADING_LANGUAGE_VERSION)).decode("utf-8") )
    print('Renderer: %s' % (glGetString(GL_RENDERER)).decode("utf-8") )

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    triangleShader.drawGameObjects()
    glutSwapBuffers()

# https://butterflyofdream.wordpress.com/2016/04/27/pyopengl-keyboard-wont-respond/
def onKeyEvent(bkey, x, y):
    # Convert bytes object to string 
    key = bkey.decode("utf-8")
    # Allow to quit by pressing 'Esc'
    if key == chr(27):
        print("Exiting")
        sys.exit()

def loadFile(filename):
    with open(join(dirname(__file__), filename)) as fp:
        return fp.read()

# 
# https://github.com/tartley/gltutpy/blob/master/t02.playing-with-colors/glwrap.py
def glGenVertexArray():
    vao_id = GLuint(0)
    vertex_array_object.glGenVertexArrays(1, vao_id)
    return vao_id.value

if __name__ == "__main__":
    main()