import fs from "fs";
import path from "path";
import { parseJsonlFile } from "./parseJsonl";

const ROOT = path.resolve(process.cwd(), "..");

export interface Task {
  id: string;
  title: string;
  path: string;
  member: string;
  priority: "high" | "medium" | "low";
  estimate_h: number;
  background?: string;
  skills?: string[];
}

export interface Project {
  id: string;
  title: string;
  status: "todo" | "in-progress" | "done" | "archived";
  due: string | null;
  repo: string | null;
  members: string[];
  tags: string[];
  description: string;
  tasks: Task[];
}

export interface LogEntry {
  ts: string;
  member: string;
  project: string;
  task_id: string;
  task: string;
  type: string;
  tokens: number;
  duration_min: number;
  tags: string[];
  error_count: number;
  notes: string;
}

export interface EventEntry {
  ts: string;
  type: string;
  member: string;
  task_id?: string;
  project?: string;
}

export function loadProjects(): Project[] {
  const dir = path.join(ROOT, "projects");
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .flatMap((f) => {
      try {
        const raw = fs.readFileSync(path.join(dir, f), "utf-8");
        return [JSON.parse(raw) as Project];
      } catch {
        return [];
      }
    });
}

export function loadLogs(): LogEntry[] {
  const dir = path.join(ROOT, "logs");
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".jsonl"))
    .flatMap((f) => parseJsonlFile<LogEntry>(path.join(dir, f)));
}

export function loadEvents(): EventEntry[] {
  return parseJsonlFile<EventEntry>(path.join(ROOT, "events.jsonl"));
}

export function loadDoneTaskIds(): Set<string> {
  const events = loadEvents();
  return new Set(
    events.filter((e) => e.type === "task_done").map((e) => e.task_id!)
  );
}
