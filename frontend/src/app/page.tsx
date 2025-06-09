import SummaryCard from "@/components/SummaryBlock";
import ToDoList from "@/components/ToDoBlock";
import ScheduledCalls from "@/components/CallsBlock";
import QABlock from "@/components/ChatBlock";
import PastWeekToDos from "@/components/pastweektodos"; // ✅ Import added

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-50 p-6 md:p-10 text-gray-900">
      <div className="max-w-6xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold tracking-tight">
          SlackMate AI Dashboard (This dashboard reflects activity as of June 9, 2025.)
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <SummaryCard />
          <ToDoList />
          <PastWeekToDos /> {/* ✅ New card for June 1–8 to-dos */}
          <ScheduledCalls />
        </div>

        <div className="pt-8">
          <QABlock />
        </div>
      </div>
    </main>
  );
}
