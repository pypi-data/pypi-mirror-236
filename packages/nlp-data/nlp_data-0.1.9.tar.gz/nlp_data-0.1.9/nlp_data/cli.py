from typer import Typer
from . import S3Storage
from enum import Enum
from pathlib import Path
from typing import Optional


app = Typer()

class CliAvailableBucket(str, Enum):
    asset = "asset"
    checkpoint = "checkpoint"


@app.command(name="list")
def list_files(bucket: CliAvailableBucket = CliAvailableBucket.checkpoint):
    s3 = S3Storage()
    files = s3.list_files(bucket.value)
    
    
@app.command(name="delete")
def delete_file(file: str, bucket: CliAvailableBucket = CliAvailableBucket.checkpoint):
    s3 = S3Storage()
    files = s3.list_files(bucket.value, show_table=False)
    if file in files:
        s3.delete_file(bucket.value, file)
    else:
        try:
            s3.delete_dir(bucket.value, file)
        except Exception as e:
            print(e)
    
    
@app.command(name="upload")
def upload(path: str, bucket: CliAvailableBucket = CliAvailableBucket.checkpoint, object_name: Optional[str] = None):
    s3 = S3Storage()
    path: Path = Path(path)
    if path.is_dir():
        s3.upload_dir(dir=path, bucket_name=bucket.value)
    else:
        s3.upload_file(path, bucket.value, object_name)
    
    
@app.command(name="download")
def download(file: str, bucket: CliAvailableBucket = CliAvailableBucket.checkpoint, save_path: Optional[str] = None):
    s3 = S3Storage()
    all_files = s3.list_files(bucket.value, show_table=False)
    if not save_path:
        save_path = Path('./')
    if file in all_files:
        s3.download_file(bucket.value, file, save_path)
    else:
        try:
            s3.download_dir(bucket_name=bucket.value, object_name=file, save_dir=save_path)
        except Exception as e:
            print(e)

        
        
        
        
if __name__ == '__main__':
    app()