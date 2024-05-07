## TO RUN THIS CODE YOU NEED TO HAVE THE FILE CREDENTIALS.JSON IN THE SAME DIRECTORY

from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json

# Scope to access Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        '/home/mininet/Documents/credentials.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials

def download_file(credentials, file_id, file_name):
    service = build('drive', 'v3', credentials=credentials)
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with open(file_name, 'wb') as f:
        f.write(fh.getvalue())

def get_folder_contents(service, folder_id):
    """
    Get the contents of a folder in Google Drive.

    Args:
        service: Google Drive service.
        folder_id: Folder ID.

    Returns:
        A list of tuples containing the file ID and file name for each file in the folder.
    """
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    file_list = []
    for item in items:
        if item['mimeType'].startswith('audio/'):
            file_list.append((item['id'], item['name']))

    return file_list

def download_audio_files(credentials, folder_id):
    """
    Download audio files from a folder in Google Drive and save the download links to a JSON file.

    Args:
        credentials: Authentication credentials.
        folder_id: ID of the folder in Google Drive.
    """
    service = build('drive', 'v3', credentials=credentials)
    audio_links = {}  # Dictionary to store download links

    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            category_name = item['name']
            audio_links[category_name] = []
            files = get_folder_contents(service, item['id'])

            for file_id, file_name in files:
                download_file(credentials, file_id, file_name)
                file_url = f"https://drive.google.com/uc?id={file_id}"
                audio_links[category_name].append({'name': file_name, 'url': file_url})

    with open('audio_links.json', 'w') as json_file:
        json.dump(audio_links, json_file, indent=4)

# ID of the main folder containing subfolders of categories
folder_id = '1Lmz9yLgj0zLQylIx2mhDDziDeSrGu_-n'

# Call the function to download audio files and get the download links
credentials = authenticate()
download_audio_files(credentials, folder_id)
