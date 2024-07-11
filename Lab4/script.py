#!/usr/bin/env python3
from math import cos, pi, sin
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy


##############################
#  variables
##############################

viewer = [0.0, 0.0, 10.0]

theta = 0.0  # pozycja obserwatora w poziomie
phi = 0.0    # pozycja obserwatora w pionie

pix2angle = 1.0
piy2angle = 1.0

scale = 1.0
R = 7.0
up_y = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
v_button_state = 0

mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0


##############################
#  startup
##############################

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


##############################
#  shutdown
##############################

def shutdown():
    pass


##############################
#  axes
##############################

def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()
    
    
##############################
#  example object
##############################

def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


##############################
# Audi 3D fractal
##############################

N = 20
tab = numpy.zeros((N + 1, N + 1, 3))
tabColor = numpy.zeros((N + 1, N + 1, 3))

def audi_fractal():
    tabFractalValues()
    drawAudiFractal()

def tabFractalValues():
    for i in range(0, N + 1):
        for j in range(0, N + 1):
            u = i / N
            v = j / N
            R = 2
            r = 0.5
            tab[i][j][0] = (R + r * cos(2 * pi * v)) * cos(2 * pi * u)
            tab[i][j][1] = (R + r * cos(2 * pi * v)) * sin(2 * pi * u)
            tab[i][j][2] = r * sin(2 * pi * v)

def drawAudiFractal():
    drawTorusLines(251, 86,   7, 0.0)
    drawTorusLines(255, 190, 11, 3.0)
    drawTorusLines(131, 56, 236, -6.0)
    drawTorusLines(255,  0, 110, -3.0)

def drawTorusLines(color_r, color_g, color_b, position):
    glColor3ub(color_r, color_g, color_b)
    for i in range(0, N):
        for j in range(0, N):
            glBegin(GL_LINES)
            glVertex3f(tab[i][j][2], tab[i][j][1] + position, -tab[i][j][0])
            glVertex3f(tab[i + 1][j][2], tab[i + 1][j][1] + position, -tab[i + 1][j][0])

            glVertex3f(tab[i][j][2], tab[i][j][1] + position, -tab[i][j][0])
            glVertex3f(tab[i][j + 1][2], tab[i][j + 1][1] + position, -tab[i][j + 1][0])
            glEnd()


##############################
#  Render
##############################

def render(time):
    global theta
    global phi
    global scale
    global R
    global v_button_state
    global up_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    x_eye = R * cos(pi * theta / 180) * cos(pi * phi / 180)
    y_eye = R * sin(pi * phi / 180)
    z_eye = R * sin(pi * theta / 180) * cos(pi * phi / 180)

    # change camera behavior after pressing 'v' button
    if v_button_state:        
        gluLookAt(x_eye, y_eye, z_eye, 0.0, 0.0, 0.0, 0.0, up_y, 0.0)

        # rotate support   
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * piy2angle

        # R value is between 0 and 10
        if right_mouse_button_pressed:
            if delta_x > 0 and R < 10:
              R += 0.1
            else:
                if R >= 1 :
                    R -= 0.1
                    
        phi %= 360

        if phi <= 90 or phi > 270:
            up_y = -1.0
        else:
            up_y = 1
    else:
        gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        # rotate support
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * piy2angle    

        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)
    
    axes()
    example_object()
    # audi_fractal()

    glFlush()


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
    global v_button_state

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_V and action == GLFW_PRESS:
        if v_button_state:
            v_button_state = 0
        else:
            v_button_state = 1


##############################
#  mouse motion callback
##############################

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y          
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


##############################
#  mouse button callback
##############################

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0
        
    # callback for right mouse button
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


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