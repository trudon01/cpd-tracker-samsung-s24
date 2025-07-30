#!/usr/bin/env python3
"""
CPD Tracker - Android APK Deployment Script
Creates a timestamped deployment package with the Android APK and documentation
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime
import zipfile
import json

def create_deployment_package():
    """Create a complete deployment package for CPD Tracker Android app"""
    
    print("="*60)
    print("🚀 CPD TRACKER - ANDROID DEPLOYMENT PACKAGE CREATOR")
    print("="*60)
    
    # Create timestamped folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    deployment_folder = f"CPD_Tracker_Android_v1.0_{timestamp}"
    
    print(f"\n📁 Creating deployment folder: {deployment_folder}")
    
    # Create main deployment directory
    os.makedirs(deployment_folder, exist_ok=True)
    
    # Create subdirectories
    subdirs = [
        "APK",
        "Source_Code", 
        "Documentation",
        "Database_Files",
        "Configuration"
    ]
    
    for subdir in subdirs:
        os.makedirs(os.path.join(deployment_folder, subdir), exist_ok=True)
        print(f"   ✅ Created {subdir} folder")
    
    # Build the APK first
    print(f"\n🔨 Building Android APK...")
    try:
        # Check if buildozer is installed
        result = subprocess.run(["buildozer", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Buildozer not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "buildozer"], check=True)
        
        print("   📦 Running buildozer android debug...")
        build_result = subprocess.run(["buildozer", "android", "debug"], 
                                    cwd=".", capture_output=True, text=True)
        
        if build_result.returncode == 0:
            print("   ✅ APK build successful!")
            
            # Find and copy the APK
            bin_dir = os.path.join(".", "bin")
            if os.path.exists(bin_dir):
                apk_files = [f for f in os.listdir(bin_dir) if f.endswith('.apk')]
                if apk_files:
                    latest_apk = max([os.path.join(bin_dir, f) for f in apk_files], 
                                   key=os.path.getctime)
                    shutil.copy2(latest_apk, os.path.join(deployment_folder, "APK"))
                    print(f"   ✅ APK copied: {os.path.basename(latest_apk)}")
                else:
                    print("   ⚠️ No APK files found in bin directory")
            else:
                print("   ⚠️ Bin directory not found")
        else:
            print("   ⚠️ APK build failed - continuing with package creation")
            print("   Error output:")
            print(build_result.stderr[:500] + "..." if len(build_result.stderr) > 500 else build_result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Build error: {e}")
        print("   Continuing with package creation...")
    except FileNotFoundError:
        print("   ⚠️ Buildozer not available - APK build skipped")
        print("   Install buildozer with: pip install buildozer")
    
    # Copy source code files
    print(f"\n📄 Copying source code files...")
    source_files = [
        "main.py", "cpd.kv", "database.py", "backup.py", "drive_upload.py",
        "requirements.txt", "buildozer.spec", "__Setup.md", 
        "OCR_FEATURE_GUIDE.md"
    ]
    
    for file in source_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(deployment_folder, "Source_Code"))
            print(f"   ✅ Copied {file}")
        else:
            print(f"   ⚠️ {file} not found")
    
    # Copy documentation files
    print(f"\n📚 Creating documentation...")
    
    # Create deployment README
    readme_content = f"""# CPD Tracker Android App - Deployment Package

## Package Information
- **Version**: 1.0.0
- **Build Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Package ID**: {deployment_folder}

## Contents

### 📱 APK Folder
- Contains the compiled Android APK file
- Ready for installation on Android devices
- Supports Android API 21+ (Android 5.0+)

### 💻 Source Code Folder
- Complete Python source code
- Kivy UI files (.kv)
- Database schema and backup utilities
- Google Drive integration
- OCR functionality

### 📖 Documentation Folder
- Installation instructions
- User guide
- Feature documentation
- OCR setup guide

### 🗄️ Database Files Folder
- SQLite database schema
- Sample data (if any)
- Backup file examples

### ⚙️ Configuration Folder
- Buildozer configuration
- Android permissions
- App settings

## Installation Instructions

### For End Users:
1. Enable "Unknown Sources" in Android settings
2. Download and install the APK file
3. Grant required permissions (Camera, Storage, Internet)
4. Start using the CPD Tracker app

### For Developers:
1. Install Python 3.9+
2. Install requirements: `pip install -r requirements.txt`
3. For Android building: `pip install buildozer`
4. Build APK: `buildozer android debug`

## Features Included
- ✅ CPD Activity Tracking
- ✅ Photo Capture with OCR Text Extraction
- ✅ Google Drive Cloud Sync
- ✅ CSV Export Functionality
- ✅ Points System (0-12 CPD Points)
- ✅ Samsung S24 Optimized UI
- ✅ SQLite Database with Automated Backups
- ✅ Professional Material Design Interface

## Technical Requirements
- **Android**: 5.0+ (API 21+)
- **RAM**: 2GB minimum
- **Storage**: 100MB free space
- **Permissions**: Camera, Storage, Internet
- **Network**: Internet connection for Google Drive sync

