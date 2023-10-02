# Python program to translate speech to text and text to speech
import speech_recognition as sr
import pyttsx3

import os

from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

import openai
openai.api_key = OPENAI_KEY

# function to conver text to speech
def speakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Initialize the recognizer
r = sr.Recognizer()

# function that record user's input into text
def record_text():
    # Loop in case of errors
    while(True):
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # Prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                print("I'm listening")

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)

                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")

# function to send messages to chatGPT
def send_to_chatGPT(messages, model="gpt-3.5-turbo"):

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = []

while(True):
    text = record_text()
    messages.append({"role":"user", "content":text})
    response = send_to_chatGPT(messages)
    speakText(response)

    print(response)