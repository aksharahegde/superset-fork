import io
import boto3

from superset import app

config = app.config


class AwsS3Helper(object):

    def __init__(self):
        self.client = boto3.client('s3',
            aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

    def upload(self, file_name, bucket, object_name):
        response = self.client.upload_file(file_name, bucket, object_name)
        return response


    def download(self, file_name, bucket):
        s3 = boto3.resource('s3')
        output = f"download_files/{file_name}"
        s3.Bucket(bucket).download_file(file_name, output)
        return output

    def fetch_file_using_key(self, bucket, object_key):
        result = self.client.get_object(Bucket=bucket, Key=object_key)
        if result:
            stream = result.get('Body').read()
            return io.BytesIO(stream)

        return None

    def convert_key_to_filename(self, key):
        split_str = key.split('/')[1:]
        return ' | '.join(split_str)

    def convert_filename_to_key(self, filename):
        key_parts = ['prod']
        suffix = '/'.join(filename.split(' | '))
        key_parts.append(suffix)
        return '/'.join(key_parts)

    def fetch_files(self, bucket):
        contents = []
        for item in self.client.list_objects(Bucket=bucket, Prefix='prod/')['Contents']:
            contents.append(item)


    def list_all_files(self, bucket):
        contents = []
        for item in self.client.list_objects(Bucket=bucket, Prefix='prod/')['Contents']:
            contents.append(item)

        return contents
