# Product Requirements Document (PRD)

## SmartEduCafe ERP — SPPOS v2.0

**Status dokumen:** Baseline produk konsolidasi — menggantikan PRD v1.2 sebagai acuan resmi
**Jenis produk:** Aplikasi web internal (Progressive Web App)
**Organisasi:** SmartEduCafe (di bawah ekosistem Taka)
**Audiens utama:** Product Manager, Engineer, UI/UX Designer, Koordinator Akademik, Tentor/Mentor, Manajemen
**Versi:** 2.0 — konsolidasi 8 dokumen sumber (lihat §16)
**Dokumen kendali:** dibangun dari, dan tetap sinkron dengan, `docs/00`–`07` di repo `sklos-local`

---

## 1. Executive Summary

SmartEduCafe ERP adalah **Student Peak Performance Operating System
(SPPOS)** — satu sistem operasi institusi yang menjalankan dua fungsi
sekaligus dalam satu backend dan satu database:

1. **SKLOS** (SmartEdu Kaizen Loop Operating System) — mengelola
   pekerjaan harian staf: aktivitas, proyek, kendala, pembelajaran,
   pengetahuan organisasi.
2. **SEC Student Intelligence** — mengelola perjalanan akademik siswa:
   target, gap, try out, mentoring, kesiapan UTBK, kurikulum bertingkat.

Kedua fungsi ini bukan dua aplikasi terpisah — mereka **dua bounded
context** yang berbagi identitas pengguna, prinsip desain, dan
infrastruktur yang sama, sesuai hierarki:

> **SEOS** (filosofi & governance) → **SPPOS** (operating system
> institusi — dokumen ini) → **SELS** (learning subsystem, student-facing)

Produk ini bukan aplikasi absensi, bukan task manager generik, dan bukan
LMS. Ia adalah sistem yang memastikan setiap pekerjaan staf dapat
ditelusuri dari target hingga hasil, dan setiap siswa dapat diketahui
posisi, target, gap, penyebab gap, dan langkah berikutnya — kapan saja,
dengan bukti, bukan asumsi.

---

## 2. Product Vision & North Star

### 2.1 Vision

Membangun sistem operasi institusi berbasis Kaizen dan AI yang membuat
setiap staf bekerja lebih terarah dan setiap siswa mendapat kejelasan
target, evidence perkembangan, dan intervensi tepat waktu — tanpa
bergantung pada rekap spreadsheet manual.

### 2.2 North Star Metrics (dua sisi produk)

| Sisi | North Star |
|---|---|
| SKLOS (staf) | **Weekly Closed Kaizen Loops** — loop dianggap selesai jika punya owner, tindakan, evidence, lesson learned, status closure |
| SEC Student Intelligence (siswa) | **Score Gap tertutup secara konsisten** — bukan lonjakan skor acak, diukur lewat median beberapa try out, bukan skor terbaik saja |

### 2.3 Prinsip Produk (DNA yang sama diwariskan dari setiap dokumen sumber)

Empat prinsip ini berulang di hampir setiap dokumen yang menjadi acuan
produk ini, dengan kata berbeda tapi makna sama — dipegang sebagai satu
DNA, bukan daftar independen:

1. **Human-in-the-Loop** — AI merangkum dan merekomendasikan; keputusan
   berdampak (skor final, role, publikasi SOP, rekomendasi karier) tetap
   milik manusia.
2. **Evidence Over Opinion** — setiap skor, status, dan rekomendasi harus
   bisa di-drill-down ke bukti.
3. **System Before Blame** — saat ada masalah, cari sistem yang gagal
   (dependency, interface, data validation), bukan langsung menyalahkan
   orang terdekat dengan masalah.
4. **Frictionless First** — input harian < 90 detik; autocomplete,
   default value, quick action, bukan form panjang.

Satu prinsip tambahan yang mengatur kecepatan pembangunan produk ini
sendiri: **Progressive Intelligence** — AI dan fitur pengalaman
(gamifikasi, presentasi episode) ditambahkan setelah data operasional
punya struktur stabil, bukan di awal.

---

## 3. Latar Belakang dan Masalah

### 3.1 Kondisi Sebelumnya

