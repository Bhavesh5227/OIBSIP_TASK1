import time
import re
import subprocess
import platform
import threading

_say_process = None      # tracks the currently running say process
_stop_flag = threading.Event()

def _speak_macos(text, rate=175):
    global _say_process
    _say_process = subprocess.Popen(["say", "-r", str(rate), text])
    _say_process.wait()   # wait for it to finish (non-blocking to other threads)
    _say_process = None

def _stop_current_speech():
    global _say_process
    if _say_process and _say_process.poll() is None:
        _say_process.terminate()
        _say_process = None

def _speak_raw(text, rate=175):
    if platform.system() == "Darwin":
        _speak_macos(text, rate)
    else:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

def _estimate_speech_duration(text):
    word_count = len(text.split())
    return (word_count / 175) * 60

def speak(text):
    print(f"Speaking: {text}")
    _speak_raw(text)
    time.sleep(0.3)

def check_for_interrupt():
    import speech_recognition as sr
    from config.settings import INTERRUPT_WORDS, ENERGY_THRESHOLD
    r = sr.Recognizer()
    r.energy_threshold = ENERGY_THRESHOLD
    r.dynamic_energy_threshold = False
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=2.0, phrase_time_limit=2)
            command = r.recognize_google(audio).lower()
            print(f"Interrupt heard: {command}")
            if any(word in command for word in INTERRUPT_WORDS):
                return True
        except:
            pass
    return False

def _listen_for_stop_background(stop_event):
    """Runs in a thread — sets stop_event if 'stop' is heard."""
    import speech_recognition as sr
    from config.settings import INTERRUPT_WORDS, ENERGY_THRESHOLD
    r = sr.Recognizer()
    r.energy_threshold = ENERGY_THRESHOLD + 1000   # higher threshold — ignore speaker bleed
    r.dynamic_energy_threshold = False

    while not stop_event.is_set():
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, timeout=2.0, phrase_time_limit=2)
                command = r.recognize_google(audio).lower()
                print(f"Background heard: {command}")
                if any(word in command for word in INTERRUPT_WORDS):
                    print("Stop detected — killing speech.")
                    stop_event.set()
                    _stop_current_speech()
                    return
            except:
                continue   # nothing heard, keep listening

def speak_interruptible(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    print(f"DEBUG sentences to speak: {sentences}")

    stop_event = threading.Event()

    # start background listener thread
    listener_thread = threading.Thread(
        target=_listen_for_stop_background,
        args=(stop_event,),
        daemon=True
    )
    listener_thread.start()

    for i, sentence in enumerate(sentences):
        if stop_event.is_set():
            break

        print(f"DEBUG speaking sentence {i+1}/{len(sentences)}: {sentence}")
        _speak_raw(sentence)
        time.sleep(0.3)
        print(f"DEBUG spoke sentence {i+1}/{len(sentences)}")

    # signal thread to stop if speech finished naturally
    stop_event.set()
    listener_thread.join(timeout=2)