from flask import Flask, render_template_string, request, redirect
import requests
app = Flask(__name__)
API_URL = "https://hello-cloud4.onrender.com"
HTML = """
<!doctype html>
<html>
<head>
<title>Ziyaretci Defteri</title>
<style>
body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
h1 { color: #333; }
input, textarea { padding: 10px; font-size: 16px; margin: 5px auto; width: 300px; display: block; }
button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
.kart { background: white; margin: 10px auto; width: 320px; padding: 12px; border-radius: 8px; text-align: left; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
.kart strong { color: #4CAF50; }
</style>
</head>
<body>
<h1>Ziyaretci Defteri</h1>
<form method="POST">
<input type="text" name="isim" placeholder="Adinizi yazin" required>
<textarea name="mesaj" placeholder="Mesajinizi yazin" rows="3" required></textarea>
<button type="submit">Gonder</button>
</form>
<h3>Ziyaretciler:</h3>
{% for z in ziyaretciler %}
<div class="kart">
<strong>{{ z.isim }}</strong>
<p>{{ z.mesaj }}</p>
</div>
{% endfor %}
</body>
</html>
"""
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form.get("isim")
        mesaj = request.form.get("mesaj")
        requests.post(API_URL + "/ziyaretciler", json={"isim": isim, "mesaj": mesaj})
        return redirect("/")
    resp = requests.get(API_URL + "/ziyaretciler")
    ziyaretciler = resp.json() if resp.status_code == 200 else []
    return render_template_string(HTML, ziyaretciler=ziyaretciler)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
