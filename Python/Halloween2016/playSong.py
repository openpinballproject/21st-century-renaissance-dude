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

