# SKLOS — Curated Project Brief (Basis Web v1)

> **Mulai dari sini kalau baru pertama kali buka repo ini:**
> `docs/07-Master-ERP-Architecture.md` — peta arsitektur konsolidasi yang
> mengikat seluruh dokumen di bawah jadi satu sistem ERP.

Disusun dari 8 dokumen yang diunggah. Dokumen ini adalah **satu sumber acuan kurasian** — bukan pengganti PRD v1.2, tetapi peta yang menjelaskan mana dokumen yang jadi baseline, mana yang sudah usang, dan apa langkah konkret berikutnya.

> **Update:** dokumen usulan "SEC Student Intelligence OS" (platform untuk siswa — Student 360, Try Out Engine, Readiness Score, Mentoring, dst.) sudah disinkronkan ke basis ini sebagai modul terpisah. Lihat `01-SEC-Student-Intelligence-Sync.md` untuk keputusan arsitektur lengkap. Ringkas: SKLOS mengurus staf internal, SEC Intelligence mengurus siswa — satu backend/Postgres yang sama, tabel domain terpisah.

> **Update 2:** lapisan brand/pedagogi SELS (Smarteducafe Elite Learning System) dan spesifikasi AI Socratic Numeracy Tutor sudah disinkronkan juga. Lihat `02-SELS-and-Tutor-Sync.md` — mengisi 100 Session Tracker yang sebelumnya ditunda, menambah Transformation Index untuk Parent Dashboard, dan menyiapkan lapisan data Error Intelligence untuk AI Coach di masa depan.

> **Update 3:** manifesto TEOS v4.0 (SEOS/SPPOS/SELS, Golden Key Teaching Method, Operating Model, Traffic-Light Risk) sudah diintegrasikan. Lihat `03-TEOS-Manifesto-Integration.md` — ini dokumen paling otoritatif sejauh ini dan memberi hierarki kanonik untuk seluruh basis.

> **Update 4:** silabus resmi 100 sesi TKA–UTBK 2026/2027 sudah diintegrasikan. Lihat `04-Kurikulum-100-Sesi-Integration.md` — mengoreksi UTBK jadi 7 subtes (sebelumnya 6, kurang PK) dan tahapan 75 sesi UTBK (Foundation/Mastery/Advanced/Integration&Peak), serta menambah `CurriculumSession` sebagai silabus rencana terpisah dari log eksekusi `TeachingSession`.

> **Update 5:** SOP SEC Elite 700+ (5R Daily Loop, sistem poin, AI Levels) sudah diintegrasikan. Lihat `05-Student-Tracking-Points-Sync.md` — menambah `DailyCheckIn` (tracking harian siswa) dan `StudentPoints` (sistem poin, sengaja terpisah dari tabel akademik), plus koreksi definisi `AI_LEVELS` yang sebelumnya belum jelas.

> **Update 6:** PU Mastery Ebook + SEC PU Learning OS Skill sudah diintegrasikan. Lihat `06-PU-Mastery-Tracking-Integration.md` — PU jadi track kurikulum ketiga (20 sesi, terpisah dari TKA/UTBK), taksonomi error & radar jebakan khusus PU (`PU_ERROR_CODES` 14 kode, `PU_TRAP_CODES` 18 kode), dan Five-Framework Cheat Sheet untuk melacak materi spesifik yang dipakai siswa.

---

## 1. Status setiap dokumen

| Dokumen | Peran | Status |
|---|---|---|
| `SKLOS-v1_2-Product-Requirements-Document-Synchronized.md` | **PRD baseline resmi** (41 bagian, termasuk spreadsheet sync, migration plan, privacy/AI controls) | ✅ Aktif — jadikan satu-satunya acuan spesifikasi |
| `SKLOS-v1_1-Product-Requirements-Document.md` (+ duplikat `__1_`) | Versi PRD sebelum sinkronisasi spreadsheet | ⚠️ Superseded oleh v1.2 — simpan sebagai arsip, jangan dipakai untuk build |
| `Smarteducafe_Manifesto_Master_Knowledge_Base_2026.md` | Log percakapan asli: evolusi ide dari mockup UI → PRD v1.1 → local pilot → Gemini/Apps Script pilot | 📚 Referensi historis / narasi keputusan |
| `SKLOS_SmartEduCafe_Rangkuman_Percakapan_dan_Kerangka_Kerja.md` | Rangkuman percakapan versi awal | 📚 Referensi historis |
| `SKLOS-Conversation-Knowledge-Base.md` | Rangkuman percakapan terstruktur (hasil "pelajari percakapan .md") | 📚 Referensi historis |
| `SKLOS-Local-Pilot-Guide.md` | Panduan teknis: PWA Next.js + FastAPI + PostgreSQL, jalan di **localhost** | ✅ Jalur A — dipakai di scaffold ini |
| `SKLOS-Gemini-Apps-Script-Guide.md` | Panduan teknis alternatif: Google Sheets + Apps Script + Gemini API, jalan di **cloud Google** | ✅ Jalur B — alternatif tanpa Node/Python/Docker |

**Temuan kurasi:** ada dua jalur implementasi yang pernah dieksplorasi, bukan satu jalur yang berevolusi:

