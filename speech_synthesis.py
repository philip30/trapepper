# -*- encoding: UTF-8 -*-

from naoqi import ALProxy

class SpeechSynthesizer:
    def __init__(self, ip="192.168.43.171"):
        self.tts = ALProxy("ALTextToSpeech", ip, 9559)
        self.tts.setLanguage("Japanese")

    def synthesize(self, response):
        print("MACHINE:",response)
        tts.say(response)
        return response

def __main__(self):
    speech_synthesizer = SpeechSynthesizer()
    speech_synthesizer.synthesize("こんにちは！")
