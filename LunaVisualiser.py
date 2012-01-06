#!/usr/bin/env python

#
# This code was created by Richard Campbell '99 (ported to Python/PyOpenGL by John Ferguson and Tony Colston 2000)
# To be honst I stole all of John Ferguson's code and just added the changed stuff for lesson 5. So he did most
# of the hard work.
#
# The port was based on the PyOpenGL tutorial module: dots.py  
#
# If you've found this code useful, please let me know (email John Ferguson at hakuin@voicenet.com).
# or Tony Colston (tonetheman@hotmail.com)

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, os, Image, time, psutil, ImageDraw
import numpy as np
from threading import *
import classes.AudioGrabber as ag
import classes.MouseSelection as ms

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
  #glEnable(GL_TEXTURE_2D)
  glClearColor(0.0, 0.0, 0.0, 0.9)	# This Will Clear The Background Color To Black
  glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
  glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
  #glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
  glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
  glEnable (GL_BLEND)
  glDisable(GL_TEXTURE_2D)
  
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  glOrtho(0, Width, 0, Height, 0, 1)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  gluLookAt(0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) # front view
  glBlendFunc(GL_SRC_ALPHA, GL_ONE)
  
  #glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
  
# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
  if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
    Height = 1
  glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  glOrtho(0, Width, 0, Height, 0, 1)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  gluLookAt(0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) # front view
  mouse.resize()
  audio.resize()

# The main drawing function. 
def DrawGLScene():
  global audio
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	# Clear The Screen And The Depth Buffer
  audio.update()
  glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
  # If escape is pressed, kill everything.
  if args[0] == ESCAPE:
    glutDestroyWindow(window)
    audio.kill()
    sys.exit()

def main():
  global window, audio, mouse

  glutInit(sys.argv)

  # Select type of Display mode:   
  #  Double buffer 
  #  RGBA color
  # Alpha components supported 
  # Depth buffer
  glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

  # get a 640 x 480 window 
  glutInitWindowSize(640, 480)

  # the window starts at the upper left corner of the screen 
  glutInitWindowPosition(0, 0)

  # Okay, like the C version we retain the window id to use when closing, but for those of you new
  # to Python (like myself), remember this assignment would make the variable local and not global
  # if it weren't for the global declaration at the start of main.
  window = glutCreateWindow("LunaVisualiser")
  
  #try:
  #except IndexError:
  #print 'Error'
  #print "Please include location of slide folders"
  #sys.exit(1)
    
  # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
  # set the function pointer and invoke a function to actually register the callback, otherwise it
  # would be very much like the C version of the code.	
  glutDisplayFunc(DrawGLScene)
  #glutDisplayFunc()

  # Uncomment this line to get full screen.
  # glutFullScreen()

  # When we are doing nothing, redraw the scene.
  glutIdleFunc(DrawGLScene)
    
  # Register the function called when our window is resized.
  glutReshapeFunc(ReSizeGLScene)

  # Register the MouseSelection class update function when mouse is ...?
  mouse = ms.MouseSelection()
  glutMouseFunc(mouse.getClick)
  glutMotionFunc(mouse.getDrag)
  glutPassiveMotionFunc(mouse.getPos)

  # Register the function called when the keyboard is pressed.  
  glutKeyboardFunc(keyPressed)

  # Initialize our window. 
  InitGL(640, 480)

  audio = ag.AudioGrabber(mouse = 'mouse', audioSrc = 'groove.wav', bufferSize = 1024, sampleRate = 44100, split = 0.3, factor = 0.2)

# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."

if __name__ == '__main__':
  try:
    GLU_VERSION_1_2
  except:
    print "Need GLU 1.2 to run this demo"
    sys.exit(1)
  main()
  glutMainLoop()
    	
