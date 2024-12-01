@echo off
echo ===== تثبيت المتطلبات =====
python -m pip install --upgrade pip
python -m pip install flask flask-sqlalchemy flask-login flask-wtf email-validator python-dotenv werkzeug==2.3.7 bootstrap-flask==2.2.0

echo ===== تشغيل التطبيق =====
python run.py
pause
