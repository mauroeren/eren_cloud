from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Veritabanı URL'sini ortam değişkeninden al veya varsayılanı kullan
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mauro_cloudsql3_dp_user:mRxhA3XBmFmkKcTgB5B4HoacB0xMekxR@dpg-d425jje3jp1c73abvcj0-a.oregon-postgres.render.com/mauro_cloudsql3_dp"
)

def connect_db():
    """Veritabanına bağlanmak için yardımcı fonksiyon."""
    return psycopg2.connect(DATABASE_URL)

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    """
    GET isteği ile son 10 ziyaretçiyi listeler.
    POST isteği ile yeni ziyaretçi ekler.
    """
    
    conn = connect_db()
    cur = conn.cursor()

    # Ziyaretçiler tablosu yoksa oluşturur
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")

    # Eğer istek POST ise, yeni veriyi ekle
    if request.method == "POST":
        isim = request.json.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()

    # Her durumda (GET veya POST sonrası) son 10 ismi çek
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    
    # Gelen veriyi (tuple listesi) düz bir listeye çevir
    isimler = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    # İsim listesini JSON formatında döndür
    return jsonify(isimler)

if __name__ == "__main__":
    # Uygulamayı 0.0.0.0 (herkese açık) adresinde ve 5001 portunda çalıştır
    app.run(host="0.0.0.0", port=5001)
