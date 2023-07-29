import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source=source, duration=1)
        audio = r.listen(source)

    # recognize speech using google
    try:
        command = r.recognize_google(audio)
        print("It thinks you said " + command)
        return command
    except sr.UnknownValueError:
        print("It could not understand audio")
        return ''
    except sr.RequestError as e:
        print("It error; {0}".format(e))        
        return ''
