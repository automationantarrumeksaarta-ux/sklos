# TEOS Manifesto (SEOS/SPPOS/SELS) — Integrasi ke ERP Basis Web

Manifesto ini (`SEC-MAN-TEOS-2026-03`, 24 bab + 13 lampiran) adalah dokumen
paling otoritatif yang diunggah sejauh ini — ia secara eksplisit
mensinkronkan "Smartedu Manifesto, Employee Operating Handbook, SPPOS
Integrated Curriculum, Master Framework 2026–2027" jadi satu sumber. Bab 8
memberi **hierarki kanonik** yang belum ada di basis sebelumnya:

> **SEOS** (meta-architecture: filosofi, governance, graduate profile) →
> **SPPOS** (operating system institusi: kurikulum, wellbeing, data, QA,
> risiko) → **SELS** (learning subsystem: teaching, mentoring, assessment)
> → **Experience engines** (SEC100, Golden Key, SLES, SEC SHOW, SEGA,
> SECE, SEAI)

Dokumen ini memetakan hierarki tersebut ke basis kode yang sudah ada, dan
hanya mengubah kode di titik-titik yang memberi nilai nyata dan berisiko
rendah — bukan menulis ulang semuanya.

---

## 1. Pemetaan hierarki ke kode yang sudah ada

| Lapisan manifesto | Sudah ada di basis sebagai |
|---|---|
| **SEOS** (filosofi, governance) | Kumpulan dokumen `docs/00`–`03` ini sendiri — tidak butuh kode, ini lapisan keputusan/prinsip |
| **SPPOS** (operating system institusi) | Backend `apps/api` secara keseluruhan: SKLOS (staf) + SEC Student Intelligence (siswa) berjalan di satu Postgres yang sama |
| **SELS** (learning subsystem) | `student_intelligence.py` + `sessions.py`: Assessment, TryOut, TeachingSession, MentoringSession, PracticeAttempt |
| **Experience engines** (SEC100, Golden Key, SLES, SEC SHOW, SEGA, SECE, SEAI) | **Sebagian**: Golden Key masuk kode iterasi ini (§2). SLES/SEC SHOW/SEGA/SECE/SEAI **sengaja ditunda** (§4) — konsisten dengan Non-Goals PRD v1.2 §4.2 yang sudah menolak "gamifikasi terlalu kompleks" sejak basis pertama dibangun |

Tidak ada rename besar-besaran di kode — istilah SPPOS/SELS dipakai di
dokumentasi dan komentar kode mulai sekarang, tabel/model yang sudah ada
tetap dipakai apa adanya supaya tidak merusak yang sudah teruji.

---

## 2. Golden Key Teaching Method — enam tahap yang menggantikan asumsi lama

Bab 9 memberi metode pengajaran kanonik: **Diagnose → Understand → Reason
→ Detect → Repair → Retain**. Ini adalah generalisasi lintas mata
pelajaran dari protokol yang sebelumnya hanya tertulis khusus untuk
Numerasi di `socratic-numeracy-tutor.md`.

**Perubahan kode:** `PracticeAttempt` (di `sessions.py`) mendapat kolom
baru `golden_key_stage` — tahap mana dari keenam tahap ini tempat siswa
berhenti/gagal. Ini melengkapi `cognitive_diagnosis` yang sudah ada
(12 kategori dari spec tutor Numerasi):

- `cognitive_diagnosis` menjawab **jenis** kesalahan (mis. `ARITHMETIC_ERROR`).
- `golden_key_stage` menjawab **di tahap mana** proses berpikir putus
  (mis. `REASON` — siswa tahu konsepnya tapi tidak bisa menjelaskan
  alasan strategi).

Dua dimensi ini bersama memberi data yang lebih tajam untuk Error Bank
dibanding satu dimensi saja.

---

## 3. Traffic-Light Risk — rekonsiliasi 3 level vs 4 level

