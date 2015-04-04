import serial

import pygame

arduino_conn = serial.Serial('/dev/ttyACM0', 9600, timeout=0)

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

key_noise = pygame.mixer.Sound('/home/pi/mspf_audio/key_noise.wav')
track_1 = pygame.mixer.Sound('/home/pi/tasty_waves.wav')

while True:
    key = arduino_conn.read()
    if key:
        key_noise.play()
