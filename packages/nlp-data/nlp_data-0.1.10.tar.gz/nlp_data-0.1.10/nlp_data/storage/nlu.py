from ..document import NLUDocList
from .base import BaseDocStore


class NLUDocStore(BaseDocStore):
    bucket_name = 'nlu'
    
    @classmethod
    def pull(cls, name: str, show_progress: bool = True) -> NLUDocList:
        name = name.strip()
        return NLUDocList.pull(url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
    
    @classmethod
    def push(cls, docs: NLUDocList, name: str, show_progress: bool = True) -> None:
        name = name.strip()
        NLUDocList.push(docs, url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)