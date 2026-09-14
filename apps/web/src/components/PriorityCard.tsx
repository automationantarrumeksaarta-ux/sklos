"use client";

import { TaskPriority } from "@/lib/types";

const STATUS_LABEL: Record<TaskPriority["status"], string> = {
  TODO: "Belum mulai",
  IN_PROGRESS: "Berjalan",
  BLOCKED: "Terhambat",
  DONE: "Selesai",
};

export default function PriorityCard({
  task,
  index,
  onUpdate,
  onStuck,
}: {
  task: TaskPriority;
  index: number;
  onUpdate: (task: TaskPriority) => void;
  onStuck: (task: TaskPriority) => void;
}) {
  return (
    <article className="rounded-card border border-line bg-white p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="font-display text-xs font-medium text-kaizen">
            Prioritas {index + 1} · {task.projectName}
          </p>
          <h3 className="mt-1 font-display text-lg font-medium text-ink">
            {task.title}
          </h3>
        </div>
        <span className="whitespace-nowrap text-xs text-ink-faint">
          {STATUS_LABEL[task.status]}
        </span>
      </div>

      <p className="mt-3 text-sm text-ink-soft">
        Definition of Done: {task.definitionOfDone}
      </p>

      <div className="mt-4">
        <div className="flex items-center justify-between text-xs text-ink-faint">
          <span>Progress</span>
          <span>{task.progress}% · Deadline {task.dueDate}</span>
        </div>
        <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-paper">
          <div
            className="h-full rounded-full bg-growth"
            style={{ width: `${task.progress}%` }}
          />
        </div>
      </div>

      <div className="mt-5 flex gap-3">
        <button
          onClick={() => onUpdate(task)}
          className="rounded-card bg-ink px-4 py-2 text-sm font-medium text-paper transition hover:bg-ink-soft"
        >
          Update
        </button>
        <button
          onClick={() => onStuck(task)}
          className="rounded-card border border-signal px-4 py-2 text-sm font-medium text-signal transition hover:bg-signal-soft"
        >
          Stuck
        </button>
      </div>
    </article>
  );
}
