import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class MouseSelection:
  
  def __init__(self):
    self.loc = 0,0
    self.selection = [(0.0, 0.0), (1.0, 1.0)]
    self.MOUSE = False
    self.button = -1
    self.resize()
    self.select = -1,-1

  def getClick(self,button,state,x,y):
    self.button = button
    self.setLoc(x,y)
    if self.MOUSE == False and state == 0:
      self.MOUSE = True
      if button == 0: self.selection = [self.loc.copy(), self.loc.copy()]
    elif self.MOUSE == True and state == 1:
      self.MOUSE = False
      if button == 1:
        if np.array(self.selection[0] == self.selection[1]).all():
          self.select = self.loc
          self.selection = [(0.0, 0.0), (1.0, 1.0)]
        else:
          self.correctSelection()

  def getDrag(self,x,y):
    self.setLoc(x,y)
    self.selection[1] = self.loc.copy()
    
  def getPos(self,x,y):
    self.setLoc(x,y)

  def setLoc(self,x,y):
    self.loc = (x,self.winSize[1] - y) / self.winSize

  def getLocPixels(self):
    return self.loc * self.winSize

  def getSelectionPixels(self):
    return self.selection * np.array([self.winSize, self.winSize])
  
  def checkClick(self):
    b = self.button
    self.button = -1
    return b
    
  def checkSelect(self):
    s = self.select
    self.select = -1,-1
    return s
    
  def correctSelection(self):
    s = self.selection
    self.selection = [(max(min(s[0][0],s[1][0]),0.0), max(min(s[0][1], s[1][1]),0.0)),(min(max(s[0][0],s[1][0]),1.0), min(max(s[0][1], s[1][1]), 1.0))]

  def resize(self):
    self.winSize = np.array([float(glutGet(GLUT_WINDOW_WIDTH)),float(glutGet(GLUT_WINDOW_HEIGHT))])
