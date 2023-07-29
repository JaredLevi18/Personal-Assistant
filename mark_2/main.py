from features import speak, listen
from features import agent

# print("write something")
# command = input()
# speak(agent.run(command))

while True:
    command = listen()
    if command == "goodbye":
        speak("Goodbye sir.")
        break
    else:
        speak(agent.run(command))
