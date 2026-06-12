import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia

# Initialize Text-to-Speech
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Listen to user's voice
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()

        except sr.UnknownValueError:
            speak("Sorry, I could not understand.")
            return ""

        except sr.RequestError:
            speak("Internet connection error.")
            return ""

        except Exception as e:
            print(e)
            return ""

# Main assistant function
def assistant():
    speak("Hello! I am your voice assistant.")

    while True:
        command = listen()

        if "hello" in command:
            speak("Hello! How can I help you?")

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif "date" in command:
            today = datetime.datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {today}")

        elif "search" in command:
            speak("What should I search for?")
            query = listen()

            if query:
                url = f"https://www.google.com/search?q={query}"
                webbrowser.open(url)
                speak(f"Searching for {query}")

        elif "wikipedia" in command:
            speak("What topic do you want to know about?")
            topic = listen()

            try:
                result = wikipedia.summary(topic, sentences=2)
                speak(result)

            except:
                speak("Sorry, I couldn't find information.")

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

        elif command != "":
            speak("Sorry, I don't know that command yet.")

# Run Assistant
assistant()