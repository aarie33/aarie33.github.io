# PRD — Website Profil & Portfolio Engineering

**Versi:** 1.0
**Tanggal:** 18 Agustus 2026
**Pemilik:** `{{NAMA}}` — Dev Lead / Backend Developer
**Status:** Draft untuk implementasi

---

## 1. Ringkasan

Mengubah portfolio berbasis PowerPoint (35 project) menjadi website statis yang di-deploy ke GitHub Pages. Website ini menggantikan PPT sebagai artefak utama saat melamar kerja, pitch ke klien, dan dibagikan lewat LinkedIn/CV.

### Masalah yang diselesaikan

| Keterbatasan PPT saat ini | Solusi di web |
|---|---|
| Harus dikirim sebagai file, tidak bisa di-link | Satu URL permanen |
| Linear — 35 slide dengan bobot sama, tidak ada yang menonjol | Tiering: unggulan vs arsip |
| Tidak bisa dicari atau difilter | Filter by stack, role, tahun, domain |
| Bukti berupa screenshot UI, padahal peran utama backend | Narasi teknis: arsitektur, skala, keputusan |
| Update = edit file, kirim ulang | Tambah 1 file markdown, push |
| Tidak terindeks Google | SEO + structured data |

### Prinsip utama

> **Volume membuktikan pengalaman. Kedalaman membuktikan kemampuan. Website harus menyajikan keduanya tanpa yang satu menenggelamkan yang lain.**

---

## 2. Target Audiens

**Primer — Tech recruiter / hiring manager (60%)**
Waktu baca 30–90 detik. Butuh cepat tahu: senioritas, stack utama, skala project. Sering buka dari mobile.

**Sekunder — Engineering lead / CTO yang mengevaluasi (25%)**
Waktu baca 5–15 menit. Membaca 2–3 case study penuh. Mencari bukti pengambilan keputusan teknis, bukan daftar teknologi.

**Tersier — Calon klien freelance (15%)**
Mencari project sejenis dengan kebutuhan mereka. Butuh filter by domain (fintech, ERP, sosial).

### User stories

- Sebagai recruiter, saya ingin tahu dalam 10 detik apakah kandidat ini backend-heavy atau fullstack, supaya saya bisa lanjut atau tidak.
- Sebagai engineering lead, saya ingin membaca satu project secara mendalam untuk menilai cara berpikirnya, bukan cuma hasil akhirnya.
- Sebagai calon klien, saya ingin memfilter project berdasarkan domain bisnis saya untuk melihat pengalaman yang relevan.
- Sebagai pemilik situs, saya ingin menambah project baru cukup dengan membuat satu file, tanpa menyentuh layout.

---

## 3. Kriteria Sukses

| Metrik | Target |
|---|---|
| Lighthouse Performance (mobile) | ≥ 95 |
| Lighthouse Accessibility | 100 |
| Largest Contentful Paint | < 1.5s (4G) |
| Total transfer halaman utama | < 500 KB |
| Total transfer halaman detail | < 800 KB |
| Waktu menambah project baru | < 5 menit |
| Semua 35 project punya URL sendiri | Ya |

---

## 4. Scope

### Termasuk
- Halaman utama, index project, 35 halaman detail, tentang, kontak
- Sistem filter & pencarian client-side
- Dark theme (satu tema, tanpa toggle)
- Responsif 320px–2560px
- Pipeline ekstraksi otomatis dari `My-Portfolio.pptx` — seluruh konten & asset digenerate, bukan dibuat manual
- Deploy otomatis via GitHub Actions
- Sitemap, RSS, Open Graph, JSON-LD

### Tidak termasuk (v1)
- CMS / admin panel
- Blog
- Multi-bahasa (v1 bahasa Inggris — lihat catatan §6.3)
- Light theme toggle
- Form kontak dengan backend (pakai `mailto:` + link langsung)
- Analytics berbayar (cukup GoatCounter/Plausible jika perlu)

---

## 5. Stack Teknis

| Layer | Pilihan | Alasan |
|---|---|---|
| Framework | **Astro 5.x** | Output HTML statis, zero JS default, content collections dengan validasi schema |
| Sumber konten | `My-Portfolio.pptx` (root project) | Diekstrak sekali oleh `scripts/extract_pptx.py`, lalu markdown jadi source of truth |
| Ekstraksi | Python + `python-pptx` + `Pillow` | Menangani mapping slide→gambar dan normalisasi ukuran |
| Konten | Markdown + frontmatter | Satu file per project, portable, diff-able di git |
| Styling | CSS murni + custom properties | 35 halaman tidak butuh Tailwind; token CSS lebih ringan dan eksplisit |
| Gambar | `astro:assets` | Konversi WebP/AVIF otomatis, `width`/`height` otomatis (cegah CLS) |
| Interaktivitas | Vanilla JS, `client:visible` | Filter & search saja — tidak perlu framework |
| Font | Self-hosted `.woff2` | Hindari request ke Google Fonts, kontrol FOUT |
| Hosting | GitHub Pages | Gratis, custom domain, sudah terintegrasi dengan repo |
| CI | GitHub Actions (`withastro/action`) | Build & deploy otomatis on push |

