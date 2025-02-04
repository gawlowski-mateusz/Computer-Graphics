#!/usr/bin/env python3

import ctypes
import sys

from glfw.GLFW import *

import glm

import numpy

from OpenGL.GL import *
from OpenGL.GLU import *


##############################
#  variables
##############################

rendering_program = None
vertex_array_object = None
vertex_buffer = None

P_matrix = None


##############################
#  Compile shaders
##############################

def compile_shaders():
    vertex_shader_source = """
        #version 330 core

        in vec4 position;
        in vec4 vertex_color_in;    // input color variable

        out vec4 vertex_color;  // output color variable

        uniform mat4 M_matrix;
        uniform mat4 V_matrix;
        uniform mat4 P_matrix;

        void main(void) {
            gl_Position = P_matrix * V_matrix * M_matrix * position;
            vertex_color = vertex_color_in;     // assign vertex color
        }
    """

    fragment_shader_source = """
        #version 330 core

        out vec4 color;
        in vec4 vertex_color;   // input color variable

        void main(void) {
            color = vertex_color;   // assign color
        }
    """

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, [vertex_shader_source])
    glCompileShader(vertex_shader)
    success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)

    if not success:
        print('Shader compilation error:')
        print(glGetShaderInfoLog(vertex_shader).decode('UTF-8'))

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, [fragment_shader_source])
    glCompileShader(fragment_shader)
    success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)

    if not success:
        print('Shader compilation error:')
        print(glGetShaderInfoLog(fragment_shader).decode('UTF-8'))

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    success = glGetProgramiv(program, GL_LINK_STATUS)

    if not success:
        print('Program linking error:')
        print(glGetProgramInfoLog(program).decode('UTF-8'))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


##############################
#  vstartup
##############################

def startup():
    global rendering_program
    global vertex_array_object
    global vertex_buffer

    print("OpenGL {}, GLSL {}\n".format(
        glGetString(GL_VERSION).decode('UTF-8').split()[0],
        glGetString(GL_SHADING_LANGUAGE_VERSION).decode('UTF-8').split()[0]
    ))

    update_viewport(None, 400, 400)
    glEnable(GL_DEPTH_TEST)

    rendering_program = compile_shaders()

    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    vertex_positions = numpy.array([
        -0.25, +0.25, -0.25,
        -0.25, -0.25, -0.25,
        +0.25, -0.25, -0.25,

        +0.25, -0.25, -0.25,
        +0.25, +0.25, -0.25,
        -0.25, +0.25, -0.25,

        +0.25, -0.25, -0.25,
        +0.25, -0.25, +0.25,
        +0.25, +0.25, -0.25,

        +0.25, -0.25, +0.25,
        +0.25, +0.25, +0.25,
        +0.25, +0.25, -0.25,

        +0.25, -0.25, +0.25,
        -0.25, -0.25, +0.25,
        +0.25, +0.25, +0.25,

        -0.25, -0.25, +0.25,
        -0.25, +0.25, +0.25,
        +0.25, +0.25, +0.25,

        -0.25, -0.25, +0.25,
        -0.25, -0.25, -0.25,
        -0.25, +0.25, +0.25,

        -0.25, -0.25, -0.25,
        -0.25, +0.25, -0.25,
        -0.25, +0.25, +0.25,

        -0.25, -0.25, +0.25,
        +0.25, -0.25, +0.25,
        +0.25, -0.25, -0.25,

        +0.25, -0.25, -0.25,
        -0.25, -0.25, -0.25,
        -0.25, -0.25, +0.25,

        -0.25, +0.25, -0.25,
        +0.25, +0.25, -0.25,
        +0.25, +0.25, +0.25,

        +0.25, +0.25, +0.25,
        -0.25, +0.25, +0.25,
        -0.25, +0.25, -0.25,
    ], dtype='float32')

    # define colors array
    vertex_colors = numpy.array([
        0.50, 0.92, 0.92, 
        0.50, 0.92, 0.92, 
        0.50, 0.92, 0.92,

        0.50, 0.92, 0.92, 
        0.50, 0.92, 0.92, 
        0.50, 0.92, 0.92,

        1.00, 0.80, 0.43, 
        1.00, 0.80, 0.43, 
        1.00, 0.80, 0.43,

        1.00, 0.80, 0.43, 
        1.00, 0.80, 0.43, 
        1.00, 0.80, 0.43,

        0.65, 0.60, 1.00, 
        0.65, 0.60, 1.00, 
        0.65, 0.60, 1.00,

        0.65, 0.60, 1.00, 
        0.65, 0.60, 1.00, 
        0.65, 0.60, 1.00,

        0.45, 0.45, 0.45, 
        0.45, 0.45, 0.45, 
        0.45, 0.45, 0.45,

        0.45, 0.45, 0.45, 
        0.45, 0.45, 0.45, 
        0.45, 0.45, 0.45,

        0.91, 0.26, 0.58, 
        0.91, 0.26, 0.58, 
        0.91, 0.26, 0.58,

        0.91, 0.26, 0.58, 
        0.91, 0.26, 0.58, 
        0.91, 0.26, 0.58,
        
        0.88, 0.43, 0.33, 
        0.88, 0.43, 0.33, 
        0.88, 0.43, 0.33,

        0.88, 0.43, 0.33, 
        0.88, 0.43, 0.33, 
        0.88, 0.43, 0.33,
    ], dtype='float32')

    # adjust color buffer
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex_positions, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    vertex_buffer_colors = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_colors)
    glBufferData(GL_ARRAY_BUFFER, vertex_colors, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)


