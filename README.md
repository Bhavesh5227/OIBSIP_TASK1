# 🎙️ Voice Assistant

A Python voice assistant that responds to spoken commands — tells time/date,
searches Google, and reads Wikipedia summaries out loud with interruptible speech.

## Demo
![Demo](assets/demo.gif)

## Features
- 🕐 Tell current time and date
- 🔍 Search Google by voice
- 📖 Read Wikipedia summaries (say "stop" to interrupt)
- 🔇 Offline text-to-speech via pyttsx3

## Project Structure
    src/          → core modules (speech, tts, commands, assistant)
    config/       → all tunable settings in one place
    tests/        → unit tests for command logic
    assets/       → demo gif

## Setup
    git clone https://github.com/YOUR_USERNAME/voice-assistant
    cd voice-assistant
    pip install -r requirements.txt

    # Mac only — required before pip install pyaudio
    brew install portaudio

## Run
    python main.py

## Voice Commands
| Say this              | What happens                    |
|-----------------------|---------------------------------|
| "hello"               | Greeting                        |
| "what time is it"     | Reads current time              |
| "today's date"        | Reads current date              |
| "search <query>"      | Opens Google search             |
| "wikipedia <topic>"   | Reads Wikipedia summary         |
| "stop"                | Interrupts Wikipedia reading    |
| "exit" / "quit"       | Closes the assistant            |

## Tech Stack
- `speech_recognition` — mic input to text via Google API
- `pyttsx3` — offline text to speech
- `wikipedia-api` — Wikipedia summaries
- `threading` — interruptible speech playback

## Requirements
Python 3.10+, internet connection for speech recognition and search