### Catatan konfigurasi

```js
// astro.config.mjs
export default defineConfig({
  site: 'https://{{USERNAME}}.github.io',
  base: '/',              // ganti ke '/portfolio' jika repo bukan {{USERNAME}}.github.io
  image: { formats: ['avif', 'webp'] },
  integrations: [sitemap()],
});
```

> **Jebakan:** jika repo bukan `{{USERNAME}}.github.io`, semua path asset butuh `base`. Selalu pakai `import.meta.env.BASE_URL` untuk link manual, jangan hardcode `/`.

---

## 6. Model Konten

### 6.1 Schema

```ts
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: ({ image }) => z.object({
    // Identitas
    id: z.string().regex(/^P-\d{3}$/),        // P-001 … P-035, stabil selamanya
    title: z.string(),
    tagline: z.string().max(90),               // satu baris, tampil di index

    // Klasifikasi
    tier: z.enum(['featured', 'standard', 'compact']),
    year: z.number().int().min(2015).max(2030),
    domain: z.enum(['Fintech', 'Social Impact', 'ERP', 'Government',
                    'E-commerce', 'Education', 'Healthcare', 'Internal Tools']),

    // Peran
    roles: z.array(z.enum(['Dev Lead', 'Backend Developer',
                           'Fullstack Developer', 'Frontend Developer',
                           'System Analyst'])).min(1),
    teamSize: z.number().int().optional(),
    duration: z.string().optional(),           // "4 bulan"
    client: z.string().optional(),

    // Teknis
    stack: z.array(z.string()).min(1),         // ['CodeIgniter 3', 'HMVC', 'MySQL']
    architecture: z.string().optional(),       // 'Monolith HMVC', 'Microservices'

    // Media
    cover: image(),
    screenshots: z.array(z.object({
      src: image(),
      caption: z.string(),                     // WAJIB — caption = konteks, bukan dekorasi
    })).default([]),

    // Link
    liveUrl: z.string().url().optional(),
    repoUrl: z.string().url().optional(),

    // Metrik dampak (opsional tapi sangat dianjurkan)
    metrics: z.array(z.object({
      label: z.string(),                       // 'Transaksi diproses'
      value: z.string(),                       // '120K+/bulan'
    })).default([]),

    // Kontrol
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
    order: z.number().default(999),
  }),
});

export const collections = { projects };
```

### 6.2 Sistem tiering

Semua 35 project punya halaman detail. Yang berbeda adalah **densitas template**, ditentukan field `tier`. Ini mencegah halaman terlihat kosong ketika kontennya memang sedikit.

| Tier | Jumlah | Isi minimum | Layout |
|---|---|---|---|
| `featured` | 6–8 | 400–700 kata, 3–5 screenshot, diagram arsitektur, ≥2 metrik | Full case study: hero besar, section bertingkat, sidebar sticky metadata |
| `standard` | ~12 | 150–250 kata, 1–2 screenshot | Satu kolom, hero sedang, metadata inline |
| `compact` | ~15 | 60–120 kata, 1 screenshot | Layout rapat, metadata dominan, screenshot lebar penuh di bawah |

**Aturan:** template `compact` sengaja dirancang agar konten pendek terlihat *disengaja*, bukan *belum selesai*. Tidak boleh ada whitespace besar yang tidak terisi.

Field `tier` bisa dinaikkan kapan saja tanpa refactor — cukup ubah frontmatter dan tambah konten.

### 6.3 Struktur isi halaman `featured`

Urutan section wajib (ini yang membedakan portfolio backend dari galeri screenshot):

1. **Konteks** — klien ini siapa, masalah bisnisnya apa
2. **Tantangan teknis** — kenapa ini tidak trivial
3. **Arsitektur & keputusan** — apa yang dipilih dan *kenapa*, termasuk trade-off yang ditolak
4. **Kontribusi spesifik** — "saya yang mengerjakan X" bukan "tim mengerjakan X"
5. **Hasil** — metrik, atau minimal outcome kualitatif
6. **Pelajaran** — 1–2 kalimat, opsional tapi menunjukkan refleksi

> **Bahasa:** tulis dalam bahasa Inggris. Audiens recruiter teknis di Indonesia terbiasa membaca CV/portfolio berbahasa Inggris, dan ini membuka peluang remote internasional. Nama klien lokal tetap ditulis apa adanya.

