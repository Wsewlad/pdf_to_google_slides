from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Your Google API credentials file

# Your main Google account email (change this to your actual email)
MAIN_GOOGLE_ACCOUNT = "wladyslawfil@gmail.com"


def upload_to_google_drive(file_path):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        "name": os.path.basename(file_path),
        "mimeType": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    }

    # Use MediaFileUpload with `resumable=True` for large files
    media = MediaFileUpload(file_path, mimetype=file_metadata["mimeType"], resumable=True)

    # Upload the file
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
    file_id = file['id']
    file_link = file['webViewLink']

    print(f"✅ Uploaded to Google Drive: {file_link}")

    # Share the file with your main Google account
    permission = {
        "type": "user",
        "role": "writer",  # Change to "reader" for view-only access
        "emailAddress": MAIN_GOOGLE_ACCOUNT
    }

    drive_service.permissions().create(fileId=file_id, body=permission).execute()
    print(f"✅ Shared with {MAIN_GOOGLE_ACCOUNT}")


if __name__ == "__main__":
    pptx_file = "output.pptx"
    upload_to_google_drive(pptx_file)
