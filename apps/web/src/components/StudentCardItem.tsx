import { StudentCard } from "@/lib/types";
import { PROGRAM_LABELS } from "@/lib/mock";

const STATUS_STYLE: Record<StudentCard["status"], string> = {
  GREEN: "border-growth bg-growth-soft text-growth",
  YELLOW: "border-kaizen bg-kaizen-soft text-kaizen",
  ORANGE: "border-signal bg-signal-soft text-signal",
  RED: "border-signal bg-signal text-paper",
};

export default function StudentCardItem({ student }: { student: StudentCard }) {
  return (
    <article className="rounded-card border border-line bg-white p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-display text-lg font-medium text-ink">
            {student.name}
          </h3>
          <p className="text-sm text-ink-soft">{student.dreamTarget}</p>
          {student.program && (
            <span className="mt-1 inline-block rounded-card bg-paper px-2 py-0.5 text-[11px] font-medium text-ink-faint">
              {PROGRAM_LABELS[student.program] ?? student.program}
            </span>
          )}
        </div>
        <span
          className={`rounded-card border px-2 py-1 text-xs font-medium ${STATUS_STYLE[student.status]}`}
        >
          {student.status}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3 text-center">
        <div>
          <p className="font-display text-xl font-bold text-ink">
            {student.currentScore}
          </p>
          <p className="text-[11px] text-ink-faint">Current</p>
        </div>
        <div>
          <p className="font-display text-xl font-bold text-ink">
            {student.targetScore}
          </p>
          <p className="text-[11px] text-ink-faint">Target</p>
        </div>
        <div>
          <p className="font-display text-xl font-bold text-signal">
            {student.scoreGap}
          </p>
          <p className="text-[11px] text-ink-faint">Gap</p>
        </div>
      </div>

      {student.readinessScore !== null && (
        <div className="mt-4 border-t border-line pt-3 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-ink-faint">Readiness</span>
            <span className="font-display font-medium text-ink">
              {student.readinessScore}/100
            </span>
          </div>
          {student.primaryBottleneck && (
            <div className="mt-1 flex items-center justify-between">
              <span className="text-ink-faint">Primary bottleneck</span>
              <span className="font-medium text-ink">
                {student.primaryBottleneck}
              </span>
            </div>
          )}
        </div>
      )}
    </article>
  );
}