### 6.4 Contoh file

```markdown
---
id: P-001
title: Ayo Donasi
tagline: Donation and zakat platform for a national Islamic foundation
tier: featured
year: 2021
domain: Social Impact
roles: [Dev Lead, Backend Developer]
teamSize: 4
duration: 5 months
client: "{{NAMA_KLIEN}}"
stack: [CodeIgniter 3, HMVC, MySQL, Midtrans, Bootstrap 4]
architecture: Modular monolith (HMVC)
cover: ./images/ayo-donasi/cover.png
screenshots:
  - src: ./images/ayo-donasi/home.png
    caption: Campaign landing with real-time funding progress
liveUrl: https://ayodonasi.id
metrics:
  - label: Campaigns managed
    value: "{{TODO}}"
  - label: Monthly transactions
    value: "{{TODO}}"
featured: true
---

## Context
{{TODO}}

## Technical challenge
{{TODO}}
```

---

## 7. Arsitektur Informasi

```
/                          Beranda
/projects/                 Index — semua 35, filterable
/projects/[slug]/          Detail project (×35)
/about/                    Tentang, pengalaman, keahlian
/contact/                  Kontak
/404
```

### Struktur folder

```
src/
├── content/
│   ├── projects/
│   │   ├── ayo-donasi.md
│   │   ├── images/ayo-donasi/*.png
│   │   └── … (35 project)
│   └── content.config.ts
├── layouts/
│   ├── Base.astro
│   └── project/
│       ├── Featured.astro
│       ├── Standard.astro
│       └── Compact.astro
├── components/
│   ├── IndexRow.astro          ← signature component
│   ├── FilterBar.astro
│   ├── BrowserFrame.astro
│   ├── StackBadge.astro
│   ├── MetricGrid.astro
│   └── Nav.astro / Footer.astro
├── styles/
│   ├── tokens.css
│   ├── base.css
│   └── motion.css
└── pages/
```

---

## 8. Spesifikasi Halaman

### 8.1 Beranda

Tugas tunggal: **dalam 10 detik, pengunjung tahu senioritas dan spesialisasi.**

| Section | Isi |
|---|---|
| Hero | Statement tesis 2 baris dalam display face besar. Bukan "Hi, I'm X" — langsung posisi: nama + peran + spesialisasi. Sub-baris ringkas: tahun pengalaman, jumlah project, domain utama. |
| Index preview | 8 baris pertama dari The Index (lihat §9.5), langsung terlihat di bawah fold. Bukti volume ditampilkan sebagai struktur, bukan klaim. |
| Featured | 3 project unggulan sebagai kartu besar dengan metrik, bukan sekadar screenshot |
| Capability | Stack dikelompokkan per kategori (Language / Framework / Database / Infra), dengan indikator kedalaman — bukan progress bar persentase palsu |
| CTA | Link ke index lengkap + kontak |

**Larangan:** tidak ada progress bar skill berbasis persentase. Tidak ada carousel otomatis. Tidak ada hero image stok.

### 8.2 Index Project (`/projects/`)

Halaman terpenting kedua. Menampilkan seluruh 35 project sebagai **tabel padat**, bukan grid kartu.

- Kolom: `ID` · `Tahun` · `Nama` · `Peran` · `Domain` · `Stack utama`
- Sticky filter bar: multi-select stack, role, domain, range tahun
- Pencarian teks instan (nama + tagline + stack)
- Counter live: "Showing 12 of 35"
- URL menyimpan state filter (`?stack=codeigniter&role=dev-lead`) supaya bisa dibagikan
- Hover pada baris → thumbnail muncul (lihat §9.5)
- Mobile: tabel berubah jadi baris ringkas dua tingkat, filter jadi bottom sheet

### 8.3 Detail Project

Tiga template sesuai `tier`. Elemen umum:

- Breadcrumb + tombol kembali yang mempertahankan filter sebelumnya
- Header: ID, tahun, judul, tagline, peran sebagai badge
- Sidebar sticky (desktop ≥1024px): klien, durasi, ukuran tim, stack, arsitektur, link live/repo
- Screenshot dalam `BrowserFrame` — **selalu dengan caption**
- Grid metrik jika ada
- Navigasi prev/next project di bawah

### 8.4 Tentang

Ringkas. Foto profil, 2–3 paragraf naratif (bukan daftar), timeline pengalaman kerja, sertifikasi jika ada, link CV PDF.

### 8.5 Kontak

Email (`mailto:`), LinkedIn, GitHub, WhatsApp. Tanpa form — form statis butuh layanan pihak ketiga dan menambah titik kegagalan. Email dilindungi obfuscation JS sederhana terhadap scraper.

---

## 9. Design System

### 9.1 Arah visual

