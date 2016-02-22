# -*- encoding: UTF-8 -*-

from naoqi import ALProxy
import sys

tts = ALProxy("ALTextToSpeech", "192.168.43.171", 9559)
tts.setLanguage("English")
# tts.setLanguage("Japanese")

for line in sys.stdin:
    tts.say(line)
