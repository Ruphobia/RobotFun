#pip install pocketsphinx

import speech_recognition as sr

# Obtain audio from the microphone
recognizer = sr.Recognizer()

def recognize_and_print(recognizer, audio):
    try:
        text = recognizer.recognize_sphinx(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
    while True:
        print("Say something!")
        audio = recognizer.listen(source)
        recognize_and_print(recognizer, audio) 
