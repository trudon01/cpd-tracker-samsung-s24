@echo off
REM CPD Tracker - Windows Native APK Build for Samsung S24
REM This script builds the Android APK using available Windows tools

echo ============================================================
echo 🚀 CPD TRACKER - SAMSUNG S24 APK BUILD (Windows Native)
echo ============================================================

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [INFO] Python detected, checking version...
python --version

REM Check if we're in the correct directory
if not exist "main.py" (
    echo [ERROR] main.py not found. Please run this script from the CPD project directory.
    pause
    exit /b 1
)

echo [INFO] Installing required Python packages...

REM Install buildozer and dependencies
pip install buildozer
pip install cython
pip install kivy
pip install pillow
pip install pytesseract
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

if %errorlevel% neq 0 (
    echo [WARNING] Some packages failed to install. Continuing anyway...
)

echo [INFO] Creating Android build environment...

REM Initialize buildozer (this will download Android SDK)
buildozer init

echo [INFO] Building Samsung S24 optimized APK...
echo [WARNING] This may take 30-90 minutes for the first build...

REM Build the APK
buildozer android debug

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo 🎉 APK BUILD COMPLETED SUCCESSFULLY!
    echo ============================================================
    echo.
    echo Your Samsung S24 APK has been created!
    echo.
    echo Location: bin\cpd*.apk
    echo.
    echo Next steps:
    echo 1. Transfer the APK to your Samsung S24
    echo 2. Enable "Install from unknown sources" in settings
    echo 3. Install the APK
    echo 4. Grant camera and storage permissions
    echo.
    echo The app includes:
    echo ✓ OCR text recognition
    echo ✓ Samsung S24 optimization
    echo ✓ Camera integration
    echo ✓ Google Drive sync
    echo ✓ CPD points tracking
    echo.
    
    REM Create timestamped deployment folder
    set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    set timestamp=%timestamp: =0%
    set deploy_folder=CPD_Samsung_S24_APK_%timestamp%
    
    mkdir "%deploy_folder%"
    copy bin\*.apk "%deploy_folder%\"
    copy buildozer.spec "%deploy_folder%\"
    copy main.py "%deploy_folder%\"
    copy cpd.kv "%deploy_folder%\"
    
    echo Deployment package created: %deploy_folder%
    echo ============================================================
    
) else (
    echo.
    echo ============================================================
    echo ❌ APK BUILD FAILED
    echo ============================================================
    echo.
    echo Common solutions:
    echo 1. Ensure you have Java JDK 8 installed
    echo 2. Make sure you have at least 5GB free disk space
    echo 3. Check your internet connection
    echo 4. Try running: pip install --upgrade buildozer
    echo.
    echo If the error mentions Android SDK:
    echo 1. Download Android Studio
    echo 2. Install Android SDK Platform-tools
    echo 3. Set ANDROID_HOME environment variable
    echo.
)

echo.
echo Press any key to exit...
pause >nul