Bukan "dark mode dengan aksen neon" generik. Referensinya adalah **dokumentasi teknis dan manifest sistem**: padat, terstruktur, rapi, tanpa dekorasi. Kepribadian datang dari tipografi kondensat berat — melanjutkan identitas yang sudah ada di PPT — bukan dari efek visual.

### 9.2 Token warna

```css
:root {
  --ink:        #101318;  /* base — charcoal kebiruan, bukan hitam murni */
  --ink-raised: #171B22;  /* surface: kartu, sidebar */
  --ink-sunken: #0B0D11;  /* container screenshot */
  --rule:       #262C36;  /* border, divider */
  --rule-hover: #3A424F;

  --text:       #E9EBEF;
  --text-muted: #8E96A3;
  --text-faint: #5B6371;  /* metadata, ID, tahun */

  --amber:      #F2C14E;  /* aksen tunggal — diambil dari palet PPT */
  --amber-dim:  #8A6D22;  /* border/state amber redup */
  --amber-wash: rgba(242, 193, 78, 0.08);
}
```

Satu aksen saja. Amber dipakai hanya untuk: link aktif, state hover baris index, indikator filter aktif, dan angka metrik. Tidak untuk heading, tidak untuk dekorasi.

### 9.3 Tipografi

| Peran | Typeface | Penggunaan |
|---|---|---|
| Display | **Anton** (atau Archivo Condensed 800) | Hero, judul halaman, nama project. Uppercase, `letter-spacing: -0.01em`. Melanjutkan identitas PPT. |
| Body | **Inter** | Paragraf, deskripsi. Weight 400/500. |
| Utility | **IBM Plex Mono** | ID project, tahun, stack badge, metadata tabel, angka metrik |

Mono pada metadata adalah yang membuat situs terasa "engineering" — bukan warna neon.

```css
--step--1: clamp(0.83rem, 0.8rem + 0.15vw, 0.9rem);
--step-0:  clamp(1rem, 0.95rem + 0.25vw, 1.13rem);
--step-1:  clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
--step-2:  clamp(1.6rem, 1.4rem + 1vw, 2.25rem);
--step-3:  clamp(2rem, 1.6rem + 2vw, 3.4rem);
--step-4:  clamp(2.6rem, 1.8rem + 4vw, 5.5rem);   /* hero display */
```

Body line-height 1.65, display 0.95. Lebar baca maksimum 68ch.

### 9.4 Spacing & layout

Skala 4px: `4 8 12 16 24 32 48 64 96 128`.
Grid 12 kolom, max-width konten 1240px, gutter 24px (mobile 16px).
Border radius: 4px untuk elemen kecil, 8px untuk kartu. Tidak ada radius besar — bertentangan dengan karakter teknis.

### 9.5 Elemen signature — The Index

Satu hal yang membuat situs ini diingat.

35 project ditampilkan sebagai baris tabel monospace bernomor stabil (`P-001`…`P-035`), padat dan sejajar seperti output sistem. **Saat kursor menyentuh sebuah baris**, screenshot project muncul sebagai thumbnail melayang yang mengikuti posisi vertikal kursor, dan baris tersebut mendapat garis aksen amber di sisi kiri.

Kenapa ini tepat, bukan sekadar gimmick:
- Menyampaikan volume secara jujur — 35 baris terlihat sekaligus, sesuatu yang mustahil di grid kartu
- Penomoran mengencode informasi nyata (indeks arsip), bukan dekorasi
- Memindahkan screenshot ke lapisan hover membuat halaman index tetap ringan dan cepat dipindai
- Selaras dengan peran backend: struktur dulu, tampilan menyusul

Di mobile, hover diganti: baris di-tap untuk expand inline menampilkan thumbnail + ringkasan sebelum masuk ke halaman detail.

### 9.6 Screenshot di atas latar gelap

Semua screenshot project berlatar terang. Menempelkannya langsung ke background gelap akan menyilaukan dan terlihat murahan.

Aturan `BrowserFrame`:
- Container `--ink-sunken` dengan padding 16px
- Border 1px `--rule`, radius 8px
- Bar browser palsu di atas (tiga titik + garis URL) — konsisten untuk semua 35 screenshot dengan rasio berbeda
- `box-shadow: 0 24px 48px -12px rgba(0,0,0,0.6)` untuk memisahkan dari background
- Screenshot sendiri diberi `border-radius: 0 0 4px 4px` dan brightness 0.96 agar tidak terlalu menyala

---

## 10. Spesifikasi Motion

Prinsip: **satu momen terkoordinasi lebih berkesan daripada banyak efek tersebar.** Animasi harus melayani pemindaian informasi, bukan menghias.

