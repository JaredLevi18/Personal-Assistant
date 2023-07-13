import openai
import pyttsx3
import speech_recognition as sr

openai.api_key = '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' #'YOUR_API_KEY'

def chat_with_bot(message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

engine = pyttsx3.init()
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

while True:
    command= input("User: ")
    response = chat_with_bot(command)
    print(response)
    speak(response)
    if command == 'bye':
        speak('Goodbye sir, have a nice day.')
        break