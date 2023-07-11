from langchain.llms import HuggingFacePipeline
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoModelForSeq2SeqLM
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
import pyttsx3
import speech_recognition as sr

model_id = 'gpt2-medium'#'facebook/blenderbot-1B-distill'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length = 100
)

local_llm = HuggingFacePipeline(pipeline=pipe)

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=local_llm)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the voice properties
voices = engine.getProperty('voices')
female_voice = None
for voice in voices:
    if 'female' in voice.name.lower():
        female_voice = voice
        break
if female_voice is not None:
    engine.setProperty('voice', female_voice.id)
else:
    print("Female voice not found. Using the default voice.")

# Function to speak the generated text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=2)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio)
        print("You said: " + command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please try again.")
        return ''
    except sr.RequestError:
        print("Sorry, I'm unable to access the speech recognition service.")
        return ''

# Example usage
speak("Hello, I'm your chatbot. How can I assist you?")
while True:
    command = listen()
    if 'stop' in command:
        speak("Goodbye, have a nice day!")
        break
    else:
        # Generate a response using your text generator model
        response = llm_chain.run(command)  # Replace with your text generator code
        speak(response)