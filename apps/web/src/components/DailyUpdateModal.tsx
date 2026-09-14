"use client";

import { useState } from "react";
import { TaskPriority } from "@/lib/types";
import { submitDailyUpdate } from "@/lib/api";

export default function DailyUpdateModal({
  task,
  onClose,
  onSaved,
}: {
  task: TaskPriority;
  onClose: () => void;
  onSaved: () => void;
}) {
  const [progress, setProgress] = useState(task.progress);
  const [energy, setEnergy] = useState(3);
  const [output, setOutput] = useState("");
  const [impact, setImpact] = useState("");
  const [nextAction, setNextAction] = useState("");
  const [saving, setSaving] = useState(false);

  async function handleSubmit() {
    setSaving(true);
    try {
      await submitDailyUpdate({
        taskId: task.id,
        progress,
        output,
        impact,
        energyLevel: energy,
        nextAction,
      });
      onSaved();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-ink/40 p-0 md:items-center md:p-6">
      <div className="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-t-card bg-paper p-6 md:rounded-card">
        <p className="font-display text-xs font-medium text-kaizen">
          Quick Daily Update
        </p>
        <h2 className="mt-1 font-display text-lg font-medium text-ink">
          {task.title}
        </h2>

        <label className="mt-5 block text-sm text-ink-soft">
          Progress: {progress}%
          <input
            type="range"
            min={0}
            max={100}
            value={progress}
            onChange={(e) => setProgress(Number(e.target.value))}
            className="mt-2 w-full accent-growth"
          />
        </label>

        <label className="mt-4 block text-sm text-ink-soft">
          Energy level: {energy}/5
          <input
            type="range"
            min={1}
            max={5}
            value={energy}
            onChange={(e) => setEnergy(Number(e.target.value))}
            className="mt-2 w-full accent-kaizen"
          />
        </label>

        <label className="mt-4 block text-sm text-ink-soft">
          Hasil hari ini
          <textarea
            value={output}
            onChange={(e) => setOutput(e.target.value)}
            rows={2}
            placeholder="Misal: 3 draft caption selesai"
            className="mt-1 w-full rounded-card border border-line bg-white p-2 text-sm text-ink"
          />
        </label>

        <label className="mt-4 block text-sm text-ink-soft">
          Dampak
          <textarea
            value={impact}
            onChange={(e) => setImpact(e.target.value)}
            rows={2}
            placeholder="Misal: menghemat 2 jam review lead"
            className="mt-1 w-full rounded-card border border-line bg-white p-2 text-sm text-ink"
          />
        </label>

        <label className="mt-4 block text-sm text-ink-soft">
          Langkah berikutnya
          <input
            value={nextAction}
            onChange={(e) => setNextAction(e.target.value)}
            placeholder="Misal: kirim draft ke lead untuk review"
            className="mt-1 w-full rounded-card border border-line bg-white p-2 text-sm text-ink"
          />
        </label>

        <div className="mt-6 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="rounded-card px-4 py-2 text-sm text-ink-faint hover:text-ink"
          >
            Batal
          </button>
          <button
            onClick={handleSubmit}
            disabled={saving}
            className="rounded-card bg-ink px-4 py-2 text-sm font-medium text-paper hover:bg-ink-soft disabled:opacity-50"
          >
            {saving ? "Menyimpan…" : "Simpan update"}
          </button>
        </div>
      </div>
    </div>
  );
}
