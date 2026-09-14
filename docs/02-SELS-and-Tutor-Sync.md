# SELS Elite Learning System × Socratic Tutor — Sinkronisasi dengan Basis

Empat dokumen baru diunggah. Dua di antaranya (`Pengjaran.md` dan
`Knowledge_Base.md`) **identik** (diverifikasi dengan `diff`) — diperlakukan
sebagai satu dokumen di bawah. Dokumen ini mendudukkan keempatnya terhadap
basis yang sudah ada (SKLOS + SEC Student Intelligence).

| Dokumen | Isinya | Posisi terhadap basis |
|---|---|---|
| `Smarteducafe_Elite_Learning_System_Master_Knowledge_v1.md` | Brand, positioning, 4 program (Smart/Intensif/Exclusive/Exclusive+Kedinasan), value ladder, 5 Transformation Index | **Lapisan konten/brand** — mengisi `Student.program` dan menambah model `TransformationIndex` |
| `..._Pengjaran.md` = `..._Knowledge_Base.md` | 4 pilar pengajaran, template sesi 10 langkah, SELS Framework | **Lapisan pedagogi** — jadi struktur field `TeachingSession` (100 Session Tracker yang sebelumnya ditunda) |
| `SEC_Elite_Socratic_Numeracy_Concept_Golden.md` | Spesifikasi lengkap (1182 baris) AI tutor Socratic untuk Numerasi: error taxonomy, mastery threshold, adaptive difficulty, laporan per 5/20 soal | **Spesifikasi AI Coach** yang sudah dijanjikan di Fase 3 roadmap — sekarang punya isi konkret |
| Dokumen "Yes — an actual website…" (framework AI→BRAND→CONVERSION→OPERATION) | Framework membangun *website publik* untuk ekosistem Taka (BPR, SmartEduCafe, kuliner, jasa) | **Di luar basis ini** — ini untuk situs marketing publik, bukan aplikasi internal. Lihat §5. |

---

## 1. Program mengisi field yang sudah ada, bukan tabel baru

`Student.program` di `student_intelligence.py` sudah berupa string bebas.
Dari Master Knowledge, nilai yang valid dikunci menjadi 4 program dengan
target transformasi masing-masing:

| Kode program | Positioning | Target kenaikan skor |
|---|---|---|
| `SMART_CLASS` | Membangun Cara Belajar yang Benar | +80 s.d. +100 |
| `INTENSIF_CLASS` | Score Acceleration Program | +100 s.d. +150 |
| `EXCLUSIVE_CLASS` | Personal Success Program | +180 s.d. +250 |
| `EXCLUSIVE_KEDINASAN` | Ultimate Success Program (SKD/TIU/TWK/TKP + psikotes + kesamaptaan) | — (kelulusan, bukan skor) |

Disimpan sebagai konstanta `PROGRAM_CATALOG` (lihat kode), bukan tabel
terpisah, karena datanya statis dan kecil — konsisten dengan prinsip
"jangan bikin tabel untuk sesuatu yang cukup jadi konstanta" di basis ini.

---

## 2. TransformationIndex ≠ Assessment — dua hal yang terlihat mirip tapi beda tujuan

Basis yang sudah ada punya `Assessment` (career/academic/learning/mental —
dari dokumen SEC Intelligence sebelumnya, untuk **diagnosis awal**).
Master Knowledge memperkenalkan **5 Transformation Index** (Academic,
Learning Habit, Character, Leadership, Future Readiness) untuk **Parent
Trust Dashboard**, dilaporkan berkala (mis. per bulan/term).

Kedua model dipertahankan terpisah:

- `Assessment` → assessment masuk / snapshot titik waktu tertentu, dipakai
  mentor untuk mendiagnosis siswa baru atau mengevaluasi ulang.
- `TransformationIndex` (baru) → laporan periodik untuk orang tua dan
  manajemen, dipakai buat Parent Trust Dashboard dan Founder Command
  Center — bukan pengganti Assessment.

Menyatukan keduanya akan mencampur tujuan "diagnosis individual" dengan
"laporan periodik ke orang tua", yang audiensnya beda dan siklus
update-nya beda.

---

## 3. 100 Session Tracker — sekarang punya struktur konkret

Sync sebelumnya (`01-SEC-Student-Intelligence-Sync.md` §3) menunda 100
Session Tracker karena belum ada struktur yang jelas. Dokumen Pengajaran
memberi struktur itu: **template 10 langkah per sesi** (Brain Activation →
Mission Brief → Concept Piercing → Guided Practice → Communicative
Challenge → Battle Practice → Error Clinic → Reflection → Daily Mission →
Mentor Review), dikelompokkan dalam 5 tahap perjalanan (dari dokumen SEC
Intelligence sebelumnya): Foundation (1–20) → Development (21–40) →
Acceleration (41–70) → Simulation (71–90) → Peak Performance (91–100).

