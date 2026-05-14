import datetime
import webbrowser
import re
from src.tts import speak, speak_interruptible
from src.weather import get_weather
from src.wiki import get_wiki
from src.ai_brain import ask_groq, clear_memory, get_history_length
from src.email_handler import send_email, parse_email_command
from src.remainders import set_reminder, list_reminders, parse_reminder_command

INTENTS = {
    "greeting":  ["hello", "hi", "hey"],
    "time":      ["time", "clock"],
    "date":      ["date", "today", "day"],
    "search":    ["search"],
    "weather":   ["weather", "temperature", "forecast"],
    "wiki":      ["wikipedia", "who is", "what is", "tell me about"],
    "email":     ["send email", "send a mail", "email to"],
    "reminder":  ["remind me", "set reminder", "set a reminder"],
    "reminders": ["list reminders", "my reminders", "show reminders", "list reminder", "my reminder", "show reminder"],
    "memory":    ["clear memory", "forget everything", "reset chat"],
    "exit":      ["exit", "quit", "bye", "goodbye"],
}

def match_intent(command):
    for intent, keywords in INTENTS.items():
        for kw in keywords:
            if re.search(rf'\b{re.escape(kw)}\b', command):
                return intent
    return "groq"   # default — send to Claude instead of "unknown"

def handle_command(command):
    intent = match_intent(command)
    print(f"DEBUG intent: {intent}")

    if intent == "greeting":
        speak("Hello! How can I assist you today?")

    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif intent == "date":
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {current_date}")

    elif intent == "search":
        query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}"
        print(f"Opening: {url}")
        webbrowser.open(url)
        speak(f"Searching for {query} on Google.")

    elif intent == "weather":
        city = command
        for kw in ["weather in", "weather for", "weather", "temperature in",
                   "temperature", "forecast for", "forecast"]:
            city = city.replace(kw, "")
        city = city.strip()
        if city:
            result = get_weather(city)
            speak(result)
        else:
            speak("Which city's weather would you like?")

    elif intent == "wiki":
        topic = command
        for kw in ["wikipedia", "who is", "what is", "tell me about"]:
            topic = topic.replace(kw, "")
        topic = topic.strip()
        if topic:
            result = get_wiki(topic)
            speak_interruptible(result)
        else:
            speak("What topic would you like to know about?")

    elif intent == "email":
        parsed = parse_email_command(command)
        if parsed:
            to, subject, body = parsed
            speak(f"Sending email to {to} about {subject}. Please wait.")
            result = send_email(to, subject, body)
            speak(result)
        else:
            speak("Please say: send email to address, about subject, saying body.")

    elif intent == "reminder":
        parsed = parse_reminder_command(command)
        if parsed:
            task, minutes = parsed
            result = set_reminder(task, minutes)
            speak(result)
        else:
            speak("Please say: remind me to task in X minutes.")

    elif intent == "reminders":
        speak(list_reminders())

    elif intent == "memory":
        clear_memory()
        speak("I have cleared our conversation history.")

    elif intent == "exit":
        speak("Goodbye!")
        import time
        time.sleep(2)
        exit()

    else:
        exchanges = get_history_length()
        if exchanges > 0:
            print(f"Sending to AI Brain! (memory: {exchanges} exchanges)")
        result = ask_groq(command)
        speak(result)