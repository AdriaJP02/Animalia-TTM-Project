## TO RUN THIS CODE YOU NEED TO HAVE THE FILE CREDENTIALS.JSON IN THE SAME DIRECTORY

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json

# Scope to access Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    # Authenticate using credentials.json file
    flow = InstalledAppFlow.from_client_secrets_file(
        '/home/mininet/Documents/credentials.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials

def get_folder_contents(service, folder_id):
    """
    Get the contents of a folder in Google Drive.

    Args:
        service: Google Drive service.
        folder_id: ID of the folder.

    Returns:
        List of tuples containing the file ID and name for each file in the folder.
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

def get_audio_links(credentials, folder_id):
    """
    Get download links for audio files in a folder on Google Drive.

    Args:
        credentials: Authentication credentials.
        folder_id: ID of the folder on Google Drive.

    Returns:
        Dictionary containing download links for audio files, organized by category.
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
                file_url = f"https://drive.google.com/uc?id={file_id}"
                audio_links[category_name].append({'name': file_name, 'url': file_url})

    return audio_links

# ID of the main folder containing category subfolders
folder_id = '1Lmz9yLgj0zLQylIx2mhDDziDeSrGu_-n'

# Authentication
credentials = authenticate()

# Get download links for audio files
audio_links = get_audio_links(credentials, folder_id)

# Save the links to a JSON file
with open('audio_links.json', 'w') as json_file:
    json.dump(audio_links, json_file, indent=4)

print("Download links have been saved to the audio_links.json file.")

