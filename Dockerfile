# TERRA NOVA game server (Python stdlib only, SQLite on a Fly volume at /data)
FROM python:3.13-slim
# TN_ADMIN_USERS empty = no admin on the public server; the owner enables one with: fly secrets set TN_ADMIN_USERS=namaakun
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    TN_HOST=0.0.0.0 PORT=8080 TN_DB_PATH=/data/gaia.sqlite3 \
    TN_ADMIN_USERS=""
WORKDIR /app
COPY server.py ./
COPY engine/ engine/
COPY data/ data/
COPY web/ web/
COPY cinematic-web/runtime/ cinematic-web/runtime/
EXPOSE 8080
CMD ["python", "server.py"]
