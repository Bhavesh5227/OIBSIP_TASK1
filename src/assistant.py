from src.speech import calibrate_microphone, listen
from src.commands import handle_command
from src.tts import speak

def run():
    calibrate_microphone()
    speak("Hello! I am your voice assistant. How can I help you today?")
    while True:
        command = listen()
        if command:
            handle_command(command)