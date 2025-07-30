@echo off
REM GitHub Repository Setup for Samsung S24 CPD Tracker

echo ============================================================
echo 🚀 GITHUB SETUP - SAMSUNG S24 CPD TRACKER
echo ============================================================

echo [INFO] Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [INFO] Git detected! Setting up repository...

REM Initialize git repository if not already done
if not exist ".git" (
    echo [INFO] Initializing Git repository...
    git init
) else (
    echo [INFO] Git repository already exists
)

REM Create .gitignore for Android/Python project
echo [INFO] Creating .gitignore for Samsung S24 project...
echo # CPD Tracker - Samsung S24 > .gitignore
echo # Python >> .gitignore
echo __pycache__/ >> .gitignore
echo *.py[cod] >> .gitignore
echo *$py.class >> .gitignore
echo *.so >> .gitignore
echo .Python >> .gitignore
echo build/ >> .gitignore
echo develop-eggs/ >> .gitignore
echo dist/ >> .gitignore
echo downloads/ >> .gitignore
echo eggs/ >> .gitignore
echo .eggs/ >> .gitignore
echo lib/ >> .gitignore
echo lib64/ >> .gitignore
echo parts/ >> .gitignore
echo sdist/ >> .gitignore
echo var/ >> .gitignore
echo wheels/ >> .gitignore
echo *.egg-info/ >> .gitignore
echo .installed.cfg >> .gitignore
echo *.egg >> .gitignore
echo MANIFEST >> .gitignore
echo. >> .gitignore
echo # Buildozer >> .gitignore
echo .buildozer/ >> .gitignore
echo .buildozer_global/ >> .gitignore
echo bin/ >> .gitignore
echo. >> .gitignore
echo # Android >> .gitignore
echo *.apk >> .gitignore
echo *.ap_ >> .gitignore
echo *.dex >> .gitignore
echo *.class >> .gitignore
echo. >> .gitignore
echo # CPD Tracker specific >> .gitignore
echo cpd_tracker/ >> .gitignore
echo CPD_Samsung_S24_Ready_*/ >> .gitignore
echo. >> .gitignore
echo # IDE >> .gitignore
echo .vscode/ >> .gitignore
echo .idea/ >> .gitignore
echo *.swp >> .gitignore
echo *.swo >> .gitignore
echo. >> .gitignore
echo # OS >> .gitignore
echo .DS_Store >> .gitignore
echo Thumbs.db >> .gitignore

REM Add all files to git
echo [INFO] Adding files to Git...
git add .
git add .github/workflows/build-samsung-s24.yml

REM Check if there are changes to commit
git diff --staged --quiet
if %errorlevel% equ 0 (
    echo [INFO] No changes to commit
) else (
    echo [INFO] Committing Samsung S24 CPD Tracker files...
    git commit -m "Samsung S24 CPD Tracker with OCR - Initial commit

    Features:
    - OCR text recognition with Tesseract
    - Samsung S24 camera integration (1080x2340)
    - CPD points tracking with SQLite database
    - Google Drive synchronization
    - Material Design UI optimized for One UI
    - ARM64/ARMv7 architecture support
    - Android API 21-31 compatibility
    - Automated GitHub Actions APK build
    
    Ready for Samsung S24, S24+, and S24 Ultra deployment"
)

echo.
echo ============================================================
echo ✅ GIT REPOSITORY READY!
echo ============================================================
echo.
echo 📋 Next Steps:
echo.
echo 1️⃣ CREATE GITHUB REPOSITORY:
echo    • Go to: https://github.com/new
echo    • Repository name: cpd-tracker-samsung-s24
echo    • Description: CPD Tracker with OCR for Samsung S24
echo    • Make it Public (for free GitHub Actions)
echo    • Click "Create repository"
echo.
echo 2️⃣ CONNECT TO GITHUB:
echo    • Copy the repository URL from GitHub
echo    • Run: git remote add origin [YOUR_REPO_URL]
echo    • Example: git remote add origin https://github.com/username/cpd-tracker-samsung-s24.git
echo.
echo 3️⃣ PUSH AND BUILD:
echo    • git push -u origin main
echo    • GitHub Actions will automatically build your Samsung S24 APK!
echo.
echo 🎯 Expected Results:
echo    • Build time: 15-30 minutes
echo    • Output: Samsung S24 optimized APK
echo    • Download: From GitHub Actions artifacts
echo.
echo ============================================================

echo.
echo [OPTIONAL] Would you like me to show you the exact commands?
echo Press any key to see the GitHub commands, or close to continue manually...
pause >nul

echo.
echo ============================================================
echo 📋 EXACT GITHUB COMMANDS
echo ============================================================
echo.
echo After creating your GitHub repository, run these commands:
echo.
echo # Connect to your GitHub repository
echo git remote add origin https://github.com/YOUR_USERNAME/cpd-tracker-samsung-s24.git
echo.
echo # Push to GitHub and trigger APK build
echo git push -u origin main
echo.
echo # Check build status
echo echo "Go to: https://github.com/YOUR_USERNAME/cpd-tracker-samsung-s24/actions"
echo.
echo ============================================================
echo 🚀 YOUR SAMSUNG S24 APK WILL BE READY IN 15-30 MINUTES!
echo ============================================================

pause
