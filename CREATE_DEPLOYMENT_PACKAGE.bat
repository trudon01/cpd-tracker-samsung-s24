@echo off
REM Quick deployment package creator for Samsung S24

echo ============================================================
echo 📦 CREATING SAMSUNG S24 DEPLOYMENT PACKAGE
echo ============================================================

REM Generate timestamp
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
set deploy_folder=CPD_Samsung_S24_Ready_%timestamp%

echo [INFO] Creating deployment folder: %deploy_folder%
mkdir "%deploy_folder%"

REM Copy source files
echo [INFO] Copying source files...
copy main.py "%deploy_folder%\"
copy cpd.kv "%deploy_folder%\"
copy database.py "%deploy_folder%\"
copy backup.py "%deploy_folder%\"
copy drive_upload.py "%deploy_folder%\"
copy requirements.txt "%deploy_folder%\"
copy buildozer.spec "%deploy_folder%\"

REM Copy any existing APK files
if exist "bin\*.apk" (
    echo [INFO] Copying existing APK files...
    copy bin\*.apk "%deploy_folder%\"
)

REM Create installation guide
echo Creating Samsung S24 installation guide...
echo # Samsung S24 Installation Guide > "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo. >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo ## Quick Install Steps >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo. >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo 1. **Transfer APK** to your Samsung S24 via USB, email, or cloud >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo 2. **Enable Unknown Sources**: >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo    - Go to Settings ^> Apps ^> Special access ^> Install unknown apps >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo    - Enable for File Manager or your browser >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo 3. **Install APK**: Tap the APK file and select Install >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo 4. **Grant Permissions**: Allow camera and storage access when prompted >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo 5. **Launch**: Find "CPD Tracker" in your app drawer >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo. >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo ## App Features >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo. >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo - 📸 **Camera Integration**: Optimized for Samsung S24 camera >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo - 🔍 **OCR Text Recognition**: Extract text from certificates and documents >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo - 📊 **CPD Points Tracking**: Automatic calculation and progress tracking >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo - ☁️ **Google Drive Sync**: Automatic backup to cloud storage >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"
echo - 🎨 **Samsung UI**: Material Design optimized for One UI >> "%deploy_folder%\INSTALL_ON_SAMSUNG_S24.md"

REM Create build instructions
echo Creating build instructions...
echo # How to Build APK > "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo. >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo To build the APK from source: >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo. >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo ## Method 1: Windows Native >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo ``` >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo BUILD_WINDOWS_NATIVE.bat >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo ``` >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo. >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo ## Method 2: Manual Buildozer >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo ``` >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo pip install buildozer >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo buildozer android debug >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"
echo ``` >> "%deploy_folder%\BUILD_INSTRUCTIONS.md"

echo.
echo ============================================================
echo ✅ DEPLOYMENT PACKAGE READY!
echo ============================================================
echo.
echo 📁 Package Location: %deploy_folder%
echo.
echo 📋 Package Contents:
echo   • Source code files
echo   • Build configuration
echo   • Installation guide
echo   • Build instructions
if exist "bin\*.apk" (
    echo   • Pre-built APK files
)
echo.
echo 🚀 Ready for Samsung S24 deployment!
echo.

explorer "%deploy_folder%"

echo Press any key to exit...
pause >nul
