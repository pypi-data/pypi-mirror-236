from .storage.s3 import S3Storage
from pathlib import Path
from typing import Optional
from jsonargparse import CLI
            
class Main():
    """nlp_data cli
    """
    def __init__(self, 
                 endport_url: str = "http://192.168.130.5:9005",
                 access_key: str = "minioadmin",
                 secret_key: str = "minioadmin"):
        self.s3 = S3Storage(endpoint_url=endport_url, access_key=access_key, secret_key=secret_key)
        
    def list(self, bucket: Optional[str] = None):
        if not bucket:
            _ = self.s3.list_buckets()
        else:
            _ = self.s3.list_files(bucket)
            
    def delete(self, file: str, bucket: str = 'asset'):
        files = self.s3.list_files(bucket, show_table=False)
        if file in files:
            self.s3.delete_file(bucket, file)
        else:
            try:
                self.s3.delete_dir(bucket, file)
            except Exception as e:
                print(e)
    
    def upload(self, path: str, bucket: str = 'asset', object_name: Optional[str] = None):
        path: Path = Path(path)
        if path.is_dir():
            self.s3.upload_dir(dir=path, bucket_name=bucket)
        else:
            self.s3.upload_file(path, bucket, object_name)
            
    def download(self, file: str, bucket: str = 'asset', save_path: Optional[str] = None):
        all_files = self.s3._get_bucket_files(bucket)
        if file in all_files:
            self.s3.download_file(bucket_name=bucket, object_name=file, save_path=save_path)
        else:
            try:
                self.s3.download_dir(bucket_name=bucket, object_name=file, save_dir=save_path)
            except Exception as e:
                print(e)
                
def run():
    CLI(Main)