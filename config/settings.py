# Speech Recognition settings
ENERGY_THRESHOLD = 3000       # minimum audio energy to consider as speech
PAUSE_THRESHOLD = 0.8         # seconds of silence to mark end of phrase
LISTEN_TIMEOUT = 5            # seconds to wait for speech before giving up
PHRASE_TIME_LIMIT = 5         # max seconds for a single phrase

# TTS settings
SPEECH_RATE = 180             # words per minute

# Interrupt words (used during Wikipedia reading)
INTERRUPT_WORDS = ["stop", "quiet", "enough", "shut up"]

# Weather API
WEATHER_API_KEY = "cbc823df887982f8cb963df68a91cc11"
WEATHER_UNITS = "metric"                # metric = Celsius