Operasional SmartEduCafe sebelumnya tersebar di banyak spreadsheet
(aktivitas staf, evaluasi siswa, kurikulum, try out) dengan keterbatasan:
data staf dan siswa tidak saling terhubung, kendala tercatat tanpa
mekanisme eskalasi, pembelajaran individu tidak otomatis jadi pengetahuan
organisasi, dan penilaian siswa berisiko terlalu subjektif tanpa evidence
yang bisa ditelusuri.

### 3.2 Masalah Inti

Organisasi belum punya satu sistem yang bisa menjawab cepat: apa yang
sedang dikerjakan setiap staf, kendala apa yang belum selesai, siswa mana
yang berisiko, apa penyebab gap skornya, dan pembelajaran apa yang layak
distandardisasi.

### 3.3 Peluang

Mengubah spreadsheet jadi sistem terintegrasi: mempercepat input,
dashboard otomatis, budaya kerja berbasis evidence, dan fondasi
kematangan AI yang bertahap dan terkontrol.

---

## 4. Lingkup Produk — Dua Bounded Context

### 4.1 SKLOS — Operasional Staf

**Siklus:** Capture → Execute → Detect Gap → Learn → Improve →
Standardize → Assess → Coach

| Modul | Fungsi |
|---|---|
| My Day | Maksimal 3 prioritas harian, Quick Daily Update (<90 detik), tombol I Got Stuck |
| Team Room | Pulse tim: task terlambat, blocker terbuka, blocker berusia >24 jam (eskalasi otomatis) |
| Admin Import | Impor spreadsheet ke staging, idempotent lewat `source_hash`, data sensitif otomatis dikecualikan dari AI |
| Knowledge Chain | `LearningEvent` (Captured→Reused) → `KnowledgeItem` (Draft→Active SOP) |

### 4.2 SEC Student Intelligence — Akademik Siswa

**Siklus:** Assessment → Target → Learning Plan → Try Out → Intervention
→ Readiness

| Modul | Fungsi |
|---|---|
| Student Room | Executive Student Card: target, current score, gap, status risiko, readiness score, primary bottleneck |
| Assessment & Try Out | 4 domain intelligence (Career/Academic/Learning/Mental) + 7 subtes UTBK (PU, PPU, PBM, PK, LBI, LBE, PM) |
| Mentoring | `MentoringSession` (Diagnose/Evidence/Intervention/Commitment/Follow-up) + `MentorCheckIn` (pulse 10 menit) |
| Daily Check-in & Poin | `DailyCheckIn` 5R (Ready Body/Recall/Reason/Reflect with AI/Recover), `StudentPoints` (7 komponen, maks 100/hari) — sengaja terpisah dari tabel akademik |
| Kurikulum | Tiga track: **TKA** (25 sesi), **UTBK** (75 sesi, 4 tahap resmi), **PU** (20 sesi, 3 tahap) — `CurriculumSession` (silabus rencana) terpisah dari `TeachingSession` (log eksekusi) |
| Error Intelligence | Taksonomi berlapis: 12 kategori mesin (`COGNITIVE_DIAGNOSES`) → 5 kategori tentor (`ERROR_CLINIC_CATEGORIES`) → taksonomi khusus per subjek (mis. `PU_ERROR_CODES` 14 kode, `PU_TRAP_CODES` 18 kode) |

---

## 5. Peran Pengguna

| Peran | Ruang kerja | Akses |
|---|---|---|
| Contributor / Staf | My Day | Task sendiri, daily update, blocker |
| Team Leader | Team Room | Task & blocker tim, delegasi |
| Tutor | TeachingSession, PracticeAttempt | Kelas yang diajar |
| Mentor | Student Room, MentorCheckIn, MentoringSession | Siswa yang dipegang; **tidak** melihat data psikologis penuh |
| Academic Director | Kurikulum, KPI kelas/tentor | Lintas kelas |
| Evaluator/HR | Assessment, evidence | Validasi skill/skor, tidak mengubah skor sendiri |
| Orang Tua | Parent Trust Dashboard (Transformation Index, Traffic-Light 3-level) | Read-only, anaknya sendiri |
| Admin | Admin Import, user/role | Administrasi teknis |
| Owner/Management | Founder Command Center (lintas SKLOS + Student Intelligence) | Semua, dengan audit log |

Prinsip role-based simplicity: setiap peran hanya melihat menu dan data
yang relevan dengan tanggung jawabnya.

