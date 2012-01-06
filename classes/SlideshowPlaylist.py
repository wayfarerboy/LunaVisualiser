#!/usr/bin/python

import sys, os, Image, time, psutil, ImageDraw
import SlideshowPanel as spanel
import TextureLoader as tl
import numpy as np

class SlideshowPlaylist:

  def __init__(self, _path, _scale, _fade, _titleDur, _duration, _font, _fontSize):
    try:
      f = open(_path+'titles', 'r')
      self.titles = f.readlines()
      f.close()
    except:
      self.titles = []
    self.textures = []
    self.dirNum = -1
    self.scale = _scale
    self.panelOrder = [ 0, 1 ]
    dirs = []
    for _root, _dirs, files in os.walk(_path):
      root = _root
      for d in _dirs:
        dirs.append(d)
      break
    dirs.sort()
    for d in dirs:
      i = dirs.index(d)
      title = None
      if len(self.titles) > 0: title = self.titles[i]
      self.textures.append(tl.TextureLoader(root, dirs[i], title, _fade, _titleDur, _duration, self.scale, _font, _fontSize))
    self.panels = [None, None]
    self.INIT = False
    
  def update(self, _size):
    if self.INIT != True:
      self.start = time.time() * 1000
      self.next_playlist(0)
      self.INIT = True
    for k in self.panelOrder:
      if self.panels[k] != None:
        resp = self.panels[k].update(time.time() * 1000, _size)
        if resp == 1 and self.panels[int(k==0)] == None:
          self.next_panel(int(k == 0))
        elif resp == 2 and self.panels[int(k==0)] != None:
          self.panels[k] = None
    
  def next_panel(self, _panelNum):
    if self.imageNum == len(self.textures[self.dirNum].playlist):
      self.next_playlist(_panelNum)
    else:
      self.panels[_panelNum] = spanel.SlideshowPanel(self.textures[self.dirNum].playlist[self.imageNum], time.time() * 1000)
      self.imageNum += 1
    self.panelOrder = self.panelOrder[::-1]

  def next_playlist(self, _panelNum):
    # if self.dirNum > -1: self.textures[self.dirNum].kill()
    self.dirNum+=1
    if self.dirNum > len(self.textures): self.dirNum = 0
    offset = 0
    if self.dirNum > 0: offset = self.textures[self.dirNum-1].playlist[len(self.textures[self.dirNum].playlist)-1]['i'] + 1
    self.textures[self.dirNum].load(offset)
    self.panels[_panelNum] = spanel.SlideshowPanel(self.textures[self.dirNum].playlist[0], time.time() * 1000)
    self.imageNum = 1