| Momen | Perilaku | Durasi / easing |
|---|---|---|
| Page load (beranda) | Hero fade+rise, lalu baris index stagger 40ms per baris seperti output yang mengalir | 600ms / `cubic-bezier(.16,1,.3,1)` |
| Scroll reveal | Section fade+rise 16px, threshold 15%, sekali saja | 500ms |
| Hover baris index | Garis aksen kiri melebar 0→3px, thumbnail fade+scale 0.96→1 | 180ms |
| Filter berubah | Baris keluar fade 120ms, masuk stagger 25ms; counter angka beranimasi | 300ms total |
| Navigasi antar halaman | View Transitions API (`<ClientRouter />`) — judul project morph ke header halaman detail | 400ms |
| Hover tombol/link | Underline tumbuh dari kiri, warna ke amber | 150ms |

### Batasan wajib

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Hanya animasikan `transform` dan `opacity`. Tidak ada parallax. Tidak ada animasi yang menunda pembacaan konten lebih dari 600ms. Tidak ada efek kursor kustom. Tidak ada text scramble.

---

## 11. Responsif

| Breakpoint | Perilaku |
|---|---|
| < 480px | Satu kolom. Index jadi baris dua tingkat. Filter jadi bottom sheet. Sidebar detail pindah ke atas sebagai list. Hero turun ke `--step-3`. |
| 480–768px | Kartu featured satu kolom penuh |
| 768–1024px | Featured dua kolom, index tampil kolom penuh tanpa kolom Domain |
| 1024–1440px | Layout penuh, sidebar sticky aktif, hover thumbnail aktif |
| > 1440px | Konten terkunci 1240px, margin tumbuh |

Target sentuh minimum 44×44px. Uji pada 320px (iPhone SE) sebagai batas bawah.

---

## 12. Performa

| Aset | Aturan |
|---|---|
| Gambar | AVIF + WebP fallback, `loading="lazy"` kecuali cover hero, `width`/`height` wajib |
| Ukuran screenshot | Maks 1600px lebar, target < 150 KB per gambar setelah konversi |
| Font | Self-host `.woff2`, `font-display: swap`, subset latin, preload display face saja |
| JS | Hanya filter + index interaction, target < 15 KB gzipped |
| CSS | Critical inline, sisanya satu file < 20 KB |
| Thumbnail index | Versi 480px terpisah, di-preload saat idle |

Budget total halaman utama: **500 KB**. Jika terlampaui, kurangi jumlah screenshot, bukan kualitas.

---

## 13. Aksesibilitas

Target WCAG 2.1 AA.

- Kontras teks utama pada `--ink`: ≥ 7:1; teks muted ≥ 4.5:1
- Focus ring terlihat: `outline: 2px solid var(--amber); outline-offset: 2px`
- Index harus dapat dinavigasi keyboard; thumbnail hover juga muncul saat focus
- Semua gambar punya `alt` deskriptif — caption ≠ alt
- Filter menggunakan elemen form native, bukan div dengan handler
- Landmark semantik: `<header> <nav> <main> <article> <footer>`
- Skip-to-content link
- Uji dengan keyboard saja dan dengan screen reader pada 1 halaman tiap tier

---

## 14. SEO & Metadata

- `<title>` unik per halaman: `{Project} — {{NAMA}}`
- Meta description dari field `tagline`
- Open Graph image: generate otomatis per project dari cover + judul (Astro OG image)
- JSON-LD `Person` di beranda, `CreativeWork` di tiap halaman project
- `sitemap.xml` via `@astrojs/sitemap`
- `robots.txt` mengizinkan semua
- Slug URL stabil, tidak boleh berubah setelah publish
- Canonical URL di semua halaman

---

## 15. Pipeline Ekstraksi dari `My-Portfolio.pptx`

### 15.1 Source of truth

File **`My-Portfolio.pptx`** berada di root folder project dan merupakan satu-satunya sumber konten awal. Seluruh isi `src/content/projects/` — file markdown maupun gambar — **digenerate dari file ini**, tidak ada yang dibuat manual pada tahap awal.

```
{{REPO_ROOT}}/
├── My-Portfolio.pptx          ← SOURCE, jangan diubah
├── scripts/
│   ├── extract_pptx.py        ← generator utama
│   ├── stack_dictionary.json  ← kamus normalisasi (bisa diedit manual)
│   └── requirements.txt
├── src/content/projects/       ← OUTPUT, hasil generate
└── .extraction-report.md       ← OUTPUT, laporan QA
```

**Aturan penting:** `My-Portfolio.pptx` bersifat read-only. Setelah ekstraksi selesai dan konten mulai diedit manual, PPT tidak lagi jadi source of truth — markdown yang menang. Skrip punya guard agar tidak menimpa file yang sudah diedit (§15.5).

