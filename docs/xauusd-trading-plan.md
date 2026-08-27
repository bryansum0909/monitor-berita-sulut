# Trading Plan XAUUSD — Manajemen Modal & Rencana Pemulihan

**Modal awal: 150.000** · **Skenario: 10 loss beruntun, trade ke-11 target 8 point (80 pip)**

> Dokumen ini memakai satuan modal apa adanya (150.000). Kalau modal Anda Rp150.000, lihat
> bagian [Realita Ukuran Modal](#8-realita-ukuran-modal-rp150000) — di situ semua angka
> diterjemahkan ke lot dan rupiah nyata.

---

## 0. Jawaban Singkat (baca ini dulu)

Pertanyaan Anda: *"bagaimana cara mengelola keuangan agar trade ke-11 bisa balik modal
dengan jarak 8 point?"*

**Jawaban jujurnya: tidak ada pengelolaan keuangan yang sehat yang bisa menutup 10 loss
beruntun dalam 1 trade.** Satu-satunya cara melakukannya adalah membesarkan lot secara
ekstrem (martingale), dan itu bukan money management — itu memindahkan risiko
kebangkrutan dari "pelan-pelan" menjadi "sekaligus".

Yang bisa dan seharusnya dilakukan:

| Pertanyaan | Jawaban |
|---|---|
| Bisa balik modal dalam 1 trade? | Tidak, kecuali risk 11,19% equity (RR 1:2) — dan itu langkah menuju MC |
| Berapa trade realistis untuk balik modal? | **6 trade menang di RR 1:2**, atau **4 trade menang di RR 1:3** |
| Kunci utamanya apa? | Membatasi kerugian per trade jadi **≤1%**, supaya 10 loss beruntun cuma −9,6%, bukan −60% |
| Setelah loss beruntun, lot dinaikkan atau diturunkan? | **Diturunkan.** Kebalikan dari naluri Anda |
| SL untuk TP 8 point? | **4 point (40 pip)** untuk RR 1:2 — jangan dipaksa lebih kecil |

Inti rencananya: **jangan cari 1 trade ajaib, tapi buat 10 loss beruntun jadi peristiwa
yang tidak berbahaya.**

---

## 1. Kenapa "Balik Modal dalam 1 Trade" adalah Jebakan

Ini bukan opini, ini aritmetika. Anggap Anda risk 2% per trade.

**Setelah 10 loss beruntun:**
- Equity: 150.000 → **122.561** (turun 18,29%)
- Untuk kembali ke 150.000, Anda butuh gain **+22,39%** (bukan +18,29% — inilah
  *asimetri drawdown*: turun 18% butuh naik 22% untuk pulih)

**Kalau Anda paksa balik modal di trade ke-11:**

| RR | Risk yang dibutuhkan di trade ke-11 | Nominal | Kalau trade ke-11 LOSS |
|---|---|---|---|
| 1:2 | **11,19% equity** | 13.720 | Equity 108.841 → DD total **27,4%**, butuh **+37,8%** |
| 1:3 | **7,46% equity** | 9.146 | Equity 113.415 → DD total **24,4%**, butuh **+32,3%** |
| 1:4 | **5,60% equity** | 6.860 | Equity 115.701 → DD total **22,9%**, butuh **+29,6%** |

Perhatikan polanya: gagal sekali di mode "balik modal", dan kebutuhan pemulihan Anda
melonjak dari +22% jadi +38%. Trade ke-12 akan menuntut lot yang lebih besar lagi.
Ini deret yang berakhir di Margin Call, bukan di breakeven.

**Kesimpulan: buang target "balik modal di trade ke-11". Ganti dengan "balik modal dalam
6 trade menang di RR 1:2, atau 4 trade menang di RR 1:3".**

---

## 2. Aturan #1 — Kecilkan Risiko per Trade

Ini satu-satunya variabel yang benar-benar Anda kendalikan. Lihat betapa besar
pengaruhnya terhadap skenario 10 loss beruntun yang sama persis:

| Risk/trade | Equity setelah 10 loss | Drawdown | Gain yang dibutuhkan | Trade menang @1:2 | Trade menang @1:3 |
|---|---|---|---|---|---|
| **0,5%** | 142.667 | −4,89% | +5,14% | 6 | 4 |
| **1,0%** ✅ | 135.657 | −9,56% | +10,57% | 6 | 4 |
| **2,0%** | 122.561 | −18,29% | +22,39% | 6 | 4 |
| 3,0% | 110.614 | −26,26% | +35,61% | 6 | 4 |
| 5,0% | 89.811 | −40,13% | +67,02% | 6 | 4 |
| 10,0% ❌ | 52.302 | −65,13% | +186,80% | 6 | 5 |

### Ini temuan paling penting di seluruh dokumen

Lihat dua kolom terakhir. **Jumlah trade menang yang dibutuhkan untuk balik modal
praktis identik — 6 di RR 1:2 dan 4 di RR 1:3 — apa pun risk %-nya.**

Artinya: memperbesar risk **sama sekali tidak mempercepat** pemulihan Anda. Yang
dilakukannya hanya membuat kerusakan lebih dalam dan membuat Anda lebih dekat ke titik
di mana pemulihan jadi mustahil secara matematis.

Risk 10% tidak membuat Anda pulih lebih cepat dari risk 1%. Sama-sama butuh 6 trade
menang di RR 1:2. Bedanya: yang satu sudah kehilangan 65% modal, yang satu baru 9,6%.

**Aturan: risk maksimum 1% per trade. Titik.**

---

## 3. Aturan #2 — Turunkan Lot Saat Kalah (Anti-Martingale)

Naluri setelah kalah beruntun adalah membesarkan lot untuk mengejar. Lakukan
kebalikannya.

### Tangga De-Risking

| Kondisi | Risk per trade | Alasan |
|---|---|---|
| Normal (equity di puncak) | **1,0%** | Mode standar |
| Setelah 2 loss beruntun | **0,75%** | Pasar mungkin tidak cocok dengan sistem Anda |
| Setelah 3 loss beruntun | **0,50%** | Perlambat kerusakan sambil cari konfirmasi |
| Setelah 4 loss beruntun | **STOP hari itu** | Hampir pasti ini masalah kondisi pasar/emosi |
| Setelah 5 loss beruntun | **STOP total, demo dulu** | Sistem butuh evaluasi, bukan modal tambahan |

**Kembali ke 1%** hanya setelah equity menyentuh kembali *high-water mark* (puncak equity
sebelumnya), bukan setelah sekadar menang 1–2 kali.

### Efeknya terhadap skenario Anda

Dengan tangga ini, **10 loss beruntun secara struktural tidak mungkin terjadi** — Anda
sudah berhenti di loss ke-4. Total kerugian maksimum sebelum berhenti:

```
1,0% + 1,0% + 0,75% + 0,50% = 3,25% dari modal  →  ±4.875 dari 150.000
```

Bandingkan dengan −18,29% (risk 2% flat) atau −65% (risk 10% flat). Inilah cara
sesungguhnya "mengelola keuangan agar bisa balik modal": dengan tidak pernah membiarkan
lubangnya jadi dalam.

---

## 4. Aturan #3 — Circuit Breaker

Batas keras. Bukan saran, tapi aturan yang tidak boleh dilanggar.

| Pemicu | Tindakan |
|---|---|
| 2 loss beruntun dalam sehari | Tutup terminal, selesai untuk hari itu |
| Kerugian harian −2% | Stop, apa pun alasannya |
| Kerugian mingguan −5% | Stop sampai Senin berikutnya |
| Drawdown −6% dari puncak equity | Turun ke risk 0,5%, review 20 trade terakhir di jurnal |
| Drawdown −10% dari puncak equity | Stop 1 minggu penuh. Sistemnya yang salah, bukan sizingnya |
| 3 trade profit beruntun | Boleh lanjut, tapi jangan naikkan lot karena "lagi panas" |

### Kenapa ini penting untuk kasus Anda

10 loss beruntun bukan kejadian aneh — ini statistik normal:

| Winrate sistem | Peluang kena 10 loss beruntun dalam 200 trade |
|---|---|
| 30% | **81,6%** — hampir pasti |
| 40% | **38,4%** — sekitar 1 dari 3 |
| 50% | **9,3%** — jarang tapi nyata |

Kalau winrate Anda 40% (normal untuk sistem RR 1:2), 10 loss beruntun akan terjadi pada
Anda. Rencana yang baik **mengantisipasinya**, bukan bereaksi panik saat terjadi.

---

## 5. Setup Trading: 8 Point / 80 Pip

### Konversi satuan XAUUSD

| Istilah | Nilai | Contoh |
|---|---|---|
| 1 point | Pergerakan harga $1,00 | 3.300,00 → 3.301,00 |
| 1 pip | Pergerakan harga $0,10 | 3.300,00 → 3.300,10 |
| 8 point | = 80 pip = $8,00 | 3.300,00 → 3.308,00 ✅ konsisten dengan soal Anda |
| Nilai 1 point per 1,00 lot | $100 | 1 lot × 8 point = $800 |
| Nilai 1 point per 0,01 lot | $1 | 0,01 lot × 8 point = $8 |

### Masalah: TP dipatok 8 point, RR-nya dari mana?

Kalau TP dikunci di 8 point, maka SL-lah yang menentukan RR:

| RR | SL | Layak? |
|---|---|---|
| 1:1,5 | 5,33 point (53 pip) | ✅ Aman, tapi RR kurang |
| **1:2** | **4,00 point (40 pip)** | ✅ **Rekomendasi** |
| 1:2,5 | 3,20 point (32 pip) | ⚠️ Ketat, hanya untuk setup presisi |
| 1:3 | 2,67 point (27 pip) | ❌ Terlalu ketat — lihat di bawah |
| 1:4 | 2,00 point (20 pip) | ❌ Hampir pasti kena noise |

**Kenapa SL 2,67 point berbahaya:** spread XAUUSD biasanya 0,15–0,35 point, ditambah
slippage saat news. Itu sudah memakan 6–13% SL Anda sebelum harga bergerak. Lebih parah:
noise normal gold di M5/M15 rutin 2–3 point. SL 2,67 point akan kena bukan karena analisis
Anda salah, tapi karena harga bernapas. **Ini kemungkinan besar penyebab 10 loss beruntun
Anda.**

### Aturan yang benar

> **SL ditentukan oleh struktur pasar, bukan oleh RR yang Anda inginkan.
> Kalau mau RR lebih besar, panjangkan TP — jangan pendekkan SL.**

| Target RR | SL | TP | Total jarak |
|---|---|---|---|
| 1:2 | 4 point (40 pip) | **8 point (80 pip)** | Sesuai skenario Anda |
| 1:3 | 4 point (40 pip) | **12 point (120 pip)** | Perpanjang TP, SL tetap |
| 1:4 | 4 point (40 pip) | **16 point (160 pip)** | Untuk trend day |

SL 4 point ditaruh di **bawah swing low** (buy) atau **di atas swing high** (sell) —
kalau struktur menuntut SL 6 point, pakai 6 point dan geser TP ke 12 point. Jangan
pernah memaksa SL masuk ke angka yang Anda inginkan.

### Winrate minimum agar tidak rugi

| RR | Breakeven winrate | Target winrate realistis |
|---|---|---|
| 1:2 | 33,3% (+biaya ≈ 36%) | 40–45% |
| 1:3 | 25,0% (+biaya ≈ 28%) | 33–40% |

Kalau winrate sistem Anda di bawah angka breakeven, **tidak ada money management yang bisa
menyelamatkannya.** Perbaiki sistemnya dulu di demo.

---

## 6. Rumus Lot Size (hafalkan ini)

```
Lot = Nominal Risiko / (100 × SL dalam point)
```

Contoh: modal 150.000, risk 1% = 1.500, SL 4 point
→ Lot = 1.500 / (100 × 4) = **3,75 lot**

Dan verifikasi TP: 3,75 lot × 100 × 8 point = 3.000 = **2× risiko** ✅ RR 1:2 benar.

### Tabel cepat (risk 1%)

| Equity | Risiko 1% | SL 3 pt | SL 4 pt | SL 5 pt | SL 6 pt |
|---|---|---|---|---|---|
| 150.000 | 1.500 | 5,00 | 3,75 | 3,00 | 2,50 |
| 135.657 | 1.357 | 4,52 | 3,39 | 2,71 | 2,26 |
| 122.561 | 1.226 | 4,09 | 3,06 | 2,45 | 2,04 |

**Hitung ulang lot setiap trade berdasarkan equity saat ini**, bukan modal awal. Ini
membuat lot otomatis mengecil saat drawdown (melindungi) dan membesar saat profit
(compounding) — tanpa Anda perlu berpikir.

---

## 7. Rencana Pemulihan dari Drawdown

Asumsi posisi Anda sekarang: setelah 10 loss beruntun di risk 2%, equity **122.561**,
butuh **+22,39%** untuk balik ke 150.000.

### Berapa lama realistisnya?

| Winrate | RR | Ekspektansi/trade | Trade dibutuhkan |
|---|---|---|---|
| 50% | 1:2 | +0,50R | **22 trade** |
| 45% | 1:2 | +0,35R | 31 trade |
| 40% | 1:2 | +0,20R | 57 trade |
| **40%** | **1:3** | **+0,60R** | **19 trade** ⭐ |
| 35% | 1:3 | +0,40R | 28 trade |
| 30% | 1:3 | +0,20R | 61 trade |

Angka "6 trade menang" di Tabel bagian 2 adalah kalau **tidak ada loss sama sekali** di
antaranya. Di dunia nyata, dengan loss yang berselang-seling, jawabannya **19–31 trade**.
Dengan 2–3 trade per hari, itu **2–3 minggu kerja**. Itu timeline yang jujur.

**Perhatikan baris berbintang:** RR 1:3 dengan winrate 40% memulihkan lebih cepat
(19 trade) daripada RR 1:2 dengan winrate 50% (22 trade). Kalau Anda ingin mempercepat
pemulihan, **naikkan RR (perpanjang TP), jangan naikkan lot.** Itu satu-satunya akselerator
yang tidak menambah risiko kebangkrutan.

### Protokol 3 Fase

**Fase 1 — Stabilisasi (10 trade pertama)**
- Risk **0,5%** per trade. Tujuannya bukan profit, tapi membuktikan sistem Anda masih jalan
- Maksimal 2 trade per hari
- Wajib jurnal setiap trade
- Lolos ke Fase 2 kalau: 10 trade selesai **dan** equity tidak turun lagi

**Fase 2 — Pemulihan (sampai equity kembali ke 150.000)**
- Risk **0,75%** per trade
- RR minimum 1:2, prioritaskan setup yang memungkinkan 1:3
- Circuit breaker penuh aktif (bagian 4)
- Kalau equity turun 3% lagi dari titik masuk Fase 2 → kembali ke Fase 1

**Fase 3 — Normal (equity ≥ 150.000)**
- Risk **1,0%** per trade
- Target realistis: **3–6% per bulan**. Bukan 100%
- Tarik 30% dari profit bulanan keluar dari akun setiap bulan

---

## 8. Realita Ukuran Modal (Rp150.000)

Kalau modal Anda benar-benar **Rp150.000** (≈ $9), ini hal yang harus dihadapi jujur.

### Akun standar/micro dengan minimum lot 0,01 — TIDAK BISA

Dengan saldo $150 sekalipun, minimum lot 0,01 memaksa risiko ini:

| SL | Kerugian di 0,01 lot | % dari $150 |
|---|---|---|
| 3 point | $3,00 | **2,00%** |
| 4 point | $4,00 | **2,67%** |
| 5 point | $5,00 | **3,33%** |

Anda **secara fisik tidak bisa** risk 1% — lot minimumnya terlalu besar. Anda terkunci di
risk 2–3,3%, yang persis kondisi yang menghasilkan drawdown 18–26% dari 10 loss beruntun.
Dengan saldo $9, satu trade 0,01 lot dengan SL 4 point adalah **44% dari akun**. Dua loss
= Margin Call.

### Solusi: Akun Cent

Rp150.000 ≈ $9,09 ≈ **909 USC** (US Cent) di akun cent. Sekarang money management jadi mungkin:

| Risk | Nominal (USC) | SL 3 pt | SL 4 pt | SL 5 pt |
|---|---|---|---|---|
| 0,5% | 4,54 | 0,02 lot | 0,01 lot | 0,01 lot |
| **1,0%** | **9,09** | **0,03 lot** | **0,02 lot** | **0,02 lot** |
| 2,0% | 18,18 | 0,06 lot | 0,05 lot | 0,04 lot |

Dengan risk 1%, SL 4 point, lot 0,02 di akun cent:
- Risiko per trade: 8 USC ≈ **Rp1.320**
- Profit per trade menang (TP 8 point, RR 1:2): 16 USC ≈ **Rp2.640**
- Target bulanan 5%: ≈ **Rp7.500**

### Ekspektasi yang jujur

Rp150.000 bukan modal untuk mencari penghasilan — **itu modal untuk membeli pengalaman
dengan risiko finansial yang tertanggung.** Gunakan untuk:

1. Membuktikan sistem Anda punya ekspektansi positif selama **100 trade berturut-turut**
2. Melatih disiplin circuit breaker sampai jadi otomatis
3. Membangun jurnal dengan data nyata

Setelah 100 trade dengan hasil positif dan tanpa satu pun pelanggaran aturan, **baru**
tambah modal. Menambah modal ke sistem yang belum terbukti hanya memperbesar angka
kerugiannya. Verifikasi spesifikasi lot dan nilai point akun cent broker Anda dengan
1 trade uji volume terkecil sebelum memakai tabel di atas.

---

## 9. Checklist Sebelum Entry

Semua harus ✅. Satu saja ❌, jangan entry.

- [ ] Setup sesuai satu pola yang tertulis di sistem saya (bukan "kelihatannya bagus")
- [ ] SL ditentukan oleh struktur (swing high/low), bukan oleh angka yang saya inginkan
- [ ] TP minimal 2× jarak SL
- [ ] Lot dihitung dengan rumus dari equity **saat ini**
- [ ] Belum kena batas circuit breaker hari ini
- [ ] Tidak ada news high-impact dalam 30 menit ke depan (NFP, CPI, FOMC)
- [ ] Saya tidak sedang marah, balas dendam, atau mengejar kerugian
- [ ] Saya siap kehilangan nominal ini tanpa perubahan apa pun pada hidup saya
- [ ] SL dan TP dipasang **bersamaan dengan entry**, bukan menyusul

## 10. Format Jurnal

Catat setiap trade. Tanpa data, Anda tidak sedang trading — Anda sedang berjudi dengan
grafik.

| Kolom | Contoh |
|---|---|
| Tanggal & jam | 2026-08-27 14:30 WITA |
| Arah | Buy / Sell |
| Entry | 3.300,50 |
| SL (point) | 4,0 |
| TP (point) | 8,0 |
| RR rencana | 1:2 |
| Lot | 0,02 |
| Risk % | 1,0% |
| Equity sebelum | 122.561 |
| Hasil (R) | +2,0R / −1,0R / +0,3R |
| Alasan entry | Break struktur H1 + retest |
| Pelanggaran aturan | Tidak ada / "lot dibesarkan" |
| Kondisi emosi | Tenang / Balas dendam |

**Review setiap 20 trade:** hitung winrate aktual, ekspektansi rata-rata (R), dan jumlah
pelanggaran aturan. Kalau pelanggaran > 0, itu masalah nomor satu Anda — bukan strateginya.

---

## Ringkasan Satu Halaman

| Parameter | Nilai |
|---|---|
| Risk per trade (normal) | **1,0%** |
| Risk setelah 2 loss beruntun | 0,75% |
| Risk setelah 3 loss beruntun | 0,50% |
| Setelah 4 loss beruntun | **Stop hari itu** |
| SL standar | 4 point (40 pip), disesuaikan struktur |
| TP RR 1:2 | 8 point (80 pip) |
| TP RR 1:3 | 12 point (120 pip) |
| Rumus lot | `Risiko ÷ (100 × SL point)` |
| Batas rugi harian | −2% |
| Batas rugi mingguan | −5% |
| Stop total | DD −10% dari puncak equity |
| Target bulanan | 3–6% |
| Waktu pemulihan realistis | 19–31 trade (2–3 minggu) |

### Tiga kalimat yang perlu diingat

1. **Memperbesar lot tidak mempercepat pemulihan** — 6 trade menang di RR 1:2 dibutuhkan
   baik di risk 1% maupun 10%; yang berbeda hanya seberapa hancur akunnya.
2. **Yang mempercepat pemulihan adalah RR yang lebih besar**, bukan lot yang lebih besar —
   panjangkan TP, jangan pendekkan SL.
3. **10 loss beruntun bukan alasan untuk mengubah money management** — itu justru bukti
   money management-nya sedang bekerja, kalau kerugiannya cuma −9,6% dan bukan −65%.

---

*Dokumen ini adalah kerangka manajemen risiko, bukan saran investasi. Trading XAUUSD
dengan leverage berisiko kehilangan seluruh modal. Uji setiap aturan di akun demo minimal
100 trade sebelum dipakai dengan uang nyata.*