- **Jalur A — Local Pilot:** Next.js (PWA) + FastAPI + PostgreSQL, dijalankan di laptop pengembang, diakses lewat Wi‑Fi lokal. Cocok untuk pilot yang perlu ownership penuh atas data model dan siap tumbuh ke deployment cloud.
- **Jalur B — Gemini/Apps Script:** Google Sheets sebagai database transisi + Apps Script sebagai backend/web app + Gemini API sebagai AI Coach. Cocok untuk pilot super-cepat tanpa infrastruktur, tapi Sheets sebagai database punya batas yang eksplisit ditolak PRD v1.2 §33 (*"Permanent Two-Way Editing Is Rejected"*) sebagai arsitektur jangka panjang.

Scaffold di repo ini (`/apps/web`, `/apps/api`, `/infra`) mengimplementasikan **Jalur A**, karena itu yang selaras dengan model data relasional lengkap di PRD v1.2 §13 dan rencana migrasi §38 (spreadsheet → staging → PostgreSQL sebagai source of truth). Jalur B tetap valid sebagai pilot paralel yang lebih cepat kalau organisasi belum siap dengan Docker/Node/Python.

---

## 2. Apa itu SKLOS (ringkas)

SmartEdu Kaizen Loop Operating System — sistem operasi organisasi untuk SmartEduCafe yang menyambungkan aktivitas harian, proyek, kendala (blocker), pembelajaran, skill, knowledge base, coaching, dan penilaian talenta dalam satu siklus:

> **Capture → Execute → Detect Gap → Learn → Improve → Standardize → Assess → Coach**

Prinsip: *simpel bagi pengguna, terstruktur bagi manajer, dapat diaudit oleh evaluator, semakin cerdas dari setiap loop pembelajaran.*

North Star Metric: **Weekly Closed Kaizen Loops** (loop dianggap selesai jika punya owner, tindakan, evidence, lesson learned, dan status closure).

---

## 3. Scope basis web ini (Fase 1 — Execution Foundation)

Mengikuti `SKLOS-Local-Pilot-Guide.md`, scaffold ini **sengaja dibatasi** ke 4 fitur inti supaya tim terbiasa pakai satu sistem sebelum fitur AI/assessment ditambahkan:

1. **My Day** — maksimal 3 prioritas, task hari ini, rutinitas.
2. **Quick Daily Update** — progress, output, impact, energy level, next action (target < 90 detik).
3. **I Got Stuck** — form blocker: deskripsi, severity, dampak, bantuan dibutuhkan.
4. **Admin Import** — impor spreadsheet ke staging, tampilkan status READY/REVIEW/BLOCKED/duplicate.

**Belum termasuk** (sesuai keputusan PRD v1.2 §4.2 dan Local Pilot Guide §2): AI Coach eksternal, push notification, Career Matrix, Monthly Assessment final, login produksi, integrasi Google Sheets real-time, data pasien asli.

---

## 4. Keputusan arsitektur yang dikunci

- **Database sebagai single source of truth**, bukan spreadsheet. Spreadsheet hanya jembatan migrasi/staging (PRD §33.1).
- **Modular monolith** dulu (Identity, Project, Activity, Skill, Knowledge, Assessment, AI Orchestrator, Notification sebagai modul dalam satu backend) — microservices ditunda sampai skala pengguna butuh (PRD §18).
- **Role-based simplicity**: Contributor, Team Leader, Evaluator/HR, Top Management, System Administrator — tiap peran hanya melihat yang relevan.
- **Human-in-the-loop wajib** untuk semua keputusan berdampak tinggi (skor final, role, publikasi SOP, rekomendasi karier) — AI hanya boleh menyiapkan dan merekomendasikan.
- **Privacy by default**: data pasien/terapi ditandai `restricted`, tidak pernah dikirim ke AI, dikecualikan dari staging aktif (Local Pilot Guide §15, PRD §39).
- **Idempotent sync**: setiap record impor punya `source_hash` + `record_uuid`; retry tidak boleh menduplikasi (PRD §35.1, §40).

---

## 5. Langkah lanjut yang disarankan (iterasi berikutnya)

1. **Jalankan scaffold ini secara lokal** (lihat `README.md` di root) — isi seed data dummy, validasi My Day / Daily Update / I Got Stuck di browser dan HP.
2. **Fase 0 — Data Foundation**: bersihkan master data karyawan, tim, proyek aktif dari `TO DO LIST SEC RB 20 07.xlsx`, siapkan sebagai file staging di `/data`.
3. Setelah pilot lokal stabil (quality gate §17 di `SKLOS-Local-Pilot-Guide.md` lulus), lanjut ke **Fase 2 — Learning Foundation** (Loop Learn, Skill Evidence, Knowledge Chain) sesuai urutan prioritas PRD v1.2 §30 — jangan lompat ke radar chart, gamifikasi, AI Coach, atau Career Matrix dulu.
4. Kalau organisasi ingin uji coba super-cepat tanpa infrastruktur sambil scaffold ini disiapkan, `SKLOS-Gemini-Apps-Script-Guide.md` bisa dijalankan paralel sebagai pilot Jalur B untuk fitur yang sama — tapi jangan jadikan Google Sheets sebagai database permanen.
