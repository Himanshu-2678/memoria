import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_response(prompt: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    chat = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Memoria, a helpful AI assistant with persistent memory. "
                    "You have access to past conversation context. "
                    "Only reference past memories when directly relevant to the current question. "
                    "Never volunteer past context unless asked. "
                    "Respond naturally like a human assistant would - avoid repetitive references to things the user already knows about themselves. "
                    "Answer only what is asked. Keep responses concise."
                ),
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature = 0.7,
        max_tokens = 512)

    return chat.choices[0].message.content.strip()