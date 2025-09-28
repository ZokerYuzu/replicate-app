# HIGHLIGHT KODE UNTUK PRESENTASI AI IBM GRANITE

## 🎯 KODE UTAMA YANG PERLU DIHIGHLIGHT

### 1. SETUP AI GRANITE - Konfigurasi Dasar

**File: `app.py` - Lines 12-30**

```python
# API Token untuk Replicate
REPLICATE_API_TOKEN = "r8_MKvmf9XcInzr6jf4bYz7qdFnJLt9axO05A0yl"

def get_ai_recommendation(product_name, size, quantity):
    """Mendapatkan rekomendasi dari AI Granite"""
    try:
        # Set API token untuk replicate
        import os
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

        prompt = f"""
        Berikan rekomendasi dalam bahasa Indonesia untuk produk fashion berikut:
        - Produk: {product_name}
        - Ukuran: {size}
        - Jumlah: {quantity}

        Berikan saran styling, kombinasi warna, dan tips perawatan yang sesuai.
        Gunakan bahasa Indonesia yang mudah dipahami dan format yang rapi dengan poin-poin.
        """
```

**🎯 POIN PENTING:**

- Environment variable setup untuk API token
- Prompt engineering dalam bahasa Indonesia
- Structured prompt dengan context yang jelas

---

### 2. MULTIPLE MODEL FALLBACK - Reliability Strategy

**File: `app.py` - Lines 32-52**

```python
        # Coba beberapa model yang berbeda
        models_to_try = [
            "ibm/granite-3.0-8b-instruct",
            "ibm-granite/granite-3.3-8b-instruct",
            "meta/llama-2-7b-chat"
        ]

        for model in models_to_try:
            try:
                print(f"Trying model: {model}")
                output = replicate.run(
                    model,
                    input={
                        "prompt": prompt,
                        "max_tokens": 300,
                        "temperature": 0.7
                    }
                )
                # Some models return a list of strings
                if isinstance(output, list):
                    return "".join([str(x) for x in output])
                return str(output)
            except Exception as model_error:
                print(f"Model {model} failed: {str(model_error)}")
                continue
```

**🎯 POIN PENTING:**

- Multiple model fallback untuk reliability
- Output format handling (list vs string)
- Detailed error logging untuk debugging
- Graceful degradation

---

### 3. AI CATALOG ANALYSIS - Business Intelligence

**File: `app.py` - Lines 167-189**

```python
def analyze_catalog_with_ai(catalog_summary: dict) -> str:
    """Gunakan AI untuk memberi insight: harga, jumlah, ukuran, rekomendasi restock & bundling."""
    try:
        import os
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
        prompt = (
            "Anda adalah asisten retail yang berpengalaman. Berdasarkan ringkasan katalog berikut, "
            "berikan insight singkat dan actionable dalam bahasa Indonesia: "
            "1) produk terlaris potensial berdasarkan stok & jenis, "
            "2) rekomendasi restock (threshold 3), "
            "3) saran bundling lintas kategori, "
            "4) range harga ideal jika harga kosong. "
            "Gunakan bahasa Indonesia yang mudah dipahami dan format yang rapi dengan poin-poin.\n\n"
            f"Ringkasan: {catalog_summary}"
        )
        output = replicate.run(
            "ibm-granite/granite-3.3-8b-instruct",
            input={
                "prompt": prompt,
                "max_tokens": 300,
                "temperature": 0.4
            }
        )
```

**🎯 POIN PENTING:**

- Specialized prompt untuk business intelligence
- Lower temperature (0.4) untuk konsistensi analisis
- Structured input dengan catalog summary
- Actionable insights generation

---

### 4. API ENDPOINTS - RESTful Design

**File: `app.py` - Lines 200-230**

```python
@app.route('/product/<int:product_id>/recommendation')
def get_recommendation(product_id):
    """Mendapatkan rekomendasi AI untuk produk tertentu"""
    product = next((p for p in products if p['id'] == product_id), None)

    if not product:
        return jsonify({'error': 'Produk tidak ditemukan'}), 404

    recommendation = get_ai_recommendation(
        product['name'],
        product['size'],
        product['quantity']
    )

    return jsonify({
        'product': product,
        'recommendation': recommendation
    })

@app.route('/analyze_catalog')
def analyze_catalog():
    """Analisis katalog: statistik lokal + insight AI untuk efisiensi harga, jumlah, ukuran."""
    local_summary = summarize_catalog_locally()
    ai_insight = analyze_catalog_with_ai(local_summary)
    return jsonify({
        'summary': local_summary,
        'ai_insight': ai_insight
    })
```

**🎯 POIN PENTING:**

- RESTful API design
- Error handling dengan HTTP status codes
- JSON response format untuk frontend integration
- Separation of concerns

---

### 5. FRONTEND INTEGRATION - JavaScript AJAX

**File: `templates/base.html` - Lines 80-104**

