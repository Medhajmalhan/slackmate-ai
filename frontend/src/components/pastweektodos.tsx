"use client";
import { useEffect, useState } from "react";
import { Card } from "./ui/card";
import { fetchPastWeekTodos } from "@/lib/api";

export default function PastWeekToDos() {
  const [todos, setTodos] = useState("");

  useEffect(() => {
    fetchPastWeekTodos().then(data => setTodos(data.todos || "No to-dos found."));
  }, []);

  return (
    <Card className="p-4 mb-6">
      <h2 className="text-lg font-bold mb-2">To-Dos (June 1–8)</h2>
      <pre className="text-sm whitespace-pre-wrap">{todos}</pre>
    </Card>
  );
}
