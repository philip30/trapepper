# -*- encoding: UTF-8 -*-

import sys
import os
from subprocess import Popen, PIPE

SERVER   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pepper/server.py")
NAOQI_PY = "/usr/bin/python"

class SpeechSynthesizer:
    def synthesize(self, response):
        command = [NAOQI_PY, SERVER]
        server_p = Popen(command, 0, shell=False, stdin=PIPE, stdout=PIPE, stderr=sys.stderr)
        out, err  = server_p.communicate(input=bytes(response + "\n", "UTF-8"))
        out = out.decode("utf-8").strip()
        print("MACHINE:", out)
        return out

def __main__():
    speech_synthesizer = SpeechSynthesizer()
    speech_synthesizer.synthesize("こんにちは！")

if __name__ == '__main__':
    __main__()
