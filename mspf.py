#!/usr/bin/env python
import argparse
import logging
import pygame
import os
import random
import sys
import serial
from string import ascii_lowercase


def sounds_from_directory(directory):
    filenames = [directory + filename for filename in os.listdir(directory) if filename.endswith(".wav")]
    sounds = [pygame.mixer.Sound(filename) for filename in filenames]
    return sounds, filenames


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Accepts characters a-z and plays an audio file.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--loglevel', help='Set log level to DEBUG, INFO, WARNING, or ERROR', default='INFO')
    parser.add_argument('--logfile', help='Log file to append to.',)
    parser.add_argument('--uart', help='File descriptor of UART to connect to.', metavar="DEVICE[,BAUD]", default='/dev/tty.usbmodem836341')
    parser.add_argument('--quote_dir', help='Directory containing quote wav files (must be 44.1kHz)', default='audio/quotes/')
    parser.add_argument('--key_dir', help='Directory containing keystroke wav files (must be 44.1kHz)', default='audio/keys/')

    args = parser.parse_args()
    log_level = args.loglevel
    log_file = args.logfile
    uart = args.uart
    quote_dir = args.quote_dir
    key_dir = args.key_dir

    numeric_log_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logging.basicConfig(level=numeric_log_level, format='%(asctime)s %(levelname)s:%(message)s', filename=log_file)

    # Parse the uart string and optional baud
    if ',' in uart:
        device, baud = uart.split(',')
    else:
        device = uart
        baud = 115200

    try:
        arduino_conn = serial.Serial(port=device, baudrate=baud, timeout=None)
    except:
        # TO DO: handle this better, check for other tty devices.
        print('No Arduino detected on uart %s' % uart)
        sys.exit(1)

    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

    keystroke_channel = pygame.mixer.Channel(1)
    quote_channel = pygame.mixer.Channel(2)

    keystroke_sounds, keystroke_filenames = sounds_from_directory(key_dir)
    quotes, quote_filenames = sounds_from_directory(quote_dir)

    while True:
        keystroke = arduino_conn.read()
        if keystroke:
            index = ascii_lowercase.index(keystroke)
            keystroke_index = random.randint(0, len(keystroke_sounds) - 1)
            keystroke_sound = keystroke_sounds[keystroke_index]
            keystroke_channel.play(keystroke_sound)

            logging.debug("Queueing quote %s" % quote_filenames[index % len(quotes)])
            quote = quotes[index % len(quotes)]
            quote_channel.queue(quote)
