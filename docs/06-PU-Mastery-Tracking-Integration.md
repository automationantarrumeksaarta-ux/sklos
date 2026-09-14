# PU Mastery Ebook × SEC PU Learning OS Skill — Tracking Materi & Kelas Terintegrasi

Dua dokumen: **PU Mastery Ebook** (20 bab konten pengajaran — Argument
Audit, WCC, T3, Analytical Grid, Quantitative Modeling, dst.) dan **SEC PU
Learning OS Skill** (spesifikasi operasional: silabus, lesson plan,
error taxonomy, radar jebakan, mastery gate — khusus mata pelajaran
Penalaran Umum). Yang pertama adalah **materi**; yang kedua adalah
**cara materi itu dilacak dan diajarkan di kelas**. Dokumen ini
mengintegrasikan yang kedua ke basis kode — yang pertama disalin sebagai
referensi konten, bukan didata-modelkan (konten pengajaran bukan baris
database).

---

## 1. PU adalah track kurikulum ketiga — bukan bagian dari UTBK atau TKA

`CurriculumSession`/`TeachingSession` sudah punya dua track (`TKA` 25
sesi, `UTBK` 75 sesi). Skill PU memberi struktur untuk track ketiga:
**`PU`, 20 sesi, terpisah dari 75 sesi UTBK** — PU di sini bukan satu
domain dalam TryOut UTBK (`UTBK_DOMAINS` sudah punya `"PU"` sebagai
subtes), melainkan **program pendalaman terpisah** yang berjalan
paralel dengan UTBK: 10 bulan × 2 sesi/bulan.

Tiga tahap PU (§10.2), beda rentang dari UTBK:

| Tahap | Bulan | Sesi |
|---|---|---|
| `FOUNDATION` | 1–3 | 1–6 |
| `ANALYSIS` | 4–7 | 7–14 |
| `MASTERY` | 8–10 | 15–20 |

**Perubahan kode:** `stage_for_session()` direfaktor dari dua tabel
hard-coded (UTBK + None untuk TKA) menjadi `TRACK_SESSION_STAGES`, sebuah
dict per track — supaya track baru (PU, dan nanti mungkin track lain)
tidak perlu menulis ulang fungsinya, cukup menambah entri dict.

Silabus 20 sesi PU (§11, peta ringkas: bulan, tahap, sesi A/B, tema
pengalaman, produk belajar) di-seed **penuh** ke `CurriculumSession` —
beda dari TKA/UTBK yang hanya sebagian, karena tabel ringkasnya sudah
cukup padat untuk diketik semua tanpa jadi pekerjaan entri data besar.

---

## 2. Dua taksonomi baru, khusus PU — melapis di atas yang generik, tidak menggantikan

Skill ini memberi taksonomi yang jauh lebih rinci dari yang generik
(`COGNITIVE_DIAGNOSES` 12 kategori, `ERROR_CLINIC_CATEGORIES` 5
kategori) — tapi **khusus untuk Penalaran Umum**:

- **`PU_ERROR_CODES`** (§9, 14 kode `PU-E1`–`PU-E14`): Konsep,
  Representasi, Inferensi, Kuantor, Negasi, Implikasi, Asumsi,
  Relevansi, Kausalitas, Constraint, Strategi, Waktu, Confidence,
  Fokus/Emosi.
