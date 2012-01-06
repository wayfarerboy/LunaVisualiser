import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import threading
import time, datetime
import math

class AudioGrabber:

  def __init__(self, id, mouse, selection):
    self.selection = selection
    self.mouse = mouse
    self.id = id

  def update(self, data):
    if self.mouse.MOUSE == True:
      average = 0.2
    else:
      average = np.average(data[int(self.selection[0][0]*len(data)):int(self.selection[1][0]*len(data))])
      average = (average - self.selection[0][1]) / (self.selection[1][1] - self.selection[0][1])
      if average > 1.0: average = 1.0
      if average < 0.0: average = 0.0
      
    s = self.selection * np.array([self.mouse.winSize, self.mouse.winSize]) + [(1,1),(0,0)]
    
    glBegin(GL_TRIANGLES)
    
    glColor4f(1.0,1.0,1.0,average)
    
    glVertex3f(self.selection[0][0], self.selection[0][1], 0.0)
    glVertex3f(self.selection[1][0], self.selection[0][1], 0.0)
    glVertex3f(self.selection[1][0], self.selection[1][1], 0.0)
    
    glVertex3f(self.selection[1][0], self.selection[1][1], 0.0)
    glVertex3f(self.selection[0][0], self.selection[1][1], 0.0)
    glVertex3f(self.selection[0][0], self.selection[0][1], 0.0)
    
    glEnd()

    glBegin(GL_LINES)
    
    glColor4f(1.0,1.0,1.0,selectionBorder)
    
    glVertex3f(self.selection[0][0], self.selection[0][1], 0.0)
    glVertex3f(self.selection[1][0], self.selection[0][1], 0.0)

    glVertex3f(self.selection[1][0], self.selection[0][1], 0.0)
    glVertex3f(self.selection[1][0], self.selection[1][1], 0.0)
    
    glVertex3f(self.selection[1][0], self.selection[1][1], 0.0)
    glVertex3f(self.selection[0][0], self.selection[1][1], 0.0)

    glVertex3f(self.selection[0][0], self.selection[1][1], 0.0)
    glVertex3f(self.selection[0][0], self.selection[0][1], 0.0)
    
    glEnd
  
  def isInside(self):
    loc = self.mouse.getLocPixels()
    select = self.selection * np.array([self.mouse.winSize, self.mouse.winSize]) + [(1,1),(0,0)]
    if loc[0] >= select[0] and loc[0] <= select[2] and loc[1] >= select[1] and loc[1] <= select[3]: return True
    return False

  def 
