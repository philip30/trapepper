# Please install PyAudio (https://people.csail.mit.edu/hubert/pyaudio/)
# PyAudio also needs PortAudio (http://www.portaudio.com/download.html)
# Finally, please install SpeechRecognition (https://pypi.python.org/pypi/SpeechRecognition/)

# Input is from microphone, so please set your microphone correctly

import speech_recognition as sr
import time

# callback for calling Google Speech Recognition API
# will be automatically called if there is an input speech detected
def callback(recognizer, audio):
    try:
        #print("You said: " + recognizer.recognize_google(audio)) #for English
        print("You said: " + recognizer.recognize_google(audio, language="ja")) #for Japanese
        print("Say something!")
    except sr.UnknownValueError:
        print("Sorry, could not understand your sentence.")
        print("Please speak again..")
    except sr.RequestError as e:
        print("Sorry, there was an error in retrieving the data. {0}".format(e))
        print("Please speak again..")

# initialize necessary instances for detecting a speech sound
r = sr.Recognizer()
m = sr.Microphone()

# set a high initial value for detecting the energy of a speech sound
r.energy_threshold = 4000
# will adjust dynamically according to the environmental condition

# listen in background allow continous listening in the main thread
stop_listening = r.listen_in_background(m, callback)
# calling function stop_listening will make the background listening stops

print("Say something!")
# keeping the program alive while not been interrupted, e.g. (ctrl+c)
while True:
    for _ in range(1): time.sleep(0.1)

# program has been stopped/killed, stop background listening
stop_listening()
