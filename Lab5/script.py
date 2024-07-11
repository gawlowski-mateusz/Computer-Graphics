#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import *


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

# buttons declaration
a_button_state = 0
d_button_state = 0
s_button_state = 0

zero_button_state = 0
one_button_state = 0
two_button_state = 0

up_arrow_state = 0
down_arrow_state = 0

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

# 2nd light source
light_ambient_v2 = [0.07, 0.2, 0.0, 1.0]
light_diffuse_v2 = [1.0, 0.0, 0.2, 1.0]
light_specular_v2 = [0.0, 1.0, 1.0, 1.0]
light_position_v2 = [7.0, 0.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

buttons_state = [0,0,0,0,0,0,0,0,0] # przechowywanie stanow klawiszy 1-9
left_buttons_state = 0
right_buttons_state = 0


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
    
    # 2nd light source
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient_v2)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse_v2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular_v2)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_v2)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT1)


##############################
#  shutdown
##############################

def shutdown():
    pass

##############################
#  Render
##############################

def render(time):
    global theta
    global phi
    global light_position
    global R
    
    global a_button_state
    global d_button_state
    global s_button_state
    
    global zero_button_state
    global one_button_state
    global two_button_state
    
    global up_arrow_state
    global down_arrow_state

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
    
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)
    
    # grade 3.5
    #diffuse
    changeValue(0, 0)
    changeValue(1, 0)
    changeValue(2, 0)  
    #ambient
    changeValue(3, 3)
    changeValue(4, 3)
    changeValue(5, 3)
    #specular
    changeValue(6, 6)
    changeValue(7, 6)
    changeValue(8, 6) 
    
    # grade 4.0
    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    x_s = R * cos(pi * theta / 180) * cos(pi * phi / 180)
    y_s = R * sin(pi * phi / 180)
    z_s = R * sin(pi * theta / 180) * cos(pi * phi / 180)
    glTranslate(x_s, y_s, z_s)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
   
    light_position[0] = x_s
    light_position[1] = y_s
    light_position[2] = z_s
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * piy2angle

    glFlush()
    

##############################
#  change value
##############################

def changeValue(index, move):   # move oznacza przesuniecie o wielkokrotnosc liczby 3
                                # bo zmieniamy 3 tablice (w kazdej 3 elementy),
                                # a nacisniete przyciski trzymam w jednej 9-elem. tablicy (dla wygody)
                                # move == 0 ---> diffuse (klawisze 1-3 odpowiadaja kolejnym wartosciom)
                                # move == 3 ---> ambient (klawisze 4-6 odpowiadaja kolejnym wartosciom)
                                # move == 6 ---> specular (klawisze 7-9 odpowiadaja kolejnym wartosciom)
                                # zmiana wartosci: klawisze strzalek - w lewo i prawo                            
    global light_diffuse
    global light_ambient 
    global light_specular 
    global left_buttons_state
    global right_buttons_state    
    
    if buttons_state[index]:
        if move == 0:
            if left_buttons_state and int(round(100*light_diffuse[index - move])) > 0:
                light_diffuse[index - move] -=  0.1
                print("light_diffuse: ", light_diffuse)
                glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
            if right_buttons_state and int(round(100*light_diffuse[index - move])) < 100:
                light_diffuse[index - move] +=  0.1
                print("light_diffuse: ",light_diffuse)
                glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
            
        if move == 3:
            if left_buttons_state and int(round(100*light_ambient[index - move])) > 0:
                light_ambient[index - move] -=  0.1
                glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
                print("light_ambient: ",light_ambient)
            if right_buttons_state and int(round(100*light_ambient[index - move])) < 100:
                light_ambient[index - move] +=  0.1
                print("light_ambient: ",light_ambient)
                glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
                
        if move == 6:
            if left_buttons_state and int(round(100*light_specular[index - move])) > 0:
                light_specular[index - move] -=  0.1
                print("light_specular: ",light_specular) 
                glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)    
            if right_buttons_state and int(round(100*light_specular[index - move])) < 100:
                light_specular[index - move] +=  0.1
                print("light_specular: ",light_specular) 
                glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
              
        left_buttons_state = 0
        right_buttons_state = 0   

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
    global buttons_state
    global left_buttons_state
    global right_buttons_state
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(1)
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(2)
    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(3)
    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(4)
    if key == GLFW_KEY_5 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(5)
    if key == GLFW_KEY_6 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(6)
    if key == GLFW_KEY_7 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(7)
    if key == GLFW_KEY_8 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(8)
    if key == GLFW_KEY_9 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(9)
    if key == GLFW_KEY_LEFT and action == GLFW_PRESS:
        left_buttons_state = 1
    if key == GLFW_KEY_RIGHT and action == GLFW_PRESS:
        right_buttons_state = 1


##############################
#  Fill zeros and change Btn
##############################

def fillZerosAndChangeBtn(i):
    global buttons_state
    buttons_state = [0] * 9     # wypelnienie zerami
    buttons_state[i-1] = 1      # przypisanie '1' w tablicy odpowiedniemu przyciskowi


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