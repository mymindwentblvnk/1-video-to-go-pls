from datetime import datetime
import os

from apiclient.http import MediaFileUpload
from googleapiclient import discovery
from google.oauth2 import service_account

from pytube import YouTube


MIME_TYPE = 'video/mp4'


class YouTubeClient(object):

    def download(self, url):
        video = YouTube(url)
        file_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%s')
        video.streams\
            .filter(mime_type=MIME_TYPE)\
            .first()\
            .download(filename=file_name)
        return '{}.mp4'.format(file_name)


class GoogleDriveClient(object):

    scopes = ['https://www.googleapis.com/auth/drive']

    def __init__(self, google_drive_folder_id, service_account_file='service-account.json'):
        self.google_drive_folder_id = google_drive_folder_id
        self.credentials = self._get_credentials(service_account_file)
        self.service = discovery.build('drive', 'v3', credentials=self.credentials)

    def _get_credentials(self, service_account_file):
        return service_account.Credentials.from_service_account_file(service_account_file,
                                                                     scopes=self.scopes)

    def upload_file(self, file_path):
        file_metadata = {
            'name': file_path,
            'parents': [self.google_drive_folder_id, ],
        }
        with open(file_path, 'r') as file_in:
            media = MediaFileUpload(file_in.name, mimetype=MIME_TYPE, resumable=True)
            request = self.service.files().create(body=file_metadata, media_body=media)
            response = None
            while response is None:
                _, response = request.next_chunk()

        os.remove(file_path)


if __name__ == '__main__':
    google_folder_id = open('parent_id.txt').read().split()
    file_name = YouTubeClient().download('https://www.youtube.com/watch?v=YNcBqW0CkpM')
    GoogleDriveClient(google_folder_id).upload_file(file_name)
