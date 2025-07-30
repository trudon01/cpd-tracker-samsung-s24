
# CPD Tracker Android App - Complete Setup Guide

## Overview
This is a professional CPD (Continuing Professional Development) Tracker Android app built with Python, Kivy, and KivyMD. The app allows users to track their professional development activities with photos, automatic backups to Google Drive, and a clean, modern interface.

## Features
- ✅ Professional Material Design UI
- ✅ Date validation and form validation
- ✅ Camera integration for photo evidence
- ✅ SQLite database with proper indexing
- ✅ Automatic backup every 2 weeks
- ✅ Google Drive integration
- ✅ Activity type selection (Paper, Conference, Project, Course, Other)
- ✅ Detailed description support
- ✅ Cross-platform compatibility

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Git
- Android SDK (for building APK)
- Google account (for Drive integration)

### VS Code Extensions (Recommended)
- Python extension
- Kivy extension
- Android extensions

## Step-by-Step Setup

### 1. Environment Setup

#### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv cpd_env

# Activate virtual environment
.\cpd_env\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

#### Linux/macOS
```bash
# Create virtual environment
python3 -m venv cpd_env

# Activate virtual environment
source cpd_env/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

### 2. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# For development/testing
pip install pytest black flake8
```

### 3. Google Drive API Setup

#### Step 3.1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Drive API
4. Go to "Credentials" section

#### Step 3.2: Create Service Account
1. Click "Create Credentials" → "Service Account"
2. Fill in service account details
3. Download the JSON key file
4. Rename it to `credentials.json`
5. Place it in the project root directory

#### Step 3.3: Share Drive Folder
1. Create a folder in Google Drive named "CPD Points"
2. Share it with the service account email (found in credentials.json)
3. Give "Editor" permissions

### 4. Test the Application

#### Desktop Testing
```bash
# Run the app
python main.py
```

#### Test Database
```bash
# Check if database is created
ls cpd_tracker/
# Should show: cpd.db

# Test Google Drive connection (optional)
python -c "from drive_upload import test_drive_connection; test_drive_connection()"
```

### 5. Building for Android

#### Install Buildozer
```bash
# Install buildozer for Android builds
pip install buildozer

# Initialize buildozer (first time only)
buildozer init
```

#### Build APK
```bash
# Build debug APK
buildozer android debug

# Build release APK (for distribution)
buildozer android release
```

### 6. Project Structure
```
cpd_tracker_app/
├── main.py                 # Main application file
├── cpd.kv                  # UI layout file
├── database.py             # Database operations
├── backup.py               # Backup management
├── drive_upload.py         # Google Drive integration
├── requirements.txt        # Python dependencies
├── buildozer.spec          # Android build configuration
├── credentials.json        # Google Drive API credentials (you create this)
└── cpd_tracker/           # App data directory
    ├── cpd.db             # SQLite database (auto-created)
    ├── backups/           # Local backups
    └── assets/
        └── photos/        # Photo storage
```

## Usage Instructions

### Adding a CPD Entry
1. **Start Date**: Enter in YYYY-MM-DD format
2. **End Date**: Enter in YYYY-MM-DD format
3. **Activity Name**: Enter descriptive name
4. **Type**: Select from chips (Paper, Conference, Project, Course, Other)
5. **Description**: Enter detailed information
6. **Photo**: Tap "Take Photo" to capture evidence
7. **Submit**: Tap "Submit Entry" to save

### Backup System
- **Automatic**: Backups occur every 2 weeks automatically
- **Manual**: Force backup by adding entries (triggers check)
- **Storage**: Local backups + Google Drive upload
- **Contents**: Database + all photos in zip format

### Database Features
- **Validation**: Dates, required fields, format checking
- **Indexing**: Optimized for fast searches
- **Logging**: Backup history tracking
- **Recovery**: Full data restoration from backups

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Solution: Ensure virtual environment is activated
# Windows
.\cpd_env\Scripts\Activate.ps1
# Linux/macOS  
source cpd_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Google Drive Authentication
```
Error: credentials.json not found
```
**Solution**: Follow Step 3 to create and download credentials.json

#### 3. Camera Permissions (Android)
```
Error: Camera permission denied
```
**Solution**: Grant camera permissions in Android settings

#### 4. Build Errors
```bash
# Clean build directory
buildozer clean

# Update buildozer
pip install --upgrade buildozer

# Rebuild
buildozer android debug
```

### Development Tips

#### VS Code Configuration
1. Set Python interpreter to virtual environment
2. Install Python and Kivy extensions
3. Configure debugging for Python files

#### Testing
```bash
# Test individual components
python -c "from database import init_db; init_db()"
python -c "from backup import test_drive_connection; test_drive_connection()"
```

#### Debugging
```python
# Add logging to any file
from kivy.logger import Logger
Logger.info("CPD: Debug message here")
```

## Deployment

### For Testing
1. Build debug APK: `buildozer android debug`
2. Install on device: `adb install bin/cpdtracker-0.1-debug.apk`

### For Production
1. Build release APK: `buildozer android release`
2. Sign the APK for Play Store distribution
3. Test thoroughly on multiple devices

## Maintenance

### Regular Tasks
- Monitor Google Drive storage quota
- Check backup logs in database
- Update dependencies periodically
- Test on new Android versions

### Updates
- Modify version in `buildozer.spec`
- Update requirements as needed
- Test thoroughly before deployment

## Security Notes

### Credentials
- Never commit `credentials.json` to version control
- Use environment variables for sensitive data in production
- Regularly rotate API keys

### Permissions
- App requests only necessary permissions
- Camera and storage access for core functionality
- Internet access for Google Drive sync

## Support

### Getting Help
1. Check this README for common solutions
2. Review error logs in VS Code terminal
3. Check Kivy/KivyMD documentation
4. Verify Google Drive API quotas

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## Version History

### v1.0.0 (Current)
- Initial release
- Core CPD tracking functionality
- Google Drive backup integration
- Professional Material Design UI
- Camera photo capture
- Automatic backup scheduling

---

**Ready to go!** Run `python main.py` to start the application.

