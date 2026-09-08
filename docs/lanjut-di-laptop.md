# Melanjutkan Project Ini di Laptop

Semua pekerjaan ada di GitHub, jadi laptop tinggal mengambilnya. Tidak ada database,
tidak ada server, tidak ada build step — dasbor XAU hanya satu file HTML.

- Repo: `https://github.com/bryansum0909/monitor-berita-sulut`
- Branch kerja saat ini: **`claude/xau-fokus-o6pzbx`** (dasbor XAU + deploy)
- Branch utama: `main` (masih berisi bot berita saja)

---

## 1. Yang perlu dipasang

| Alat | Untuk apa | Wajib? |
|---|---|---|
| [Git](https://git-scm.com/downloads) | mengambil dan mengirim perubahan | ya |
| Browser | membuka dasbor | ya |
| [Python 3.11+](https://www.python.org/downloads/) | menjalankan bot berita | hanya kalau mau menjalankan botnya |
| [Node.js](https://nodejs.org) | prasyarat Claude Code | hanya kalau mau lanjut pakai Claude |

Saat memasang Git di Windows, biarkan pilihan default — yang penting **Git Bash** ikut
terpasang, karena beberapa perintah di bawah lebih enak dijalankan di situ.

---

## 2. Ambil project ke laptop (sekali saja)

Buka **Git Bash** (atau PowerShell) di folder mana pun, lalu:

```bash
git clone https://github.com/bryansum0909/monitor-berita-sulut.git
cd monitor-berita-sulut
git checkout claude/xau-fokus-o6pzbx
```

Perintah `checkout` otomatis mengikuti branch yang sudah ada di GitHub. Cek dengan:

```bash
git log --oneline -3
```

Kalau muncul commit `feat: jalur deploy dasbor XAU ke VPS`, berarti sudah benar.

Sebelum memasukkan nama dan email untuk commit (sekali saja per laptop):

```bash
git config --global user.name "Bryan Sumilat"
git config --global user.email "bryansumilat09@gmail.com"
```

---

## 3. Buka dasbornya

Tidak perlu server. Klik dua kali `dashboard/xau-pipeline.html`, atau:

```bash
# Windows
start dashboard/xau-pipeline.html
# macOS
open dashboard/xau-pipeline.html
```

Setelah mengedit filenya, cukup **refresh browser** — tidak ada yang perlu dikompilasi.

> Halaman memuat font dari Google Fonts. Kalau laptop offline, hurufnya jatuh ke font
> sistem; isinya tetap jalan penuh karena semua logika ada di dalam file itu.

---

## 4. Menjalankan bot berita (opsional)

```bash
pip install -r requirements.txt
```

PowerShell:

```powershell
$env:TELEGRAM_BOT_TOKEN = "token-dari-botfather"
$env:TELEGRAM_CHAT_ID   = "chat-id-anda"
python monitor_berita.py
```

Git Bash / macOS / Linux:

```bash
TELEGRAM_BOT_TOKEN=xxx TELEGRAM_CHAT_ID=yyy python monitor_berita.py
```

Bot yang di GitHub Actions tetap jalan sendiri tiap 5 menit — menjalankan lokal hanya
untuk mengetes perubahan.

---

## 5. Menyimpan dan mengirim perubahan

```bash
git add -A
git commit -m "penjelasan singkat apa yang diubah"
git push origin claude/xau-fokus-o6pzbx
```

Sebelum mulai kerja, **selalu tarik dulu** — supaya tidak bentrok kalau ada perubahan
yang dikerjakan dari sesi cloud:

```bash
git pull origin claude/xau-fokus-o6pzbx
```

Kalau muncul konflik, jangan panik: `git status` menunjukkan file mana yang bentrok,
buka filenya, hapus penanda `<<<<<<<` / `=======` / `>>>>>>>`, lalu `git add` dan
`git commit`.

---

## 6. Menggabungkan ke `main`

Kalau dasbor sudah dianggap beres:

**Lewat GitHub (disarankan, ada layar diff):** buka repo → tombol **Compare & pull
request** pada branch `claude/xau-fokus-o6pzbx` → **Create pull request** → **Merge**.

**Lewat terminal:**

```bash
git checkout main
git pull origin main
git merge claude/xau-fokus-o6pzbx
git push origin main
```

---

## 7. Lanjut memakai Claude Code di laptop

```bash
npm install -g @anthropic-ai/claude-code
cd monitor-berita-sulut
claude
```

Ada juga aplikasi desktop dan ekstensi VS Code / JetBrains; cara pasang terbaru ada di
`https://code.claude.com/docs`.

Yang perlu diingat: **sesi baru tidak membawa ingatan sesi lama.** Jadi pembuka yang
paling efektif kira-kira begini:

> "Repo ini punya dasbor XAU di `dashboard/xau-pipeline.html` (branch
> `claude/xau-fokus-o6pzbx`). Baca file itu dan `docs/xauusd-trading-plan.md` dulu,
> lalu saya mau [permintaan Anda]."

Beberapa perintah yang sering berguna: `/artifacts` (membuka kembali dasbor yang sudah
dipublish), `/init` (membuat CLAUDE.md berisi catatan repo), `/code-review` (memeriksa
perubahan sebelum push).

---

## 8. Kalau ingin dasbor tampil di VPS

Ikuti `deploy/README.md`. Ringkasnya: dari laptop cukup

```bash
./deploy/deploy-vps.sh --host IP_VPS --user root
```

atau isi tiga secret di GitHub supaya deploy jalan otomatis tiap kali `dashboard/`
berubah.
