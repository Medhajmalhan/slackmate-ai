import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure root path is available for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.summarizer_agent import get_summary
from agents.todo_agent import get_weekly_todos, get_past_week_todos
from agents.scheduled_calls_agent import get_upcoming_calls
from agents.llm_qa_agent import answer_query

app = FastAPI()

# Enable CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://slackmate-frontend.onrender.com"],  # Replace with actual domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for POST /qa
class QueryRequest(BaseModel):
    query: str

@app.get("/summary")
def summary():
    try:
        return {"summary": get_summary()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/todos")
def todos():
    try:
        return {"todos": get_weekly_todos()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scheduled-calls")
def scheduled_calls():
    try:
        return {"scheduled_calls": get_upcoming_calls()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qa")
def qa(request: QueryRequest):
    try:
        return {"answer": answer_query(request.query)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/past-week-todos")
def past_week_todos():
    try:
        return {"todos": get_past_week_todos()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

