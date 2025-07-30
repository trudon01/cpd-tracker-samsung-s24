# CPD Tracker - Installation Guide

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
