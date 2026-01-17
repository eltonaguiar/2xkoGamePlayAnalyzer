@echo off
echo Starting web server from output directory...
echo.
echo Make sure you're in the output directory!
echo Files should be accessible at:
echo   http://localhost:8000/video_player.html
echo   http://localhost:8000/clips/mistake_unknown_0.mp4
echo.
cd /d "%~dp0"
python -m http.server 8000
pause
