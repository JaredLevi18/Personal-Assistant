from features import speak, listen
from features import agent

while True:
    command = listen()
    if command == "goodbye":
        speak("Goodbye sir.")
        break
    else:
        speak(agent.run(command))
