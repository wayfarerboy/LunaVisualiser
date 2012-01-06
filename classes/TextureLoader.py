#!/usr/bin/python

# A class to load a directory of images and convert them to OpenGL textures
# An optional title can be passed to the class, and this is then
# created using PIL

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import sys, os, Image, time, psutil, ImageDraw, ImageFont
import numpy as np

class TextureLoader:

  def __init__(self, _root, _dirname, _title, _fade, _titleDur, _duration, _scale, _font, _fontSize):
    self.playlist = []
    self.imagelist = []
    self.current = 0
    self.title = _title
    self.font = _font
    self.fontSize = _fontSize
    self.fade = _fade
    self.titleDur = _titleDur+_fade
    self.duration = _duration+_fade
    self.titleImage = None
    self.scale = _scale
    self.INIT = False
    for dirname, dirnames, filenames in os.walk(_root+_dirname):
      for filename in filenames:
        filepath = os.path.join(dirname, filename)
        try:
          im = Image.open(filepath)
          rawImg = im.tostring("raw", "RGBX", 0, -1)
        except:
          im = None
          rawImg = None
          pass
        if im != None and rawImg != None:
          self.imagelist.append({'filepath':filepath,'dirname':_dirname})
          #im.close()

  def load(self, offset):
    self.INIT = True
    # Create title texture
    windowSize = np.array([glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)])
    print windowSize
    titleImage = Image.new('RGB', windowSize.astype(tuple))
    titleImage.paste((0,0,0), None)
    imInfo = {'fade': self.fade, 'scale': 1.0, 'duration':self.fade*1.5, 'filepath':'Blank page', 'img':titleImage.tostring('raw', 'RGBX', 0, -1), 'size':np.array(titleImage.size).astype(float), 'i':offset, 'title':False}
    self.playlist.append(imInfo)
    self.convert_to_texture(imInfo)
    offset+=1
    if self.title != None:
      draw = ImageDraw.Draw(titleImage)
      font = ImageFont.truetype(self.font, int(self.fontSize * (windowSize[0] * windowSize[1])))
      textSize = draw.textsize(self.title, font=font)
      loc = (np.array(titleImage.size) - np.array(textSize)) * 0.5
      draw.text(loc.astype(tuple), self.title, font=font, fill=(255,255,255))
      imInfo = {'fade': self.fade, 'scale': 1.0, 'duration':self.titleDur,'filepath':'Title page: '+self.title, 'img':titleImage.tostring('raw', 'RGBX', 0, -1), 'size':np.array(titleImage.size).astype(float), 'i':offset, 'title':True}
      self.playlist.append(imInfo)
      self.convert_to_texture(imInfo)
      offset+=1
    # Load images into memory
    for img in self.imagelist:
      im = Image.open(img['filepath'])
      img['img'] = im.tostring("raw", "RGBX", 0, -1)
      img['size'] = np.array(im.size).astype(float)
      img['i'] = self.imagelist.index(img)+offset
      img['title'] = False
      img['scale'] = self.scale
      img['duration'] = self.duration
      img['fade'] = self.fade
      self.playlist.append(img)
      self.convert_to_texture(img)
    titleImage = Image.new('RGB', windowSize.astype(tuple))
    titleImage.paste((0,0,0), None)
    imInfo = {'fade': self.fade, 'scale': 1.0, 'duration':self.fade*1.5, 'filepath':'Blank page', 'img':titleImage.tostring('raw', 'RGBX', 0, -1), 'size':np.array(titleImage.size).astype(float), 'i':len(self.imagelist)+offset, 'title':False}
    self.playlist.append(imInfo)
    self.convert_to_texture(imInfo)
    offset+=1

  def convert_to_texture(self, imInfo):
    # Convert image to OpenGL texture
    glGenTextures(1, imInfo['i'])
    glBindTexture(GL_TEXTURE_2D, imInfo['i'])   # 2d texture (x and y size)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, imInfo['size'][0], imInfo['size'][1], 0, GL_RGBA, GL_UNSIGNED_BYTE, imInfo['img'])
    print str(imInfo['i'])+': '+os.path.basename(imInfo['filepath'])+' loaded: '+self.convert_bytes(psutil.avail_phymem())+' free'

  def convert_bytes(self, bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
      terabytes = bytes / 1099511627776
      size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
      gigabytes = bytes / 1073741824
      size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
      megabytes = bytes / 1048576
      size = '%.2fM' % megabytes
    elif bytes >= 1024:
      kilobytes = bytes / 1024
      size = '%.2fK' % kilobytes
    else:
      size = '%.2fb' % bytes
    return size

  def kill(self):
    idList = []
    for imInfo in self.playlist:
      idList.append(int(imInfo['i']))
    glDeleteTextures(1, idList)
