import os
import pygame
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
female_voice = None
for voice in voices:
    if 'female' in voice.name.lower():
        female_voice = voice
        break
if female_voice is not None:
    engine.setProperty('voice', female_voice.id)
else: print("Female voice not found.")

# function to speak
def speak(text):
    engine.say(text=text)
    engine.runAndWait()


heloo  = 0000000000000001
