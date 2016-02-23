import sys, re
import pyaudio, wave
import requests
import speech_recognition as sr # SpeechRecognition (https://pypi.python.org/pypi/SpeechRecognition/)
import threading, time

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

    # callback for calling Google Speech Recognition API
    # called by other thread created by main thread
    def callback(self, recognizer, audio, res):
        try:
            #res[0] = recognizer.recognize_google(audio) #for English
            res[0] = recognizer.recognize_google(audio, language="ja") #for Japanese
            return True
        except sr.UnknownValueError:
            print("Sorry, could not understand your sentence.")
            print("Please speak again..")
            return False
        except sr.RequestError as e:
            print("Sorry, there was an error in retrieving the data. {0}".format(e))
            print("Please speak again..")
            return False
    
    # threading function for detecting and recognizing speech
    def threaded_listen(self, recognizer, microphone, res):
        flag = False
        with microphone as source:
            print("Say something!")
            while flag == False: # iterate while speech not detected / not successfully recognized
                try: # try to detect a start of an input speech
                    audio = recognizer.listen(source, 1)
                except sr.WaitTimeoutError: # speech not detected
                    try: # give very little time (0.1 s) to exit program (interrupt w/ ctrl+c)
                        time.sleep(0.1)
                    except KeyboardInterrupt:
                        sys.exit()
                    else:
                        pass
                else: # speech has been detected, recognize it
                    if flag == False:
                        flag = self.callback(recognizer, audio, res) # return success indicator
    
    # start listening by creating other thread because of
    # error in listen() function if using main thread
    def start_listen(self, recognizer, microphone, res):
        listener_thread = threading.Thread(target=self.threaded_listen(recognizer, microphone, res))
        listener_thread.daemon = True
        listener_thread.start()

    def recognize(self):
        if self.debug:
            return input("User: ")
        else:
            ##### using asr_julius? #####
            #url = "http://192.168.43.29:8000/asr_julius"
            #self.record()
            #files = {
            #        'myFile': open('./trapepper/sample.wav', 'rb')
            #        }
            #r = self.s.post(url, files=files)
            #line = r.text.split('\n')[0].split(':')[-1].replace(' ', '')

            #log("INPUT:", line)
            #if len(line) == 0: return None
            #else: return line
            
            ##### using Google speech recognition API (w/ PyPi SpeechRecognition) #####
            # initialize necessary instances for detecting a speech sound
            rec = sr.Recognizer()
            mic = sr.Microphone()
        
            # set a high initial value for detecting the energy of a speech sound
            rec.energy_threshold = 4000
            # will adjust dynamically according to the environmental condition
        
            # string for recognized speech
            res_str = [""]
        
            # start listening and recognizing input speech sound
            self.start_listen(rec, mic, res_str)
        
            return res_str[0]
