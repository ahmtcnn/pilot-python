# Kasıtlı eski base image — Trivy image scan CVE bulmalı
FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000
# --- Trivy misconfig: root user ---
CMD ["python", "app.py"]
