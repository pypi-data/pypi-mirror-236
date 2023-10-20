from ..document import DialogueDocList
from .base import BaseDocStore


class DialogueDocStore(BaseDocStore):
    
    bucket_name = 'dialogue'
    
    @classmethod
    def pull(cls, name: str, show_progress: bool = True) -> DialogueDocList:
        name = name.strip()
        return DialogueDocList.pull(url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
    
    @classmethod
    def push(cls, docs: DialogueDocList, name: str, show_progress: bool = True) -> None:
        name = name.strip()
        DialogueDocList.push(docs, url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)