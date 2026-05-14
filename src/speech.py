import speech_recognition as sr
from config.settings import ENERGY_THRESHOLD, PAUSE_THRESHOLD, LISTEN_TIMEOUT, PHRASE_TIME_LIMIT

recognizer = sr.Recognizer()  # create ONCE globally, not per call

def calibrate_microphone():
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = ENERGY_THRESHOLD
        recognizer.pause_threshold = PAUSE_THRESHOLD
        recognizer.non_speaking_duration = 0.3   # cuts silence faster
        recognizer.phrase_threshold = 0.2         # starts capturing quicker
        print("Ready.")

def listen():
    with sr.Microphone() as source:
        print("\n== * == * == * ==\n")
        print("Listening...")
        try:
            audio = recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT
            )
        except sr.WaitTimeoutError:
            return ""

    try:
        command = recognizer.recognize_google(audio, language="en-IN")  # Indian English accent
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError:
        print("Speech service unavailable.")
        return ""