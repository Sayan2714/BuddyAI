from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

chat_memory = []

class Message(BaseModel):
    user_message: str

@app.get("/")
def home():
    return {"message": "BuddyAI Running"}

@app.post("/chat")
def chat(message: Message):

    chat_memory.append(f"User: {message.user_message}")

    conversation = f"""
You are BuddyAI, a friendly personal AI companion.
You help users with careers, motivation, learning, and life goals.

Conversation:
{chr(10).join(chat_memory)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation
    )

    ai_reply = response.text

    chat_memory.append(f"BuddyAI: {ai_reply}")

    return {"reply": ai_reply}