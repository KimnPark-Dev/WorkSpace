import { loadProjects, loadLogs, loadEvents, loadDoneTaskIds } from "@/lib/loadData";
import DashboardTabs from "@/components/DashboardTabs";

export default function DashboardPage() {
  const projects = loadProjects();
  const logs = loadLogs();
  const events = loadEvents();
  const doneTaskIds = loadDoneTaskIds();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-100 px-6 py-4">
        <h1 className="text-xl font-bold text-gray-800">WorkSpace Dashboard</h1>
        <p className="text-sm text-gray-400">ssong · dohyun · taeho</p>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-6">
        <DashboardTabs
          projects={projects}
          events={events}
          logs={logs}
          doneTaskIds={doneTaskIds}
        />
      </main>
    </div>
  );
}
