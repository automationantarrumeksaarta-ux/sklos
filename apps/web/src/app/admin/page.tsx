"use client";

import { useState } from "react";
import { importSpreadsheet } from "@/lib/api";
import { SyncRunSummary } from "@/lib/types";

export default function AdminImportPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<SyncRunSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [importing, setImporting] = useState(false);

  async function handleImport() {
    if (!file) return;
    setImporting(true);
    setError(null);
    try {
      const summary = await importSpreadsheet(file);
      setResult(summary);
    } catch (e) {
      setError(
        e instanceof Error
          ? `${e.message} — pastikan backend FastAPI berjalan di :8000`
          : "Gagal mengimpor"
      );
    } finally {
      setImporting(false);
    }
  }

  return (
    <div className="max-w-2xl">
      <header>
        <p className="font-display text-sm text-ink-faint">Standardize</p>
        <h1 className="mt-1 font-display text-3xl font-bold text-ink">
          Admin Import
        </h1>
        <p className="mt-2 text-sm text-ink-soft">
          Impor{" "}
          <code className="rounded bg-white px-1 py-0.5 text-xs">
            SKLOS-Spreadsheet-Sync-Bridge-v1.0.xlsx
          </code>{" "}
          ke staging. Record BLOCKED tidak menjadi task aktif. Import ulang
          tidak menimbulkan duplikasi.
        </p>
      </header>

      <section className="mt-8 rounded-card border border-line bg-white p-6">
        <label className="block text-sm text-ink-soft">
          Pilih file spreadsheet (.xlsx)
          <input
            type="file"
            accept=".xlsx"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="mt-2 block w-full text-sm text-ink"
          />
        </label>

        <button
          onClick={handleImport}
          disabled={!file || importing}
          className="mt-5 rounded-card bg-ink px-4 py-2 text-sm font-medium text-paper hover:bg-ink-soft disabled:opacity-50"
        >
          {importing ? "Mengimpor…" : "Jalankan import"}
        </button>

        {error && (
          <p className="mt-4 rounded-card border border-signal bg-signal-soft p-3 text-sm text-signal">
            {error}
          </p>
        )}

        {result && (
          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-5">
            {[
              ["Inserted", result.inserted],
              ["Updated", result.updated],
              ["Duplicate", result.duplicate],
              ["Review", result.review],
              ["Blocked", result.blocked],
            ].map(([label, value]) => (
              <div
                key={label as string}
                className="rounded-card border border-line p-3 text-center"
              >
                <p className="font-display text-xl font-bold text-ink">
                  {value}
                </p>
                <p className="text-xs text-ink-faint">{label}</p>
              </div>
            ))}
          </div>
        )}
      </section>

      <p className="mt-6 text-xs text-ink-faint">
        Sesuai kebijakan privasi PRD §39: record dengan{" "}
        <code>privacy_sensitive = TRUE</code> ditandai restricted dan tidak
        pernah dikirim ke layanan AI.
      </p>
    </div>
  );
}
