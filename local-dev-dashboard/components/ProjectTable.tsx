"use client";

import { useState } from "react";
import { Project } from "@/lib/loadData";

const STATUS_LABELS: Record<string, string> = {
  "all": "전체",
  "todo": "예정",
  "in-progress": "진행 중",
  "active": "유지관리",
  "archived": "아카이브",
};

const STATUS_COLORS: Record<string, string> = {
  "todo": "bg-gray-100 text-gray-600",
  "in-progress": "bg-blue-100 text-blue-700",
  "active": "bg-purple-100 text-purple-700",
  "archived": "bg-yellow-100 text-yellow-700",
};

const PRIORITY_COLORS: Record<string, string> = {
  high: "text-red-500",
  medium: "text-yellow-500",
  low: "text-gray-400",
};

interface Props {
  projects: Project[];
  doneTaskIds: Set<string>;
}

export default function ProjectTable({ projects, doneTaskIds }: Props) {
  const [filter, setFilter] = useState("all");

  const filtered = filter === "all" ? projects : projects.filter((p) => p.status === filter);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="p-4 border-b border-gray-100 flex gap-2 flex-wrap">
        {Object.entries(STATUS_LABELS).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
              filter === key ? "bg-gray-800 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="divide-y divide-gray-50">
        {filtered.map((project) => {
          const pending = project.tasks.filter((t) => !doneTaskIds.has(t.id));
          return (
            <div key={project.id} className="p-4">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold">{project.title}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${STATUS_COLORS[project.status] ?? ""}`}>
                      {STATUS_LABELS[project.status] ?? project.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500 mt-0.5">{project.description}</p>
                </div>
                {project.due && (
                  <span className="text-xs text-gray-400 whitespace-nowrap">~ {project.due}</span>
                )}
              </div>

              {pending.length > 0 && (
                <ul className="mt-2 space-y-1">
                  {pending.map((t) => (
                    <li key={t.id} className="text-sm flex items-center gap-2 text-gray-600">
                      <span className={`text-xs font-bold ${PRIORITY_COLORS[t.priority]}`}>
                        {t.priority.toUpperCase()}
                      </span>
                      <span>{t.title}</span>
                      <span className="text-gray-400 text-xs">@{t.member} · {t.estimate_h}h</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