Lampiran E manifesto mengunci **tiga** status resmi: Hijau, Kuning, Merah
— dengan kriteria eksplisit (mis. Merah = "absen berulang, penurunan
besar, burnout, konflik, integritas, keselamatan, ancaman keluar").

Basis yang sudah ada (`StudentRiskScore.status`) memakai **empat** level:
GREEN/YELLOW/ORANGE/RED, dari dokumen SEC Intelligence yang lebih dulu
diintegrasikan.

**Keputusan:** kode tidak diubah (empat level tetap dipakai secara
internal — bedanya berguna untuk mentor membedakan "mulai tertinggal"
dari "butuh intervensi serius"), tetapi ditambahkan fungsi
`to_traffic_light()` yang memetakan ke tiga level resmi manifesto:

```text
GREEN  → Hijau
YELLOW → Kuning
ORANGE → Kuning   (masih perlu intervensi mentor, belum eskalasi)
RED    → Merah
```

Parent Trust Dashboard dan laporan ke manajemen harus memakai
`to_traffic_light()`, bukan status internal mentah — supaya bahasa yang
sampai ke orang tua konsisten dengan definisi resmi di Lampiran E.

---

## 4. Check-In Mentor 10 Menit — pulse check baru, bukan pengganti Mentoring Session

Lampiran D memberi struktur check-in cepat (6 menit terbagi: Kondisi 1–5,
Target 3 hari, Completion, Error/Blocker, Next Action, Risk) yang **beda
tujuan** dari `MentoringSession` yang sudah ada (Diagnose/Evidence/
Intervention/Commitment/Follow-up — lebih dalam, lebih jarang).

Pola ini sama persis dengan hubungan **Quick Daily Update vs Weekly
Review** di SKLOS: satu cepat dan sering, satu dalam dan jarang. Karena
polanya sudah dikenal di basis ini, model baru `MentorCheckIn` dibuat
mengikuti bentuk yang sama dengan `DailyLog` SKLOS (`condition_1to5` ~
`energy_level`, `next_action`, `risk_status`).

Endpoint: `POST /api/v1/students/{id}/check-ins`.

---

## 5. Operating Model (Bab 19) — memvalidasi, bukan mengubah, desain SKLOS

Bab ini menegaskan dua aturan yang **sudah** jadi prinsip SKLOS sejak
awal, tanpa perlu diketahui dari bab ini:

- "Setiap orang maksimal 2–3 prioritas aktif" → persis batas 3 prioritas
  di My Day.
- "Blocked lebih dari 24 jam dieskalasikan" → prinsip yang sama dengan
  notifikasi blocker escalation di PRD v1.2 §9.

**Perubahan kode:** ditambahkan properti `is_overdue` pada `Blocker`
(>24 jam sejak `opened_at` dan belum `resolved_at`) supaya aturan ini
bisa dibaca langsung dari data, bukan dihitung manual di Team Room.

**Belum diubah:** alur status task kanonik dari Bab 19 (`Backlog → Ready
→ In Progress → Review → Approved → Done → Archived`) lebih kaya dari
`Task.status` yang sudah ada (`TODO/IN_PROGRESS/BLOCKED/DONE`). Tidak
diganti di iterasi ini karena mengubahnya akan merambat ke
`PriorityCard`, `STATUS_LABEL`, dan logika di `daily_logs.py` yang sudah
berjalan — dicatat sebagai item roadmap, bukan dieksekusi buru-buru.

---

## 6. Yang sengaja tidak dibangun (Experience Engines)

SLES (experience layer ala serial), SEC SHOW (format episode: hook →
story → investigation → reveal → battle → Boss Fight → Error Clinic →
recall → next episode), SEGA (gamification engine), SECE (content
proof), SEAI (AI support dengan guardrail safeguarding + consent) —
semuanya **eksplisit ditunda**, dengan alasan yang sama seperti yang
sudah tercatat sejak sync pertama basis ini:

> PRD v1.2 §4.2 (Non-Goals MVP): *"Gamifikasi terlalu kompleks"* dan
> *"Menjalankan multi-agent autonomous execution tanpa persetujuan"*
> sudah ditolak untuk MVP sejak sebelum manifesto ini ada.

Ini bukan basis mengabaikan manifesto — manifesto sendiri menaruh
Experience Engines di layer paling atas hierarki (§1), di atas SPPOS dan
SELS yang harus stabil dulu. Urutan pembangunan basis ini (Fase 1
Execution → Fase 2 Learning → Fase 3 Intelligence → Fase 4 Growth) sudah
konsisten dengan urutan itu — Experience Engines masuk Fase 4.

---

## 7. Ringkasan perubahan kode

- `apps/api/app/models/sessions.py` — `GOLDEN_KEY_STAGES` konstanta,
  kolom `golden_key_stage` di `PracticeAttempt`, model baru
  `MentorCheckIn`.
- `apps/api/app/models/core.py` — properti `Blocker.is_overdue`.
- `apps/api/app/models/student_intelligence.py` — fungsi
  `to_traffic_light()`.
- `apps/api/app/routers/sessions.py` — `POST /api/v1/students/{id}/check-ins`.
- `apps/api/app/seed_students.py` — satu contoh check-in dan
  `golden_key_stage` pada practice attempt yang sudah ada.
