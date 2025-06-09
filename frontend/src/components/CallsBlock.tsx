"use client";
import { useEffect, useState } from "react";
import { Card } from "./ui/card";
import { fetchScheduledCalls } from "@/lib/api";

export default function ScheduledCalls() {
  const [calls, setCalls] = useState<string>("Loading...");

  useEffect(() => {
    fetchScheduledCalls()
      .then(data => setCalls(data.scheduled_calls || "No scheduled calls found."))
      .catch(() => setCalls("Failed to load scheduled calls."));
  }, []);

  return (
    <Card className="p-4 mb-6 whitespace-pre-wrap">
      <h2 className="text-lg font-bold mb-2">Scheduled Calls for today</h2>
      <div className="text-sm">{calls}</div>
    </Card>
  );
}
