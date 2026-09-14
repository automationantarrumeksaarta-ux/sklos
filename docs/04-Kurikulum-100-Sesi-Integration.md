# Kurikulum 100 Sesi TKA–UTBK 2026/2027 — Integrasi ke Sistem Kurikulum

Dokumen ini (25 sesi TKA + 75 sesi UTBK, versi 1.0) adalah **silabus
operasional** — lebih konkret dan otoritatif dari dokumen manapun yang
sudah diintegrasikan soal struktur UTBK dan tahapan 100 sesi. Dua koreksi
penting muncul dari sini, plus satu lapisan data baru: **kurikulum
sebagai silabus rencana**, terpisah dari `TeachingSession` yang sudah ada
(log eksekusi aktual per siswa per tentor).

---

## 1. Koreksi: UTBK punya 7 subtes, bukan 6

Dokumen SEC Intelligence yang lebih dulu diintegrasikan (§6 di sync
pertama) memakai enam domain: PU, PPU, PBM, LBI, LBE, PM. Kurikulum ini
mengoreksi jadi **tujuh**, sesuai struktur resmi UTBK 2026:

> **TPS:** PU (Penalaran Umum), PPU (Pengetahuan & Pemahaman Umum), PBM
> (Pemahaman Bacaan & Menulis), **PK (Pengetahuan Kuantitatif)** — domain
> yang sebelumnya hilang.
> **Tes Literasi:** LBI, LBE.
> **Terpisah:** PM (Penalaran Matematika).

`UTBK_DOMAINS` di `student_intelligence.py` diperbaiki jadi 7 elemen.
`TryOutDomainScore.domain` sudah berupa string bebas jadi tidak perlu
migration — baris lama tetap valid, PK baru bisa dipakai mulai sekarang.

---

## 2. Koreksi: tahapan 75 sesi UTBK, bukan tebakan generik

`stage_for_session()` yang sudah ada sebelumnya memakai lima tahap generik
(Foundation 1–20 / Development 21–40 / Acceleration 41–70 / Simulation
71–90 / Peak 91–100) yang diadaptasi dari dokumen visi awal — **tebakan**,
bukan dari silabus resmi.

Silabus ini memberi batas yang benar, dan hanya untuk **75 sesi UTBK**
(TKA adalah track terpisah, bukan bagian dari 100 sesi yang sama):

| Tahap UTBK | Rentang sesi | Fokus |
|---|---|---|
| `FOUNDATION` | 1–21 | 3 putaran seluruh 7 subtes |
| `MASTERY` | 22–49 | 4 putaran pendalaman seluruh subtes |
| `ADVANCED` | 50–63 | speed, HOTS, simulasi per subtes |
| `INTEGRATION_PEAK` | 64–75 | simulasi gabungan, mini TO, full UTBK, taper |

**Perubahan kode:** `TeachingSession` mendapat kolom `track` (`"TKA"` atau
`"UTBK"`). `stage_for_session(session_number, track)` sekarang butuh
`track` — untuk `TKA` tidak ada sub-tahap resmi di silabus ini (sesi 1–25
berjalan sekuensial: orientasi/baseline → 3 mapel wajib → 2 track pilihan
→ simulasi & sprint), jadi fungsi mengembalikan `None` untuk track TKA.
`session_number` sekarang **per-track** (TKA-01..25 dan UTBK-01..75
adalah dua penomoran terpisah), bukan satu urutan 1–100 seperti asumsi
sebelumnya.

---

## 3. CurriculumSession — silabus rencana, terpisah dari log eksekusi

Sebelumnya `TeachingSession` menyimpan **apa yang benar-benar terjadi** di
satu sesi (catatan tentor, attendance, mastery aktual). Silabus ini
memberi **apa yang seharusnya diajarkan** di tiap nomor sesi — dokumen
rencana, bukan log. Keduanya dipisah jadi dua tabel supaya rencana bisa
direvisi tanpa menimpa riwayat eksekusi, dan eksekusi bisa menyimpang dari
rencana tanpa mengubah silabus:

- **`CurriculumSession`** (baru) — satu baris per nomor sesi per track:
  domain/subtes, judul materi/USP, outcome terukur. Ini silabus resmi.
- **`TeachingSession`** (sudah ada) — log aktual: siapa mengajar siapa,
  kapan, hasilnya apa. `TeachingSession.topic` bisa diisi dari
  `CurriculumSession.materi_usp` sesi yang sama sebagai default, lalu
  tentor boleh menyesuaikan kalau kelas menyimpang dari rencana.

