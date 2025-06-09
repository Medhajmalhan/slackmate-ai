"use client";
import { useEffect, useState } from "react";
import { Card } from "./ui/card";
import { fetchTodos } from "@/lib/api";

export default function TodoList() {
  const [todos, setTodos] = useState<string>("Loading...");

  useEffect(() => {
    fetchTodos()
      .then(data => setTodos(data.todos || "No to-dos found."))
      .catch(() => setTodos("Failed to load to-dos."));
  }, []);

  return (
    <Card className="p-4 mb-6 whitespace-pre-wrap">
      <h2 className="text-lg font-bold mb-2">To-Dos for today (9 june)</h2>
      <div className="text-sm">{todos}</div>
    </Card>
  );
}
