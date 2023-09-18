import wave
import sys

import speech_recognition as sr

import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

def main():
    print('Hello, World')


    # Initialize recognizer
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Speak now!')
        audio = r.listen(source)

    print(f'Finished listening!')
    text = r.recognize_google(audio, language='de-DE')
    print(text)



if __name__ == '__main__':
    main()