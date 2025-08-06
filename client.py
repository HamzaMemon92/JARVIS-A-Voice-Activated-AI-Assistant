# client.py

import google.generativeai as genai
from config import settings  # Import your loaded settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def gemini_process_command(command):
    prompt = f"""
You are Jarvis, a virtual Indian AI assistant created by Spartan. Use a friendly, sharp tone to respond smartly.
Stay short, clear, and on-topic.

User said:
{command}

Respond like a helpful assistant.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini error:", e)
        return "Sorry, Gemini couldn't process your request."
