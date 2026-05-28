# Bot Monitor Berita Viral Manado/Sulut → Telegram

Bot otomatis yang scan berita Manado / Sulawesi Utara tiap **5 menit** dan kirim ke Telegram Bryan. Gratis, jalan 24/7 di **GitHub Actions** (tidak butuh server / VPS).

## Apa yang di-monitor

- **Google News RSS** dengan keyword: Manado, Sulawesi Utara, viral Manado, viral Sulut, Minahasa, Bitung, Tomohon, Kawanua (paling reliable — agregator dari ratusan portal).
- **Portal nasional**: Antara, Detik, Liputan6, CNN Indonesia, CNBC, Tempo, Suara, JawaPos — difilter otomatis untuk berita yang mengandung kata Sulut.
- **Portal lokal Sulut**: Berita Manado, Manado Post (dicoba via `/feed/`; jika tidak aktif akan di-skip secara otomatis).

Berita yang mengandung kata "viral", "heboh", "trending", "geger", "netizen" akan ditandai 🔥 **VIRAL** dan diprioritaskan di urutan atas.

## ⚠️ Soal Facebook Group & Twitter/X

Saya jujur: **Facebook Group dan Twitter/X tidak bisa di-scrape otomatis 24/7 dengan cara yang gratis dan stabil**:

- **Facebook**: melarang scraping, akun bot akan di-banned dalam hitungan jam. Untuk FB **Page publik** (bukan Group), Bryan bisa pakai jasa **fetchrss.com** atau **rss.app** (free tier) untuk convert ke RSS, lalu tempel URL-nya ke `config.json` di bagian `custom_rss_feeds`.
- **Twitter/X**: API resmi sekarang minimum $100/bulan. Scraper gratis (snscrape) sudah mati sejak 2023.

Berita "Lambe Kawanua"-style biasanya nge-share berita yang sudah ada di portal — jadi monitor Google News + portal lokal **sudah meng-cover sebagian besar berita viral** yang nantinya muncul di FB Group.

---

## Setup (sekali saja, ~15 menit)

### Step 1 — Bikin Bot Telegram

1. Buka Telegram, cari **@BotFather**.
2. Ketik `/newbot` → ikuti instruksi (kasih nama bot, mis. `BeritaSulutBot`).
3. BotFather akan kasih **TOKEN** seperti: `7891234567:AAEabcdefGHIJKLmnopQRSTuv-XYZ1234567`.
4. **Simpan token ini** — anggap seperti password.

### Step 2 — Dapatkan Chat ID

**Opsi A — Chat pribadi (paling mudah):**

1. Cari bot yang baru dibuat di Telegram (sesuai username yang diberikan ke BotFather), klik **Start**.
2. Kirim pesan apa saja, misal `halo`.
3. Buka di browser (ganti `<TOKEN>` dengan token Bryan):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. Cari di hasilnya `"chat":{"id": 123456789, ...}` — angka itu **chat_id** Bryan.

**Opsi B — Channel Telegram (kalau mau publish ke channel):**

1. Buat channel baru di Telegram.
2. Tambahkan bot sebagai **Admin** channel (kasih permission Post Messages).
3. Kirim 1 pesan apa saja di channel.
4. Sama seperti di atas, panggil `getUpdates`. Chat ID channel biasanya angka negatif seperti `-1001234567890`.

### Step 3 — Pilih cara deploy

#### Cara A (Recommended): GitHub Actions — gratis, jalan 24/7

