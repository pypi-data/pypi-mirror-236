from ..document import EmbeddingDocList
from .base import BaseDocStore

class EmbeddingDocStore(BaseDocStore):
    
    bucket_name = 'embedding'
    
    @classmethod
    def pull(cls, name: str, show_progress: bool = True) -> EmbeddingDocList:
        name = name.strip()
        return EmbeddingDocList.pull(url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
    
    @classmethod
    def push(cls, docs: EmbeddingDocList, name: str, show_progress: bool = True) -> None:
        name = name.strip()
        EmbeddingDocList.push(docs, url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)