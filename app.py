"""
Pilot Python (Flask) — KASITLI ZAFİYETLİ.
Sadece AppSec pipeline'ını test etmek için. Production'da KULLANMA.
"""
import os
import sqlite3
import subprocess
from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

# --- SECRET SCAN: hardcoded creds (gerçek-görünümlü ama FAKE) ---
# NOT: "EXAMPLE" eki olan AWS değerleri Gitleaks allowlist'inde, o yüzden farklı pattern.
AWS_ACCESS_KEY_ID = "AKIAZ7XYK4NMBPLMQ8XY"                       # gitleaks: aws-access-token
AWS_SECRET_ACCESS_KEY = "vN3pQ7tR9sL2mX5kJ8hG6fD4cB1zA0yU3wE7iO9p"
GITHUB_TOKEN = "ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789AB"      # gitleaks: github-pat
SLACK_WEBHOOK = "https://hooks.slack.com/services/T07A1B2C3D4/B07E5F6G7H8/JkLmNoPqRsTuVwXyZ012abc"
STRIPE_KEY = "sk_live_51HxYzAbCdEfGhIjKlMnOpQrStUvWxYz0123456789abcdef0123"
JWT_SECRET = "hardcoded-jwt-secret-do-not-use"
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAvR8Dn2k4l7G9aZj6r3sNkX1pY4mQ2zT5eC8wPq0bF7vH9uL3
fAKEKEYfAKEKEYfAKEKEYfAKEKEYfAKEKEYfAKEKEYfAKEKEYfAKEKEYfAKEKEY
-----END RSA PRIVATE KEY-----"""


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INT, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'alice'), (2, 'bob')")
    return conn


@app.route("/")
def index():
    return "Pilot Python — vulnerable demo"


@app.route("/user")
def user():
    # --- SAST: SQL Injection (string formatting) ---
    name = request.args.get("name", "")
    conn = get_db()
    query = "SELECT * FROM users WHERE name = '%s'" % name   # Semgrep yakalar
    rows = conn.execute(query).fetchall()
    return {"rows": rows}


@app.route("/ping")
def ping():
    # --- SAST: Command Injection ---
    host = request.args.get("host", "127.0.0.1")
    result = subprocess.check_output("ping -c 1 " + host, shell=True)  # Semgrep yakalar
    return result


@app.route("/greet")
def greet():
    # --- SAST + ZAP DAST: Reflected XSS ---
    name = request.args.get("name", "world")
    template = "<h1>Hello %s</h1>" % name                    # Semgrep yakalar, ZAP da
    return render_template_string(template)


@app.route("/go")
def go():
    # --- ZAP DAST: Open Redirect ---
    target = request.args.get("url", "/")
    return redirect(target)


if __name__ == "__main__":
    # --- SAST: debug=True production'da tehlikeli ---
    app.run(host="0.0.0.0", port=5000, debug=True)
