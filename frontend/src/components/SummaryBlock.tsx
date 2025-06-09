"use client"
import { useEffect, useState } from "react";
import { Card } from "./ui/card";
import { fetchSummary } from "@/lib/api";

export default function SummaryCard() {
  const [summary, setSummary] = useState("");

  useEffect(() => {
    fetchSummary().then(data => setSummary(data.summary));
  }, []);

  return (
    <Card className="p-4 mb-6">
      <h2 className="text-lg font-bold mb-2">Weekly Summary</h2>
      <p className="text-sm whitespace-pre-line">{summary}</p>
    </Card>
  );
}
