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

def get_summary(messages_file_path="messages.json") -> str:
    try:
        with open(messages_file_path, "r") as f:
            messages = json.load(f)
    except FileNotFoundError:
        return "❌ messages.json file not found."
    except Exception as e:
        return f"❌ Failed to load messages: {e}"

    if not messages:
        return "No messages found in the data."

    # Determine the most recent timestamp and filter last 7 days
    timestamps = [datetime.strptime(msg['timestamp'], "%Y-%m-%d %H:%M:%S") for msg in messages]
    latest = max(timestamps)
    week_ago = latest - timedelta(days=7)

    recent_messages = [
        msg for msg in messages
        if week_ago <= datetime.strptime(msg['timestamp'], "%Y-%m-%d %H:%M:%S") <= latest
    ]

    if not recent_messages:
        return "No recent messages found in the last 7 days."

    # Format messages
    formatted = [
        f"[{msg.get('channel', 'unknown')}] {msg.get('sender', 'Unknown')}: {msg.get('content', '')}"
        for msg in recent_messages
    ]
    joined = "\n".join(formatted)

    # Summarization prompt
    prompt = (
        "You are an intelligent assistant that summarizes company-wide developments on Slack for Gary, "
        "a senior engineer at Meta.\n\n"
        "Below is a collection of Slack messages received in various public and private channels. Your job is to provide "
        "an insightful weekly overview of important themes, product developments, ongoing engineering discussions, and "
        "team movements — without listing individual tasks, calls, or reminders.\n\n"
        "Ignore:\n"
        "- personal to-do requests\n"
        "- reminders\n"
        "- calendar invites or scheduled meetings\n\n"
        "Focus on:\n"
        "- major technical developments (e.g. deployments, infrastructure updates, staging rollouts)\n"
        "- key product or model experimentation (e.g. Gemini, Llama2, inference changes)\n"
        "- strategic discussions or high-level technical blockers\n"
        "- inter-team collaborations or cross-functional updates\n"
        "- Gary’s involvement in decision-making, approvals, or leadership moments\n\n"
        "Tone: analytical but conversational — write as if summarizing the week for Gary. Use 'you' instead of 'Gary'. "
        "Keep the summary under 200 words.\n\n"
        "Messages:\n\n"
        f"{joined}\n\n"
        "Now generate the weekly summary:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Summarization failed: {e}"
