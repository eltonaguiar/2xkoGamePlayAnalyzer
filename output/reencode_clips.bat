@echo off
echo Re-encoding video clips to H.264 for browser compatibility...
echo.
cd /d "%~dp0"
python reencode_clips.py
pause
