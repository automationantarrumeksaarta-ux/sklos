# SEC Student Intelligence OS × SKLOS — Sinkronisasi dengan Basis Web

Dokumen baru yang diunggah mengusulkan **SEC Student Intelligence Platform**
(Student 360, Assessment, Try Out Engine, 100 Session Tracker, Mentoring,
Bottleneck Engine, Readiness Score, Founder Command Center, CRM). Dokumen
ini mensinkronkan usulan tersebut dengan basis web SKLOS yang sudah
di-scaffold (`apps/web`, `apps/api`), bukan menggantikannya.

---

## 1. Ini dua bounded context, bukan satu produk yang membesar

| | **SKLOS** (sudah dibangun) | **SEC Student Intelligence** (baru) |
|---|---|---|
| Subjek utama | **Staff/kontributor internal** SmartEduCafe | **Siswa** SmartEduCafe |
| Siklus inti | Capture → Execute → Detect Gap → Learn → Standardize | Assessment → Target → Learning Plan → Try Out → Intervention → Readiness |
| North Star | Weekly Closed Kaizen Loops | Score Gap tertutup / Readiness siswa naik |
| Entitas inti | User, Project, Task, DailyLog, Blocker | Student, Assessment, TryOut, MentoringSession, RiskScore |
| Contoh pengguna | Contributor, Team Leader, Admin | Student, Parent, Tutor, Mentor, Academic Director, Owner |

**Keputusan sinkronisasi:** kedua sistem berbagi satu platform SmartEduCafe
(satu backend modular monolith, satu Postgres, satu Next.js app), tetapi
tabelnya **terpisah** — tidak dipaksakan jadi satu model data. Ini konsisten
dengan prinsip modular monolith di PRD v1.2 §18: domain baru ditambahkan
sebagai modul baru, bukan menumpuk ke model `Task`/`Project` yang sudah ada.

Titik temu yang sah — bukan penggabungan tabel, tapi relasi eksplisit:

- **User** tetap satu tabel identitas untuk kedua sistem. Role diperluas
  (lihat §2) sehingga seorang Tutor/Mentor login sekali, tetapi memakai dua
  ruang kerja berbeda: **My Day** (SKLOS, untuk pekerjaan operasionalnya
  sendiri) dan **Student Room** (SEC Intelligence, untuk siswa yang ia
  pegang).
- Sesi mentoring/one-on-one *boleh* dicatat sebagai `Task` + `DailyLog` di
  SKLOS (karena itu memang pekerjaan si mentor hari itu) **dan** sebagai
  `MentoringSession` di SEC Intelligence (karena itu evidence perkembangan
  siswa). Dua pencatatan dengan tujuan berbeda — jangan disatukan jadi satu
  tabel supaya evaluasi mentor (SKLOS) tidak tercampur dengan data siswa
  yang sensitif.
- Notification Service tetap satu layanan bersama (PRD v1.2 §18).

---

## 2. Perluasan role

`users.role` di basis SKLOS semula: `CONTRIBUTOR | TEAM_LEADER | ADMIN`.
Untuk mengakomodasi 6 role dari dokumen SEC Intelligence, nilai yang
didukung diperluas menjadi:

```text
OWNER               — Founder Command Center, lintas kedua sistem
ACADEMIC_DIRECTOR   — kurikulum, skor, performa tutor
MENTOR              — assessment, mentoring, intervention siswa
TUTOR               — kelas, attendance, assignment, mastery
STUDENT             — belajar, target, try out, progres milik sendiri
PARENT              — monitoring terbatas, read-only
CONTRIBUTOR         — role SKLOS lama, staf non-akademik
TEAM_LEADER         — role SKLOS lama
ADMIN               — administrasi teknis kedua sistem
```

Kolom `role` tetap `String` (bukan enum DB) di scaffold ini supaya
penambahan role tidak perlu migration — tapi validasi nilai yang diizinkan
harus dipindah ke Pydantic/enum begitu masuk pilot sungguhan.

**Prinsip akses yang dikunci dari dokumen sumber:** Tutor tidak melihat
data psikologis sensitif siswa secara penuh; Parent tidak masuk ke data
operasional internal. Ini prinsip yang sama dengan PRD v1.2 §39 (Privacy
and AI Controls) yang sudah berlaku di SKLOS — diteruskan, bukan dibuat
ulang.

