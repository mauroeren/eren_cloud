from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# Arka uç API'nizin adresi
API_URL = "https://eren-cloud.onrender.com"

# Tüm HTML içeriği bir değişkende
HTML = """
<!doctype html>
<html>
<head>
    <title>Mikro Hizmetli Selam!</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
        h1 { color: #333; }
        input { padding: 10px; font-size: 16px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
        li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Mikro Hizmetli Selam!</h1>
    <p>Adını yaz</p>
    
    <form method="POST">
        <input type="text" name="isim" placeholder="Adını yaz" required>
        <button type="submit">Gönder</button>
    </form>
     <form method="POST">
        <input type="text" name="isim" placeholder="Adını yaz" required>
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
        isim = request.form.get("isim")
        # API'nin /ziyaretciler endpoint'ine POST isteği gönder
        requests.post(API_URL + "/ziyaretciler", json={"isim": isim})
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
