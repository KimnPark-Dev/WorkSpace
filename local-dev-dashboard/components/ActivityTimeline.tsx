"use client";

import { useMemo } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, Legend,
} from "recharts";
import { EventEntry, LogEntry } from "@/lib/loadData";

interface Props {
  events: EventEntry[];
  logs: LogEntry[];
}

const MEMBERS = ["ssong", "dohyun", "taeho"] as const;
const MEMBER_COLORS: Record<string, string> = {
  ssong: "#6366f1",
  dohyun: "#10b981",
  taeho: "#f59e0b",
};

export default function ActivityTimeline({ events, logs }: Props) {
  const dailyData = useMemo(() => {
    type Row = { date: string; ssong: number; dohyun: number; taeho: number };
    const counts: Record<string, Row> = {};

    for (const l of logs) {
      const date = l.ts.slice(0, 10);
      if (!counts[date]) counts[date] = { date, ssong: 0, dohyun: 0, taeho: 0 };
      const m = l.member as keyof Row;
      if (m in counts[date]) (counts[date][m] as number)++;
    }
    // fallback: if no logs for a day, still show days with events
    for (const e of events) {
      const date = e.ts.slice(0, 10);
      if (!counts[date]) counts[date] = { date, ssong: 0, dohyun: 0, taeho: 0 };
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
        <p className="text-sm font-semibold text-gray-600 mb-3">최근 14일 멤버별 활동</p>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={dailyData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" tick={{ fontSize: 10 }} tickFormatter={(v) => v.slice(5)} />
            <YAxis tick={{ fontSize: 10 }} allowDecimals={false} />
            <Tooltip />
            <Legend iconSize={10} wrapperStyle={{ fontSize: 12 }} />
            {MEMBERS.map((m) => (
              <Bar key={m} dataKey={m} name={m} stackId="a" fill={MEMBER_COLORS[m]} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <p className="text-sm font-semibold text-gray-600 mb-2">활동 피드</p>
        <ul className="space-y-1.5 max-h-64 overflow-y-auto">
          {recent.map((e, i) => (
            <li key={i} className="text-sm flex gap-2 items-center text-gray-600">
              <span className="text-gray-400 text-xs w-32 shrink-0">{e.ts.slice(0, 16).replace("T", " ")}</span>
              <span
                className="font-medium w-14 shrink-0"
                style={{ color: MEMBER_COLORS[e.member] ?? "#6b7280" }}
              >
                {e.member}
              </span>
              <span className="text-blue-500 text-xs w-24 shrink-0">{e.type}</span>
              {e.task_id && <span className="text-gray-400 text-xs">{e.task_id}</span>}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
