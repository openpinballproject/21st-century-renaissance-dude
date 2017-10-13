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
# @file:   battTest.py
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
# Battery test to verify cell phone recharge battery pack has enough power to
# run Halloween costume for at least 2 hours
#
#===============================================================================
import time

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

WholeStrip = SubStrip(0,72,0)
WholeStrip1 = SubStrip(0,72,1)
WholeStrip2 = SubStrip(0,72,2)

Green = Color(255, 0, 0)
Red = Color(0, 255, 0)
Blue = Color(0, 0, 255)
White = Color(255, 255, 255)
Black = 0

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

   wait_ms=250
   while (True):
      theaterChase(strip,WholeStrip, Red, erase_prev=False)
      theaterChase(strip,WholeStrip1, Green, erase_prev=False)
      theaterChase(strip,WholeStrip2, Blue, erase_prev=False)
      strip.show()
      time.sleep(wait_ms/1000.0)