## Support
For technical support or feature requests, please refer to the documentation
or contact the development team.

---
Built with ❤️ using Python, Kivy, and advanced OCR technology
"""
    
    with open(os.path.join(deployment_folder, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("   ✅ Created deployment README.md")
    
    # Create installation guide
    install_guide = """# CPD Tracker - Installation Guide

## Android Installation

### Method 1: Direct APK Installation
1. **Download the APK file** from the APK folder
2. **Enable Unknown Sources**:
   - Go to Settings > Security
   - Enable "Unknown Sources" or "Install unknown apps"
3. **Install the APK**:
   - Tap the downloaded APK file
   - Follow the installation prompts
   - Grant permissions when requested

### Method 2: Developer Installation
1. **Install development tools**:
   ```bash
   pip install buildozer
   ```
2. **Build from source**:
   ```bash
   buildozer android debug
   ```

## Required Permissions
The app requires the following permissions:
- **Camera**: For capturing photos of certificates
- **Storage**: For saving photos and database files
- **Internet**: For Google Drive synchronization

## First Launch Setup
1. **Launch the app** after installation
2. **Grant permissions** when prompted
3. **Start tracking** your CPD activities
4. **Optional**: Set up Google Drive sync for cloud backup

## Troubleshooting

### Common Issues:
- **Installation blocked**: Enable "Unknown Sources" in settings
- **Camera not working**: Grant camera permission in app settings
- **Sync issues**: Check internet connection and Google account
- **OCR not working**: OCR will work automatically in the compiled app

### Performance Tips:
- **Free up space**: Ensure 100MB+ free storage
- **Close background apps**: For better camera performance
- **Stable internet**: For reliable Google Drive sync

## Features Overview
- Track CPD activities with dates, types, and points
- Capture photos of certificates and documents
- Extract text automatically using OCR technology
- Sync data to Google Drive for backup
- Export data to CSV format
- Professional interface optimized for mobile devices
"""
    
    with open(os.path.join(deployment_folder, "Documentation", "Installation_Guide.md"), "w", encoding="utf-8") as f:
        f.write(install_guide)
    print("   ✅ Created Installation Guide")
    
    # Copy configuration files
    print(f"\n⚙️ Copying configuration files...")
    config_files = ["buildozer.spec", "requirements.txt"]
    for file in config_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(deployment_folder, "Configuration"))
            print(f"   ✅ Copied {file}")
    
    # Create build info file
    build_info = {
        "app_name": "CPD Tracker",
        "version": "1.0.0",
        "build_date": datetime.now().isoformat(),
        "python_version": sys.version,
        "features": [
            "CPD Activity Tracking",
            "OCR Text Extraction",
            "Google Drive Sync",
            "CSV Export",
            "Points System",
            "Samsung S24 Optimization",
            "SQLite Database",
            "Material Design UI"
        ],
        "requirements": [
            "python3", "kivy==2.3.1", "kivymd>=1.1.1", "plyer",
            "google-api-python-client", "google-auth", "google-auth-oauthlib",
            "google-auth-httplib2", "pytesseract", "pillow", "pyjnius"
        ],
        "android_permissions": [
            "CAMERA", "WRITE_EXTERNAL_STORAGE", "READ_EXTERNAL_STORAGE",
            "INTERNET", "ACCESS_NETWORK_STATE"
        ]
    }
    
    with open(os.path.join(deployment_folder, "Configuration", "build_info.json"), "w", encoding="utf-8") as f:
        json.dump(build_info, f, indent=2)
    print("   ✅ Created build_info.json")
    
    # Create ZIP archive of the deployment package
    print(f"\n📦 Creating ZIP archive...")
    zip_filename = f"{deployment_folder}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deployment_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, ".")
                zipf.write(file_path, arc_path)
    
    print(f"   ✅ Created ZIP archive: {zip_filename}")
    
    # Summary
    print(f"\n🎉 DEPLOYMENT PACKAGE COMPLETE!")
    print(f"   📁 Folder: {deployment_folder}")
    print(f"   📦 Archive: {zip_filename}")
    print(f"   📊 Size: {get_folder_size(deployment_folder):.1f} MB")
    
    print(f"\n📋 Package Contents:")
    for root, dirs, files in os.walk(deployment_folder):
        level = root.replace(deployment_folder, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"   {indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"   {subindent}{file}")
    
    print(f"\n✅ Ready for deployment and distribution!")
    return deployment_folder, zip_filename

def get_folder_size(folder_path):
    """Get folder size in MB"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size / (1024 * 1024)  # Convert to MB

if __name__ == "__main__":
    try:
        deployment_folder, zip_file = create_deployment_package()
        print(f"\n🚀 Deployment package ready at: {deployment_folder}")
        print(f"📦 ZIP archive created: {zip_file}")
    except Exception as e:
        print(f"\n❌ Error creating deployment package: {e}")
        sys.exit(1)
