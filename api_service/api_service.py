from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hello_cloud1_db_user:d7ZKfT6I8IUdEN9oRWWGCWDTbXhTRYBa@dpg-d3tjhcggjchc73fan1dg-a.oregon-postgres.render.com/hello_cloud1_db")

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT, mesaj TEXT)")
        conn.commit()
        if request.method == "POST":
            isim = request.json.get("isim")
            mesaj = request.json.get("mesaj")
            if isim:
                cur.execute("INSERT INTO ziyaretciler (isim, mesaj) VALUES (%s, %s)", (isim, mesaj))
                conn.commit()
        cur.execute("SELECT isim, mesaj FROM ziyaretciler ORDER BY id DESC LIMIT 10")
        rows = [{"isim": row[0], "mesaj": row[1]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
