"use client";
import { useState } from "react";
import { Card } from "./ui/card";
import { Textarea } from "./ui/textarea";
import { Button } from "./ui/button";
import { askLLM } from "@/lib/api";

export default function QABlock() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    if (!question.trim()) return;
    setLoading(true);
    const response = await askLLM(question);
    setAnswer(response.answer || "No response.");
    setLoading(false);
  }

  return (
    <Card className="p-4">
      <h2 className="text-lg font-bold mb-2">Ask SlackMate AI</h2>
      <Textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question based on recent Slack activity..."
        className="mb-2"
      />
      <Button onClick={handleAsk} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </Button>
      {answer && (
        <div className="mt-4 text-sm whitespace-pre-line border-t pt-4">
          <strong>Answer:</strong> {answer}
        </div>
      )}
    </Card>
  );
}
