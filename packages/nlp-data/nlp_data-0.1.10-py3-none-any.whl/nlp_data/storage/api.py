from .base import BaseDocStore
from ..document import APIDocList

class APIDocStore(BaseDocStore):
    
    bucket_name = 'api'
    
    @classmethod
    def pull(cls, name: str, show_progress: bool = True) -> APIDocList:
        name = name.strip()
        return APIDocList.pull(url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
    
    @classmethod
    def push(cls, docs: APIDocList, name: str, show_progress: bool = True) -> None:
        name = name.strip()
        APIDocList.push(docs, url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)