### 15.2 Menjalankan

```bash
pip install -r scripts/requirements.txt
python scripts/extract_pptx.py                  # generate semua
python scripts/extract_pptx.py --dry-run        # preview tanpa menulis file
python scripts/extract_pptx.py --slide 12       # ulang satu slide saja
python scripts/extract_pptx.py --force          # timpa file yang sudah diedit
```

`scripts/requirements.txt`:
```
python-pptx>=1.0.2
Pillow>=10.4.0
python-slugify>=8.0.4
```

### 15.3 Yang digenerate

Sekali jalan, skrip menghasilkan **semua** hal berikut:

| Output | Path | Keterangan |
|---|---|---|
| Markdown per project | `src/content/projects/{slug}.md` | Frontmatter terisi + body dengan heading `{{TODO}}` |
| Screenshot utama | `src/content/projects/images/{slug}/cover.png` | Shape gambar terbesar di slide |
| Screenshot tambahan | `src/content/projects/images/{slug}/shot-{n}.png` | Gambar besar lain di slide yang sama |
| Thumbnail index | `src/content/projects/images/{slug}/thumb.webp` | 480px lebar, untuk hover The Index |
| Laporan QA | `.extraction-report.md` | Daftar slide yang perlu review manual |
| Slide mentah | `.extraction-cache/slide-{n}.png` | Render slide utuh, untuk verifikasi (gitignored) |

### 15.4 Algoritma

**Tahap 1 — Klasifikasi slide.**
Tidak semua slide adalah project. Slide diklasifikasikan sebagai:
- `project` — punya ≥1 gambar besar + teks judul
- `contact` — cocok pola email/telepon/LinkedIn → diekstrak ke `src/data/contact.json`
- `cover` / `divider` — teks saja tanpa gambar besar, atau < 3 shape → dilewati, dicatat di laporan

**Tahap 2 — Pemilihan gambar.**
`python-pptx` sudah menangani relationship slide→media, jadi `shape.image` selalu memberi gambar yang benar untuk slide tersebut.

```python
PICTURE = 13
slide_area = prs.slide_width * prs.slide_height

pics = [s for s in slide.shapes if s.shape_type == PICTURE]
pics = [p for p in pics if (p.width * p.height) / slide_area > 0.05]  # buang dekorasi
pics.sort(key=lambda p: p.width * p.height, reverse=True)
```

Threshold 5% luas slide membuang titik-titik dekoratif, garis, dan logo kecil yang ada di tiap slide. Gambar terbesar jadi `cover`, sisanya jadi `shot-{n}`.

**Tahap 3 — Ekstraksi teks berbasis ukuran font.**
Kunci akurasinya adalah membaca `run.font.size`, bukan urutan shape.

```python
runs = []
for shape in slide.shapes:
    if not shape.has_text_frame: continue
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if not run.text.strip(): continue
            size = run.font.size.pt if run.font.size else inherited_size(shape, para)
            runs.append({'text': run.text.strip(), 'size': size,
                         'top': shape.top, 'left': shape.left})

runs.sort(key=lambda r: -r['size'])
```

Aturan pemetaan:

| Target | Aturan |
|---|---|
| `title` | Run dengan font terbesar. Jika ada beberapa berukuran sama, ambil yang paling atas. |
| `roles` | Regex `(?i)\b(dev lead\|team lead\|backend\|front[\s-]?end\|full[\s-]?stack\|system analyst)\b` — bisa lebih dari satu |
| `stack` | Teks dalam kurung `\(([^)]+)\)`, dipecah dengan `[,/&+]` atau spasi, lalu dinormalisasi |
| `year` | Regex `\b(20\d{2})\b` di teks manapun; jika tidak ada → `{{TODO}}` |
| `client` | Baris yang diawali `Client:`, `PT `, `CV `, `Yayasan `, `Dinas ` |
| `teamSize` | Regex `(\d+)\s*(orang\|people\|dev\|member)` |
| `tagline` | Run terpanjang yang bukan title/role/stack, dipotong 90 karakter |

**Tahap 4 — Normalisasi stack.**
`scripts/stack_dictionary.json` memetakan varian penulisan ke bentuk kanonik. Tanpa ini, filter di The Index akan pecah jadi puluhan entri duplikat.

```json
{
  "codeigniter 3": "CodeIgniter 3",
  "codeigniter3":  "CodeIgniter 3",
  "ci3":           "CodeIgniter 3",
  "ci 3":          "CodeIgniter 3",
  "hmvc":          "HMVC",
  "laravel 8":     "Laravel",
  "mysql":         "MySQL",
  "postgres":      "PostgreSQL",
  "bootstrap 4":   "Bootstrap",
  "js":            "JavaScript"
}
```

