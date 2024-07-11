#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
import random
import numpy as np

##############################
#  variables
##############################

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi  = 0.0
pix2angle = 1.0
piy2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
R = 5.0

# material declaration
mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

# 1st light source
light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


##############################
#  startup
##############################

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # material
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # 1st light source
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


##############################
#  shutdown
##############################

def shutdown():
    pass


##############################
#  spin
##############################

def spin (angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


##############################
#  Render
##############################

def render(time):
    global theta
    global phi
     
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * piy2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    spin(time * 180 / pi)
    draw_egg_triangles()
    glFlush()

    
##############################
#  egg matrix values
##############################

n = 20
egg_matrix = np.zeros((n + 1, n + 1, 3))
egg_matrix_vectors = np.zeros((n + 1, n + 1, 3))

def egg_matrix_values():
    for i in range (0, n + 1):
        for j in range (0, n + 1):
            u = i / n
            v = j / n
            
            egg_matrix[i][j][0] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * cos(pi * v)  # x coordinate
            egg_matrix[i][j][1] =  160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2)                                            # y coordinate
            egg_matrix[i][j][2] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * sin(pi * v)  # z coordinate
            

##############################
#  egg matrix vectors values
##############################
            
def egg_matrix_vectors_values():
    for i in range (0, n + 1):
        for j in range (0, n + 1):
            u = i / n
            v = j / n
            
            xu = (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * cos(pi * v)
            xv = pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * sin(pi * v)
            yu = 640 * pow(u, 3) - 960 * pow(u, 2) + 320 * u
            yv = 0
            zu = (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * sin(pi * v)
            zv = (- pi) * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * cos(pi * v)

            x = yu * zv - zu * yv
            y = zu * xv - xu * zv
            z = xu * yv - yu * xv
            
            sum = pow(x, 2) + pow(y, 2) + pow(z, 2)
            length = sqrt(sum)
 
            if length > 0:
                x = x / length 
                y = y / length
                z = z / length            
            
            egg_matrix_vectors[i][j][0] =  x
            egg_matrix_vectors[i][j][1] =  y
            egg_matrix_vectors[i][j][2] =  z
    

##############################
#  draw egg triangles
##############################

def draw_egg_triangles(): 
    for i in range (0, n):
        for j in range (0, n):
            glBegin(GL_TRIANGLES)
            glNormal3f(egg_matrix_vectors[i][j][0], egg_matrix_vectors[i][j][1], egg_matrix_vectors[i][j][2])
            glVertex3f(egg_matrix[i][j][0], egg_matrix[i][j][1] - 5, egg_matrix[i][j][2])
            
            glNormal3f(egg_matrix_vectors[i + 1][j][0], egg_matrix_vectors[i + 1][j][1], egg_matrix_vectors[i + 1][j][2])
            glVertex3f(egg_matrix[i + 1][j][0], egg_matrix[i + 1][j][1] - 5, egg_matrix[i + 1][j][2])
            
            glNormal3f(egg_matrix_vectors[i + 1][j + 1][0], egg_matrix_vectors[i + 1][j + 1][1], egg_matrix_vectors[i + 1][j + 1][2])
            glVertex3f(egg_matrix[i + 1][j + 1][0], egg_matrix[i + 1][j + 1][1] - 5, egg_matrix[i + 1][j + 1][2])
            
            glNormal3f(egg_matrix_vectors[i][j + 1][0], egg_matrix_vectors[i][j + 1][1], egg_matrix_vectors[i][j + 1][2])
            glVertex3f(egg_matrix[i][j + 1][0], egg_matrix[i][j + 1][1] - 5, egg_matrix[i][j + 1][2])
            
            glNormal3f(egg_matrix_vectors[i][j][0], egg_matrix_vectors[i][j][1], egg_matrix_vectors[i][j][2])
            glVertex3f(egg_matrix[i][j][0], egg_matrix[i][j][1] - 5, egg_matrix[i][j][2])
            
            glNormal3f(egg_matrix_vectors[i + 1][j + 1][0], egg_matrix_vectors[i + 1][j + 1][1], egg_matrix_vectors[i + 1][j + 1][2])
            glVertex3f(egg_matrix[i + 1][j + 1][0], egg_matrix[i + 1][j + 1][1] - 5, egg_matrix[i + 1][j + 1][2])
            glEnd()
            

##############################
#  update viewport
##############################

def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


##############################
#  keyboard key callback
##############################

def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


##############################
#  mouse motion callback
##############################

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


##############################
#  mouse button callback
##############################

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


##############################
#  main
##############################

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
        
    random.seed(1)
    egg_matrix_vectors_values() 
    egg_matrix_values()

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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