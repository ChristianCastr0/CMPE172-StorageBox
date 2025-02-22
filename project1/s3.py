import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

class S3:
    BUCKET_NAME="project1-bucket123"
    ACCESS_KEY_ID=''
    ACCESS_SECRET_KEY=''

    s3 = boto3.client('s3')

    def upload(self, filename, object_name, email):
        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )

        s3.Bucket("BUCKET_NAME").put_object(Key=email+'/'+object_name, Body=filename)

        print('done')

    def download(self, object_key, filename):
        try:
            s3.Bucket(BUCKET_NAME).download_file(object_key, filename)
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise