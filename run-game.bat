@echo off
rem TERRA NOVA - jalankan server lokal lalu buka browser. Biarkan jendela ini terbuka selama bermain.
cd /d "%~dp0"
start "" http://127.0.0.1:8765/
py -3 server.py || python server.py
pause
