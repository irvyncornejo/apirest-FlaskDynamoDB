import os
import wget
import zipfile

class PackageDB:
    def __init__(self):
        self.location_full = os.getcwd().split('/')
        self.location = '/'.join(self.location_full)
    
    def download_dynamo(self):
        url = 'https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.zip'
        name = 'dynamodb_local_latest.zip'
        wget.download(url, name)
        self.unzip_files(name, '/dynamodb')
    
    def unzip_files(self, name, files):
        with zipfile.ZipFile(f'{os.getcwd()}/{name}', 'r') as zip_ref:
            zip_ref.extractall(self.location+files)
        os.remove(f'{os.getcwd()}/{name}')

if __name__ == '__main__':
    PackageDB().download_dynamo()