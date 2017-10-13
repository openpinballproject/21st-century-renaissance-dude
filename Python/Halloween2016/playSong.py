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
# @file:   playSong.py
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
# Simple test song to verify button/pygame functionality.  The 48s sample
# starts playing immediately, after the sample is completed, it waits for the
# button to be pressed and released.  At that time, it plays the shorter 27s
# sample.
#
#===============================================================================
import pygame
from time import sleep
from neopixel import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reset = False

pygame.mixer.init()
pygame.mixer.music.load("/home/pi/Halloween/startSample-48s.mp3")
while (GPIO.input(23) == 1):
	sleep(0.1)

pygame.mixer.music.play()
while (pygame.mixer.music.get_busy() == 1):
	sleep(0.1)

pygame.mixer.music.load("/home/pi/Halloween/midSample-27s.mp3")

while (GPIO.input(23) == 0):
	sleep(0.1)

while (GPIO.input(23) == 1):
	sleep(0.1)

pygame.mixer.music.play()

while (pygame.mixer.music.get_busy() == 1):
	sleep(0.1)

