"use client";

import { useState } from "react";
import SummaryCards from "./SummaryCards";
import ProjectTable from "./ProjectTable";
import MemberTaskList from "./MemberTaskList";
import ActivityTimeline from "./ActivityTimeline";
import { Project, EventEntry, LogEntry } from "@/lib/loadData";

interface Props {
  projects: Project[];
  events: EventEntry[];
  logs: LogEntry[];
  doneTaskIds: Set<string>;
}

const TABS = [
  { key: "summary",  label: "요약" },
  { key: "projects", label: "프로젝트" },
  { key: "members",  label: "멤버" },
  { key: "activity", label: "활동" },
] as const;

type TabKey = (typeof TABS)[number]["key"];

export default function DashboardTabs({ projects, events, logs, doneTaskIds }: Props) {
  const [tab, setTab] = useState<TabKey>("summary");

  return (
    <div>
      <nav className="flex gap-1 border-b border-gray-200 mb-6">
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-4 py-2 text-sm font-medium transition-colors border-b-2 -mb-px ${
              tab === t.key
                ? "border-indigo-500 text-indigo-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            {t.label}
          </button>
        ))}
      </nav>

      {tab === "summary" && (
        <SummaryCards projects={projects} events={events} doneTaskIds={doneTaskIds} />
      )}
      {tab === "projects" && (
        <ProjectTable projects={projects} doneTaskIds={doneTaskIds} />
      )}
      {tab === "members" && (
        <MemberTaskList projects={projects} doneTaskIds={doneTaskIds} />
      )}
      {tab === "activity" && (
        <ActivityTimeline events={events} logs={logs} />
      )}
    </div>
  );
}
