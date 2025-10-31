from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hello_cloud1_db_user:d7ZKfT6I8IUdEN9oRWWGCWDTbXhTRYBa@dpg-d3tjhcggjchc73fan1dg-a.oregon-postgres.render.com/hello_cloud1_db")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")

    if request.method == "POST":
        isim = request.json.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()

    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(isimler)

# Yeni: şehir endpoint'i — ziyaretciler ile aynı mantıkta
@app.route("/sehir", methods=["GET", "POST"])
def sehir():
    conn = connect_db()
    cur = conn.cursor()

    # Tablo adı sehirler — ziyaretciler ile çakışmaz
    cur.execute("CREATE TABLE IF NOT EXISTS sehirler (id SERIAL PRIMARY KEY, isim TEXT)")

    if request.method == "POST":
        # Hem "isim" hem de "sehir" alanlarını kabul edelim
        isim = request.json.get("isim") or request.json.get("sehir")
        if isim:
            cur.execute("INSERT INTO sehirler (isim) VALUES (%s)", (isim,))
            conn.commit()

    cur.execute("SELECT isim FROM sehirler ORDER BY id DESC LIMIT 10")
    sehirler = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(sehirler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
