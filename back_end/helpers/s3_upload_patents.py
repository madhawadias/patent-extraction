import boto3,os
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv()

class AmazolnS3:
    def __init__(self, bucket_name):
        self.ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
        self.ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
        self.BUCKET_NAME = bucket_name

    def upload(self, file, file_name):
        try:
            s3 = boto3.resource(
                's3',
                aws_access_key_id=self.ACCESS_KEY_ID,
                aws_secret_access_key=self.ACCESS_SECRET_KEY,
                config=Config(signature_version='s3v4')
            )
            result = s3.Bucket(self.BUCKET_NAME).put_object(Key=file_name, Body=file, ContentType='image/jpeg')
            print(result)
        except FileNotFoundError:
            return 0
        except KeyError:
            return 0
        except Exception:
            return 0

    def upload_pdf(self, file, file_name):
        try:
            s3 = boto3.resource(
                's3',
                aws_access_key_id=self.ACCESS_KEY_ID,
                aws_secret_access_key=self.ACCESS_SECRET_KEY,
                config=Config(signature_version='s3v4')
            )
            result = s3.Bucket(self.BUCKET_NAME).put_object(Key=file_name, Body=file)
            print(result)
            return 1
        except FileNotFoundError:
            return 0
        except KeyError:
            return 0
        except Exception:
            return 0
