import os
import pickle
import pandas as pd
from googleapiclient.discovery import build

from .creds import load_creds
load_creds()

with open(os.getenv("GOOGLE_DRIVE_PICKLE"), 'rb') as f:
    creds = pickle.load(f)

class Drive:
    """
    Using the built service, this Class
    enables you to move files around from
    one folder to another
    """
    def __init__(self, source, target):
        self.service = build(
            "drive", 'v3',
            credentials=creds
        )
        self.source = source
        self.target = target

    def fetch_source_files(self):

        query = f"parents = '{self.source}'"
        response = self.service.files().list(q=query).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')

        # A unique token is generated for each page view of length 100
        while nextPageToken:
            response = self.service.files().list(
                q=query,
                pageToken=nextPageToken).execute()

            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')

        print(f"Found {len(files)} files in source folder SQL Backup.")

        return files

    def move_source_to_target(self):

        """
        Only keep the last 10 days of backups
        in the SQL Backup folder and move the 
        rest to Long Term (so that our server disk
        which is running the Google Drive client will
        not be full)
        """

        files = self.fetch_source_files()

        df = pd.DataFrame(files)

        # Date filtering
        df['date'] = df['name'].str.split('_').str[0].apply(pd.to_datetime, format='%Y-%m-%d')
        ten_days_ago = (pd.to_datetime('today') - pd.Timedelta('10 days')).strftime('%Y-%m-%d')

        files_to_move = df[df['date'] < ten_days_ago].to_dict('records')
        files_remaining = df[df['date'] >= ten_days_ago]

        min_date = files_remaining['date'].min().strftime('%Y-%m-%d')
        max_date = files_remaining['date'].max().strftime('%Y-%m-%d')

        # Move only the required files

        success = 0

        for index, file in enumerate(files_to_move, 1):
            if file['mimeType'] != 'application/vnd.google-apps.folder':
                print(
                    f"[File {index} of {len(files_to_move)}] Moving {file['name']} to SQL Backup (Long Term) ...")

                try:
                    self.service.files().update(
                        fileId=file.get('id'),
                        addParents=self.target,
                        removeParents=self.source
                    ).execute()

                    success += 1

                except Exception as e:
                    print(f"Moving the file {file['name']} failed.")
                    print(e)

        print(f"Successfully moved {success} out of {len(files)} files.")
        print(f"There are {len(files_remaining)} backup files remaining in SQL Backup.")
        print(f"We kept the last 10 days of backup: {min_date} - {max_date}.")