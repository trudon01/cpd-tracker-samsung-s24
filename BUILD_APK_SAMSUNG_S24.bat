@echo off
REM CPD Tracker - Windows APK Build Launcher for Samsung S24
REM This script sets up WSL and builds the Android APK

echo ============================================================
echo 🚀 CPD TRACKER - SAMSUNG S24 APK BUILD LAUNCHER
echo ============================================================

REM Check if WSL is installed
wsl --status >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] WSL is not installed or not working properly
    echo.
    echo Installing WSL2...
    wsl --install --distribution Ubuntu
    echo.
    echo [INFO] WSL2 installation initiated. Please reboot your computer
    echo [INFO] After reboot, run this script again to build the APK
    pause
    exit /b 1
)

echo [INFO] WSL detected, checking distribution...

REM List WSL distributions
wsl -l -v

echo.
echo [INFO] Starting APK build process in WSL...
echo [WARNING] This process may take 30-60 minutes for the first build
echo.

REM Make the script executable and run it
wsl chmod +x /mnt/c/1Python/13_CPD_Android_Program/build_samsung_s24_apk.sh
wsl bash /mnt/c/1Python/13_CPD_Android_Program/build_samsung_s24_apk.sh

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo 🎉 APK BUILD COMPLETED SUCCESSFULLY!
    echo ============================================================
    echo.
    echo Your Samsung S24 optimized APK is ready!
    echo Check the generated folder for:
    echo  - Android APK file
    echo  - Samsung S24 installation guide
    echo  - Complete documentation
    echo.
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo ❌ APK BUILD FAILED
    echo ============================================================
    echo.
    echo Please check the error messages above and try again.
    echo Common solutions:
    echo  1. Ensure internet connection is stable
    echo  2. Make sure you have enough disk space (5GB+)
    echo  3. Try running the script again
    echo.
)

echo.
echo Press any key to exit...
pause >nul
