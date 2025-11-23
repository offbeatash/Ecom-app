@echo off
echo ========================================================
echo       E-Commerce App - GitHub Update Script
echo ========================================================
echo.
echo This script will:
echo 1. Initialize a new git repository.
echo 2. Commit your secure code.
echo 3. Force push to GitHub to OVERWRITE the insecure history.
echo.
echo WARNING: This will replace the code on your GitHub repository
echo with the code in this folder.
echo.

set /p repo_url="Enter your GitHub Repository URL (e.g., https://github.com/username/repo.git): "

if "%repo_url%"=="" (
    echo Error: Repository URL cannot be empty.
    pause
    exit /b
)

echo.
echo Initializing Git...
git init

echo.
echo Adding files...
git add .

echo.
echo Committing changes...
git commit -m "Refactor: Secure secrets and fix bugs"

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Adding remote origin...
git remote remove origin 2>nul
git remote add origin %repo_url%

echo.
echo Pushing to GitHub (Force)...
git push -u origin main --force

echo.
echo ========================================================
echo Done! Check your GitHub repository.
echo NOTE: Remember to add your .env secrets to your hosting
echo provider if you deploy this app (e.g., Vercel, Heroku).
echo ========================================================
pause
