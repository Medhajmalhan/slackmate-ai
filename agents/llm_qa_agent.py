import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-1.5-flash")

def answer_query(query: str, messages_file_path="messages.json") -> str:
    try:
        with open(messages_file_path, "r") as f:
            messages = json.load(f)
    except FileNotFoundError:
        return "❌ messages.json file not found."
    except Exception as e:
        return f"❌ Failed to load messages: {e}"

    if not messages:
        return "No messages available."

    # Format all messages
    formatted = [
        f"[{msg.get('timestamp')}] [{msg.get('channel', 'unknown')}] {msg.get('sender', 'Unknown')}: {msg.get('content', '')}"
        for msg in messages
    ]
    context = "\n".join(formatted)

    prompt = (
        "You are a smart assistant trained on internal Slack messages from a company called Meta.\n"
        "Gary, a senior engineer, wants to ask questions about what’s happening in his team or across departments based on the Slack activity.\n"
        "Use the context below to answer his question accurately and helpfully.\n\n"
        f"Context:\n{context}\n\n"
        f"Question from Gary: {query}\n\n"
        "Answer:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Query response failed: {e}"
