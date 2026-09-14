# SKLOS — Local Pilot Basis Web

> **Mulai dari sini:** `docs/PRD-v2.0-Consolidated.md` — spesifikasi produk resmi (menggantikan PRD v1.2 sebagai acuan utama).
> **Peta arsitektur teknis:** `docs/07-Master-ERP-Architecture.md`

Basis web untuk **SmartEdu Kaizen Loop Operating System (SKLOS)**, sesuai
`SKLOS-v1_2-Product-Requirements-Document-Synchronized.md` dan
`SKLOS-Local-Pilot-Guide.md`. Baca `docs/00-Curated-Project-Brief.md` dulu
untuk peta lengkap semua dokumen sumber dan keputusan arsitektur.

Repo ini sekarang berisi **dua bounded context** dalam satu basis (lihat
`docs/01-SEC-Student-Intelligence-Sync.md`,
`docs/02-SELS-and-Tutor-Sync.md`,
`docs/03-TEOS-Manifesto-Integration.md`,
`docs/04-Kurikulum-100-Sesi-Integration.md` untuk silabus resmi, dan
`docs/05-Student-Tracking-Points-Sync.md` untuk tracking harian siswa +
sistem poin, dan `docs/06-PU-Mastery-Tracking-Integration.md` untuk
track kurikulum PU 20-sesi):

- **SKLOS** — operasional staf internal: My Day, Quick Daily Update,
  I Got Stuck, Admin Import, Team Room.
- **SEC Student Intelligence** — akademik siswa: Student Room (Executive
  Student Card, program SELS, 100 Session Tracker, Error Intelligence
  dari Socratic Numeracy Tutor).

Scope pilot ini (Fase 1 — Execution Foundation) untuk SKLOS: **My Day**,
**Quick Daily Update**, **I Got Stuck**, **Admin Import**. Untuk SEC
Intelligence: 5 modul pertama dari 8 di roadmap sumber (Student 360,
Assessment, Try Out Engine, Mentoring, Risk/Readiness). Belum termasuk AI
Coach, push notification, Career Matrix, Bottleneck Engine, CRM, atau
assessment final di kedua sisi.

```text
sklos-local/
├── apps/
│   ├── web/    Next.js 14 (App Router, TypeScript, Tailwind)
│   └── api/    FastAPI + SQLAlchemy
├── data/       Letakkan file spreadsheet pilot di sini (tidak di-commit)
├── docs/       Dokumen kurasian dan acuan
└── infra/      docker-compose untuk PostgreSQL + Adminer
```

## Jalankan lokal

### 1. Database

```bash
cd infra
docker compose -f docker-compose.local.yml up -d
```

Adminer: `http://localhost:8080` — Server `db`, user `sklos`, password
`sklos_local_password`, database `sklos_local`.

### 2. Backend (FastAPI)

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
python -m app.seed               # isi data dummy: user, project, task
python -m app.seed_students       # isi data dummy: siswa, try out, mentoring, check-in harian, poin
python -m app.seed_curriculum     # isi silabus: 3 sesi TKA + 7 sesi UTBK
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Cek: `http://localhost:8000/health` dan `http://localhost:8000/docs`.

### 3. Frontend (Next.js)

```bash
cd apps/web
npm install
cp .env.local.example .env.local
npm run dev
```

Buka `http://localhost:3000` — akan redirect ke `/today` (My Day).

> `.env.local.example` menyalakan `NEXT_PUBLIC_USE_MOCK_AUTH=true` secara
> default, jadi My Day tampil dengan data mock walau backend belum jalan.
> Set ke `false` untuk memakai data sungguhan dari FastAPI + Postgres.

### 4. Buka dari ponsel

```bash
ipconfig        # Windows — cari IPv4
ip addr         # macOS/Linux
```

Buka `http://IP-LAPTOP:3000` dari ponsel yang satu Wi-Fi. Update
`NEXT_PUBLIC_API_URL` di `.env.local` dan `CORS_ORIGINS` di `apps/api/.env`
menjadi IP tersebut, lalu restart kedua server. Izinkan port 3000 dan 8000
hanya untuk **Private Network** — jangan dibuka ke internet publik.

## Quality gate sebelum pilot 3–5 hari

Lihat checklist lengkap di `SKLOS-Local-Pilot-Guide.md` §17. Minimum:

- [ ] `npm run lint` dan `npm run build` berhasil di `apps/web`.
- [ ] `pytest` berhasil di `apps/api` (tambahkan test sesuai fitur baru).
- [ ] Daily update dapat diselesaikan dalam < 90 detik.
- [ ] Tidak ada data pasien/terapi asli di `/data` atau di database.
- [ ] Import spreadsheet kedua tidak menambah duplicate (`source_hash`).

## Langkah berikutnya

Lihat bagian 5 di `docs/00-Curated-Project-Brief.md` untuk urutan Fase 0–4
yang disarankan (Data Foundation → Execution → Learning → Intelligence).
