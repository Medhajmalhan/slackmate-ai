// lib/api.ts
const BASE_URL = "https://slackmate-backend.onrender.com"; // Your FastAPI server

export async function fetchSummary() {
  const res = await fetch(`${BASE_URL}/summary`);
  return res.json();
}

export async function fetchTodos() {
  const res = await fetch(`${BASE_URL}/todos`);
  return res.json();
}

export async function fetchScheduledCalls() {
  const res = await fetch(`${BASE_URL}/scheduled-calls`);
  return res.json();
}

export async function askLLM(query: string) {
  const res = await fetch(`${BASE_URL}/qa`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }), // ✅ key must be "query"
  });
  return res.json();
}

export async function fetchPastWeekTodos() {
  const res = await fetch(`${BASE_URL}/past-week-todos`);
  return res.json();
}
