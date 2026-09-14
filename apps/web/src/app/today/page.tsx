"use client";

import { useEffect, useState } from "react";
import { fetchTodayPriorities } from "@/lib/api";
import { TaskPriority } from "@/lib/types";
import PriorityCard from "@/components/PriorityCard";
import DailyUpdateModal from "@/components/DailyUpdateModal";
import StuckModal from "@/components/StuckModal";

const MOCK_USER_ID = "USER-001";

export default function TodayPage() {
  const [tasks, setTasks] = useState<TaskPriority[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updateTarget, setUpdateTarget] = useState<TaskPriority | null>(null);
  const [stuckTarget, setStuckTarget] = useState<TaskPriority | null>(null);
  const [toast, setToast] = useState<string | null>(null);

  useEffect(() => {
    fetchTodayPriorities(MOCK_USER_ID)
      .then(setTasks)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  function showToast(message: string) {
    setToast(message);
    setTimeout(() => setToast(null), 2500);
  }

  return (
    <div className="max-w-2xl">
      <header>
        <p className="font-display text-sm text-ink-faint">Selamat datang</p>
        <h1 className="mt-1 font-display text-3xl font-bold text-ink">
          My Day
        </h1>
        <p className="mt-2 text-sm text-ink-soft">
          Maksimal tiga prioritas. Update dalam kurang dari 90 detik.
        </p>
      </header>

      <section className="mt-8 space-y-4">
        {loading && (
          <p className="text-sm text-ink-faint">Memuat prioritas…</p>
        )}
        {error && (
          <p className="rounded-card border border-signal bg-signal-soft p-3 text-sm text-signal">
            {error}
          </p>
        )}
        {!loading && !error && tasks.length === 0 && (
          <p className="rounded-card border border-line bg-white p-6 text-center text-sm text-ink-faint">
            Belum ada prioritas hari ini. Minta lead menambahkan task, atau
            impor data lewat Admin Import.
          </p>
        )}
        {tasks.slice(0, 3).map((task, i) => (
          <PriorityCard
            key={task.id}
            task={task}
            index={i}
            onUpdate={setUpdateTarget}
            onStuck={setStuckTarget}
          />
        ))}
      </section>

      {updateTarget && (
        <DailyUpdateModal
          task={updateTarget}
          onClose={() => setUpdateTarget(null)}
          onSaved={() => {
            setUpdateTarget(null);
            showToast("Update tersimpan.");
          }}
        />
      )}

      {stuckTarget && (
        <StuckModal
          task={stuckTarget}
          onClose={() => setStuckTarget(null)}
          onSaved={() => {
            setStuckTarget(null);
            showToast("Blocker dikirim ke lead.");
          }}
        />
      )}

      {toast && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 rounded-card bg-ink px-4 py-2 text-sm text-paper shadow-lg">
          {toast}
        </div>
      )}
    </div>
  );
}