---

## 6. Model Data Inti (ringkasan)

| Domain | Entitas |
|---|---|
| Identitas & Org | `User`, `Project` |
| SKLOS | `Task`, `DailyLog`, `Blocker`, `StagingActivity`, `SyncRun`, `AuditLog` |
| Knowledge Chain | `LearningEvent`, `KnowledgeItem` |
| Siswa | `Student`, `Assessment`, `TryOut`, `TryOutDomainScore`, `TransformationIndex`, `StudentRiskScore` |
| Kurikulum & Sesi | `CurriculumSession`, `TeachingSession`, `PracticeAttempt`, `MentoringSession`, `MentorCheckIn` |
| Tracking Harian & Poin | `DailyCheckIn`, `StudentPoints` |

Field lengkap tiap entitas ada di `apps/api/app/models/*.py` — dokumen
ini sengaja tidak mereproduksi skema penuh supaya tidak dua sumber
kebenaran untuk hal yang sama; kode adalah sumber definitif.

---

## 7. Kebutuhan Fungsional Kunci

- **FR-01** Setiap task punya owner, deadline, dan Definition of Done.
- **FR-02** Blocker >24 jam ditandai overdue untuk eskalasi (`Blocker.is_overdue`).
- **FR-03** Setiap skor siswa (risk, readiness, mastery) dapat di-drill-down sampai evidence sumbernya.
- **FR-04** Import spreadsheet idempotent — retry payload sama tidak menduplikasi data.
- **FR-05** Data sensitif (`privacy_sensitive=true`) otomatis dikecualikan dari input AI.
- **FR-06** Poin siswa tidak pernah menjadi input untuk tabel akademik (`Assessment`/`TryOut`/`StudentRiskScore`) — dipisah secara arsitektural.
- **FR-07** Status verifikasi (`Task.verification_status`) terpisah dari status eksekusi — "Done" bukan otomatis "Verified".
- **FR-08** Traffic-Light resmi untuk laporan orang tua memakai 3 level (Hijau/Kuning/Merah), dipetakan dari status internal 4 level lewat `to_traffic_light()`.
- **FR-09** Silabus (`CurriculumSession`) dan log eksekusi (`TeachingSession`) adalah tabel terpisah — revisi rencana tidak menimpa riwayat, penyimpangan kelas tidak mengubah silabus.

---

## 8. Kebutuhan Non-Fungsional

- **Mobile-first**: My Day, Daily Update, Stuck, Student Room harus nyaman dipakai dari smartphone.
- **Auditability**: perubahan pada skor, role, assessment, dan data sensitif tercatat di `AuditLog`.
- **Privacy by design**: klasifikasi data (`PUBLIC_INTERNAL` … `RESTRICTED_PATIENT`) menentukan akses dan kelayakan masuk ke AI.
- **Frictionless**: target input harian < 90 detik untuk staf maupun siswa.

---

## 9. Arsitektur Teknis

```text
Next.js 14 PWA (App Router, TypeScript, Tailwind)
        │
        ▼
FastAPI (modular monolith — satu backend, modul per domain)
        │
        ▼
PostgreSQL (satu database, satu source of truth)
```

Modular monolith dipilih dari awal (bukan microservices) — layanan
dipisah nanti hanya kalau skala pengguna/tim benar-benar membutuhkannya.
Environment lokal: `docker-compose.local.yml` (Postgres + Adminer).

---

## 10. Yang Sengaja Di Luar Lingkup (Non-Goals)

| Item | Alasan |
|---|---|
| Experience Engines (SLES presentasi, SEC SHOW, SEGA, SECE, SEAI) | Ditunda sampai SPPOS/SELS inti stabil — prinsip Progressive Intelligence |
| Arsitektur milestone M0–M9 (10 bulan penuh) | Struktur data sudah jelas di dokumen sumber, tapi lingkupnya lebih besar dari kebutuhan tiap iterasi produk |
| Website publik/marketing | Audiens beda (calon siswa), basis kode terpisah dari ERP internal ini |
| 12 Prompt Engines / Daily Prompt OS | Panduan pemakaian AI generatif oleh staf — materi pelatihan, bukan fitur aplikasi |
| Alur status task 7-tahap kanonik (Backlog→...→Archived) | Dicatat sebagai roadmap; migrasi dari 4-tahap yang sudah dipakai UI ditunda untuk menghindari breaking change |
| AI Coach / chat Socratic sungguhan | Data layer (Error Intelligence, taksonomi) sudah siap; pemanggilan LLM aktual menunggu keputusan model, kontrol biaya, dan privacy review |
| Career prediction otomatis, leaderboard publik, multi-agent autonomous execution | Ditolak sejak MVP pertama |

