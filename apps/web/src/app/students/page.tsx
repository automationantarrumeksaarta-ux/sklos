"use client";

import { useEffect, useState } from "react";
import { fetchStudents } from "@/lib/api";
import { StudentCard } from "@/lib/types";
import StudentCardItem from "@/components/StudentCardItem";

export default function StudentsPage() {
  const [students, setStudents] = useState<StudentCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStudents()
      .then(setStudents)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-3xl">
      <header>
        <p className="font-display text-sm text-ink-faint">
          SEC Student Intelligence — ruang kerja terpisah dari My Day
        </p>
        <h1 className="mt-1 font-display text-3xl font-bold text-ink">
          Student Room
        </h1>
        <p className="mt-2 text-sm text-ink-soft">
          Executive Student Card: posisi sekarang, target, gap, dan
          bottleneck utama tiap siswa dalam satu tampilan.
        </p>
      </header>

      <section className="mt-8 grid gap-4 sm:grid-cols-2">
        {loading && <p className="text-sm text-ink-faint">Memuat siswa…</p>}
        {error && (
          <p className="rounded-card border border-signal bg-signal-soft p-3 text-sm text-signal">
            {error}
          </p>
        )}
        {!loading &&
          !error &&
          students.map((student) => (
            <StudentCardItem key={student.id} student={student} />
          ))}
      </section>

      <p className="mt-6 text-xs text-ink-faint">
        Modul ini baru mencakup 5 dari 8 fitur MVP di
        docs/01-SEC-Student-Intelligence-Sync.md §3 — 100 Session Tracker
        dan Bottleneck Engine menyusul.
      </p>
    </div>
  );
}