1. **Bikin akun GitHub** di [github.com](https://github.com) (kalau belum punya).
2. Buat **repository baru** (bisa pilih Private). Namanya bebas, mis. `monitor-berita-sulut`.
3. Upload semua file di folder ini ke repo tersebut. Cara paling mudah:
   - Di halaman repo, klik **"Add file" → "Upload files"**.
   - Drag semua file dari folder `Data News sulut` ke browser.
   - Klik **Commit changes**.
4. Set **Secrets** (tempat aman simpan token):
   - Buka repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
   - Tambah 2 secret:
     - Name: `TELEGRAM_BOT_TOKEN` → Value: token dari BotFather
     - Name: `TELEGRAM_CHAT_ID` → Value: chat ID dari Step 2
5. **Aktifkan Actions**: buka tab **Actions** di repo → klik tombol **"I understand my workflows, go ahead and enable them"**.
6. Tes manual: tab **Actions** → klik **"Monitor Berita Sulut"** → tombol **"Run workflow"** → tunggu ~1 menit → cek Telegram. 🎉
7. Setelah itu, bot akan otomatis jalan **tiap 5 menit**, 24/7, selamanya gratis.

> **Catatan**: GitHub Actions free tier untuk repo public = tak terbatas. Untuk repo private = 2000 menit/bulan. Script ini selesai dalam ~30 detik per run × 12 run/jam × 24 jam × 30 hari ≈ 4.300 menit. **Jadi sebaiknya repo dibuat PUBLIC** (atau toleransi 1 run per 10 menit kalau private).

#### Cara B: Jalan lokal di komputer Bryan

Bot hanya jalan saat komputer hidup & script dijalankan. Cocok untuk testing.

```bash
# 1. Install Python 3.10+ (https://python.org)
# 2. Buka terminal di folder ini
pip install -r requirements.txt

# 3. Set environment variable (Windows PowerShell)
$env:TELEGRAM_BOT_TOKEN = "token-dari-botfather"
$env:TELEGRAM_CHAT_ID = "chat-id-anda"

# 4. Test sekali
python monitor_berita.py

# 5. Untuk otomatis tiap 5 menit, pakai Task Scheduler Windows
#    atau buka terminal dan jalankan:
while ($true) { python monitor_berita.py; Start-Sleep 300 }
```

Atau di Linux/Mac (cron):
```bash
*/5 * * * * cd /path/to/folder && TELEGRAM_BOT_TOKEN=xxx TELEGRAM_CHAT_ID=xxx python3 monitor_berita.py
```

---

## Customisasi

Edit `config.json` untuk:

- **Tambah/kurangi keyword** filter (`keywords`).
- **Tambah query Google News** baru (`google_news_queries`) — mis. `"banjir Manado"`, `"polisi Sulut"`.
- **Tambah feed RSS sendiri** di `custom_rss_feeds` — termasuk FB Page yang sudah Bryan convert via fetchrss.com.
- **Ubah marker viral** di `viral_markers`.

Edit environment variable di workflow (`.github/workflows/monitor.yml`):

- `LOOKBACK_HOURS`: berapa jam ke belakang berita yang dipertimbangkan (default 6).
- `MAX_NEWS_PER_RUN`: batas berita per run agar tidak spam (default 15).

---

## Troubleshooting

**Bot tidak kirim apa-apa?**
- Cek log di tab **Actions** → klik run terakhir → expand step "Jalankan monitor". Akan kelihatan berapa berita ditemukan.
- Pastikan chat ID benar (kadang orang salin token sebagai chat ID).
- Untuk channel, pastikan bot sudah dipromote jadi Admin.

**Banyak duplikat?**
- Pastikan workflow ada step "Commit state.json" — itu yang simpan history berita yang sudah dikirim.

**Mau lebih cepat dari 5 menit?**
- GitHub Actions minimum cron adalah 5 menit (kadang slip jadi ~10 menit saat jam sibuk). Untuk real-time sub-menit butuh VPS sendiri (~$5/bulan di DigitalOcean/Hetzner).

---

## File di repo ini

| File | Fungsi |
|------|--------|
| `monitor_berita.py` | Script utama — fetch RSS, filter, kirim Telegram |
| `config.json` | Daftar keyword, query Google News, RSS feeds |
| `requirements.txt` | Dependensi Python (feedparser, requests) |
| `state.json` | Riwayat berita yang sudah dikirim (auto-update) |
| `.github/workflows/monitor.yml` | GitHub Actions — cron 5 menit |
| `.gitignore` | File yang di-skip git |
| `README.md` | Dokumen ini |
