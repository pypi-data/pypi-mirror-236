from typer import Typer
from . import S3Storage
from jsonargparse import CLI 
from enum import Enum
# from pathlib import Path
# from wasabi import msg


# app = Typer()

class CliAvailableBucket(str, Enum):
    asset = "asset"
    checkpoint = "checkpoint"


# @app.command(name="list")
# def list_files(bucket: Optional[CliAvailableBucket] = None):
#     s3 = S3Storage()
#     if not bucket:
#         s3.list_buckets()
#     else:
#         s3.list_files(bucket.value)
    
# @app.command(name="delete")
# def delete_file(bucket: CliAvailableBucket, file: str):
#     s3 = S3Storage()
#     s3.delete_file(bucket.value, file)
    
# @app.command(name="upload")
# def upload(path: str, bucket: CliAvailableBucket, object_name: Optional[str] = None):
#     s3 = S3Storage()
#     s3.upload_file(path, bucket.value, object_name)
    
# @app.command(name="download")
# def download(file: str, bucket: CliAvailableBucket = CliAvailableBucket.checkpoint, save_path: Optional[str] = None):
#     s3 = S3Storage()
#     all_files = s3.list_files(bucket.value, show_table=False)
#     if not save_path:
#         save_path = Path('./')
#     if file in all_files:
#         s3.download_file(bucket.value, file, save_path)
#     else:
#         try:
#             s3.download_dir(bucket_name=bucket.value, object_name=file, save_dir=save_path)
#         except Exception as e:
#             print(e)
#             msg.fail(f"File {file} not found in bucket {bucket.value}")

class NLPDataCLI:
    def __init__(self, bucket: CliAvailableBucket = CliAvailableBucket.checkpoint):
        self.bucket = bucket.value
        self.s3 = S3Storage()
        
    def list_files(self):
        self.s3.list_files(self.bucket)
        
def main():
    CLI(NLPDataCLI)
        
        
        
        
if __name__ == '__main__':
    main()