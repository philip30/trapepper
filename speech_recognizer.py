import sys

from trapepper.util import log

class SpeechRecognition:
    
    def __init__(self, debug=False):
        self.debug = debug

    def recognize(self):
        if self.debug:
            return input("User: ")
        else:
            line = sys.stdin.readline().strip()
            log("INPUT:", line)
            if len(line) == 0: return None
            else: return line
