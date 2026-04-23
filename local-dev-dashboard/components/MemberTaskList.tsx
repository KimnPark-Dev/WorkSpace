"use client";

import { Project, Task } from "@/lib/loadData";

interface TaskWithProject extends Task {
  projectId: string;
  projectTitle: string;
}

interface Props {
  projects: Project[];
  doneTaskIds: Set<string>;
}

const MEMBER_STYLES: Record<string, { badge: string; dot: string }> = {
  ssong:  { badge: "bg-indigo-100 text-indigo-700",  dot: "bg-indigo-400" },
  dohyun: { badge: "bg-emerald-100 text-emerald-700", dot: "bg-emerald-400" },
  taeho:  { badge: "bg-amber-100 text-amber-700",    dot: "bg-amber-400" },
};

const PRIORITY_COLORS: Record<string, string> = {
  high: "text-red-500",
  medium: "text-yellow-500",
  low: "text-gray-400",
};

export default function MemberTaskList({ projects, doneTaskIds }: Props) {
  const byMember: Record<string, TaskWithProject[]> = {};

  for (const p of projects) {
    for (const t of p.tasks) {
      if (doneTaskIds.has(t.id)) continue;
      if (!byMember[t.member]) byMember[t.member] = [];
      byMember[t.member].push({ ...t, projectId: p.id, projectTitle: p.title });
    }
  }

  const members = Object.keys(byMember).sort();

  if (members.length === 0) {
    return (
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 text-center text-gray-400 text-sm">
        미완료 태스크가 없습니다.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {members.map((member) => {
        const tasks = byMember[member];
        const style = MEMBER_STYLES[member] ?? { badge: "bg-gray-100 text-gray-700", dot: "bg-gray-400" };
        return (
          <div key={member} className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
            <div className="flex items-center gap-2 mb-3">
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${style.badge}`}>
                @{member}
              </span>
              <span className="text-xs text-gray-400">{tasks.length}개 남음</span>
            </div>
            <ul className="space-y-2.5">
              {tasks.map((t) => (
                <li key={t.id} className="flex gap-2 items-start">
                  <span className={`mt-1.5 w-1.5 h-1.5 rounded-full shrink-0 ${style.dot}`} />
                  <div>
                    <p className="text-sm text-gray-700 leading-snug">{t.title}</p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {t.projectId} ·{" "}
                      <span className={PRIORITY_COLORS[t.priority]}>{t.priority}</span>
                      {" "}· {t.estimate_h}h
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        );
      })}
    </div>
  );
}
