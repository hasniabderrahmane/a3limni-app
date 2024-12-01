@echo off
echo Installing requirements...
python -m pip install -r requirements.txt

echo Starting the application...
python run.py
pause
