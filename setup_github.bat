@echo off
echo ========================================
echo GitHub Repository Setup
echo ========================================
echo.
echo This script will help you push your project to GitHub.
echo.
echo STEP 1: Create a new repository on GitHub
echo   1. Go to https://github.com/new
echo   2. Repository name: 2xkoGPAnalyzer (or your preferred name)
echo   3. Description: Broken draft proof of concept - 2XKO Gameplay Analyzer
echo   4. Set to Public or Private (your choice)
echo   5. DO NOT initialize with README, .gitignore, or license
echo   6. Click "Create repository"
echo.
echo STEP 2: Copy the repository URL
echo   It will look like: https://github.com/YOUR_USERNAME/2xkoGPAnalyzer.git
echo.
set /p REPO_URL="Enter your GitHub repository URL: "
echo.
echo Adding remote repository...
git remote add origin %REPO_URL%
echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main
echo.
echo Done! Your project should now be on GitHub.
echo.
pause
