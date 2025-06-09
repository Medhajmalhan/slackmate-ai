Problem Statement

Workplace communication platforms like Slack contain a wealth of unstructured information — updates, requests, schedules, decisions, and discussions — but this content is often lost in the noise of ongoing messages. Professionals frequently miss to-dos, calls, or important updates buried within dozens of threads and channels.

The problem:
There is no consolidated, intelligent way to parse Slack conversations and present personalized, actionable insights.

Why AI Agents?

AI agents excel at interpreting natural language, understanding context, and extracting structured information from noisy data. By dividing responsibilities across specialized agents, we ensure:

    Separation of concerns (e.g., one agent focuses only on tasks, another on summaries)

    Parallel processing of different goals

    More accurate and focused outputs

Why Multi-Agent Collaboration?

Multi-agent systems allow the following:

    Independent focus on specialized tasks (summarization, to-do extraction, Q&A, scheduled calls)

    Scalable addition of future agents (e.g., a KPI Tracker or Sentiment Agent)

    Easier debugging and extension due to modular architecture

Project Description – SlackMate AI

SlackMate-AI is a multi-agent dashboard that helps a senior engineer (Gary) at a company like Meta gain key insights from Slack messages between June 1 and June 9, 2025.

This MVP works on a static dataset (messages.json) to simulate Slack exports and showcases 4 collaborating agents:
| Agent                     | Description                                                                |
| ------------------------- | -------------------------------------------------------------------------- |
| **Summarizer Agent**      | Gives a weekly high-level overview of themes, updates, and product changes |
| **To-Do Agent**           | Extracts and lists Gary's actionable items with a focus on deadlines       |
| **Scheduled Calls Agent** | Identifies scheduled calls for June 9 only                                 |
| **LLM Q\&A Agent**        | Lets the user ask open-ended queries to Slack data via natural language    |

Tools, Libraries, and Frameworks

    Frontend: Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui

    Backend: FastAPI

    LLM API: Google Gemini 1.5 Flash (via google.generativeai)

    Communication: REST API endpoints (hosted locally via Uvicorn)

    Deployment Stack (MVP): Localhost with optional Vercel (frontend) + Railway (backend) in future

    State Management: Minimal (via useState), future upgrade to context or Redux

LLM Selection
💎 Ideal Model:

    Google Gemini 1.5 Pro or GPT-4-turbo

        Rich context memory

        Higher factual consistency and instruction following

        Optimized for structured multi-agent tasks

🆓 Free Tier Option Used in MVP:

    Google Gemini 1.5 Flash

        Fast inference, low latency

        Suitable for parsing messages and generating short outputs

        Available via free Google API quota

        Justification: Since this is a prototype, we’ve optimized for low latency and free access. Gemini 1.5 Flash performs sufficiently well in parsing and generating structured tasks from natural language messages. For a production version, we would upgrade to Gemini 1.5 Pro or GPT-4.
Code and Deployment
GitHub Repo: https://github.com/Medhajmalhan/slackmate-ai

Frontend: /frontend (Next.js)
Backend: /api (FastAPI)

Project Structure:
slackmate-ai/
├── api/
│   └── main.py
│   └── agents/
│       ├── summarizer_agent.py
│       ├── todo_agent.py
│       ├── scheduled_calls_agent.py
│       └── llm_qa_agent.py
│   └── messages.json
├── frontend/
│   └── src/
│       ├── components/
│       ├── lib/api.ts
│       └── app/page.tsx
└── README.md

Why We Didn’t Use Real-Time Slack API

    Slack API requires OAuth app setup, which may be out of scope or restricted for academic demos.

    We simulate real Slack exports using a curated static JSON file (messages.json) to demonstrate the concept.

    This also allows us to control data quality and ensure consistent behavior across agents.
    
    To maintain privacy and ensure full control of message data, we simulate Slack messages from multiple users using a JSON dataset.
    
    This allows us to demonstrate realistic multi-agent interactions including task extraction, prioritization, and summarization.

 Future Scope and Production Features
 | Feature                           | Description                                                                |
| --------------------------------- | -------------------------------------------------------------------------- |
| ✅ Real-time Slack API Integration | Live fetch messages, respond to new data in real-time                      |
| ✅ Multiple Data Sources           | Extend to Notion, Google Meet, Google Docs, GitHub PRs                     |
| ✅ Knowledge Graph                 | Store semantic entities (tasks, projects, people) and relate them visually |
| ✅ Vector DB + LangChain           | Enable retrieval-based answering on message chunks                         |
| ✅ Persistent State                | Use Postgres / Supabase to store tasks, checkboxes, completions            |
| ✅ Check Filters in Dashboard      | Mark a to-do as “completed” and exclude from next view                     |
| ✅ Notifications / Nudges          | Alert when Gary misses a task or skips a meeting                           |
| ✅ Agent Collaboration Layer       | Share context or memory across agents                                      |
| ✅ User Profiles                   | Support multiple employees, their data streams, and roles                  |


What the MVP Does (And Why)
| Component       | MVP Implementation                                    | Reason                                                        |
| --------------- | ----------------------------------------------------- | ------------------------------------------------------------- |
| Data            | Static Slack messages (`messages.json`) from June 1–9 | Simple, mockable, and avoids API throttling or OAuth overhead |
| Agents          | 4 agents in isolation (Summary, To-Do, Calls, QA)     | Clean separation of concerns; easily testable                 |
| Frontend        | Basic cards with agent outputs + QA chat              | Functional, readable UI for evaluators                        |
| LLM API         | Gemini 1.5 Flash                                      | Free-tier, fast, and consistent                               |
| Dates Hardcoded | All references assume "today" is June 9, 2025         | Ensures consistent outputs regardless of when accessed        |

Setup & Run Instructions

Backend:

cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

Frontend:

cd frontend
npm install
npm run dev

Visit: http://localhost:3000

Deployed link of demo : https://slackmate-frontend.onrender.com/
