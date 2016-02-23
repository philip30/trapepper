#!/usr/bin/python

import sys

# Pepper configuration
NAME = "PepperSpeechSynthesis"
IP = "192.168.43.171"
LANG = "Japanese"
PORT = 9559

try:
    from naoqi import ALProxy
    import sys
    
    tts = ALProxy(NAME, IP, PORT)
    tts.setLanguage(LANG)
except Exception:
    pass

for line in sys.stdin:
    try:
        tts.say(line)
    except Exception:
        pass

    print(line)
    sys.stdout.flush()

