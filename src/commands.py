import datetime
import webbrowser
import wikipedia
from src.tts import speak, speak_interruptible
from src.weather import get_weather
from src.wiki import get_wiki
import re

INTENTS = {
    "greeting":  ["hello", "hi", "hey"],
    "time":      ["time", "clock"],
    "date":      ["date", "today", "day"],
    "search":    ["search"],
    "weather":   ["weather", "temperature", "forecast"],
    "wiki":      ["wikipedia", "who is", "what is", "tell me about"],
    "exit":      ["exit", "quit", "bye", "goodbye"],
}

def match_intent(command):
    """Match keywords as whole words only, preventing substring false matches."""
    for intent, keywords in INTENTS.items():
        for kw in keywords:
            # \b = word boundary — "hi" won't match inside "hitler"
            if re.search(rf'\b{re.escape(kw)}\b', command):
                return intent
    return "unknown"

def handle_command(command):
    intent = match_intent(command)
    print(f"DEBUG intent: {intent}")        # ← add this

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
        print(f"DEBUG city extracted: '{city}'")     # ← add this
        if city:
            result = get_weather(city)
            print(f"DEBUG weather result: {result}") # ← add this
            speak(result)
        else:
            speak("Which city's weather would you like?")

    elif intent == "wiki":
        topic = command
        for kw in ["wikipedia", "who is", "what is", "tell me about"]:
            topic = topic.replace(kw, "")
        topic = topic.strip()
        print(f"DEBUG topic extracted: '{topic}'")   # ← add this
        if topic:
            result = get_wiki(topic)
            print(f"DEBUG wiki result: {result}")    # ← add this
            speak_interruptible(result)
        else:
            speak("What topic would you like to know about?")

    elif intent == "exit":
        speak("Goodbye!")
        import time
        time.sleep(2)
        exit()

    else:
        speak("Sorry, I didn't understand that command.")