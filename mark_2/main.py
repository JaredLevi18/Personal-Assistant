from features import speak, listen
import openai

openai.api_key = # your API key

def chat_with_bot(message):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt= message,
        max_tokens = 150,
        temperature = 0.7,
        n = 1,
        stop = None,
    )
    return response.choices[0].text.strip()

while True:
    command = listen()
    response = chat_with_bot(command)
    print(response)
    speak(response)
    if command == "bye":
        speak("Goodbye sir.")
        break