```javascript
// Function untuk mendapatkan rekomendasi AI
function getAIRecommendation(productId) {
  const button = document.getElementById("ai-btn-" + productId);
  const originalText = button.innerHTML;

  button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
  button.disabled = true;

  fetch("/product/" + productId + "/recommendation")
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert("Error: " + data.error);
      } else {
        showRecommendation(data.recommendation, productId);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Terjadi kesalahan saat mendapatkan rekomendasi AI");
    })
    .finally(() => {
      button.innerHTML = originalText;
      button.disabled = false;
    });
}
```

**🎯 POIN PENTING:**

- Async/await pattern dengan fetch API
- Loading state management
- Error handling untuk user experience
- Cleanup dengan finally block

---

### 6. OUTPUT FORMATTING - Smart Text Processing

**File: `templates/base.html` - Lines 115-137**

```javascript
function showRecommendation(recommendation, productId) {
  // Clean up output: if it's JSON-like array string, try to parse
  let cleaned = recommendation;
  try {
    const parsed = JSON.parse(recommendation);
    if (Array.isArray(parsed)) {
      cleaned = parsed.join("\n\n");
    } else if (typeof parsed === "object") {
      cleaned = JSON.stringify(parsed, null, 2);
    }
  } catch (_) {
    // not JSON, continue
  }

  // If already contains HTML tags, use as is, otherwise convert markdown
  if (cleaned.includes("<strong>") || cleaned.includes("<br>")) {
    // Already formatted HTML, use as is
  } else {
    // Convert markdown-like **bold** to <strong> and newlines to <br>
    cleaned = cleaned
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n\n/g, "<br><br>")
      .replace(/\n/g, "<br>");
  }

  recommendationDiv.innerHTML = `
        <h6><i class="fas fa-robot me-2"></i>Rekomendasi AI Granite:</h6>
        <div>${cleaned}</div>
        <button class="btn btn-sm btn-outline-light mt-2" onclick="this.parentElement.remove()">
            <i class="fas fa-times me-1"></i>Tutup
        </button>
    `;
}
```

**🎯 POIN PENTING:**

- Smart detection untuk HTML vs Markdown
- Automatic formatting conversion
- Safe HTML rendering dengan innerHTML
- User-friendly interface

---

### 7. FALLBACK SYSTEM - Manual Recommendations

**File: `app.py` - Lines 65-144**

```python
def get_manual_recommendation(product_name, size, quantity):
    """Rekomendasi manual jika AI tidak tersedia"""
    recommendations = {
        "baju": f"""
        <strong>🎨 Rekomendasi untuk {product_name} ukuran {size}:</strong><br><br>

        <strong>✨ Tips Styling:</strong><br>
        • Cocok untuk acara casual dan semi-formal<br>
        • Kombinasi dengan celana jeans atau chino<br>
        • Aksesori dengan jam tangan atau gelang sederhana<br><br>

        <strong>🎨 Kombinasi Warna:</strong><br>
        • Warna netral: putih, hitam, navy, abu-abu<br>
        • Cocok dipadukan dengan warna earth tone<br><br>

        <strong>🧺 Tips Perawatan:</strong><br>
        • Cuci dengan air dingin untuk menjaga warna<br>
        • Setrika dengan suhu sedang<br>
        • Simpan dengan hanger untuk mencegah kerutan
        """,
        # ... celana dan sepatu recommendations
    }

    # Cari jenis produk berdasarkan nama
    product_lower = product_name.lower()
    for product_type, recommendation in recommendations.items():
        if product_type in product_lower:
            return recommendation

    # Default recommendation
    return f"""
    <strong>🎨 Rekomendasi untuk {product_name} ukuran {size}:</strong><br><br>
    <!-- Default recommendation content -->
    """
```

**🎯 POIN PENTING:**

- Intelligent product type detection
- Structured HTML output
- Consistent formatting dengan AI output
- Reliability dengan fallback

---

### 8. ERROR HANDLING & DEBUGGING

**File: `app.py` - Lines 248-256**

```python
@app.route('/test_ai')
def test_ai():
    """Test endpoint untuk AI"""
    try:
        print("Testing AI recommendation...")
        recommendation = get_ai_recommendation("Kaos Polo", "L", 5)
        print(f"Recommendation received: {recommendation[:100]}...")
        return jsonify({
            'status': 'success',
            'recommendation': recommendation
        })
    except Exception as e:
        print(f"Error in test_ai: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/debug_ai')
def debug_ai():
    """Debug endpoint untuk melihat status AI"""
    return jsonify({
        'api_token_set': bool(REPLICATE_API_TOKEN),
        'token_length': len(REPLICATE_API_TOKEN) if REPLICATE_API_TOKEN else 0,
        'replicate_available': True,
        'manual_recommendation': get_manual_recommendation("Test Product", "M", 1)[:100] + "..."
    })
```

**🎯 POIN PENTING:**

