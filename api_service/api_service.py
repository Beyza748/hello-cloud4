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

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()

    # Tabloya sehir sütunu ekledik
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id SERIAL PRIMARY KEY,
            isim TEXT,
            sehir TEXT
        )
    """)

    if request.method == "POST":
        data = request.json
        isim = data.get("isim")
        sehir = data.get("sehir")
        if isim and sehir:
            cur.execute(
                "INSERT INTO ziyaretciler (isim, sehir) VALUES (%s, %s)",
                (isim, sehir)
            )
            conn.commit()

    # Artık hem isim hem şehir çekiyoruz
    cur.execute("SELECT isim, sehir FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    ziyaretciler_list = [{"isim": row[0], "sehir": row[1]} for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(ziyaretciler_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
