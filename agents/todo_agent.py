import os
import json
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-1.5-flash")

def get_weekly_todos(messages_file_path="messages.json") -> str:
    try:
        with open(messages_file_path, "r") as f:
            messages = json.load(f)
    except FileNotFoundError:
        return "❌ messages.json file not found."
    except Exception as e:
        return f"❌ Failed to load messages: {e}"

    if not messages:
        return "No messages available to extract to-dos."

    # Treat June 9, 2025 as "today" for filtering
    today = datetime(2025, 6, 9)
    week_ago = today - timedelta(days=7)

    # Filter only messages from the past week till June 9
    recent_messages = [
        msg for msg in messages
        if week_ago <= datetime.strptime(msg['timestamp'], "%Y-%m-%d %H:%M:%S") <= today
    ]

    if not recent_messages:
        return "No messages found in the date range."

    formatted = [
        f"[{msg.get('channel', 'unknown')}] {msg.get('sender', 'Unknown')}: {msg.get('content', '')}"
        for msg in recent_messages
    ]
    joined = "\n".join(formatted)

    # Prompt to extract only to-dos due on June 9, 2025
    prompt = (
        "You're an AI assistant helping Gary, a senior engineer at Meta, track urgent to-dos due **today (June 9, 2025)**.\n\n"
        "Below are Slack messages from the past week.\n"
        "Extract only the action items that Gary is responsible for **and are due on June 9, 2025**.\n"
        "This includes:\n"
        "- Tasks with explicit deadline of June 9\n"
        "- Mentions like 'today', 'by EOD', 'this evening', etc. (assume these refer to June 9)\n\n"
        "Exclude:\n"
        "- Calls, meetings, or sync invites\n"
        "- Updates with no actionable task for Gary\n"
        "- Tasks due after June 9 or with no clear deadline\n\n"
        "Output a clean bullet list of to-dos for Gary to finish today:\n\n"
        f"{joined}\n\n"
        "Gary's to-dos due today:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"To-Do extraction failed: {e}"

def get_past_week_todos(messages_file_path="messages.json") -> str:
    try:
        with open(messages_file_path, "r") as f:
            messages = json.load(f)
    except FileNotFoundError:
        return "❌ messages.json file not found."
    except Exception as e:
        return f"❌ Failed to load messages: {e}"

    if not messages:
        return "No messages available to extract to-dos."

    # Define date range: June 1 to June 8, 2025
    start_date = datetime(2025, 6, 1)
    end_date = datetime(2025, 6, 8, 23, 59, 59)

    filtered_messages = [
        msg for msg in messages
        if start_date <= datetime.strptime(msg['timestamp'], "%Y-%m-%d %H:%M:%S") <= end_date
    ]

    if not filtered_messages:
        return "No messages found from June 1 to 8, 2025."

    formatted = [
        f"[{msg.get('channel', 'unknown')}] {msg.get('sender', 'Unknown')}: {msg.get('content', '')}"
        for msg in filtered_messages
    ]
    joined = "\n".join(formatted)

    prompt = (
        "You are an AI assistant helping Gary, a senior engineer at Meta, track his work.\n"
        "Below are Slack messages from **June 1 to June 8, 2025**.\n"
        "Extract **only actionable to-dos for Gary** — things he must complete, review, follow up on, or assist with.\n"
        "Exclude:\n"
        "- meetings, syncs, or reminders\n"
        "- passive updates or discussions\n\n"
        "Output a clean bullet list of action items, each on a new line.\n\n"
        f"Messages:\n\n{joined}\n\nExtract Gary’s to-dos from June 1–8:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Past Week To-Do extraction failed: {e}"
