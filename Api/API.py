#A function to download the file
from __future__ import print_function
import pickle
import os.path
import io
import shutil
import requests
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)


if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)  

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)

def FileDownload(file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
    done = False
    try:
        # Download the data in chunks
        while not done:
            status, done = downloader.next_chunk()
            fh.seek(0)
            # Write the received data to the file
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)
                print("File Downloaded")
                # Return True if file Downloaded successfully
                return True
    except:
        # Return False if something went wrong
        print("Something went wrong.")
        return False


def GetFileList():
    results = service.files().list(
        pageSize=10, fields="files(id, name)").execute()
    items = results.get('files', [])
    return items



def FileUpload(filepath):
    # Extract the file name out of the file path
    name = filepath.split('/')[-1]
		# Find the MimeType of the file
    mimetype = MimeTypes().guess_type(name)[0]
    # create file metadata
    file_metadata = {'name': name}

    try:
        media = MediaFileUpload(filepath, mimetype=mimetype)
        # Create a new file in the Drive storage
        file =service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        print("File Uploaded.")

    except Exception as ex:
        print("Can't upload file")
			# Raise UploadError if file is not uploaded.
			#raise UploadError("Can't Upload File.")