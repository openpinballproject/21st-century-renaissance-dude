#!/usr/bin/env python
#
#===============================================================================
#
#                         OOOO
#                       OOOOOOOO
#      PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
#    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#   PPP         PPP   OOO      OOO   PPP         PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#   PPP         PPP   OOO      OOO   PPP         PPP
#    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#     PPPPPPPPPPPPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP    OOO    OOO    PPP
#               PPP     OOOOOOOO     PPP
#              PPPPP      OOOO      PPPPP
#
# @file:   interGalactic.py
# @author: Hugh Spahr
# @date:   10/10/2016
#
# @note:   Open Pinball Project
#          Copyright 2016, Hugh Spahr
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#===============================================================================
#
# Main program to run the Halloween 2016 costume.  It plays a 48s sample
# of Intergalactic by the Beastie Boys, and animates LED lights to synchronize
# with the music.  To start the show, a button is pressed and released.
#
#===============================================================================
import time
import datetime
import pygame
from time import sleep
from neopixel import *

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

debug = False
if not debug:
   from neopixel import *

class SubStrip:
   def __init__(self, startIdx, numLeds, currIdx):
      self.startIdx = startIdx
      self.numLeds = numLeds
      self.currIdx = currIdx

# LED strip configuration:
LED_COUNT      = 132     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 127     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

Glasses = SubStrip(0,23,0)
Glasses1 = SubStrip(0,23,0)
Glasses2 = SubStrip(0,23,0)
Unused = SubStrip(23,8,0)
BtmMouth = SubStrip(31,10,0)
TopMouth = SubStrip(41,9,0)
Spiral = SubStrip(50,82,0)
Spiral1 = SubStrip(50,82,0)
Spiral2 = SubStrip(50,82,0)
WholeStrip = SubStrip(0,132,0)

Green = Color(255, 0, 0)
Red = Color(0, 255, 0)
Blue = Color(0, 0, 255)
White = Color(255, 255, 255)
Purple = Color(255, 255, 0)
Black = 0

def createTrail(strip, substrip, color, bgnd_color=0, forward=True, erase_prev=False, increment=1):
   """Create a trail of lights"""
   setpixels = []
   clearpixels = []
   if forward:
      for i in range(substrip.startIdx + (substrip.currIdx % increment), substrip.startIdx + substrip.currIdx, increment):
         # Turn off previous LED
         if erase_prev and (i != substrip.startIdx):
            if not debug:
               strip.setPixelColor(i - 1, bgnd_color)
            clearpixels.append(i - 1)
         # Turn on new LED
         if not debug:
            strip.setPixelColor(i, color)
         setpixels.append(i)
   else:
      for i in range(substrip.startIdx + substrip.numLeds - 1 - (substrip.currIdx % increment), substrip.startIdx + substrip.numLeds - 1 - substrip.currIdx, -increment):
         # Turn off previous LED
         if erase_prev and (i != substrip.startIdx + substrip.numLeds - 1):
            if not debug:
               strip.setPixelColor(i + 1, bgnd_color)
            clearpixels.append(i + 1)
         # Turn on new LED
         if not debug:
            strip.setPixelColor(i, color)
         setpixels.append(i)
   substrip.currIdx += 1
   if (substrip.currIdx > substrip.numLeds):
      substrip.currIdx -= increment
   if debug:
      print "Setpixels = " + repr(setpixels)
      print "Clearpixels = " + repr(clearpixels)

def setColor(strip, substrip, color):
   """Set color across whole substrip"""
   setpixels = []
   for i in range(substrip.startIdx, substrip.startIdx + substrip.numLeds):
      if not debug:
         strip.setPixelColor(i, color)
      setpixels.append(i)
   if debug:
      print "Setpixels = " + repr(setpixels)

def openMouth(strip, color):
   """Set color on whole mouth"""
   setColor(strip, BtmMouth, color)
   setColor(strip, TopMouth, color)

def closeMouth(strip, color):
   """Set color on only bottom mouth"""
   setColor(strip, BtmMouth, color)
   setColor(strip, TopMouth, 0)
      
def theaterChase(strip, substrip, color, bgnd_color=0, forward=True, erase_prev=True, increment=3):
   """Movie theater light style chaser animation."""
   setpixels = []
   clearpixels = []
   if erase_prev:
      if forward:
         if substrip.currIdx == 0:
            prevIdx = increment - 1
         else:
            prevIdx = substrip.currIdx - 1
      else:
         if substrip.currIdx == increment - 1:
            prevIdx = 0
         else:
            prevIdx = substrip.currIdx + 1
   for i in range(substrip.startIdx, substrip.startIdx + substrip.numLeds, increment):
      # Turn off previous LED
      if erase_prev:
         if (i+prevIdx < substrip.startIdx + substrip.numLeds):
            if not debug:
               strip.setPixelColor(i+prevIdx, bgnd_color)
            clearpixels.append(i+prevIdx)
      # Turn on new LED
      if (i+substrip.currIdx < substrip.startIdx + substrip.numLeds):
         if not debug:
            strip.setPixelColor(i+substrip.currIdx, color)
         setpixels.append(i+substrip.currIdx)
   if forward:
      substrip.currIdx += 1
      if substrip.currIdx == increment:
         substrip.currIdx = 0
   else:
      substrip.currIdx -= 1
      if substrip.currIdx < 0:
         substrip.currIdx = increment - 1
   if debug:
      print "Setpixels = " + repr(setpixels)
      print "Clearpixels = " + repr(clearpixels)


