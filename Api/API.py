#A function to download the file
from __future__ import print_function
import os.path
import io
import shutil
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.oauth2.credentials import Credentials
import json

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())


        global service
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
                #print("File Downloaded")
                # Return True if file Downloaded successfully
                return True
    except:
        # Return False if something went wrong
        print("Something went wrong.")
        return False


def GetFileList():
    if os.path.exists('folder_id.txt'):
        f= open('folder_id.txt')
        folder_id = f.read()
    else:
        print("You have not created any files")

    query=f"parents= '{folder_id}' "

    results = service.files().list(q=query, orderBy='ModifiedTime desc',
        pageSize=10, fields="NextPageToken files(id, name)").execute()
    items = results.get('files', [])
    return items



def FileUpload(filepath):

    if os.path.exists('folder_id.txt'):
        f=open('folder_id.txt', 'r')
        folder_id = f.read()
    else:
        #creating a folder named 'HashedFiles'
        folder_metadata={
            "name":"HashedFiles",
            "mimeType":"application/vnd.google-apps.folder"
        }

        folder = service.files().create(body=folder_metadata, fields='id').execute()


        folder_id = folder.get('id')

        with open('folder_id.txt','w') as f:
            f.write(folder_id)


    # Extract the file name out of the file path
    name = filepath.split('/')[-1]
		# Find the MimeType of the file
    mimetype = MimeTypes().guess_type(name)[0]
    # create file metadata
    file_metadata = {
        'name': name,
        'parents':[folder_id]

    }

    try:
        media = MediaFileUpload(filepath, mimetype=mimetype, resumable=True)
        # Create a new file in the Drive storage
        file =service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        #print("File Uploaded.")

    except Exception as ex:
        print("Can't upload file")
			# Raise UploadError if file is not uploaded.
			#raise UploadError("Can't Upload File.")