---

## 3. MVP yang disinkronkan ke basis (bukan 21 modul sekaligus)

Dokumen sumber sendiri sudah memberi urutan realistis di §26:

> Student 360 → Assessment → Try Out Engine → 100 Session Tracker →
> Mentoring → Readiness Score → Bottleneck Engine → Founder Command Center

Basis kode di repo ini menambahkan **lapisan data untuk 5 modul pertama**
saja (`apps/api/app/models/student_intelligence.py`):

1. `Student` — profil inti + target + gap (bagian dari Student 360).
2. `Assessment` — skor empat domain (Career/Academic/Learning/Mental
   Intelligence) per siswa per tanggal.
3. `TryOut` + `TryOutDomainScore` — skor enam domain UTBK (PU/PPU/PBM/
   LBI/LBE/PM) per try out, sumber untuk Score Trend dan velocity.
4. `MentoringSession` — Diagnose/Evidence/Intervention/Commitment/
   Follow-up per sesi one-on-one.
5. `StudentRiskScore` — snapshot GREEN/YELLOW/ORANGE/RED + alasan.

**Belum dimasukkan ke kode** (sesuai urutan yang sama, ditunda ke iterasi
berikutnya setelah 5 modul di atas stabil): 100 Session Tracker sebagai
tabel terpisah (untuk pilot awal, sesi belajar rutin bisa memakai
`RoutineOccurrence`/`Task` SKLOS yang sudah ada, dikaitkan lewat
`student_id` opsional), Bottleneck Engine (butuh data historis dari 5
modul di atas dulu supaya diagnosisnya bermakna, bukan tebakan), Founder
Command Center gabungan, CRM/lead pipeline, University Admission
Intelligence, AI Student Coach, dan Parent Dashboard.

Endpoint yang ditambahkan: `GET /api/v1/students`,
`GET /api/v1/students/{student_id}`. Halaman frontend: `/students` (daftar
Executive Student Card ringkas) — dipasang di rel navigasi sebagai ruang
kerja terpisah dari My Day, bukan menu tambahan di dalamnya.

---

## 4. Readiness Score — dipakai sebagai formula referensi, bukan final

Bobot SRS dari dokumen sumber (§24) dipakai apa adanya di
`student_intelligence.py` sebagai default constant, dengan catatan yang
sama seperti di dokumen sumber: **formula harus dikalibrasi ulang dengan
data riil SEC** sebelum dipakai untuk keputusan apa pun. Ini sejalan
dengan prinsip *Evidence Over Opinion* dan *Confidence Discipline* yang
sudah dipegang SKLOS — skor tanpa evidence yang cukup tidak boleh
diberi label pasti (lih. PRD v1.2 §6 Confidence Score untuk Kaizen Score,
prinsip yang sama berlaku untuk SRS).

---

## 5. Tentang prompt #4–#6 di dokumen yang sama

Bagian *Turn Your Data Into Answers*, *Turn ChatGPT Into Your Research
Team*, dan *Create An Entire Presentation* adalah **template prompt** untuk
dipakai langsung ke Claude/ChatGPT saat menganalisis spreadsheet, melakukan
riset pasar, atau membuat deck — bukan spesifikasi fitur aplikasi. Tidak
ada yang perlu disinkronkan ke basis web dari ketiganya; ini pustaka
prompt terpisah (cocok untuk BPR ARA, SmartEduCafe, Hotways, dll. sesuai
catatan di dokumen sumber), bukan bagian dari SKLOS atau SEC Intelligence.

---

## 6. Langkah lanjut

1. Jalankan migration/`create_all` baru (tabel `students`, `assessments`,
   `tryouts`, `tryout_domain_scores`, `mentoring_sessions`,
   `student_risk_scores`) lewat `python -m app.seed_students` setelah
   backend jalan.
2. Validasi Executive Student Card di `/students` dengan 2–3 data dummy
   siswa dulu — jangan impor data siswa asli sebelum klasifikasi privasi
   (§39 PRD) diterapkan ke tabel baru ini juga.
3. Setelah 5 modul ini stabil di pilot, lanjut ke 100 Session Tracker dan
   Bottleneck Engine sesuai urutan §26 dokumen sumber — jangan lompat ke
   AI Student Coach atau CRM dulu.
