import serial
import time

import pygame

try:
    arduino_conn = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
except:
    print('no arduino')

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()

key_channel = pygame.mixer.Channel(1)
track_channel = pygame.mixer.Channel(2)

key_noise = pygame.mixer.Sound('/home/herb/mspf_audio/key_noise.wav')
track_1 = pygame.mixer.Sound('/home/herb/mspf_audio/01.wav')


key_channel.play(key_noise)
# track_channel.play(track_1)
time.sleep(2)
key_noise.play()


while False:
    key = arduino_conn.read()
    if key:
        key_noise.play()
