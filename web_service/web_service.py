from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# Arka uç API'nizin adresi
API_URL = "https://eren-cloud.onrender.com"

# HTML GÜNCELLENDİ: Sadece CSS (stil) kısmı değişti.
HTML = """
<!doctype html>
<html>
<head>
    <title>Mikro Hizmetli Selam!</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
        h1 { color: #333; }
        input { padding: 10px; font-size: 16px; margin: 5px; } /* Dikeyde boşluk eklendi */
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; margin-top: 10px;}
        
        /* Liste başındaki varsayılan boşluğu kaldır */
        ul {
            padding: 0;
            margin-top: 15px;
        }

        /* --- DEĞİŞİKLİK BURADA --- */
        li { 
            background: white; 
            margin: 5px; /* Öğeler arası boşluk */
            padding: 8px 12px; /* İç boşluk */
            border-radius: 5px; 
            list-style-type: none; 
            display: inline-block; /* Öğeleri yan yana dizler */
            width: auto; /* Genişliği içeriğe göre ayarlar */
            box-shadow: 0 1px 3px rgba(0,0,0,0.1); /* Hafif gölge */
        }
    </style>
</head>
<body>
    <h1>Mikro Hizmetli Selam!</h1>
    <p>İki alanı da doldur</p>
    
    <!-- 
      Form yapısı (HTML) aynı kaldı.
    -->
    <form method="POST">
        <input type="text" name="veri1" placeholder="İlk veriyi yaz" required>
        <br>
        <input type="text" name="veri2" placeholder="İkinci veriyi yaz" required>
        <br>
        <button type="submit">Gönder</button>
    </form>
    
    <h3>Ziyaretçiler:</h3>
    <ul>
        {% for ad in isimler %}
            <li>{{ ad }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# @app.route VE index() FONKSİYONU TAMAMEN AYNI KALDI
@app.route("/", methods=["GET", "POST"])
def index():
    # Eğer kullanıcı form gönderdiyse (POST)
    if request.method == "POST":
        # "veri1" ve "veri2" olarak adlandırdığımız iki alanı da alıyoruz.
        veri1 = request.form.get("veri1")
        veri2 = request.form.get("veri2")
        
        # YENİ MANTIK:
        # Arka uca "isim" olarak iki ayrı istek gönderiyoruz.
        # Böylece listeye iki ayrı satır olarak eklenecekler.
        
        # 1. isteği (veri1) gönder
        if veri1:
            requests.post(API_URL + "/ziiyaretciler", json={"isim": veri1})
            
        # 2. isteği (veri2) gönder
        if veri2:
            requests.post(API_URL + "/ziyaretciler", json={"isim": veri2})
        
        # Sayfayı yenilemek için ana sayfaya yönlendir
        return redirect("/")

    # Eğer normal sayfa ziyaretiyse (GET)
    # API'nin /ziyaretciler endpoint'inden verileri çek
    resp = requests.get(API_URL + "/ziyaretciler")
    
    # İstek başarılıysa JSON verisini al, değilse boş liste kullan
    isimler = resp.json() if resp.status_code == 200 else []
    
    # HTML şablonunu ve isimler listesini kullanarak sayfayı oluştur
    return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__":
    # Uygulamayı 0.0.0.0 (herkese açık) adresinde ve 5000 portunda çalıştır
    app.run(host="0.0.0.0", port=5000)
