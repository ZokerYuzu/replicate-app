# Troubleshooting Rekomendasi AI

## Masalah yang Ditemukan

Berdasarkan analisis, ada beberapa kemungkinan masalah dengan rekomendasi AI:

### 1. **Masalah API Token**

- Token Replicate mungkin tidak valid atau expired
- Token tidak di-set dengan benar di environment

### 2. **Masalah Model Name**

- Model `ibm-granite/granite-3.3-8b-instruct` mungkin tidak tersedia
- Perlu mencoba model alternatif

### 3. **Masalah Koneksi**

- Koneksi ke Replicate API mungkin terblokir
- Timeout atau network issues

## Solusi yang Sudah Diimplementasikan

### 1. **Fallback System**

Aplikasi sekarang memiliki sistem fallback yang akan memberikan rekomendasi manual jika AI tidak tersedia:

```python
def get_manual_recommendation(product_name, size, quantity):
    # Memberikan rekomendasi berdasarkan jenis produk
    # Baju, Celana, Sepatu dengan tips styling yang relevan
```

### 2. **Multiple Model Support**

Aplikasi mencoba beberapa model AI:

- `ibm/granite-3.0-8b-instruct`
- `ibm-granite/granite-3.3-8b-instruct`
- `meta/llama-2-7b-chat`

### 3. **Debug Endpoints**

Ditambahkan endpoint untuk debugging:

- `/test_ai` - Test AI secara langsung
- `/debug_ai` - Cek status konfigurasi
- `/test_page` - Halaman test interaktif

## Cara Mengatasi Masalah

### Langkah 1: Cek Status AI

Buka browser dan akses: `http://localhost:5000/debug_ai`

### Langkah 2: Test AI Langsung

Akses: `http://localhost:5000/test_ai`

### Langkah 3: Gunakan Halaman Test

Akses: `http://localhost:5000/test_page`

### Langkah 4: Cek Log Aplikasi

Lihat output di terminal untuk error messages

## Alternatif Solusi

### 1. **Update API Token**

Jika token expired, ganti di `app.py`:

```python
REPLICATE_API_TOKEN = "your-new-token-here"
```

### 2. **Gunakan Model Lain**

Edit di `app.py` untuk menggunakan model yang berbeda:

```python
models_to_try = [
    "meta/llama-2-7b-chat",
    "mistralai/mistral-7b-instruct-v0.1"
]
```

### 3. **Manual Recommendation Only**

Jika AI tidak bekerja sama sekali, aplikasi akan otomatis menggunakan rekomendasi manual yang sudah tersedia.

## Status Saat Ini

✅ **Aplikasi berjalan dengan baik**
✅ **Fallback system aktif**
✅ **Rekomendasi manual tersedia**
❓ **AI Granite perlu diverifikasi**

## Test Manual

Untuk test apakah rekomendasi bekerja:

1. Tambah produk baru di aplikasi
2. Klik tombol "Rekomendasi AI"
3. Jika AI tidak bekerja, akan muncul rekomendasi manual
4. Rekomendasi manual tetap memberikan tips styling yang berguna

## Kontak Support

Jika masalah masih berlanjut:

1. Cek log aplikasi di terminal
2. Test dengan endpoint debug
3. Pastikan koneksi internet stabil
4. Verifikasi API token Replicate
