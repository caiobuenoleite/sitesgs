import os
import io
from google_drive.Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = './google_drive/credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service =Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

file_ids = [
    '1zb2qwQErw6V5LTkt7pYcetAd0KwyIGqz',
    '1nCdsBEyO5Uv4M8FlXDhSjVKi5s_rxEgM'
]
file_names = [
    'confirmados.xlsx',
    'obitos.xlsx'
]

for file_id, file_name in zip(file_ids,file_names):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh,request=request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print('Download progress {0}'.format(status.progress() * 100))

    fh.seek(0)
    path = os.path.join('./datasets',file_name)
    with open(path,'wb') as f:
        f.write(fh.read())
        f.close()


