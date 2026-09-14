# SEC Elite 700+ SOP — Sinkronisasi Fitur Tracking Siswa & Sistem Poin

Dokumen ini fokus sempit sesuai permintaan: **fitur tracking siswa** dan
**sistem poin** dari SOP SEC Elite 700+ (10 bulan, milestone M0–M9, 5R
Daily Loop). Arsitektur milestone 10-bulan penuh **sengaja ditunda** ke
iterasi berikutnya (§5) — lingkupnya lebih besar dari yang diminta kali
ini.

---

## 1. DailyCheckIn — pola ketiga yang sama bentuknya, subjek berbeda

Basis ini sudah punya dua pola "pulse check" berbentuk sama: `DailyLog`
milik staf (SKLOS, diisi sendiri) dan `MentorCheckIn` (diisi mentor
tentang siswa, dari sync sebelumnya). SOP ini memberi bentuk ketiga:
**Check-in Harian Siswa** (§14.1) — diisi siswa sendiri, tentang dirinya
sendiri, mengikuti 5R (Ready Body, Recall, Reason, Reflect with AI,
Recover).

Model baru `DailyCheckIn` (di `apps/api/app/models/checkin.py`) memetakan
persis ke formulir §14.1: tidur/energi/stres, latihan fisik+durasi+RPE,
catatan recall, statistik Reason (jumlah soal, benar, menit fokus, soal
"mahal waktu"), error dominan, level AI Learning, catatan daya juang,
recovery, dan komitmen besok.

**`error_dominant` memakai `ERROR_CLINIC_CATEGORIES` yang sudah ada** —
dokumen ini memakai lima kategori yang sama persis (Konsep/Ceroboh/
Strategi/Waktu/Emosi) yang sebelumnya diintegrasikan dari kurikulum 100
sesi. Ini konfirmasi silang yang bagus: taksonomi itu memang standar
SmartEduCafe, bukan kebetulan satu dokumen.

---

## 2. AI Levels — koreksi definisi yang sebelumnya masih kosong

Sync sebelumnya (`04-Kurikulum-100-Sesi-Integration.md` §5) menambahkan
kolom `TeachingSession.ai_level` (L1–L6) tapi **tidak tahu artinya** —
hanya mencatat pola "jawaban awal → feedback → revisi" tanpa definisi per
level. SOP ini memberi definisi lengkap (§10):

| Level | Nama | Fungsi |
|---|---|---|
| 1 | Golden Key Solver | Memahami konsep tersulit |
| 2 | Detektor Kerentanan | Menemukan blindspot |
| 3 | Simulasi Kesalahan Nyata | Menguji alasan dan distractor |
| 4 | Feynman Arena | Menjelaskan ulang |
| 5 | Personalized 7-Day Sprint | Memperbaiki dua kelemahan |
| 6 | Doomsday Simulator | Melatih tekanan waktu bertahap |

Konstanta `AI_LEVELS` ditambahkan di `checkin.py` dengan definisi ini.
`TeachingSession.ai_level` dan `DailyCheckIn.ai_learning_level` sekarang
sama-sama merujuk katalog yang sama — koreksi dari catatan "skala belum
jelas" di sync sebelumnya.

---

## 3. Sistem Poin — sengaja terpisah dari tabel akademik

Bagian 12 SOP eksplisit: *"Poin tidak boleh menggantikan akurasi,
mastery, atau review."* Prinsip ini dipegang secara arsitektural, bukan
cuma tertulis: `StudentPoints` **tidak** terhubung ke `Assessment`,
`TryOut`, atau `StudentRiskScore` — poin hanya mengukur proses harian
(disiplin, kehadiran, kepatuhan 5R), bukan penguasaan materi.

Tujuh komponen dari §12, disimpan sebagai konstanta `POINT_COMPONENTS`
(nama → poin maksimum), total maksimum 100/hari:

```text
Menutup hari        10
Latihan fisik        10
Target fokus         20
Target HOTS          20
Active Recall        20
AI Learning          10
Refleksi             10
```

`StudentPoints` menyimpan poin aktual per komponen untuk satu hari
(bukan hanya total), supaya bisa diaudit komponen mana yang sering tidak
tercapai — konsisten dengan prinsip *Evidence Over Opinion* yang sudah
dipegang basis ini sejak SKLOS.

**Level siswa** ("ROOKIE" di contoh dashboard SOP) — dokumen sumber
**tidak** memberi tabel tingkatan lengkap, hanya satu contoh. Fungsi
`student_level(total_points_accumulated)` di kode memberi tingkatan kerja
(ROOKIE → CONSISTENT → DISCIPLINED → ELITE) sebagai **usulan awal yang
perlu dikalibrasi dengan data riil** — sama seperti catatan pada SRS
weights di sync SEC Intelligence pertama. Jangan dipakai untuk keputusan
apa pun sebelum dikalibrasi.

---

## 4. Status mingguan — dikodekan sebagai fungsi murni, sesuai kriteria numerik eksplisit

Beda dari Traffic-Light Risk manifesto (kualitatif, §11.1 sebelumnya),
SOP ini memberi **kriteria numerik eksplisit** untuk status mingguan
(§11.1 dokumen ini):

| Status | Kriteria |
|---|---|
| HIJAU | completion ≥80%, tidur ≥7 jam, stres <7 |
| KUNING | completion 60–79%, tidur 6.5–6.9 jam, atau stres 7–8 |
| MERAH | completion <60%, tidur <6.5 jam, atau stres 9–10 |
| BELUM_ADA_DATA | check-in belum diisi |

Karena kriterianya numerik dan eksplisit, ini dikodekan sebagai fungsi
murni `weekly_status(completion_rate, sleep_hours, stress)` — bukan
disimpan manual seperti `StudentRiskScore.status` (yang memang butuh
judgment mentor). Dua cara input status ini sengaja dibedakan: satu
dihitung otomatis dari angka, satu dinilai manusia.

---

## 5. Yang sengaja ditunda

- **Arsitektur milestone M0–M9** (10 bulan, gerbang Lulus/Tahan/Ulang
  Terarah/Eskalasi) — lingkupnya adalah *program journey* penuh, bukan
  "tracking + poin" yang diminta kali ini. Struktur datanya (`milestone
  code`, target kapasitas, target akademik, kriteria gerbang) sudah jelas
  di sumber dan siap diimplementasikan sebagai iterasi terpisah.
- **Formulir Review Mingguan (§14.2)** — bisa dihitung dari agregasi
  `DailyCheckIn` yang sudah ada (completion rate, fokus rata-rata,
  performance decay), jadi tidak butuh tabel baru — cukup query agregat,
  ditambahkan saat dashboard mingguan dibangun.
- **Reward/konsekuensi edukatif** (§12.1) — kebijakan operasional, belum
  perlu representasi data.
- **Surfacing poin di frontend** — `StudentCardItem` belum menampilkan
  poin/level; endpoint API sudah tersedia (`GET
  /api/v1/students/{id}/points-summary`), UI menyusul.

---

## 6. Ringkasan perubahan kode

- `apps/api/app/models/checkin.py` (baru) — `AI_LEVELS`,
  `POINT_COMPONENTS`, model `DailyCheckIn`, model `StudentPoints`,
  fungsi `student_level()` dan `weekly_status()`.
- `apps/api/app/routers/checkins.py` (baru) —
  `POST /api/v1/students/{id}/daily-check-ins`,
  `GET /api/v1/students/{id}/points-summary`.
- `apps/api/app/seed_students.py` — 3 hari contoh check-in + poin untuk
  Dila.
- `docs/references/SOP-SEC-Elite-700-Plus.md` — teks lengkap SOP.
