import tkinter as tk
from src.speech import listen
from src.commands import handle_command
from src.tts import speak
from src.remainders import start_scheduler
import threading

def on_click():
    # Run listening in a thread so the UI doesn't freeze
    def process():
        btn.config(text="Listening...", state="disabled", bg="red")
        command = listen()
        if command:
            handle_command(command)
        btn.config(text="Tap to Speak", state="normal", bg="systemButtonFace")
    
    threading.Thread(target=process).start()

def start_gui():
    start_scheduler()
    root = tk.Tk()
    root.title("AI Assistant")
    root.geometry("300x200")

    global btn
    label = tk.Label(root, text="Voice Assistant", font=("Arial", 16))
    label.pack(pady=20)

    btn = tk.Button(root, text="Tap to Speak", command=on_click, height=3, width=20)
    btn.pack(pady=10)

    speak("Assistant GUI ready.")
    root.mainloop()

if __name__ == "__main__":
    start_gui()