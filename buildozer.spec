[app]

# (str) Title of your application
title = CPD Tracker

# (str) Package name
package.name = cpdtracker

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example.cpdtracker

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,db,txt,md

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.3.1,kivymd>=1.1.1,plyer,google-api-python-client,google-auth,google-auth-oauthlib,google-auth-httplib2,pytesseract,pillow,pyjnius,sqlite3

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[android]

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references = @jar/my-android-jar.jar

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = apk

# (list) Permissions
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 31

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

[ios]

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios

# Automatic signing
ios.codesign.allowed = false