- **`PU_TRAP_CODES`** (§8, 18 kode `PU-R1`–`PU-R18`, "Radar Jebakan
  PU"): pola jebakan spesifik seperti "hubungan dibalik", "kuantor
  diperkuat", "afirmasi konsekuen", "korelasi dianggap sebab", dst.

**Keputusan arsitektur:** tidak dibuat kolom terpisah per domain (yang
akan meledak jika PPU, PBM, dll. nanti punya taksonomi sendiri-sendiri).
`PracticeAttempt` mendapat dua kolom generik-tapi-fleksibel:
`subject_error_code` dan `subject_trap_code` (string bebas, mis.
`"PU-E3"`, `"PU-R7"`) — hanya diisi ketika `domain` punya katalog
terdefinisi (baru PU sejauh ini). Kolom `cognitive_diagnosis` (12
kategori umum) tetap diisi bersamaan sebagai kategori kasar; kode PU
adalah detail tambahan, bukan pengganti — sama pola dengan
`golden_key_stage` yang sudah ada.

---

## 3. Five-Framework Cheat Sheet — melacak materi apa yang dipakai, bukan mengajarkannya lewat kode

Ebook mengajarkan lima framework inti: **Argument Audit, WCC (Witness–
Chain–Counterexample), T3 (Translate–Transform–Test), Analytical Grid,
Quantitative Modeling**. Konstanta `PU_FRAMEWORKS` ditambahkan, dan
`PracticeAttempt.framework_used` (baru) mencatat framework mana yang
sedang dipakai siswa saat soal itu dikerjakan.

Ini menjawab bagian "tracking materi" dari permintaan: dashboard nanti
bisa menjawab *"siswa ini kuat di WCC tapi lemah di T3"* — bukan cuma
"lemah di PU secara umum". Isi materi framework itu sendiri (bagaimana
cara mengajarkannya) tetap di dalam ebook, disalin ke
`docs/references/PU-Mastery-Ebook.md` — bukan didata-modelkan, karena itu
konten pedagogis untuk dibaca tentor, bukan struktur yang perlu di-query.

---

## 4. Format sesi 90+30 — sudah kompatibel, tidak perlu kolom baru

Format tetap PU (§13): 90 menit bersama tentor (Concept Piercing, Reason,
Boss Fight/Error Clinic) + 30 menit recall & drilling mandiri. Field
bebas teks `TeachingSession` yang sudah ada (dari sync kurikulum
sebelumnya) sudah cukup menampung pembagian ini — tidak ada kolom baru.

---

## 5. Dua "5R" yang beda arti — potensi kebingungan, dicatat eksplisit

Skill PU §22 memakai **Mentor Review 5R**: Result, Reality, Reason,
Response, Reuse — ini **identik** dengan "Session Note 5R" di TEOS
manifesto Lampiran B yang sudah dicatat di `03-TEOS-Manifesto-
Integration.md`, jadi tidak perlu field baru, cukup diisi ke
`TeachingSession.mentor_review` dengan struktur lima bagian itu.

**Yang perlu diwaspadai:** SOP SEC Elite 700+ (`05-Student-Tracking-
Points-Sync.md`) juga punya "5R" — tapi itu **5R harian siswa** (Ready
Body, Recall, Reason, Reflect with AI, Recover), konsep yang sama sekali
berbeda meski singkatannya sama persis. Dua "5R" ini **tidak boleh
disatukan** — satu untuk refleksi mentor tentang sesi mengajar, satu
untuk rutinitas harian siswa. Dicatat di sini supaya iterasi berikutnya
tidak keliru menggabungkan keduanya.

---

## 6. SEC SHOW PU — tetap ditunda, konsisten dengan keputusan sebelumnya

§14.1 skill ini menerapkan format "SEC SHOW" (hook → story →
investigation → reveal → Boss Fight → Error Clinic → recall → next
episode) khusus untuk kelas PU, dengan tema episode per bulan (Logic
Detective, Security Protocol, Courtroom Evidence, dst — sudah masuk ke
kolom `materi_usp`/deskripsi `CurriculumSession` sebagai judul tema, tapi
**mesin presentasinya sendiri tidak dibangun**). Ini konsisten dengan
keputusan `03-TEOS-Manifesto-Integration.md` §6: Experience Engines
(termasuk SEC SHOW) ditunda sampai SPPOS/SELS inti stabil — dokumen ini
tidak mengubah keputusan itu, hanya menunjukkan SEC SHOW *akan* dipakai
di PU nanti begitu engine-nya dibangun.

---

## 7. Ringkasan perubahan kode

- `apps/api/app/models/sessions.py` — `TRACK_SESSION_STAGES` (refactor
  dari tabel UTBK-only), `stage_for_session()` generik per track;
  `PU_ERROR_CODES`, `PU_TRAP_CODES`, `PU_FRAMEWORKS`; kolom baru di
  `PracticeAttempt`: `framework_used`, `subject_error_code`,
  `subject_trap_code`.
- `apps/api/app/seed_curriculum.py` — 20 sesi PU penuh (track `"PU"`).
- `docs/references/PU-Mastery-Ebook.md` dan
  `docs/references/SEC-PU-Learning-OS-Skill.md` — referensi konten dan
  spesifikasi operasional lengkap.