**Lingkup seed:** tidak semua 100 baris silabus diketik ulang ke database
di iterasi ini — itu pekerjaan entri data, bukan keputusan arsitektur.
Yang di-seed: 3 sesi TKA pertama dan 7 sesi UTBK pertama (satu putaran
spiral penuh: PU→PPU→PBM→PK→LBI→LBE→PM), cukup untuk membuktikan modelnya
benar. Teks lengkap silabus disalin ke
`docs/references/Kurikulum-100-Sesi-TKA-UTBK.md` — entri sisanya tinggal
disalin dari sana ke `seed_curriculum.py` atau diimpor lewat Admin Import
yang sudah ada di SKLOS.

---

## 4. Error Clinic: dua taksonomi untuk dua kebutuhan berbeda

Template Rencana Ajar (§12) memakai kategori error yang **sederhana**
untuk dipakai tentor di kelas secara cepat: **Konsep, Ceroboh, Strategi,
Waktu, Emosi** (5 kategori). Ini berbeda dari `COGNITIVE_DIAGNOSES` (12
kategori) di `PracticeAttempt`, yang berasal dari spec AI Tutor Numerasi
dan dirancang untuk diagnosis mesin yang lebih presisi.

**Keputusan:** tidak diseragamkan jadi satu taksonomi — tujuannya beda.
Tentor menandai error dengan 5 kategori cepat saat kelas berlangsung;
sistem (atau AI Coach nanti) bisa mendetailkan jadi 12 kategori saat
menganalisis `PracticeAttempt` satu per satu. Fungsi
`to_error_clinic_category()` ditambahkan di `sessions.py` untuk memetakan
12 kategori mesin ke 5 kategori tentor, dipakai saat menampilkan ringkasan
Error Clinic ke tentor di UI (bukan mengganti data mentah).

---

## 5. AI Level per sesi — skala berbeda dari level soal

Template Rencana Ajar mencantumkan **AI Level: L1–L6** dengan pola
"jawaban awal → feedback AI → revisi → penjelasan lisan" (dari Kontrak
Belajar §3 tentang AI etis). Ini **bukan** skala yang sama dengan
`PracticeAttempt.level` (L1–L6 = tingkat kesulitan soal, dari spec tutor
Numerasi §8). Dua field L1–L6 yang namanya kebetulan sama tapi artinya
beda — supaya tidak tertukar, kolom baru di `TeachingSession` diberi nama
eksplisit `ai_level`, terpisah dari `level` di `PracticeAttempt`.

---

## 6. TKA — elective plug-in matrix disimpan sebagai referensi, bukan tabel relasional

Matriks Plug-In (§8): siswa TKA memilih **dua** dari sepuluh track mapel
pilihan (Matematika Lanjut, Fisika, Kimia, Biologi, Ekonomi, Sosiologi,
Geografi, Sejarah, Pendidikan Pancasila, Bahasa Asing), masing-masing
punya 4 sub-blok (A: Peta/Dasar, B: Klaster 1, C: Klaster 2, D:
Aplikasi/Simulasi) yang menggantikan materi sesi TKA 14–21.

**Keputusan:** disimpan sebagai konstanta `TKA_ELECTIVE_TRACKS` (bukan
tabel terpisah — datanya statis dan kecil, sama seperti `PROGRAM_CATALOG`
di sync sebelumnya). `Student` mendapat kolom baru `tka_elective_tracks`
(teks bebas, mis. `"Fisika,Ekonomi"`) untuk mencatat dua pilihan siswa.

---

## 7. Yang tidak diubah

- `TeachingSession` 10-langkah (Brain Activation … Mentor Review) dari
  sync sebelumnya **tidak direstrukturisasi** mengikuti 7-tahap silabus
  ini (Mission&Diagnostic → Concept Piercing → Reason&Battle → Error
  Clinic → Recall → Task Force → Retest). Kedua bentuk cukup mirip dan
  saling tumpang tindih — field teks bebas yang sudah ada cukup menampung
  detail tambahan tanpa migration baru.
- Kalender implementasi (§10) dan cadence review (7 hari/bulan/per TO)
  dicatat sebagai referensi operasional, tidak dikodekan sebagai
  scheduler — SKLOS belum punya modul penjadwalan.

---

## 8. Ringkasan perubahan kode

- `apps/api/app/models/student_intelligence.py` — `UTBK_DOMAINS` jadi 7
  domain (tambah `PK`); `Student.tka_elective_tracks`;
  `TKA_ELECTIVE_TRACKS` konstanta.
- `apps/api/app/models/sessions.py` — `TeachingSession.track` dan
  `.ai_level`; `stage_for_session()` butuh parameter `track`, rentang
  UTBK dikoreksi; `ERROR_CLINIC_CATEGORIES` + `to_error_clinic_category()`;
  model baru `CurriculumSession`.
- `apps/api/app/routers/curriculum.py` — `GET /api/v1/curriculum?track=`.
- `apps/api/app/seed_curriculum.py` — 3 sesi TKA + 7 sesi UTBK (satu
  putaran spiral penuh).
- `docs/references/Kurikulum-100-Sesi-TKA-UTBK.md` — teks lengkap silabus.
