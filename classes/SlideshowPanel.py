#!/usr/bin/python

# A class to load a directory of images and convert them to OpenGL textures
# An optional title can be passed to the class, and this is then
# created using PIL

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np
import random

class SlideshowPanel:

  def __init__(self, _texture, _timing):
    self.texture = _texture
    self.timer = [ float(_timing), self.texture['duration'] ]
    self.scale = self.texture['scale']
    self.rand = np.array([np.array([random.random(), random.random()]), np.array([random.random(), random.random()])])
    self.sizes = int(random.random()*2)

  def update(self, timing, _size):
    perc = (timing - self.timer[0]) / self.timer[1]
    alph = 1.0
    RET = 0
    if timing - self.timer[0] > self.timer[1] - self.texture['fade']:
      RET = 1
      alph = 1 - (timing - self.timer[0] - (self.timer[1] - self.texture['fade'])) / self.texture['fade']
      if alph < 0: alph = 0
    if perc > 1:
      perc = 1.0
      RET = 2
    sizes = []
    sizes.append(self.fill_area(_size, self.texture['size']))
    sizes.append(sizes[0] * self.scale)
    loc = (np.array([_size, _size]) - sizes) * self.rand
    if self.scale == 1.0:
      newLoc = [0,0]
      newSize = _size
    else:
      newLoc = self.lerp(loc[0], loc[1], perc)
      newSize = self.lerp(sizes[0], sizes[1], perc)
    glBindTexture(GL_TEXTURE_2D,self.texture['i'])
    glBegin(GL_QUADS) # Start Drawing The Quad
    glColor4f(alph, alph, alph, alph)
    glTexCoord2f(0,0)
    glVertex3f(newLoc[0], newLoc[1],perc) # Top Right Of The Quad (Top)
    glTexCoord2f(0,1)
    glVertex3f(newLoc[0], newLoc[1]+newSize[1],perc) # Top Left Of The Quad (Top)
    glTexCoord2f(1,1)
    glVertex3f(newLoc[0]+newSize[0], newLoc[1]+newSize[1], perc) # Bottom Left Of The Quad (Top)
    glTexCoord2f(1,0)
    glVertex3f(newLoc[0]+newSize[0], newLoc[1], perc) # Bottom Right Of The Quad (Top)
    glEnd() # Done Drawing The Quad
    return RET

  def fill_area(self, _area, _size):
    aRatio = _area[0] / _area[1]
    sRatio = _size[0] / _size[1]
    _scale = _area[1] / _size[1]
    if sRatio < aRatio:
      _scale = _area[0] / _size[0]
    return np.array(_size * _scale)

  def lerp(self, _a1, _a2, p):
    a1 = _a1
    a2 = _a2
    if self.sizes == 1:
      a1 = _a2
      a2 = _a1
    a3 = a2 - a1
    a4 = a3 * p
    return a4 + a1
