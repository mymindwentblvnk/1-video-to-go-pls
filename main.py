from google.oauth2 import service_account
from apiclient.http import MediaFileUpload
from googleapiclient import discovery
from pytube import YouTube


# YouTube('https://youtu.be/9bZkp7q19f0').streams.filter(file_extension='mp4').first().download(filename='video')

def credentials_from_file():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'service-account.json'
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,
                                                                        scopes=SCOPES)
    return credentials


if __name__ == '__main__':
    credentials = credentials_from_file()
    service = discovery.build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': 'video.mp4',
        'parents': ['1mI969yzWh8PX0uK8M_SVKkxfNurLUusT']
    }

    # https://github.com/cfinch/Shocksolution_Examples/blob/master/GoogleCloudPlatform/driveAPIexample.py
    with open('video.mp4', 'r') as tf:
        media = MediaFileUpload(tf.name, mimetype='video/mp4')
        cloudFile = service.files().create(body=file_metadata, media_body=media).execute()
