import os
import json
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-1.5-flash")

def get_upcoming_calls(messages_file_path="messages.json") -> str:
    try:
        with open(messages_file_path, "r") as f:
            messages = json.load(f)
    except FileNotFoundError:
        return "❌ messages.json file not found."
    except Exception as e:
        return f"❌ Failed to load messages: {e}"

    if not messages:
        return "No messages available."

    # Filter messages for June 9, 2025 only
    target_date = datetime(2025, 6, 9)
    relevant_messages = []
    for msg in messages:
        try:
            ts = datetime.strptime(msg['timestamp'], "%Y-%m-%d %H:%M:%S")
            if ts.date() == target_date.date():
                relevant_messages.append(msg)
        except Exception:
            continue  # skip if timestamp format is incorrect

    if not relevant_messages:
        return "No messages found for June 9, 2025."

    formatted = [
        f"[{msg.get('channel', 'unknown')}] {msg.get('sender', 'Unknown')}: {msg.get('content', '')}"
        for msg in relevant_messages
    ]
    joined = "\n".join(formatted)

    prompt = (
        "You're an AI assistant reviewing internal Slack messages.\n"
        "Gary, a senior engineer at Meta, wants to know all scheduled or suggested meetings and calls mentioned "
        "**on June 9, 2025**. Do not include events from any other date.\n\n"
        "Assume vague references like 'today', 'tonight', or '6PM' refer to June 9.\n"
        "Do not list generic updates or tasks — only calls or syncs.\n\n"
        "Format:\n"
        "* [Time PST]: [Sender] - [Purpose]\n\n"
        "Messages:\n\n"
        f"{joined}\n\n"
        "List only meetings or calls for June 9, 2025:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Scheduled Calls extraction failed: {e}"