# Main program logic follows:
if __name__ == '__main__':
   # Create NeoPixel object with appropriate configuration.
   if not debug:
      strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
      # Intialize the library (must be called once before other functions).
      strip.begin()
   else:
      strip = 0

   pygame.mixer.init()

   while (True):
      pygame.mixer.music.load("/home/pi/Halloween/startSample-48s.mp3")
         
      while (GPIO.input(23) == 0):
         time.sleep(0.1)

      while (GPIO.input(23) == 1):
         time.sleep(0.1)

      print "starting show"
      pygame.mixer.music.play()
      songStart = datetime.datetime.now()
      setColor(strip, WholeStrip, 0)
      strip.show()
      Glasses.currIdx = 0
      BtmMouth.currIdx = 0
      TopMouth.currIdx = 0
      Spiral.currIdx = 0
      WholeStrip.currIdx = 0
      startTime = time.time()
      wait_ms = 100
      update = True
      closeMouth(strip, Red)
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=5,milliseconds=0):
         if update:
            theaterChase(strip,Glasses, Red)
            createTrail(strip,Spiral, Red, increment=3, erase_prev=True)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)
      
      setColor(strip, WholeStrip, 0)
      closeMouth(strip, Green)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=9,milliseconds=400):
         if update:
            theaterChase(strip,Glasses, Green,forward=False)
            createTrail(strip,Spiral, Green, increment=3, erase_prev=True)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      setColor(strip, WholeStrip, 0)
      closeMouth(strip, Red)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=13,milliseconds=900):
         if update:
            theaterChase(strip,Glasses, Red)
            createTrail(strip,Spiral, Red, increment=3, erase_prev=True)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)


      setColor(strip, WholeStrip, 0)
      closeMouth(strip, Green)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=18,milliseconds=400):
         if update:
            theaterChase(strip,Glasses, Green,forward=False)
            createTrail(strip,Spiral, Green, increment=3, erase_prev=True)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      update = True
      Spiral.currIdx = 0
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=23,milliseconds=0):
         if update:
            theaterChase(strip,Glasses, Blue)
            theaterChase(strip,Spiral, Blue)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=23,milliseconds=800):
         if update:
            theaterChase(strip,Glasses, Blue,forward=False)
            theaterChase(strip,Spiral, Blue,forward=False)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=25,milliseconds=200):
         if update:
            theaterChase(strip,Glasses, Blue)
            theaterChase(strip,Spiral, Blue)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=26,milliseconds=300):
         if update:
            theaterChase(strip,Glasses, Blue,forward=False)
            theaterChase(strip,Spiral, Blue,forward=False)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=27,milliseconds=500):
         if update:
            theaterChase(strip,Glasses, Blue)
            theaterChase(strip,Spiral, Blue)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=29,milliseconds=600):
         if update:
            theaterChase(strip,Glasses, Blue,forward=False)
            theaterChase(strip,Spiral, Blue,forward=False)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=30,milliseconds=800):
         if update:
            theaterChase(strip,Glasses, Blue)
            theaterChase(strip,Spiral, Blue)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, Green)
      strip.show()
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=31,milliseconds=0):
         time.sleep(wait_ms/1000.0)

      openMouth(strip, 0)
      strip.show()
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=31,milliseconds=500):
         time.sleep(wait_ms/1000.0)

      openMouth(strip, Red)
      strip.show()
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=31,milliseconds=700):
         time.sleep(wait_ms/1000.0)

      openMouth(strip, 0)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=33,milliseconds=600):
         if update:
            theaterChase(strip,Spiral, Green)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, Green)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=33,milliseconds=800):
         if update:
            theaterChase(strip,Spiral, Green)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, 0)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=35,milliseconds=800):
         if update:
            theaterChase(strip,Spiral, Green, forward=False)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, Red)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=36,milliseconds=0):
         if update:
            theaterChase(strip,Spiral, Green, forward=False)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, 0)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=38,milliseconds=100):
         if update:
            theaterChase(strip,Spiral, Red)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, Blue)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=38,milliseconds=300):
         if update:
            theaterChase(strip,Spiral, Red)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, 0)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=40,milliseconds=500):
         if update:
            theaterChase(strip,Spiral, Red, forward=False)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, Purple)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=40,milliseconds=700):
         if update:
            theaterChase(strip,Spiral, Red, forward=False)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, 0)
      update = True
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=41,milliseconds=100):
         if update:
            theaterChase(strip,Spiral, Purple)
            strip.show()
            update = False
         else:
            update = True
         time.sleep(wait_ms/1000.0)

      openMouth(strip, White)
      Glasses.currIdx = 2
      Glasses1.currIdx = 1
      Glasses2.currIdx = 0
      Spiral.currIdx = 2
      Spiral1.currIdx = 1
      Spiral2.currIdx = 0
      wait_ms = 100
      while datetime.datetime.now() - songStart <= datetime.timedelta(seconds=42,milliseconds=100):
         theaterChase(strip,Glasses, Red, erase_prev=False)
         theaterChase(strip,Glasses1, Green, erase_prev=False)
         theaterChase(strip,Glasses2, Blue, erase_prev=False)
         theaterChase(strip,Spiral, Red, erase_prev=False)
         theaterChase(strip,Spiral1, Green, erase_prev=False)
         theaterChase(strip,Spiral2, Blue, erase_prev=False)
         strip.show()
         time.sleep(wait_ms/1000.0)

      setColor(strip, WholeStrip, 0)
      strip.show()
      print "show over"
