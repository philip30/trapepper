import sys, re
import pyaudio, wave
import requests

from trapepper.util import log

class SpeechRecognition:
    
    def __init__(self, debug=False):
        self.debug = debug
        self.s = requests.Session()

    def record(self):
        print("recording...")
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = 7
        
        p = pyaudio.PyAudio()
        
        stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=chunk)
        
        frames = []
        for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
            print("recording... ", str(i), "/", int(RATE / chunk * RECORD_SECONDS), "\r")
            data = stream.read(chunk)
            frames.append(data)
        
        wf = wave.open("./trapepper/sample.wav", "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


    def recognize(self):
        if self.debug:
            return input("User: ")
        else:
            url = "http://192.168.43.29:8000/asr_julius"
            self.record()
            files = {
                    'myFile': open('./trapepper/sample.wav', 'rb')
                    }
            r = self.s.post(url, files=files)
            line = r.text.split('\n')[0].split(':')[-1].replace(' ', '')

            log("INPUT:", line)
            if len(line) == 0: return None
            else: return line
