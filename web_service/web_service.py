from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# Arka uç API'nizin adresi
API_URL = "https://eren-cloud.onrender.com"

# HTML GÜNCELLENDİ: Artık tek bir form ve tek bir buton var.
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
        li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; list-style-type: none; }
    </style>
</head>
<body>
    <h1>Mikro Hizmetli Selam!</h1>
    <p>İki alanı da doldur</p>
    
    <!-- 
      DEĞİŞİKLİK: 
      İki formu tek bir formda birleştirdik.
      Input'lara "isim1" ve "isim2" adlarını verdik.
      Tek bir buton bıraktık.
    -->
    <form method="POST">
        <input type="text" name="isim1" placeholder="İsmizi Yazınız" required>
        <br>
        <input type="text" name="isim2" placeholder="Şehrinizi Yazınız" required>
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

@app.route("/", methods=["GET", "POST"])
def index():
    # Eğer kullanıcı form gönderdiyse (POST)
    if request.method == "POST":
        # DEĞİŞİKLİK: 
        # "veri1" ve "veri2" olarak adlandırdığımız iki alanı da alıyoruz.
        veri1 = request.form.get("isim1")
        veri2 = request.form.get("isim2")
        
        # YENİ MANTIK:
        # Arka uca "isim" olarak iki ayrı istek gönderiyoruz.
        # Böylece listeye iki ayrı satır olarak eklenecekler.
        
        # 1. isteği (veri1) gönder
        if veri1:
            requests.post(API_URL + "/ziyaretciler", json={"isim": isim1})
            
        # 2. isteği (veri2) gönder
        if veri2:
            requests.post(API_URL + "/ziyaretciler", json={"isim": isim1})
        
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
