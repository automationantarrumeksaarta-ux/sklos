"use client";

import { useState } from "react";
import { TaskPriority, BlockerPayload } from "@/lib/types";
import { submitBlocker } from "@/lib/api";

export default function StuckModal({
  task,
  onClose,
  onSaved,
}: {
  task: TaskPriority;
  onClose: () => void;
  onSaved: () => void;
}) {
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState<BlockerPayload["severity"]>("MEDIUM");
  const [impact, setImpact] = useState("");
  const [helpNeeded, setHelpNeeded] = useState("");
  const [saving, setSaving] = useState(false);

  async function handleSubmit() {
    setSaving(true);
    try {
      await submitBlocker({
        taskId: task.id,
        description,
        severity,
        impact,
        helpNeeded,
      });
      onSaved();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-ink/40 p-0 md:items-center md:p-6">
      <div className="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-t-card bg-paper p-6 md:rounded-card">
        <p className="font-display text-xs font-medium text-signal">
          I Got Stuck
        </p>
        <h2 className="mt-1 font-display text-lg font-medium text-ink">
          {task.title}
        </h2>
        <p className="mt-1 text-xs text-ink-faint">
          Lead akan mendapat notifikasi begitu ini dikirim.
        </p>

        <label className="mt-5 block text-sm text-ink-soft">
          Apa masalahnya?
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            placeholder="Jelaskan kendala secara singkat"
            className="mt-1 w-full rounded-card border border-line bg-white p-2 text-sm text-ink"
          />
        </label>

        <fieldset className="mt-4">
          <legend className="text-sm text-ink-soft">Seberapa serius?</legend>
          <div className="mt-2 flex gap-2">
            {(["LOW", "MEDIUM", "HIGH"] as const).map((level) => (
              <button
                key={level}
                type="button"
                onClick={() => setSeverity(level)}
                className={`rounded-card border px-3 py-1.5 text-xs font-medium ${
                  severity === level
                    ? "border-signal bg-signal-soft text-signal"
                    : "border-line text-ink-faint"
                }`}
              >
                {level === "LOW" ? "Ringan" : level === "MEDIUM" ? "Sedang" : "Berat"}
              </button>
            ))}
          </div>
        </fieldset>

        <label className="mt-4 block text-sm text-ink-soft">
          Dampak kalau tidak segera selesai
          <textarea
            value={impact}
            onChange={(e) => setImpact(e.target.value)}
            rows={2}
            className="mt-1 w-full rounded-card border border-line bg-white p-2 text-sm text-ink"
          />
        </label>

        <label className="mt-4 block text-sm text-ink-soft">
          Bantuan apa yang dibutuhkan?
          <input
            value={helpNeeded}
            onChange={(e) => setHelpNeeded(e.target.value)}
            placeholder="Misal: akses akun, review lead, klarifikasi brief"
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
            disabled={saving || !description}
            className="rounded-card bg-signal px-4 py-2 text-sm font-medium text-paper hover:opacity-90 disabled:opacity-50"
          >
            {saving ? "Mengirim…" : "Kirim blocker"}
          </button>
        </div>
      </div>
    </div>
  );
}
