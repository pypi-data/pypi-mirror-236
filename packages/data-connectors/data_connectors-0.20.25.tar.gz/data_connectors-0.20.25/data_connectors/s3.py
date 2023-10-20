import os
import boto3
from botocore.exceptions import ClientError

from .creds import load_creds
load_creds()

class S3:
    # Pass in your bucket name. Defaults to flowstate
    def __init__(self, bucket=None):
        self.client = boto3.client(
            's3',
            aws_access_key_id = os.getenv("AWS-ACCESS-KEY-ID")
            aws_secret_access_key = os.os.getenv("AWS-SECRET-ACCESS-KEY")
        )
        self.bucket = "flowstate" if bucket is None else bucket

    def list_buckets(self):
        """
        Listing buckets
        :return:
        """
        for key in self.client.list_buckets()['Buckets']:
            print(key['Name'])

    def list_objects_in_bucket(self, folder=None):

        folder = '' if folder is None else folder

        for key in self.client.list_objects(
            Bucket=self.bucket,
            Prefix=folder)['Contents']:

            print(key['Key'])

    def delete(self, key):
        self.client.delete_object(Bucket=self.bucket, Key=key)

    def upload(self, file_name, object_name=None, **extra_args):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param object_name: S3 object name. If not specified then file_name is used
        :param extra_args: Pass in ExtraArgs={'ACL': 'public-read'} for public access
        :return: True if file was uploaded, else False

        -- USAGE -- 
        
        from src.utils.s3 import S3
        FILE_NAME = 'google-drive-oauth-2.0.json'
        S3().upload(file_name=FILE_NAME, object_name=f'creds/{FILE_NAME}')

        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        try:
            response = self.client.upload_file(
                file_name, self.bucket, object_name,
                **extra_args
            )

            print(f"Upload success: https://s3-ap-southeast-1.amazonaws.com/{self.bucket}/{object_name}")

        except ClientError as e:
            logger.error(e)
            return False
        
        return response



    def upload_csv(self, df, folder_name, file_name, **extra_args):
        """
        Converts a DataFrame to csv file and uploads it to S3
        """
        file_name = f"{file_name}.csv"
        df.to_csv(file_name, index=False)
        self.upload(file_name=f'./{file_name}', object_name=f"{folder_name}/{file_name}", **extra_args)
        os.remove(f'./{file_name}')

