import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        r.adjust_for_ambient_noise(source=source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing")
        command = r.recognize_google(audio)
        print("You said" + command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please try againg.")
        return ""
    except sr.RequestError:
        print("Sorry, I'm not able to acces the speech recognition service.")
        return ""