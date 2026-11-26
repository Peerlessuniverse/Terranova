@echo off
cd /d "%~dp0runtime"
echo TERRA NOVA cinematic: http://127.0.0.1:8790/
start "" http://127.0.0.1:8790/
python -m http.server 8790 --bind 127.0.0.1
