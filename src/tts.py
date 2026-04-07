import pyttsx3
import time

engine = pyttsx3.init()

def speak(text):
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()
    word_count = len(text.split())
    duration = (word_count / 175) * 60
    time.sleep(duration + 0.5)

def check_for_interrupt():
    import speech_recognition as sr
    from config.settings import INTERRUPT_WORDS, ENERGY_THRESHOLD
    global stop_speaking
    r = sr.Recognizer()
    r.energy_threshold = ENERGY_THRESHOLD
    r.dynamic_energy_threshold = False
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=0.8, phrase_time_limit=2)
            command = r.recognize_google(audio).lower()
            print(f"Interrupt heard: {command}")
            if any(word in command for word in INTERRUPT_WORDS):
                return True
        except:
            pass
    return False

def speak_interruptible(text):
    sentences = text.replace("! ", ". ").replace("? ", ". ").split(". ")
    for sentence in sentences:
        if sentence.strip():
            engine.say(sentence)
            engine.runAndWait()
            if check_for_interrupt():
                print("Speech interrupted.")
                break
            time.sleep(0.1)