- Comprehensive error logging
- Debug endpoints untuk troubleshooting
- Graceful degradation dengan fallback
- Production-ready error handling

---

### 9. CATALOG ANALYSIS - Local Statistics

**File: `app.py` - Lines 146-165**

```python
def summarize_catalog_locally() -> dict:
    """Ringkasan statistik lokal tanpa AI (cepat dan deterministik)."""
    total_items = len(products)
    total_stock = sum(p.get('quantity', 0) for p in products)
    total_value = sum((p.get('quantity', 0) * p.get('price', 0)) for p in products)
    by_type = {}
    for p in products:
        by_type[p.get('type', 'Lainnya')] = by_type.get(p.get('type', 'Lainnya'), 0) + 1
    sizes = {}
    for p in products:
        sizes[p.get('size', 'N/A')] = sizes.get(p.get('size', 'N/A'), 0) + p.get('quantity', 0)
    low_stock = [p for p in products if p.get('quantity', 0) <= 3]
    return {
        'total_products': total_items,
        'total_stock': total_stock,
        'total_value': total_value,
        'by_type': by_type,
        'sizes': sizes,
        'low_stock': low_stock[:10]
    }
```

**🎯 POIN PENTING:**

- Efficient data processing
- Local statistics calculation
- Low stock detection
- Performance optimization

---

### 10. FRONTEND CATALOG ANALYSIS

**File: `templates/index.html` - Lines 160-200**

```javascript
document.getElementById("analyze-btn").addEventListener("click", function () {
  const panel = document.getElementById("analysis-panel");
  const content = document.getElementById("analysis-content");
  panel.style.display = "block";
  content.innerHTML = '<div class="text-muted"><i class="fas fa-spinner fa-spin me-2"></i>Mengambil analisis...</div>';
  fetch("/analyze_catalog")
    .then((r) => r.json())
    .then((data) => {
      const s = data.summary;
      const ai = data.ai_insight;
      // Format AI text - handle both HTML and markdown
      let aiText = ai;
      if (!ai.includes("<strong>") && !ai.includes("<br>")) {
        aiText = ai
          .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
          .replace(/\n\n/g, "<br><br>")
          .replace(/\n/g, "<br>");
      }
      content.innerHTML = `
            <div class="row">
              <div class="col-md-5">
                <h6 class="mb-2">Ringkasan Lokal</h6>
                <ul class="mb-3">
                  <li><strong>Total Produk:</strong> ${s.total_products}</li>
                  <li><strong>Total Stok:</strong> ${s.total_stock}</li>
                  <li><strong>Perkiraan Nilai Stok:</strong> Rp ${s.total_value.toLocaleString("id-ID")}</li>
                </ul>
                <h6 class="mb-2">Stok Rendah (≤ 3)</h6>
                ${s.low_stock.length ? "<ul>" + s.low_stock.map((p) => `<li>${p.name} (${p.size}) - ${p.quantity}</li>`).join("") + "</ul>" : '<div class="text-muted">Tidak ada</div>'}
              </div>
              <div class="col-md-7">
                <h6 class="mb-2">Insight AI</h6>
                <div class="ai-recommendation">${aiText}</div>
              </div>
            </div>
          `;
    })
    .catch((err) => {
      content.innerHTML = `<div class="text-danger">Gagal mengambil analisis: ${err}</div>`;
    });
});
```

**🎯 POIN PENTING:**

- Dynamic UI updates
- Error handling untuk user experience
- Format handling untuk AI output
- Responsive design dengan Bootstrap

---

## 🎯 RINGKASAN KODE UNTUK PRESENTASI

### **Kode Paling Penting untuk Di-highlight:**

1. **Setup AI Granite** (Lines 12-30) - Konfigurasi dasar
2. **Multiple Model Fallback** (Lines 32-52) - Reliability strategy
3. **AI Catalog Analysis** (Lines 167-189) - Business intelligence
4. **API Endpoints** (Lines 200-230) - RESTful design
5. **Frontend Integration** (Lines 80-104) - JavaScript AJAX
6. **Output Formatting** (Lines 115-137) - Smart text processing
7. **Fallback System** (Lines 65-144) - Manual recommendations
8. **Error Handling** (Lines 248-256) - Debugging tools

### **Demo Flow:**

1. **Setup** → Tunjukkan konfigurasi AI Granite
2. **Integration** → Tunjukkan API endpoints
3. **Frontend** → Tunjukkan JavaScript integration
4. **Live Demo** → Test rekomendasi AI
5. **Analysis** → Test analisis katalog
6. **Error Handling** → Tunjukkan fallback system

### **Key Messages:**

- ✅ **Reliability**: Multiple model fallback
- ✅ **User Experience**: Loading states dan error handling
- ✅ **Business Value**: AI-powered insights
- ✅ **Scalability**: RESTful API design
- ✅ **Maintainability**: Clean code structure