Token yang tidak ada di kamus tetap dipakai apa adanya, tapi **dicatat di laporan QA** sebagai `UNMAPPED` supaya kamu bisa menambahkannya ke kamus lalu jalankan ulang.

**Tahap 5 — Slug & ID.**
- `slug` = `slugify(title)`. Jika bentrok, tambah suffix `-2`.
- `id` = `P-{nomor urut slide project, 3 digit}` — **stabil selamanya**, tidak berubah walau urutan slide diubah nanti.
- Mapping `slide → id → slug` disimpan di `.extraction-cache/manifest.json` agar `--slide N` bisa regenerate tanpa menggeser ID lain.

**Tahap 6 — Pemrosesan gambar.**
```python
img = Image.open(io.BytesIO(shape.image.blob))
if img.mode in ('RGBA', 'P'): img = img.convert('RGB')
if img.width > 1600:
    img = img.resize((1600, int(img.height * 1600 / img.width)), Image.LANCZOS)
img.save(cover_path, 'PNG', optimize=True)

thumb = img.copy(); thumb.thumbnail((480, 480), Image.LANCZOS)
thumb.save(thumb_path, 'WEBP', quality=78)
```

Konversi AVIF/WebP final tetap ditangani `astro:assets` saat build. Skrip hanya menormalkan ukuran agar tidak ada PNG 4000px masuk ke repo.

**Tahap 7 — Tulis markdown.**
Semua project default `tier: compact`, `draft: false`. Field yang tidak terdeteksi ditulis eksplisit sebagai `{{TODO}}` — bukan dihapus — supaya mudah dicari dengan `grep -r "{{TODO}}" src/content/`.

### 15.5 Guard anti-timpa

Setiap file hasil generate diberi penanda di frontmatter:

```yaml
_generated: true
_sourceSlide: 7
_extractedAt: 2026-08-18
```

Saat dijalankan ulang, skrip **melewati** file yang `_generated`-nya sudah dihapus atau di-set `false` — artinya kamu sudah mengeditnya secara manual. Ini yang membuat pipeline aman dijalankan berkali-kali sambil kamu menulis case study.

Setelah sebuah project selesai kamu tulis, hapus tiga field `_*` tersebut. Itu sinyal "file ini milik saya sekarang".

### 15.6 Laporan QA

`.extraction-report.md` wajib dibaca sebelum lanjut ke fase berikutnya. Isinya:

```markdown
# Extraction Report — 18 Aug 2026
Source: My-Portfolio.pptx (42 slides)

## Ringkasan
- 35 slide → project
- 1 slide  → contact (slide 42)
- 6 slide  → dilewati (cover, divider, thank-you)

## Perlu review manual
| Slide | ID | Project | Isu |
|---|---|---|---|
| 12 | P-009 | {{TODO}} | Judul tidak terdeteksi — tidak ada run dominan |
| 18 | P-014 | Sistem Antrian | 3 gambar besar — pastikan cover benar |
| 23 | P-018 | E-Katalog | Tahun tidak ditemukan |

## Stack tidak dikenal (tambahkan ke stack_dictionary.json)
- "Codeigniter4" (slide 20)
- "Vue Js" (slide 27)

## Slide tanpa gambar
- Slide 31 — hanya teks, cek manual
```

### 15.7 Ekspektasi realistis

Akurasi ~80–90%. Hasil ekstraksi adalah **draft**, bukan final.

Yang hampir selalu perlu koreksi manual:
- Judul pada slide dengan layout berbeda dari mayoritas
- Slide yang punya lebih dari satu screenshot besar — urutan cover bisa salah
- Stack yang ditulis tanpa kurung
- Tahun, ukuran tim, dan metrik — mayoritas memang tidak ada di PPT

**Verifikasi wajib setelah fase 0:** buka semua 35 file, cocokkan `cover.png` dengan nama project. Gambar tertukar antar project adalah kesalahan paling merusak kredibilitas dan paling sulit terdeteksi belakangan. Render slide di `.extraction-cache/` ada khusus untuk keperluan ini.

Skrip **tetap disimpan di repo** (tidak dibuang), karena berguna jika kamu memperbarui PPT atau menemukan slide yang perlu diekstrak ulang.

---

## 16. Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push: { branches: [main] }
  workflow_dispatch:
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: pages, cancel-in-progress: true }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: withastro/action@v3
  deploy:
    needs: build
    environment: { name: github-pages, url: '${{ steps.deployment.outputs.page_url }}' }
    runs-on: ubuntu-latest
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Repository Settings → Pages → Source: **GitHub Actions**.
Custom domain opsional: tambah `public/CNAME` berisi domain, lalu set DNS `CNAME` ke `{{USERNAME}}.github.io`.

---

## 17. Fase Pengerjaan

