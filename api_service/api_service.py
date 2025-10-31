from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://hello_cloud1_db_user:d7ZKfT6I8IUdEN9oRWWGCWDTbXhTRYBa@dpg-d3tjhcggjchc73fan1dg-a.oregon-postgres.render.com/hello_cloud1_db"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

# ----------------- ZİYARETÇİLER -----------------
@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()

    # Tabloyu oluştur
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id SERIAL PRIMARY KEY,
            isim TEXT
        )
    """)

    # POST ile veri ekle
    if request.method == "POST":
        isim = request.json.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()

    # GET ile son 10 ziyaretçiyi al
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(isimler)

# ----------------- ÖRNEK TEST -----------------
# POST isteği ile veri eklemek için örnek:
# curl -X POST http://localhost:5001/ziyaretciler \
#      -H "Content-Type: application/json" \
#      -d '{"isim": "Ahmet"}'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

