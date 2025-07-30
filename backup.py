import os
import zipfile
import shutil
from datetime import datetime, timedelta
from database import get_entries_count, log_backup, get_last_backup_date
from drive_upload import upload_to_drive
from kivy.logger import Logger
import threading

# Backup configuration
BACKUP_INTERVAL_DAYS = 14  # 2 weeks
BACKUP_DIR = "cpd_tracker/backups"
DB_PATH = "cpd_tracker/cpd.db"
PHOTOS_DIR = "cpd_tracker/assets/photos"

def ensure_backup_directory():
    """Ensure backup directory exists"""
    os.makedirs(BACKUP_DIR, exist_ok=True)

def create_backup():
    """Create a complete backup of database and photos"""
    try:
        ensure_backup_directory()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)
        
        # Copy database
        if os.path.exists(DB_PATH):
            db_dst = os.path.join(backup_folder, "cpd.db")
            shutil.copy2(DB_PATH, db_dst)
            Logger.info("CPD: Database copied to backup")
        
        # Copy photos
        photos_backup_dir = os.path.join(backup_folder, "photos")
        if os.path.exists(PHOTOS_DIR):
            shutil.copytree(PHOTOS_DIR, photos_backup_dir, dirs_exist_ok=True)
            Logger.info("CPD: Photos copied to backup")
        else:
            os.makedirs(photos_backup_dir, exist_ok=True)
        
        # Create zip file
        zip_path = f"{backup_folder}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_folder)
                    zipf.write(file_path, arcname)
        
        # Clean up temporary folder
        shutil.rmtree(backup_folder)
        
        # Get entries count for logging
        entries_count = get_entries_count()
        
        Logger.info(f"CPD: Backup created successfully: {zip_path}")
        return zip_path, entries_count
        
    except Exception as e:
        Logger.error(f"CPD: Error creating backup: {e}")
        raise

def upload_backup_to_drive(zip_path):
    """Upload backup to Google Drive"""
    try:
        upload_to_drive(zip_path)
        Logger.info(f"CPD: Backup uploaded to Google Drive: {zip_path}")
        return True
    except Exception as e:
        Logger.error(f"CPD: Error uploading backup to Google Drive: {e}")
        return False

def cleanup_old_backups(keep_count=10):
    """Clean up old local backup files, keeping only the most recent ones"""
    try:
        if not os.path.exists(BACKUP_DIR):
            return
        
        # Get all backup files
        backup_files = [f for f in os.listdir(BACKUP_DIR) if f.startswith("backup_") and f.endswith(".zip")]
        backup_files.sort(reverse=True)  # Most recent first
        
        # Remove old backups
        for backup_file in backup_files[keep_count:]:
            backup_path = os.path.join(BACKUP_DIR, backup_file)
            try:
                os.remove(backup_path)
                Logger.info(f"CPD: Removed old backup: {backup_file}")
            except Exception as e:
                Logger.warning(f"CPD: Could not remove backup {backup_file}: {e}")
                
    except Exception as e:
        Logger.error(f"CPD: Error cleaning up old backups: {e}")

def is_backup_needed():
    """Check if backup is needed based on last backup date"""
    try:
        last_backup = get_last_backup_date()
        if not last_backup:
            return True
        
        last_backup_date = datetime.strptime(last_backup, "%Y-%m-%d %H:%M:%S")
        days_since_backup = (datetime.now() - last_backup_date).days
        
        return days_since_backup >= BACKUP_INTERVAL_DAYS
        
    except Exception as e:
        Logger.error(f"CPD: Error checking backup need: {e}")
        return True  # Default to backup needed if error

def perform_backup():
    """Perform complete backup process"""
    try:
        Logger.info("CPD: Starting backup process")
        
        # Create backup
        zip_path, entries_count = create_backup()
        
        # Try to upload to Google Drive
        upload_success = upload_backup_to_drive(zip_path)
        status = "completed" if upload_success else "local_only"
        
        # Log backup
        log_backup(zip_path, entries_count, status)
        
        # Clean up old backups
        cleanup_old_backups()
        
        Logger.info(f"CPD: Backup process completed. Status: {status}")
        return True, status
        
    except Exception as e:
        Logger.error(f"CPD: Backup process failed: {e}")
        return False, str(e)

def schedule_backup():
    """Check if backup is needed and perform it in background if necessary"""
    if is_backup_needed():
        Logger.info("CPD: Backup needed, starting background backup")
        
        def backup_thread():
            try:
                success, status = perform_backup()
                if success:
                    Logger.info(f"CPD: Background backup completed: {status}")
                else:
                    Logger.error(f"CPD: Background backup failed: {status}")
            except Exception as e:
                Logger.error(f"CPD: Background backup thread error: {e}")
        
        # Start backup in separate thread to avoid blocking UI
        thread = threading.Thread(target=backup_thread, daemon=True)
        thread.start()
    else:
        Logger.info("CPD: No backup needed at this time")

def force_backup():
    """Force an immediate backup regardless of schedule"""
    Logger.info("CPD: Forcing immediate backup")
    return perform_backup()
