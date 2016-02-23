#!/usr/bin/python

import sys

# Pepper configuration
NAME = "ALTextToSpeech"
IP = "192.168.43.171"
LANG = "Japanese"
PORT = 9559

from naoqi import ALProxy
import sys
    
tts = ALProxy(NAME, IP, PORT)
tts.setLanguage(LANG)

for line in sys.stdin:
    #try:
    tts.say(line)

    print(line)
    sys.stdout.flush()
