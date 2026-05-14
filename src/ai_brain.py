from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a helpful voice assistant. Follow these rules strictly:
- Be concise, max 2-3 sentences since your reply will be spoken aloud
- No bullet points, no markdown, no special characters
- No emojis or symbols
- Speak naturally as if in conversation
- If asked about time, weather, or reminders, say you will handle that separately"""

#Maintaining chat history manually
chat_history = [{"role": "system", "content":SYSTEM_PROMPT}]

def ask_groq(user_input):
    global chat_history
    try:
        #Adding user message to chat history
        chat_history.append({"role": "user", "content": user_input})

        # Create completion
        response = client.chat.completions.create(
            messages=chat_history,
            model=GROQ_MODEL,
            max_tokens=150,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content.strip()
        
        # Add assistant reply to history to maintain context
        chat_history.append({"role": "assistant", "content": reply})
        
        print(f"Groq: {reply}")
        return reply

    except Exception as e:
        print(f"Groq error: {e}")
        return _fallback(user_input)

def _fallback(user_input):
    u = user_input.lower()
    if any(w in u for w in ["joke", "funny"]):
        return "Why don't scientists trust atoms? Because they make up everything."
    elif any(w in u for w in ["how are you", "how do you do"]):
        return "I am doing great, thank you for asking!"
    elif any(w in u for w in ["your name", "who are you", "what are you"]):
        return "I am your voice assistant, built with Python."
    elif any(w in u for w in ["thank", "thanks"]):
        return "You are welcome!"
    elif any(w in u for w in ["help", "what can you do"]):
        return ("I can tell time, date, weather, search Google, "
                "read Wikipedia, set reminders, and send emails.")
    else:
        return "I am not sure about that. Try asking me about weather, time, or Wikipedia."

def clear_memory():
    global chat_history
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Groq memory cleared.")
    return "Memory cleared."

def get_history_length():
    return (len(chat_history) - 1)// 2