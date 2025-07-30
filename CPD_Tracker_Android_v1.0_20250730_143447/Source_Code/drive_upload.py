import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError
from kivy.logger import Logger

# Google Drive configuration
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'
FOLDER_NAME = 'CPD Points'

def check_credentials():
    """Check if Google Drive credentials exist"""
    return os.path.exists(SERVICE_ACCOUNT_FILE)

def get_drive_service():
    """Initialize and return Google Drive service"""
    try:
        if not check_credentials():
            raise FileNotFoundError(f"Google Drive credentials file '{SERVICE_ACCOUNT_FILE}' not found")
        
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        return service
        
    except GoogleAuthError as e:
        Logger.error(f"CPD: Google authentication error: {e}")
        raise
    except Exception as e:
        Logger.error(f"CPD: Error initializing Google Drive service: {e}")
        raise

def find_or_create_folder(service, folder_name):
    """Find existing folder or create new one"""
    try:
        # Search for existing folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])
        
        if folders:
            folder_id = folders[0]['id']
            Logger.info(f"CPD: Found existing folder '{folder_name}' with ID: {folder_id}")
            return folder_id
        
        # Create new folder
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        
        Logger.info(f"CPD: Created new folder '{folder_name}' with ID: {folder_id}")
        return folder_id
        
    except Exception as e:
        Logger.error(f"CPD: Error with folder operations: {e}")
        raise

def upload_to_drive(zip_path):
    """Upload backup file to Google Drive"""
    try:
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Backup file not found: {zip_path}")
        
        # Initialize service
        service = get_drive_service()
        
        # Find or create CPD Points folder
        folder_id = find_or_create_folder(service, FOLDER_NAME)
        
        # Prepare file metadata
        file_name = os.path.basename(zip_path)
        file_metadata = {
            'name': file_name,
            'parents': [folder_id],
            'description': f'CPD Tracker backup created on {os.path.getctime(zip_path)}'
        }
        
        # Upload file
        media = MediaFileUpload(zip_path, mimetype='application/zip', resumable=True)
        
        Logger.info(f"CPD: Uploading {file_name} to Google Drive...")
        
        request = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,size'
        )
        
        # Execute upload with progress tracking
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                Logger.info(f"CPD: Upload progress: {progress}%")
        
        file_id = response.get('id')
        file_size = response.get('size', 'Unknown')
        
        Logger.info(f"CPD: Upload completed successfully!")
        Logger.info(f"CPD: File ID: {file_id}")
        Logger.info(f"CPD: File size: {file_size} bytes")
        
        return file_id
        
    except FileNotFoundError as e:
        Logger.error(f"CPD: File error: {e}")
        raise
    except GoogleAuthError as e:
        Logger.error(f"CPD: Google authentication error: {e}")
        raise
    except Exception as e:
        Logger.error(f"CPD: Upload error: {e}")
        raise

def test_drive_connection():
    """Test Google Drive connection"""
    try:
        service = get_drive_service()
        
        # Try to list files (limited) to test connection
        results = service.files().list(pageSize=1, fields="files(id, name)").execute()
        
        Logger.info("CPD: Google Drive connection test successful")
        return True
        
    except Exception as e:
        Logger.error(f"CPD: Google Drive connection test failed: {e}")
        return False

def get_upload_quota_info():
    """Get Google Drive storage quota information"""
    try:
        service = get_drive_service()
        
        about = service.about().get(fields="storageQuota").execute()
        quota = about.get('storageQuota', {})
        
        limit = int(quota.get('limit', 0))
        usage = int(quota.get('usage', 0))
        
        return {
            'limit': limit,
            'usage': usage,
            'available': limit - usage,
            'usage_percentage': (usage / limit * 100) if limit > 0 else 0
        }
        
    except Exception as e:
        Logger.error(f"CPD: Error getting quota info: {e}")
        return None