| Fase | Isi | Selesai bila |
|---|---|---|
| **0 — Ekstraksi** | Tulis `scripts/extract_pptx.py`, jalankan terhadap `My-Portfolio.pptx`, generate seluruh markdown + gambar + thumbnail | `.extraction-report.md` bersih, 35 file ada, semua cover diverifikasi cocok dengan nama project |
| **1 — Fondasi** | Setup Astro, token CSS, font, layout Base, deploy pipeline | Halaman kosong live di GitHub Pages |
| **2 — Index** | Content collection, komponen IndexRow, halaman `/projects/`, filter | 35 project tampil, filter berfungsi, state di URL |
| **3 — Detail** | Tiga template tier, BrowserFrame, sidebar, navigasi prev/next | 35 halaman detail dapat diakses |
| **4 — Beranda & statis** | Hero, featured, capability, about, contact | Semua halaman lengkap |
| **5 — Motion** | Page-load sequence, scroll reveal, hover index, view transitions | Reduced-motion diuji |
| **6 — Konten** | Tulis 6–8 case study featured + 12 standard | Tidak ada `{{TODO}}` tersisa |
| **7 — Polish** | Audit Lighthouse, aksesibilitas keyboard, OG image, SEO, uji 320px | Semua target §3 tercapai |

Fase 1–5 adalah pekerjaan teknis dan bisa cepat. **Fase 6 adalah bottleneck sebenarnya** dan bergantung sepenuhnya pada penulisan — alokasikan waktu paling besar di sini.

---

## 18. Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Halaman tier compact terlihat kosong | Kredibilitas turun | Template compact dirancang padat sejak awal; uji dengan konten paling pendek |
| 35 case study tidak pernah selesai ditulis | Situs stagnan setengah jadi | Semua default `compact`; naikkan bertahap. Situs tetap layak publish sejak hari pertama |
| Screenshot kualitas rendah dari PPT | Terlihat tidak profesional | Ambil ulang screenshot dari situs live untuk project yang masih aktif |
| Nama klien / data sensitif | Masalah NDA | Field `client` opsional; boleh diisi deskripsi generik ("national Islamic foundation") |
| Base path GitHub Pages salah | Semua gambar broken | Uji `npm run build && npm run preview` sebelum push pertama |
| Ekstraksi salah map gambar | Screenshot tertukar antar project | Render slide utuh disimpan di `.extraction-cache/`; review manual 35 gambar setelah fase 0 — wajib, tidak bisa dilewati |
| Skrip ditimpa ulang setelah konten diedit | Kehilangan tulisan case study | Guard `_generated` (§15.5) — file yang sudah diedit dilewati kecuali `--force` |
| Slide non-project ikut terekstrak | File markdown sampah | Klasifikasi slide di tahap 1; slide yang dilewati dicatat di laporan QA |

---

## 19. Yang Perlu Disiapkan

Sebelum implementasi dimulai:

- [x] ~~File PPT sumber~~ — `My-Portfolio.pptx` sudah ada di root project
- [ ] Nama lengkap, tagline profesional, foto profil
- [ ] Email, LinkedIn, GitHub, WhatsApp
- [ ] Username GitHub + nama repo yang diinginkan
- [ ] Daftar 6–8 project yang akan jadi `featured`
- [ ] Untuk tiap project featured: ukuran tim, durasi, metrik dampak (angka nyata)
- [ ] Konfirmasi project mana yang terikat NDA
- [ ] CV PDF terbaru (opsional, untuk link di halaman About)
- [ ] Custom domain (opsional)

---

## Lampiran — Keputusan yang Sengaja Diambil

**Kenapa tabel, bukan grid kartu?**
Grid kartu adalah default portfolio dan memaksa scroll panjang untuk 35 item. Tabel menampilkan seluruh arsip sekaligus, dapat dipindai, dan mendukung filter secara natural. Untuk seseorang dengan 35 project, volume itu sendiri adalah argumen — dan hanya tabel yang bisa menunjukkannya.

**Kenapa satu aksen warna saja?**
Palet gelap dengan banyak warna cepat terlihat seperti template dashboard. Amber tunggal — diambil dari PPT yang sudah ada — menjaga kontinuitas identitas dan memaksa hierarki dibangun lewat tipografi dan spasi, yang lebih tahan lama.

**Kenapa tidak ada light mode toggle?**
Menambah beban maintenance dua kali lipat untuk 35 halaman dengan screenshot berlatar terang yang butuh perlakuan berbeda per tema. Satu tema yang dieksekusi rapi lebih baik daripada dua tema setengah matang.

**Kenapa bahasa Inggris?**
Membuka peluang remote internasional tanpa mengorbankan audiens lokal, yang sudah terbiasa dengan portfolio berbahasa Inggris.