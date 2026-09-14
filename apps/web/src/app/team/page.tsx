import { MOCK_PRIORITIES } from "@/lib/mock";

export default function TeamRoomPage() {
  const openBlockers = 1;
  const atRiskProjects = MOCK_PRIORITIES.filter((t) => t.progress < 50).length;

  return (
    <div className="max-w-2xl">
      <header>
        <p className="font-display text-sm text-ink-faint">Detect Gap</p>
        <h1 className="mt-1 font-display text-3xl font-bold text-ink">
          Team Room
        </h1>
        <p className="mt-2 text-sm text-ink-soft">
          Ringkasan minim untuk fase pilot — versi penuh Weekly Review dan
          Delegation Builder menyusul di Fase 2.
        </p>
      </header>

      <section className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-3">
        <div className="rounded-card border border-line bg-white p-4">
          <p className="font-display text-2xl font-bold text-ink">
            {MOCK_PRIORITIES.length}
          </p>
          <p className="text-xs text-ink-faint">Task aktif</p>
        </div>
        <div className="rounded-card border border-signal bg-signal-soft p-4">
          <p className="font-display text-2xl font-bold text-signal">
            {openBlockers}
          </p>
          <p className="text-xs text-signal">Blocker terbuka</p>
        </div>
        <div className="rounded-card border border-line bg-white p-4">
          <p className="font-display text-2xl font-bold text-ink">
            {atRiskProjects}
          </p>
          <p className="text-xs text-ink-faint">Progress &lt; 50%</p>
        </div>
      </section>
    </div>
  );
}
