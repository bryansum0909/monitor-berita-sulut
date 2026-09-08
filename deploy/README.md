# Hosting Dasbor XAU di VPS

Dasbor ini satu file HTML mandiri (`dashboard/xau-pipeline.html`) — tidak ada build step,
tidak ada database, tidak ada backend. "Hosting" di sini artinya menaruh satu file di VPS
dan menyuruh nginx menyajikannya.

Ada tiga cara, dari yang paling otomatis ke paling manual.

---

## Cara 1 — Otomatis lewat GitHub Actions (rekomendasi)

Setiap push yang menyentuh `dashboard/`, file langsung terkirim ke VPS. Tidak ada kunci SSH
yang disimpan di komputer manapun selain GitHub Secrets.

### Langkah 1 — Buat kunci SSH khusus deploy (di komputer Bryan)

```bash
ssh-keygen -t ed25519 -C "deploy-dasbor-xau" -f ~/.ssh/xau_deploy -N ""
```

Hasilnya dua file: `~/.ssh/xau_deploy` (privat) dan `~/.ssh/xau_deploy.pub` (publik).

### Langkah 2 — Pasang kunci publik di VPS

```bash
ssh-copy-id -i ~/.ssh/xau_deploy.pub USER@IP_VPS
# atau manual:
cat ~/.ssh/xau_deploy.pub | ssh USER@IP_VPS "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### Langkah 3 — Ambil sidik jari host (biar tidak trust-on-first-use)

```bash
ssh-keyscan -H IP_VPS
```

Salin seluruh keluarannya untuk dipakai di langkah berikut.

### Langkah 4 — Isi Secrets di GitHub

Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| Secret | Isi | Wajib |
|---|---|---|
| `VPS_HOST` | IP atau domain VPS | ya |
| `VPS_USER` | user SSH, mis. `root` atau `deploy` | ya |
| `VPS_SSH_KEY` | **isi file** `~/.ssh/xau_deploy` (kunci privat, termasuk baris BEGIN/END) | ya |
| `VPS_KNOWN_HOSTS` | keluaran `ssh-keyscan` dari langkah 3 | sangat disarankan |
| `VPS_PATH` | folder tujuan, default `/var/www/xau` | tidak |
| `VPS_PORT` | port SSH kalau bukan 22 | tidak |

### Langkah 5 — Jalankan

Tab **Actions** → **Deploy Dasbor XAU ke VPS** → **Run workflow**. Setelah itu berjalan
otomatis tiap kali `dashboard/` berubah.

---

## Cara 2 — Satu perintah dari komputer sendiri

Kalau tidak mau menaruh kunci di GitHub, jalankan dari komputer yang sudah bisa SSH ke VPS:

```bash
./deploy/deploy-vps.sh --host IP_VPS --user root --path /var/www/xau
```

Skrip ini membuat foldernya, mengirim isi `dashboard/` dengan rsync, lalu menampilkan isi
folder di VPS sebagai konfirmasi.

---

## Cara 3 — Manual, tanpa alat apa pun

```bash
scp dashboard/xau-pipeline.html root@IP_VPS:/var/www/xau/
```

Atau buka file di GitHub → **Raw** → simpan → unggah lewat panel hosting.

---

## Pasang nginx (sekali saja, di VPS)

```bash
sudo mkdir -p /var/www/xau
sudo cp deploy/nginx-xau.conf /etc/nginx/sites-available/xau
sudo ln -sf /etc/nginx/sites-available/xau /etc/nginx/sites-enabled/xau
sudo nginx -t && sudo systemctl reload nginx
```

Edit `server_name` di file itu lebih dulu (isi domain, atau `_` kalau mau lewat IP saja).

### HTTPS gratis

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d xau.domain-anda.com
```

### Kunci dengan password

Dasbor trading sebaiknya tidak terbuka untuk umum:

```bash
sudo apt install apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd bryan
```

lalu buka dua baris `auth_basic` di `deploy/nginx-xau.conf` dan reload nginx.

---

## Catatan

- Halaman memuat font dari Google Fonts. Kalau VPS tidak boleh keluar internet, font akan
  jatuh ke fallback sistem — tampilan tetap jalan, hanya hurufnya berbeda.
- Semua angka di dasbor dihasilkan di browser (simulasi). Tidak ada koneksi ke broker,
  jadi tidak ada kredensial apa pun yang perlu ditaruh di VPS.
