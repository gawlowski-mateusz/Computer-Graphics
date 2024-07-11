#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as numpy
import random
from math import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

###############################
#   Default code
###############################

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
    

###############################
#   Grade 3.0
#   Egg draw - points
###############################

N = 25
tab = numpy.zeros((N + 1, N + 1, 3))
tabColor = numpy.zeros((N + 1, N + 1, 3))

def grade_3_0():    
    tabValues()
    drawEggPoints()
    
# Table values insert
def tabValues():    
    for i in range(0, N + 1):
        for j in range(0, N + 1):
            u = i / N
            v = j / N
            tab[i][j][0] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * cos(pi * v)   # x coordinate
            tab[i][j][1] = 160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2)                                              # y coordinate
            tab[i][j][2] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * sin(pi * v)   # z coordinate

def drawEggPoints():
    glColor3ub(255, 20, 147)
    for i in range(0, N + 1):
        for j in range(0, N + 1):
            glBegin(GL_POINTS)
            glVertex3f(tab[i][j][0], tab[i][j][1] - 5, tab[i][j][2])
            glEnd()


###############################
#   Grade 3.5
#   Egg draw - lines
###############################

def grade_3_5():
    tabValues()
    drawEggLines()
    
def drawEggLines():
    glColor3ub(255, 20, 147)
    for i in range (0, N):
        for j in range (0, N):
            glBegin(GL_LINES)
            glVertex3f(tab[i][j][0], tab[i][j][1] - 5, tab[i][j][2])
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1] - 5, tab[i + 1][j][2])
 
            glVertex3f(tab[i][j][0], tab[i][j][1] - 5,  tab[i][j][2])
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1] - 5, tab[i][j + 1][2])
            glEnd();  
  
  
###############################
#   Grade 4.0
#   Egg draw - triangles
###############################

def grade_4_0():
    tabValues()
    random.seed(11)
    tabColorValues()
    drawEggTriangles()
    
# Table of colors generate     
def tabColorValues():
    for i in range (0, N + 1):
        for j in range (0, N + 1):
            u = i / N
            v = j / N
            tabColor[i][j][0] =  random.random()
            tabColor[i][j][1] =  random.random()
            tabColor[i][j][2] =  random.random()
    
    # Color on 1st connection set
    for i in range (0, int(N / 2) - 1):
        tabColor[N - i][N][0] = tabColor[i][0][0]
        tabColor[N - i][N][1] = tabColor[i][0][1]
        tabColor[N - i][N][2] = tabColor[i][0][2]
    
    # Color on 2nd connection set
    for j in range(0, int(N / 2) + 1):
        tabColor[N][N - j][0] = tabColor[0][j][0]
        tabColor[N][N - j][1] = tabColor[0][j][1]
        tabColor[N][N - j][2] = tabColor[0][j][2]

def drawEggTriangles(): 
    for i in range (0, N):
        for j in range (0, N):
            glBegin(GL_TRIANGLES)
            glColor3f(tabColor[i][j][0], tabColor[i][j][1], tabColor[i][j][2])
            glVertex3f(tab[i][j][0], tab[i][j][1] - 5, tab[i][j][2])
            
            glColor3f(tabColor[i][j + 1][0], tabColor[i][j + 1][1], tabColor[i][j + 1][2])
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1] - 5, tab[i][j + 1][2])            
            
            glColor3f(tabColor[i + 1][j][0], tabColor[i + 1][j][1], tabColor[i + 1][j][2])
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1] - 5, tab[i + 1][j][2])
   
            glColor3f(tabColor[i][j + 1][0], tabColor[i][j + 1][1], tabColor[i][j + 1][2])
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1] - 5,  tab[i][j + 1][2])
           
            glColor3f(tabColor[i + 1][j][0], tabColor[i + 1][j][1], tabColor[i + 1][j][2])
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1] - 5,  tab[i + 1][j][2])
           
            glColor3f(tabColor[i + 1][j + 1][0], tabColor[i + 1][j + 1][1], tabColor[i + 1][j + 1][2])
            glVertex3f(tab[i + 1][j + 1][0], tab[i + 1][j + 1][1] - 5, tab[i + 1][j + 1][2])
            glEnd()


###############################
#   Grade 4.5
#   Egg draw - triangles strip
###############################

def grade_4_5():
    tabValues()
    random.seed(12)
    tabColorValues()
    drawEggTrianglesStrip()
    
def drawEggTrianglesStrip():
    for i in range (0, N):
        for j in range (0, N):
            glBegin(GL_TRIANGLE_STRIP)
            glColor3f(tabColor[i][j][0], tabColor[i][j][1], tabColor[i][j][2])
            glVertex3f(tab[i][j][0], tab[i][j][1] - 5, tab[i][j][2])  
            
            glColor3f(tabColor[i + 1][j][0], tabColor[i + 1][j][1], tabColor[i + 1][j][2])
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1] - 5, tab[i + 1][j][2])
     
            glColor3f(tabColor[i][j + 1][0], tabColor[i][j + 1][1], tabColor[i][j + 1][2])
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1] - 5, tab[i][j + 1][2])  
            
            glColor3f(tabColor[i + 1][j + 1][0], tabColor[i + 1][j+1][1], tabColor[i + 1][j + 1][2])
            glVertex3f(tab[i + 1][j + 1][0], tab[i + 1][j+1][1] - 5, tab[i + 1][j + 1][2])
            glEnd()


###############################
#   Grade 5.0
#   3D Fractal
###############################

def grade_5_0():
    tabFractalValues()
    drawAudiFractal()
    spin(90)

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
            glVertex3f(tab[i][j][0], tab[i][j][1] + position, tab[i][j][2])
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1] + position, tab[i + 1][j][2])

            glVertex3f(tab[i][j][0], tab[i][j][1] + position, tab[i][j][2])
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1] + position, tab[i][j + 1][2])
            glEnd()      

        
###############################
#   Render function
###############################   

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    spin(time * 180 / 3.1415)
    axes()
    #grade_3_0()
    #grade_3_5()
    #grade_4_0()
    #grade_4_5()
    grade_5_0()

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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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