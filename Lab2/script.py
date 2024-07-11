#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

####################
# DEFAULT CODE
####################

def default_code():
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

####################
# FOR 3.0
# Colorful triangle
####################

def grade_3_0():
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 0.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(50.0, 0.0)
    glEnd()

####################
# FOR 3.5
# Rectangle
####################

def grade_3_5(starting_x, starting_y, size_a, size_b):
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(starting_x, starting_y)
    glVertex2f(starting_x - size_a, starting_y)
    glVertex2f(starting_x - size_a, starting_y + size_b)
    glEnd()

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(starting_x, starting_y)
    glVertex2f(starting_x, starting_y + size_b)
    glVertex2f(starting_x - size_a, starting_y + size_b)
    glEnd()

####################
# FOR 4.0
# Colorful rectangle
####################

def grade_4_0(starting_x, starting_y, size_a, size_b, deformation, color_r, color_g, color_b):
    size_a *= deformation
    size_b *= deformation

    glColor3ub(color_r, color_g, color_b)
    glBegin(GL_TRIANGLES)
    glVertex2f(starting_x, starting_y)
    glVertex2f(starting_x - size_a, starting_y)
    glVertex2f(starting_x - size_a, starting_y + size_b)
    glEnd()

    color_r = (color_r * deformation) % 255
    color_g = (color_g * deformation) % 255
    color_b = (color_b * deformation) % 255

    glColor3ub(color_r, color_g, color_b)
    glBegin(GL_TRIANGLES)
    glVertex2f(starting_x, starting_y)
    glVertex2f(starting_x, starting_y + size_b)
    glVertex2f(starting_x - size_a, starting_y + size_b)
    glEnd()

####################
# FOR 4.5
# Sierpinski rug
####################

def sierpinski_rug(position_x, position_y, size_a, size_b, level):
    if level > 0:
        level -= 1
        size_a /= 3.0
        size_b /= 3.0

        sierpinski_rug(position_x + size_a, position_y , size_a, size_b, level)
        sierpinski_rug(position_x + size_a, position_y - size_b ,size_a, size_b, level)
        sierpinski_rug(position_x, position_y - size_b, size_a, size_b, level)
        sierpinski_rug(position_x - size_a, position_y - size_b, size_a, size_b, level)
        sierpinski_rug(position_x - size_a, position_y, size_a, size_b, level)
        sierpinski_rug(position_x - size_a, position_y + size_b, size_a, size_b, level)
        sierpinski_rug(position_x, position_y + size_b, size_a, size_b, level)
        sierpinski_rug(position_x + size_a, position_y + size_b, size_a, size_b, level)
    else:
        sierpinski_rug_new_rectangle(position_x, position_y, size_a, size_b, 0.0)


def sierpinski_rug_new_rectangle(pos_x, pos_y, size_a, size_b, deformation):
    # pos_x, pos_y - center coordinates
    # size_a, size_b - side size
    # deformation - degree of similarity

    glBegin(GL_TRIANGLES)
    glVertex2f(pos_x - (size_a / 2), pos_y + (size_b / 2) + deformation * size_b)   #upper left vertex + deformation
    glVertex2f(pos_x + (size_a / 2), pos_y + (size_b / 2))                          #upper right vertex
    glVertex2f(pos_x - (size_a / 2) + deformation * size_a, pos_y - (size_b / 2))   #lower left vertex + deformation
    glEnd()


    glBegin(GL_TRIANGLES)
    glVertex2f(pos_x + (size_a / 2) + deformation * size_a, pos_y + (size_b / 2))   #upper right vertex + deformation
    glVertex2f(pos_x - (size_a / 2), pos_y - (size_b / 2))                          #lower left vertex
    glVertex2f(pos_x + (size_a / 2), pos_y - (size_b / 2) - deformation * size_b)   #lower right vertex + deformation
    glEnd()
    

def grade_4_5(iterations):
    sierpinski_rug(0.0, 0.0, 200.0, 100.0, iterations)

######################
# FOR 5.0
# Sierpinski triangle
######################

def sierpinski_triangle(starting_x, starting_y, size, depth):
    # starting_x, starting_y - starting (extreme) coordinates
    # size - side size
    # depth - number of iterations

    if depth == 0:
        # Draw triangle
        glBegin(GL_TRIANGLES)
        glVertex2f(starting_x, starting_y)
        glVertex2f(starting_x + size, starting_y)
        glVertex2f(starting_x + size / 2, starting_y + size * (3 ** 0.5) / 2)
        glEnd()
    else:
        # Find center of triangle
        mid_x = starting_x + size / 2
        mid_y = starting_y + size * (3 ** 0.5) / 2
        
        # Recursive draw three smaller triangles
        sierpinski_triangle(starting_x, starting_y, size / 2, depth - 1)
        sierpinski_triangle(mid_x, starting_y, size / 2, depth - 1)
        sierpinski_triangle(starting_x + size / 4, starting_y + size * (3 ** 0.5) / 4, size / 2, depth - 1)


def grade_5_0(iterations):
    sierpinski_triangle(-100, -100, 200, iterations)

####################
# RENDER
####################

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    random.seed(12)
    deformation = random.randint(0, 3)
    color_r = random.randint(0, 255)
    color_g = random.randint(0, 255)
    color_b = random.randint(0, 255)

    #default_code()
    #grade_3_0()
    #grade_3_5(10.0, 20.0, 30.0, 60.0)
    #grade_4_0(0.0, 0.0, 20.0, 30.0, deformation, color_r, color_g, color_b)
    #grade_4_5(5)
    grade_5_0(5)

    glFlush()



def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
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