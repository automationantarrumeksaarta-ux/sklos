# SmartEduCafe ERP — Arsitektur Master (Satu Sistem, Bukan Kumpulan Dokumen)

Dokumen ini adalah **indeks konsolidasi** dari seluruh dokumen yang sudah
diintegrasikan ke basis `sklos-local`. Dua dokumen terakhir yang diunggah
("Master Conversation Synthesis — AI OS" dan "AI Kaizen Operating System
Iterasi v2.0") ternyata adalah **dokumen genesis** — cikal bakal SKLOS
sebelum berganti nama, lengkap dengan model data yang dijanjikan PRD v1.2
tapi belum pernah diimplementasikan di kode sampai sekarang (§3). Dokumen
ini menutup lingkaran itu: semua yang sudah dibahas, sekarang benar-benar
satu sistem, bukan tujuh dokumen paralel.

---

## 1. Satu ERP, tiga lapisan, sesuai hierarki manifesto

Mengikuti hierarki kanonik dari `03-TEOS-Manifesto-Integration.md`:

```text
SEOS   (filosofi & governance)     → dokumen ini + docs/00-06
SPPOS  (operating system institusi) → apps/api (satu Postgres, satu backend)
SELS   (learning subsystem)         → student_intelligence.py, sessions.py, checkin.py
```

Di bawah SPPOS ada **dua bounded context** yang berjalan di backend yang
sama (`01-SEC-Student-Intelligence-Sync.md`):

- **SKLOS** — operasional staf: siapa mengerjakan apa, hari ini.
- **SEC Student Intelligence** — akademik siswa: posisi, target, gap,
  intervensi.

---

## 2. Peta modul kode → dokumen sumber

| Modul kode | Dokumen sumber | Sync doc |
|---|---|---|
| `models/core.py` (User, Project, Task, DailyLog, Blocker) | AI Kaizen OS v2.0 §5 (genesis SKLOS) | doc ini §3 |
| `models/knowledge.py` (LearningEvent, KnowledgeItem) | AI Kaizen OS v2.0 §5.5-5.6 | doc ini §3 |
| `models/student_intelligence.py` (Student, Assessment, TryOut, TransformationIndex) | SEC Student Intelligence OS + SELS Master Knowledge | `01`, `02` |
| `models/sessions.py` (TeachingSession, PracticeAttempt, CurriculumSession, MentorCheckIn) | TEOS Manifesto + Kurikulum 100 Sesi + PU Learning OS Skill | `02`, `03`, `04`, `06` |
| `models/checkin.py` (DailyCheckIn, StudentPoints) | SOP SEC Elite 700+ | `05` |
| `routers/*` | (mengikuti model di atas) | — |

**Prinsip yang menyatukan semuanya** (dipegang sejak modul pertama
dibangun, dikonfirmasi berulang di setiap dokumen berikutnya — lihat
Source Policy S0–S4 di AI OS Synthesis §9, yang persis sama dengan
`privacy_classification` PRD v1.2 §39 yang sudah dipakai `StagingActivity`
sejak awal): **Human-in-the-Loop, Evidence Over Opinion, System Before
Blame, Frictionless First.** Empat prinsip ini disebut ulang dengan kata
berbeda di hampir setiap dokumen yang diunggah — bukan kebetulan,
melainkan DNA yang sama diwariskan dari genesis SKLOS.

---

## 3. Gap yang baru ditutup: Knowledge Chain akhirnya ada tabelnya

PRD v1.2 (dokumen paling pertama diintegrasikan) sudah menjanjikan
"Knowledge Chain dan SOP" di §10.7 — alur `Blocker → Solusi → Lesson
Learned → Validation → Knowledge Item → SOP → Training → Reuse`. Tapi di
semua iterasi sebelumnya, **tabel untuk ini tidak pernah dibuat** — fokus
selalu bergeser ke modul yang sedang aktif dibahas.

AI Kaizen OS v2.0 §5.5–5.6 memberi struktur field yang persis dibutuhkan,
jadi ditambahkan sekarang:

- **`LearningEvent`** — satu baris per insight, dengan `learning_stage`
  (Captured → Implemented → Validated → Standardized → Reused).
- **`KnowledgeItem`** — aset pengetahuan, `sop_status` (Draft → Tested →
  Approved → Active → Retired). Promosi ke SOP tetap keputusan manusia
  (default `DRAFT`), konsisten dengan prinsip Human-in-the-Loop.

Endpoint: `POST/GET /api/v1/knowledge/learning-events`,
`GET /api/v1/knowledge/items`.

---

## 4. Refinement additif pada Task dan Blocker — tidak mengubah yang sudah jalan

Genesis SKLOS memberi dua konsep yang **belum ada** di `Task`/`Blocker`
sejak Fase 1 dibangun, dan keduanya ditambahkan sebagai kolom baru
(nullable, tidak mengubah field/status yang sudah dipakai UI My Day/Team
Room — konsisten dengan kehati-hatian yang sudah dicatat di
`03-TEOS-Manifesto-Integration.md` §5 soal tidak mengubah `Task.status`):

- **`Task.verification_status`** — dimensi terpisah dari `status`. Aturan
  eksplisit dari sumber: *"Done bukan Verified"* — task bisa berstatus
  `DONE` tapi `verification_status` masih `REVIEW_NEEDED` sampai reviewer
  memeriksa evidence.
- **`Task.impact_score` / `.urgency_score`** + fungsi `compute_priority()`
  — Base Priority = Impact × Urgency, P1–P4. Ini pelengkap opsional untuk
  `Task.priority` (ordinal yang sudah dipakai My Day), bukan pengganti.
- **`Blocker.status`** (Open → Investigating → Corrective Action Running
  → Resolved → Verified Closed), **`.root_cause_category`** (Human /
  Process / System / Technology / Knowledge / Policy / Communication),
  **`.recurrence_flag`** — sebelumnya `Blocker` cuma punya
  `opened_at`/`resolved_at`, tanpa kategori penyebab sama sekali.

---

## 5. Kaizen Intelligent Gap Framework — dipegang sebagai template analisis, bukan tabel

AI Kaizen OS v2.0 §8 memberi kerangka analisis akar masalah dengan 6
domain gap (Outcome, Execution, Capability, Coordination, System,
Learning). Ini **template berpikir untuk Weekly Review**, bukan
struktur data — sama perlakuannya dengan KPI Tree dan Operating Model
dari manifesto TEOS yang sudah didokumentasikan tanpa tabel baru.
Ditambahkan ke `docs/references/` sebagai acuan mentor/koordinator saat
mengisi `TeachingSession.mentor_review` atau `LearningEvent`.

---

## 6. Peta lengkap dokumen yang sudah diintegrasikan

| # | Dokumen | Yang diintegrasikan |
|---|---|---|
| — | PRD v1.2, Local Pilot Guide, Gemini Apps Script Guide | Basis web pertama (Next.js + FastAPI + Postgres) |
| `01` | SEC Student Intelligence OS | Modul akademik siswa, terpisah dari SKLOS |
| `02` | SELS Master Knowledge + Socratic Numeracy Tutor | 100 Session Tracker, Error Intelligence |
| `03` | TEOS Manifesto v4.0 | Hierarki SEOS/SPPOS/SELS, Golden Key, Traffic-Light, Check-In Mentor |
| `04` | Kurikulum 100 Sesi TKA-UTBK | 7 domain UTBK (koreksi dari 6), tahapan resmi, `CurriculumSession` |
| `05` | SOP SEC Elite 700+ | `DailyCheckIn`, `StudentPoints`, definisi `AI_LEVELS` |
| `06` | PU Mastery Ebook + PU Learning OS Skill | Track PU 20-sesi, `PU_ERROR_CODES`, `PU_TRAP_CODES` |
| `07` (ini) | AI OS Synthesis + AI Kaizen OS v2.0 (genesis) | Knowledge Chain, refinement Task/Blocker, konsolidasi arsitektur |

---

## 7. Yang masih sengaja di luar basis

Tidak berubah dari keputusan-keputusan sebelumnya — dicantumkan ulang di
sini supaya satu dokumen ini cukup sebagai peta lengkap:

- **Experience Engines** (SLES presentasi, SEC SHOW, SEGA, SECE, SEAI) —
  ditunda sampai SPPOS/SELS inti stabil (`03` §6).
- **Arsitektur milestone M0–M9** (10 bulan penuh) — struktur datanya jelas
  tapi lingkupnya lebih besar dari yang diminta tiap iterasi (`05` §5).
- **Website publik marketing** — audiens beda (calon siswa, bukan
  pengguna internal), basis kode terpisah (`02` §5).
- **12 Prompt Engines / Daily Prompt OS / Platform Adapter** (AI OS
  Synthesis §6-8) — ini panduan cara staf memakai AI generatif
  (ChatGPT/Gemini/NotebookLM) dalam pekerjaan sehari-hari, bukan fitur
  aplikasi. Relevan untuk SOP pelatihan staf, tidak untuk `sklos-local`.
- **Alur status task kanonik 7-tahap** (Backlog→...→Archived, dari
  Operating Model TEOS §19) — dicatat sebagai roadmap, belum
  menggantikan `Task.status` 4-tahap yang sudah dipakai UI.