Model baru `TeachingSession` (lihat `apps/api/app/models/sessions.py`)
mengimplementasikan ini sekarang — bukan lagi ditunda — karena kedua
dokumen bersama-sama sudah memberi struktur yang cukup untuk dibangun
tanpa menebak-nebak.

**Catatan lingkup:** setiap field 10-langkah disimpan sebagai catatan teks
singkat tutor (bukan form panjang) — selaras prinsip *Frictionless First*
basis ini dan batas "30–60 detik/siswa" yang diminta dokumen sumber untuk
input tutor setelah kelas.

---

## 4. Socratic Numeracy Tutor — spesifikasi AI Coach, dibangun sebagai lapisan data dulu

Dokumen ini adalah **system prompt siap pakai** untuk tutor AI Numerasi
(PM), lengkap dengan protokol Socratic questioning, 12 jenis Cognitive
Diagnosis, Confidence Calibration, Mastery Threshold (6 status:
Introduced → Developing → Unstable → Procedural Mastery → Transfer
Mastery → Automatic), dan Adaptive Difficulty Engine.

**Keputusan sinkronisasi:** belum memanggil LLM sungguhan di iterasi ini
(itu tetap Fase 3 — AI Coach di roadmap PRD v1.2 §8, dan prinsip
*Progressive Intelligence* basis ini: AI masuk setelah data punya struktur
stabil). Yang disinkronkan sekarang adalah **lapisan data**-nya, supaya
begitu AI Coach diaktifkan, ia punya tempat menulis dan membaca:

- Model baru `PracticeAttempt` — satu baris per soal latihan: level
  (L1–L6), cognitive diagnosis (12 kategori persis dari dokumen §14),
  confidence (1–5), status penguasaan (6 status dari §18).
- Field `student_id` menghubungkannya ke `Student` yang sama dengan SEC
  Intelligence, dan ke `domain` (PU/PPU/PBM/LBI/LBE/PM) yang sama dengan
  `TryOutDomainScore` — supaya nanti Bottleneck Engine (masih ditunda)
  bisa membaca dua sumber ini sekaligus.
- Teks lengkap dokumen (`SEC_Elite_Socratic_Numeracy_Concept_Golden.md`)
  disalin ke `docs/prompts/socratic-numeracy-tutor.md` di repo ini supaya
  siap dipakai langsung sebagai system prompt saat AI Coach dibangun —
  tidak perlu ditulis ulang nanti.

Endpoint chat/dialog Socratic **tidak** dibangun sekarang — itu perlu
keputusan model AI, kontrol biaya, dan privacy review (PRD v1.2 §39)
terlebih dahulu, sama seperti Gemini Coach di jalur Apps Script yang
sudah dibatasi tombol manual, bukan panggilan otomatis per soal.

---

## 5. Website publik — di luar basis ini, dicatat sebagai deliverable terpisah

Dokumen framework "AI → BRAND → CONVERSION → OPERATION" untuk membangun
website publik (§8 di dalamnya, "Smart Education Adaptation": Website =
Learn → Practice → Measure → Improve) **cocok secara konsep** dengan
Student Room yang sudah dibangun, tapi audiensnya beda:

- Basis ini (`sklos-local`) = aplikasi internal untuk staf dan siswa aktif
  yang sudah terdaftar.
- Website publik = marketing/lead-gen untuk calon siswa, dibangun terpisah
  (bisa Next.js baru atau landing builder), pakai *konten* dari Master
  Knowledge (10 USP, Brand Promise, 4 program, testimoni) sebagai bahan
  copy — bukan berbagi basis kode dengan `sklos-local`.

Tidak dibangun di iterasi ini. Kalau dibutuhkan, sitemap yang disarankan
dari kedua dokumen (Home → Problem → Solution → 4 Program → Proof/SELS
Framework → Parent Trust Dashboard preview → FAQ → CTA konsultasi) sudah
cukup jadi titik mulai untuk deliverable terpisah nanti.

---

## 6. Ringkasan perubahan kode

- `apps/api/app/models/sessions.py` — `TeachingSession` (100 Session
  Tracker) dan `PracticeAttempt` (Error Intelligence dari Socratic Tutor).
- `apps/api/app/models/student_intelligence.py` — tambah
  `TransformationIndex`, konstanta `PROGRAM_CATALOG`.
- `apps/api/app/routers/sessions.py` — `GET /api/v1/students/{id}/journey`
  (ringkasan tahap 100 sesi + error bank ringkas).
- `apps/api/app/seed_students.py` — data dummy diperluas: program, index,
  beberapa sesi dan practice attempt.
- `apps/web` — kartu siswa di Student Room menampilkan badge program dan
  tahap sesi (Foundation/Development/Acceleration/Simulation/Peak).
- `docs/prompts/socratic-numeracy-tutor.md` — salinan penuh system prompt,
  siap pakai untuk Fase 3 AI Coach.
