import speech_recognition as sr
from config.settings import ENERGY_THRESHOLD, PAUSE_THRESHOLD, LISTEN_TIMEOUT, PHRASE_TIME_LIMIT

def calibrate_microphone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Ready.")

def listen():
    r = sr.Recognizer()
    r.energy_threshold = ENERGY_THRESHOLD
    r.pause_threshold = PAUSE_THRESHOLD

    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT)
        except sr.WaitTimeoutError:
            return ""

    try:
        command = r.recognize_google(audio).lower()
        print(f"User said: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError:
        print("Speech service unavailable.")
        return ""