---

## 11. Roadmap Fase

| Fase | Fokus | Status |
|---|---|---|
| 0 — Data Foundation | Master data staf, tim, proyek aktif | Prasyarat pilot |
| 1 — Execution Foundation | My Day, Daily Update, Blocker, Admin Import | **Dibangun** |
| 2 — Learning Foundation | Skill evidence, Knowledge Chain, TeachingSession, kurikulum | **Dibangun** (data layer) |
| 3 — Intelligence Foundation | AI summary, Kaizen Score otomatis, AI Coach aktif | Data layer siap, AI belum diaktifkan |
| 4 — Growth Intelligence | Experience Engines, prediksi risiko, knowledge graph | Belum dimulai |

---

## 12. Acceptance Criteria MVP

1. Daily update (staf maupun siswa) selesai rata-rata < 90 detik.
2. Setiap task punya owner, deadline, Definition of Done.
3. Blocker dapat ditelusuri sampai resolusi, dengan kategori root cause.
4. Semua skor siswa dapat dibuka sampai evidence.
5. Import spreadsheet kedua tidak menambah duplikasi.
6. Poin siswa tidak pernah mengubah skor akademik.
7. AI tidak menerima data yang ditandai sensitif.
8. Riwayat perubahan skor, role, dan data sensitif tercatat di audit log.

---

## 13. Metrik Keberhasilan

| Kategori | Metrik |
|---|---|
| Adopsi | Weekly active users, completion rate daily update/check-in |
| Eksekusi | On-time completion, blocker age, repeated issue rate |
| Pembelajaran | Learning events captured, knowledge reuse rate |
| Akademik | Median 3 try out terakhir, performance decay, error recurrence |
| Manajemen | Waktu penyiapan laporan (target < 15 menit) |

---

## 14. Risiko Utama

| Risiko | Mitigasi |
|---|---|
| Input fatigue | Batas 90 detik, autocomplete, template |
| Poin dijadikan proxy penguasaan materi | Dipisah arsitektural dari tabel akademik (FR-06) |
| AI hallucination / rekomendasi tidak relevan | Human validation wajib, confidence level ditampilkan |
| Penilaian siswa part-time tidak adil | Normalisasi berdasarkan workload/komitmen yang disepakati |
| Data pasien/terapi bocor ke AI | Klasifikasi privasi otomatis + audit setiap pemanggilan AI |

---

## 15. Langkah Berikutnya

1. **Fase 0**: bersihkan master data staf/tim/proyek dari spreadsheet yang ada.
2. Jalankan pilot lokal (`README.md` di repo `sklos-local`) dengan 2 contributor, 1 team leader, 1 mentor, 1 admin.
3. Validasi acceptance criteria §12 selama 3–5 hari pilot.
4. Setelah stabil, lanjut ke aktivasi AI Coach (Fase 3) — mulai dari rules engine sebelum AI generatif penuh.

---

## 16. Dokumen Sumber

PRD ini mengonsolidasi seluruh dokumen yang telah diintegrasikan
sepanjang pengembangan basis ini. Rincian keputusan integrasi tiap
dokumen ada di `docs/00`–`07`; teks lengkap sumber ada di
`docs/references/`.

1. SmartEduCafe Manifesto & PRD v1.1/v1.2, Local Pilot Guide, Gemini Apps Script Guide
2. SEC Student Intelligence OS (proposal)
3. SELS Master Knowledge, Pengajaran, Socratic Numeracy Tutor
4. TEOS Manifesto v4.0 (SEOS/SPPOS/SELS, Golden Key, Operating Model)
5. Kurikulum 100 Sesi TKA–UTBK 2026/2027
6. SOP & Pedoman Transformasi SEC Elite 700+
7. PU Mastery Ebook, SEC PU Learning OS Skill
8. AI OS Master Conversation Synthesis, AI Kaizen Operating System v2.0 (genesis)
