"use client";

import { Project, EventEntry } from "@/lib/loadData";

interface Props {
  projects: Project[];
  events: EventEntry[];
  doneTaskIds: Set<string>;
}

export default function SummaryCards({ projects, events, doneTaskIds }: Props) {
  const totalTasks = projects.flatMap((p) => p.tasks).length;
  const inProgress = projects.filter((p) => p.status === "in-progress").length;

  const recent = [...events]
    .sort((a, b) => b.ts.localeCompare(a.ts))
    .slice(0, 3);

  const cards = [
    { label: "전체 프로젝트", value: projects.length },
    { label: "진행 중", value: inProgress },
    { label: "전체 태스크", value: totalTasks },
    { label: "완료 태스크", value: doneTaskIds.size },
  ];

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {cards.map((c) => (
          <div key={c.label} className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
            <p className="text-sm text-gray-500">{c.label}</p>
            <p className="text-3xl font-bold mt-1">{c.value}</p>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <p className="text-sm font-semibold text-gray-600 mb-2">최근 이벤트</p>
        <ul className="space-y-1">
          {recent.map((e, i) => (
            <li key={i} className="text-sm text-gray-600 flex gap-2">
              <span className="text-gray-400">{e.ts.slice(0, 16).replace("T", " ")}</span>
              <span className="font-medium">{e.member}</span>
              <span className="text-blue-500">{e.type}</span>
              {e.task_id && <span className="text-gray-500">{e.task_id}</span>}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
