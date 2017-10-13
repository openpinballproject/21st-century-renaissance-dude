# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
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
WholeStrip = SubStrip(0,132,0)

Green = Color(255, 0, 0)
Red = Color(0, 255, 0)
Blue = Color(0, 0, 255)
White = Color(255, 255, 255)
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

   while (True):
      while (GPIO.input(23) == 0):
         time.sleep(0.1)

      while (GPIO.input(23) == 1):
         time.sleep(0.1)

      print "starting show"
      setColor(strip, WholeStrip, 0)
      strip.show()
      Glasses.currIdx = 0
      BtmMouth.currIdx = 0
      TopMouth.currIdx = 0
      Spiral.currIdx = 0
      WholeStrip.currIdx = 0
      startTime = time.time()
      rounds = 12
      wait_ms = 250
      openMouth(strip, Red)
      for i in range(rounds):
         theaterChase(strip,Glasses, Red)
         createTrail(strip,Spiral, Red, increment=3, erase_prev=True)
         strip.show()
         time.sleep(wait_ms/1000.0)
      
      setColor(strip, WholeStrip, 0)
      closeMouth(strip, Green)
      for i in range(rounds):
         theaterChase(strip,Glasses, Green,forward=False)
         createTrail(strip,Spiral, Green, increment=3, erase_prev=True)
         strip.show()
         time.sleep(wait_ms/1000.0)

      setColor(strip, WholeStrip, 0)
      openMouth(strip, Blue)
      for i in range(rounds):
         theaterChase(strip,Glasses, Blue)
         createTrail(strip,Spiral, Blue, increment=3, erase_prev=True)
         strip.show()
         time.sleep(wait_ms/1000.0)

      setColor(strip, WholeStrip, 0)
      openMouth(strip, Green)
      Glasses.currIdx = 2
      Glasses1.currIdx = 1
      Glasses2.currIdx = 0
      for i in range(rounds):
         theaterChase(strip,Glasses, Red, erase_prev=False)
         theaterChase(strip,Glasses1, Green, erase_prev=False)
         theaterChase(strip,Glasses2, Blue, erase_prev=False)
         createTrail(strip,Spiral, Blue, increment=3, erase_prev=True)
         strip.show()
         time.sleep(wait_ms/1000.0)

      setColor(strip, WholeStrip, 0)
      setColor(strip, Glasses, White)
      strip.show()

      time.sleep(5)
      setColor(strip, WholeStrip, 0)
      strip.show()
      print "show over"
