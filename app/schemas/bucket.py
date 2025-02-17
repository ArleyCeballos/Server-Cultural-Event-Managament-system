from pydantic import BaseModel


class FileData(BaseModel):
    file_bytes: bytes
    content_type: str
    file_name: str
