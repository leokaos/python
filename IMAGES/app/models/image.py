from pydantic import BaseModel


class ImageDTO(BaseModel):
    content: str
