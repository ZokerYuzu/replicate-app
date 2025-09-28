# Katalog Belanjaan AI

Aplikasi web sederhana untuk mengelola katalog produk fashion (baju, celana, sepatu) yang terintegrasi dengan AI Granite untuk memberikan rekomendasi styling.

## Fitur

- ✅ Menambah produk ke katalog (baju, celana, sepatu)
- ✅ Mengelola ukuran dan jumlah stok
- ✅ Rekomendasi AI dari Granite untuk styling dan tips perawatan
- ✅ Interface web yang user-friendly dengan Bootstrap
- ✅ Update dan hapus produk
- ✅ Ringkasan statistik katalog

## Instalasi

1. Clone atau download project ini
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:

```bash
python app.py
```

4. Buka browser dan akses: `http://localhost:5000`

## Cara Penggunaan

### Menambah Produk

1. Klik tombol "Tambah Produk Baru"
2. Isi form dengan:
   - Nama produk (contoh: Kaos Polo, Jeans Slim)
   - Jenis produk (Baju/Celana/Sepatu)
   - Ukuran sesuai jenis produk
   - Jumlah stok
   - Harga (opsional)

### Mendapatkan Rekomendasi AI

1. Di halaman utama, klik tombol "Rekomendasi AI" pada produk yang diinginkan
2. AI Granite akan memberikan saran styling, kombinasi warna, dan tips perawatan

### Mengelola Produk

- **Edit Jumlah**: Klik tombol "Edit Jumlah" untuk mengubah stok
- **Hapus Produk**: Klik tombol "Hapus" untuk menghapus produk dari katalog

## Teknologi yang Digunakan

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **AI**: IBM Granite 3.3 8B Instruct via Replicate
- **Icons**: Font Awesome

## Struktur Project

```
replicate-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   └── add_product.html  # Add product form
└── README.md             # Documentation
```

## API Endpoints

- `GET /` - Halaman utama katalog
- `GET/POST /add_product` - Form tambah produk
- `GET /product/<id>/recommendation` - Rekomendasi AI untuk produk
- `GET /delete_product/<id>` - Hapus produk
- `POST /update_quantity/<id>` - Update jumlah produk

## Catatan

- Data disimpan dalam memory (tidak persistent)
- Untuk production, gunakan database seperti SQLite atau PostgreSQL
- API token Replicate sudah dikonfigurasi untuk demo
- Aplikasi berjalan dalam mode debug untuk development
