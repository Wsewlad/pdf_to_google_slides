from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Your Google API credentials file

# Your main Google account email (change this to your actual email)
emails = ["wladyslawfil@gmail.com", "yaraukrainka@gmail.com", "oksana.stavytska@gmail.com"]


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

    # share for two people
    permission1 = {
        "type": "user",
        "role": "writer",  # Change to "reader" for view-only access
        "emailAddress": emails[0]
    }
    permission2 = {
        "type": "user",
        "role": "writer",  # Change to "reader" for view-only access
        "emailAddress": emails[1]
    }
    permission3 = {
        "type": "user",
        "role": "writer",  # Change to "reader" for view-only access
        "emailAddress": emails[2]
    }

    drive_service.permissions().create(fileId=file_id, body=permission1).execute()
    drive_service.permissions().create(fileId=file_id, body=permission2).execute()
    drive_service.permissions().create(fileId=file_id, body=permission3).execute()


if __name__ == "__main__":
    pptx_file = "output.pptx"
    upload_to_google_drive(pptx_file)
