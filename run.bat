@echo off
call .venv\Scripts\activate
set PYTHONPATH=%CD%\src
set SECRET_KEY=123
start http://127.0.0.1:5000
python src/app.py
pause