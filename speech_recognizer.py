import sys, re
import requests

from trapepper.util import log

class SpeechRecognition:
    
    def __init__(self, debug=False):
        self.debug = debug
        self.s = requests.Session()

    def recognize(self):
        if self.debug:
            return input("User: ")
        else:
            url = "http://localhost:8000/asr_julius"
            url = "http://192.168.43.29:8000/asr_julius"
            files = {
                    'myFile': open('./trapepper/resources/nara_1chann.wav', 'rb')
                    }
            r = self.s.post(url, files=files)
            line = r.text.split('\n')[0].split(':')[-1].replace(' ', '')

            log("INPUT:", line)
            if len(line) == 0: return None
            else: return line
