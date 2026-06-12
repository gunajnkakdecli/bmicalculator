import speech_recognition as sr
import pyttsx3
import datetime
import requests
import wikipedia
import webbrowser
import smtplib
import threading
import time

from email.message import EmailMessage
from config import *

# --------------------
# Text To Speech
# --------------------

engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# --------------------
# Speech Recognition
# --------------------

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        try:

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=5
            )

            command = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("You:", command)

            return command.lower()

        except sr.UnknownValueError:
            print("Could not understand")
            return ""

        except Exception as e:
            print(e)
            return ""

# --------------------
# Weather
# --------------------

def get_weather(city):

    try:

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url)

        data = response.json()

        print(data)

        if response.status_code != 200:

            speak("Weather service error")
            return

        temp = data["main"]["temp"]

        description = data["weather"][0]["description"]

        speak(
            f"The temperature in {city} is "
            f"{temp} degree Celsius with "
            f"{description}"
        )

    except Exception as e:

        print(e)

        speak(
            "Unable to get weather information"
        )

# --------------------
# Email
# --------------------

def send_email():

    try:

        speak(
            "Tell receiver email address"
        )

        receiver = input(
            "Receiver Email: "
        )

        speak("Subject")

        subject = input(
            "Subject: "
        )

        speak("Message")

        body = input(
            "Message: "
        )

        msg = EmailMessage()

        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver
        msg["Subject"] = subject

        msg.set_content(body)

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            smtp.send_message(msg)

        speak("Email sent successfully")

    except Exception as e:

        print(e)

        speak("Email sending failed")

# --------------------
# Reminder
# --------------------

def set_reminder(seconds, message):

    def reminder():

        time.sleep(seconds)

        speak(
            f"Reminder: {message}"
        )

    threading.Thread(
        target=reminder,
        daemon=True
    ).start()

# --------------------
# Wikipedia Search
# --------------------

def search_wikipedia(topic):

    try:

        result = wikipedia.summary(
            topic,
            sentences=2
        )

        speak(result)

    except:

        speak(
            "No information found"
        )

# --------------------
# Command Processing
# --------------------

def process_command(command):

    if "hello" in command:

        speak("Hello")

    elif "time" in command:

        now = datetime.datetime.now()

        speak(
            now.strftime("%I:%M %p")
        )

    elif "date" in command:

        speak(
            str(
                datetime.date.today()
            )
        )

    elif "weather" in command:

        city = command.replace(
            "weather",
            ""
        ).replace(
            "in",
            ""
        ).strip()

        if city == "":

            speak(
                "Which city?"
            )

            city = listen()

        if city:

            get_weather(city)

    elif "search" in command:

        topic = command.replace(
            "search",
            ""
        )

        search_wikipedia(topic)

    elif "email" in command:

        send_email()

    elif "youtube" in command:

        webbrowser.open(
            "https://youtube.com"
        )

        speak(
            "Opening YouTube"
        )

    elif "reminder" in command:

        speak(
            "How many seconds?"
        )

        sec = input(
            "Seconds: "
        )

        try:

            sec = int(sec)

            speak(
                "Reminder message"
            )

            msg = input(
                "Message: "
            )

            set_reminder(
                sec,
                msg
            )

            speak(
                "Reminder set"
            )

        except:

            speak(
                "Invalid number"
            )

    elif "exit" in command:

        speak("Goodbye")

        return False

    else:

        search_wikipedia(command)

    return True

# --------------------
# Main
# --------------------

def run_assistant():

    speak(
        "Advanced Voice Assistant Started"
    )

    running = True

    while running:

        command = listen()

        if command:

            running = process_command(
                command
            )

if __name__ == "__main__":

    run_assistant()