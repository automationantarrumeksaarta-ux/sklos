import { BlockerPayload, DailyUpdatePayload, StudentCard, SyncRunSummary, TaskPriority } from "./types";
import { MOCK_PRIORITIES, MOCK_STUDENTS } from "./mock";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK_AUTH === "true";

// Every call falls back to local mock data when the FastAPI backend is not
// running yet, so the frontend can be reviewed on its own before the API
// and Postgres are wired up. Set NEXT_PUBLIC_USE_MOCK_AUTH=false once the
// backend from /apps/api is running to hit the real endpoints.

export async function fetchTodayPriorities(userId: string): Promise<TaskPriority[]> {
  if (USE_MOCK) return MOCK_PRIORITIES;
  const res = await fetch(`${API_URL}/api/v1/tasks/today?user_id=${userId}`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Gagal memuat prioritas hari ini");
  return res.json();
}

export async function submitDailyUpdate(payload: DailyUpdatePayload): Promise<void> {
  if (USE_MOCK) {
    console.info("[mock] daily update", payload);
    return;
  }
  const res = await fetch(`${API_URL}/api/v1/daily-logs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Gagal menyimpan daily update");
}

export async function submitBlocker(payload: BlockerPayload): Promise<void> {
  if (USE_MOCK) {
    console.info("[mock] blocker", payload);
    return;
  }
  const res = await fetch(`${API_URL}/api/v1/blockers`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Gagal menyimpan blocker");
}

export async function fetchStudents(): Promise<StudentCard[]> {
  if (USE_MOCK) return MOCK_STUDENTS;
  const res = await fetch(`${API_URL}/api/v1/students`, { cache: "no-store" });
  if (!res.ok) throw new Error("Gagal memuat data siswa");
  return res.json();
}

export async function importSpreadsheet(file: File): Promise<SyncRunSummary> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/api/v1/import/spreadsheet`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error("Gagal mengimpor spreadsheet");
  return res.json();
}
