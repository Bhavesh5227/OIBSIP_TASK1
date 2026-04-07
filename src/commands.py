import datetime
import webbrowser
import wikipedia
from src.tts import speak, speak_interruptible

def handle_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")

    elif any(word in command for word in ["time", "clock"]):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif any(word in command for word in ["date", "today", "day"]):
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {current_date}")

    elif "search" in command:
        query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}"
        print(f"Opening: {url}")
        webbrowser.open(url)
        speak(f"Searching for {query} on Google.")

    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=3)
            print(f"Reading: {summary}")
            speak_interruptible(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"That topic is ambiguous. Try being more specific.")
            print(f"Disambiguation options: {e.options[:5]}")
        except wikipedia.exceptions.PageError:
            speak(f"Sorry, I couldn't find {query} on Wikipedia.")

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        import time
        time.sleep(2)
        exit()

    else:
        speak("Sorry, I didn't understand that command.")