##############################
#  shutdown
##############################

def shutdown():
    global rendering_program
    global vertex_array_object
    global vertex_buffer

    glDeleteProgram(rendering_program)
    glDeleteVertexArrays(1, vertex_array_object)
    glDeleteBuffers(1, vertex_buffer)


##############################
#  render
##############################

def render(time):
    glClearBufferfv(GL_COLOR, 0, [0.0, 0.0, 0.0, 1.0])
    glClearBufferfi(GL_DEPTH_STENCIL, 0, 1.0, 0)

    M_matrix = glm.rotate(glm.mat4(1.0), time, glm.vec3(1.0, 1.0, 0.0))

    V_matrix = glm.lookAt(
        glm.vec3(0.0, 0.0, 1.0),
        glm.vec3(0.0, 0.0, 0.0),
        glm.vec3(0.0, 1.0, 0.0)
    )

    glUseProgram(rendering_program)

    M_location = glGetUniformLocation(rendering_program, "M_matrix")
    V_location = glGetUniformLocation(rendering_program, "V_matrix")
    P_location = glGetUniformLocation(rendering_program, "P_matrix")
    glUniformMatrix4fv(M_location, 1, GL_FALSE, glm.value_ptr(M_matrix))
    glUniformMatrix4fv(V_location, 1, GL_FALSE, glm.value_ptr(V_matrix))
    glUniformMatrix4fv(P_location, 1, GL_FALSE, glm.value_ptr(P_matrix))

    glDrawArrays(GL_TRIANGLES, 0, 36)


##############################
#  update viewport
##############################

def update_viewport(window, width, height):
    global P_matrix

    aspect = width / height
    P_matrix = glm.perspective(glm.radians(70.0), aspect, 0.1, 1000.0)

    glViewport(0, 0, width, height)


##############################
#  keyboard key callback
##############################

def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


##############################
#  glfw error callback
##############################

def glfw_error_callback(error, description):
    print('GLFW Error:', description)


##############################
#  main
##############################

def main():
    glfwSetErrorCallback(glfw_error_callback)

    if not glfwInit():
        sys.exit(-1)

    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    # Poniższą linijkę odkomentować w przypadku pracy w systemie macOS!
    # glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()