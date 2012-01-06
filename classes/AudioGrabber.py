import pyaudio
import aubio
import numpy as np
import struct
import wave

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import threading
import time, datetime
import math

class AudioGrabber:

  def __init__(self, mouse, audioSrc = 'pulse', bufferSize = 512, sampleRate = 44100, split = 0.4, factor = 0.2):
    self.bufferSize = bufferSize
    self.sampleRate = sampleRate
    self.stream = None
    self.audioSrc = audioSrc
    self.data = np.array([])
    self.split = split
    self.factor = factor
    self.resize()
    self.chunks = []
    self.ffts = []
    self.STOPPED = False
    self.mouse = mouse
    self.selections = []

  def update(self):
    if self.stream is None:
        self.p = pyaudio.PyAudio()
        if len(self.audioSrc) > 5:
          wf = wave.open(self.audioSrc, 'rb')
          self.sampleRate = wf.getframerate()
          self.stream = self.p.open(format = self.p.get_format_from_width(wf.getsampwidth()),
                                    channels = wf.getnchannels(),
                                    rate = wf.getframerate(),
                                    output = True)
        else:
          for x in range(self.p.get_device_count()):
            if self.p.get_device_info_by_index(x)['name'] == audioSrc:
              break;
          if x < self.p.get_device_count()-1:
            self.stream = self.p.open(format = pyaudio.paInt16, 
                                      channels = 1, 
                                      rate = self.sampleRate, 
                                      input = True, 
                                      frames_per_buffer = self.bufferSize*2, 
                                      input_device_index = x)
          else:
            raise Exception("Could not find pulse audio device")
        threading.Thread(target=self.getstream).start()

    if len(self.chunks) > 0:
      d = np.fromstring(self.chunks.pop(0), dtype=np.short)
      ffty = np.fft.fft(d)
      ffty = abs(ffty[0:len(ffty)*0.5])*0.0001
      ffty1 = ffty[:len(ffty)*0.5]
      ffty2 = ffty[len(ffty)*0.5::]+2
      ffty2 = ffty2[::-1]
      ffty = ffty1+ffty2
      ffty = np.log(ffty)-2
      #fftx,ffty = self.downSample(self.fftx,ffty,5)
      ffty = self.smoothMemory(ffty,3)
      if len(ffty) > 0: self.data = ffty[1:int(len(ffty)*self.split)] * self.factor
      
    if len(self.data) > 0:
      #print str(len(ffty))+' samples, '+str((min(ffty)+1)*0.5)+' -> '+str((max(ffty)+1)*0.5)
      count = 0.0

      glBegin(GL_TRIANGLES)
      glColor4f(1.0, 1.0, 1.0, 0.6)

      for i in self.data:
        val = np.array([(count/len(self.data), (count+1)/len(self.data)), (0.0, i)]) * self.winSize
        glVertex3f(val[0][0], val[1][0], 0.0)
        glVertex3f(val[0][1], val[1][0], 0.0)
        glVertex3f(val[0][1], val[1][1], 0.0)
      
        glVertex3f(val[0][1], val[1][1], 0.0)
        glVertex3f(val[0][0], val[1][1], 0.0)
        glVertex3f(val[0][0], val[1][0], 0.0)
        count += 1.0
      glEnd()

      click = self.checkClick()
      select = self.mouse.checkSelect()
      
      for s in self.selections:
        s.update(self.data)
      if self.checkClick() == 0: self.MOUSE = True # Check for a new click
      if self.MOUSE == True:
        selection = self.mouse.getSelection() # Get current selection if mouse has registered a click
        if self.mouse.MOUSE == False: # If the mouse has been released
          self.MOUSE = False # Set local variable
          self.selections.append(selection) # Add selection to array if the mouse has been released
      
      ss = self.selections # Make a copy of the selections
      if self.MOUSE == True: ss.prepend(selection) # Prepend the current selection to the temp selections list 
      
      for s in ss:

        if self.mouse.MOUSE == True:
          average = 0.2
        else:
          average = np.average(self.data[int(s[0][0]*len(self.data)):int(s[1][0]*len(self.data))])
          average = (average - s[0][1]) / (s[1][1] - s[0][1])
          if average > 1.0: average = 1.0
          if average < 0.0: average = 0.0
      
        s = s * np.array([self.mouse.winSize, self.mouse.winSize]) + [(1,1),(0,0)]
         
        glBegin(GL_TRIANGLES)
        
        glColor4f(1.0,1.0,1.0,average)
        
        glVertex3f(s[0][0], s[0][1], 0.0)
        glVertex3f(s[1][0], s[0][1], 0.0)
        glVertex3f(s[1][0], s[1][1], 0.0)
        
        glVertex3f(s[1][0], s[1][1], 0.0)
        glVertex3f(s[0][0], s[1][1], 0.0)
        glVertex3f(s[0][0], s[0][1], 0.0)
        
        glEnd()

        glBegin(GL_LINES)
        
        glColor4f(1.0,1.0,1.0,1.0)
        
        glVertex3f(s[0][0], s[0][1], 0.0)
        glVertex3f(s[1][0], s[0][1], 0.0)

        glVertex3f(s[1][0], s[0][1], 0.0)
        glVertex3f(s[1][0], s[1][1], 0.0)
        
        glVertex3f(s[1][0], s[1][1], 0.0)
        glVertex3f(s[0][0], s[1][1], 0.0)

        glVertex3f(s[0][0], s[1][1], 0.0)
        glVertex3f(s[0][0], s[0][1], 0.0)
        
        glEnd()

  def downSample(self, fftx,ffty,degree=10):
    x,y=[],[]
    for i in range(len(ffty)/degree-1):
      x.append(fftx[i*degree+degree/2])
      y.append(sum(ffty[i*degree:(i+1)*degree])/degree)
    return [x,y]

  def smoothMemory(self, ffty, degree=3):
    self.ffts = self.ffts+[ffty]
    if len(self.ffts) <= degree: return ffty
    self.ffts = self.ffts[1:]
    return np.average(np.array(self.ffts),0)

  def getstream(self):
    while self.STOPPED is False:
      try:
        self.chunks.append(self.stream.read(self.bufferSize))
      except IOError,e:
        if e[1] == pyaudio.paInputOverflowed:
          pass
  
  def resize(self):
    self.winSize = np.array([(glutGet(GLUT_WINDOW_WIDTH),glutGet(GLUT_WINDOW_WIDTH)), (glutGet(GLUT_WINDOW_HEIGHT), glutGet(GLUT_WINDOW_HEIGHT))]) * np.array([(1.0,1.0),(1.0,1.0)])

  def kill(self):
    STOPPED = True
    self.close()
    
  def close(self):
    self.stream.stopstream()
    self.stream.close()
    self.p.terminate()
