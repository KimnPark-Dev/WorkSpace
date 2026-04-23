"use client";

import { useMemo } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { EventEntry, LogEntry } from "@/lib/loadData";

interface Props {
  events: EventEntry[];
  logs: LogEntry[];
}

export default function ActivityTimeline({ events, logs }: Props) {
  const dailyData = useMemo(() => {
    const counts: Record<string, { date: string; events: number; logs: number }> = {};

    for (const e of events) {
      const date = e.ts.slice(0, 10);
      if (!counts[date]) counts[date] = { date, events: 0, logs: 0 };
      counts[date].events++;
    }
    for (const l of logs) {
      const date = l.ts.slice(0, 10);
      if (!counts[date]) counts[date] = { date, events: 0, logs: 0 };
      counts[date].logs++;
    }

    return Object.values(counts).sort((a, b) => a.date.localeCompare(b.date)).slice(-14);
  }, [events, logs]);

  const recent = useMemo(() => {
    return [...events, ...logs.map((l) => ({
      ts: l.ts,
      type: l.type,
      member: l.member,
      task_id: l.task_id,
    }))]
      .sort((a, b) => b.ts.localeCompare(a.ts))
      .slice(0, 20);
  }, [events, logs]);

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <p className="text-sm font-semibold text-gray-600 mb-3">최근 14일 활동</p>
        <ResponsiveContainer width="100%" height={160}>
          <BarChart data={dailyData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" tick={{ fontSize: 10 }} tickFormatter={(v) => v.slice(5)} />
            <YAxis tick={{ fontSize: 10 }} />
            <Tooltip />
            <Bar dataKey="events" name="이벤트" fill="#6366f1" radius={[3, 3, 0, 0]} />
            <Bar dataKey="logs" name="로그" fill="#10b981" radius={[3, 3, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <p className="text-sm font-semibold text-gray-600 mb-2">활동 피드</p>
        <ul className="space-y-1.5 max-h-64 overflow-y-auto">
          {recent.map((e, i) => (
            <li key={i} className="text-sm flex gap-2 items-center text-gray-600">
              <span className="text-gray-400 text-xs w-32 shrink-0">{e.ts.slice(0, 16).replace("T", " ")}</span>
              <span className="font-medium w-12 shrink-0">{e.member}</span>
              <span className="text-blue-500 text-xs w-24 shrink-0">{e.type}</span>
              {e.task_id && <span className="text-gray-400 text-xs">{e.task_id}</span>}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
