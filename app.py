from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import replicate
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# In-memory storage untuk produk (dalam production gunakan database)
products = []

# API Token untuk Replicate
REPLICATE_API_TOKEN = os.environ.get('REPLICATE_API_TOKEN', "r8_MKvmf9XcInzr6jf4bYz7qdFnJLt9axO05A0yl")

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
        
        # Jika semua model gagal, berikan rekomendasi manual
        return get_manual_recommendation(product_name, size, quantity)
        
    except Exception as e:
        print(f"Error in AI recommendation: {str(e)}")
        return get_manual_recommendation(product_name, size, quantity)

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
        "celana": f"""
        <strong>🎨 Rekomendasi untuk {product_name} ukuran {size}:</strong><br><br>
        
        <strong>✨ Tips Styling:</strong><br>
        • Cocok untuk berbagai kesempatan<br>
        • Padukan dengan kemeja atau t-shirt<br>
        • Gunakan ikat pinggang untuk tampilan lebih rapi<br><br>
        
        <strong>🎨 Kombinasi Warna:</strong><br>
        • Warna klasik: navy, hitam, khaki<br>
        • Cocok dengan warna-warna terang di bagian atas<br><br>
        
        <strong>🧺 Tips Perawatan:</strong><br>
        • Cuci terbalik untuk menjaga warna<br>
        • Jangan terlalu sering dicuci<br>
        • Simpan dengan cara dilipat atau digantung
        """,
        "sepatu": f"""
        <strong>🎨 Rekomendasi untuk {product_name} ukuran {size}:</strong><br><br>
        
        <strong>✨ Tips Styling:</strong><br>
        • Cocok untuk berbagai outfit<br>
        • Padukan dengan jeans, celana chino, atau dress<br>
        • Pilih warna yang netral untuk fleksibilitas<br><br>
        
        <strong>🎨 Kombinasi Warna:</strong><br>
        • Warna klasik: hitam, putih, coklat, navy<br>
        • Cocok dengan hampir semua warna outfit<br><br>
        
        <strong>🧺 Tips Perawatan:</strong><br>
        • Bersihkan setelah digunakan<br>
        • Gunakan shoe tree untuk menjaga bentuk<br>
        • Rotasi penggunaan untuk memperpanjang umur
        """
    }
    
    # Cari jenis produk berdasarkan nama
    product_lower = product_name.lower()
    for product_type, recommendation in recommendations.items():
        if product_type in product_lower:
            return recommendation
    
    # Default recommendation
    return f"""
    <strong>🎨 Rekomendasi untuk {product_name} ukuran {size}:</strong><br><br>
    
    <strong>✨ Tips Styling:</strong><br>
    • Pilih warna yang sesuai dengan kulit dan personalitas<br>
    • Padukan dengan aksesori yang tepat<br>
    • Sesuaikan dengan acara yang akan dihadiri<br><br>
    
    <strong>🎨 Kombinasi Warna:</strong><br>
    • Gunakan prinsip color wheel untuk kombinasi yang harmonis<br>
    • Pilih satu warna dominan dan warna aksen<br><br>
    
    <strong>🧺 Tips Perawatan:</strong><br>
    • Baca label perawatan dengan teliti<br>
    • Simpan di tempat yang kering dan sejuk<br>
    • Bersihkan secara teratur sesuai jenis bahan
    """

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

def analyze_catalog_with_ai(catalog_summary: dict) -> str:
    """Gunakan AI untuk memberi insight: harga, jumlah, ukuran, rekomendasi restock & bundling."""
    try:
        import os
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
        prompt = (
            "Anda adalah asisten retail yang berpengalaman. Berdasarkan ringkasan katalog berikut, berikan insight singkat dan actionable dalam bahasa Indonesia: "
            "1) produk terlaris potensial berdasarkan stok & jenis, 2) rekomendasi restock (threshold 3), "
            "3) saran bundling lintas kategori, 4) range harga ideal jika harga kosong. "
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
        if isinstance(output, list):
            return "".join([str(x) for x in output])
        return str(output)
    except Exception as e:
        return f"Insight AI tidak tersedia: {e}"

@app.route('/')
def index():
    """Halaman utama menampilkan semua produk"""
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """Menambah produk baru ke katalog"""
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_type = request.form['product_type']
        size = request.form['size']
        quantity = int(request.form['quantity'])
        price = float(request.form.get('price', 0))
        
        # Validasi input
        if not product_name or not product_type or not size or quantity <= 0:
            flash('Semua field harus diisi dengan benar!', 'error')
            return redirect(url_for('add_product'))
        
        # Cek apakah produk sudah ada
        existing_product = next((p for p in products if p['name'].lower() == product_name.lower() and p['size'] == size), None)
        
        if existing_product:
            # Update jumlah jika produk sudah ada
            existing_product['quantity'] += quantity
            flash(f'Jumlah produk {product_name} ukuran {size} diperbarui!', 'success')
        else:
            # Tambah produk baru
            new_product = {
                'id': len(products) + 1,
                'name': product_name,
                'type': product_type,
                'size': size,
                'quantity': quantity,
                'price': price
            }
            products.append(new_product)
            flash(f'Produk {product_name} berhasil ditambahkan!', 'success')
        
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

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

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    """Menghapus produk dari katalog"""
    global products
    products = [p for p in products if p['id'] != product_id]
    flash('Produk berhasil dihapus!', 'success')
    return redirect(url_for('index'))

@app.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    """Update jumlah produk"""
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        return jsonify({'error': 'Produk tidak ditemukan'}), 404
    
    new_quantity = int(request.form['quantity'])
    if new_quantity <= 0:
        flash('Jumlah harus lebih dari 0!', 'error')
        return redirect(url_for('index'))
    
    product['quantity'] = new_quantity
    flash(f'Jumlah {product["name"]} diperbarui menjadi {new_quantity}!', 'success')
    return redirect(url_for('index'))

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

@app.route('/test_page')
def test_page():
    """Halaman test untuk AI"""
    return app.send_static_file('test_ai.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)