from pydantic import BaseModel


class Response(BaseModel):
    data: str
    message: str
    type: str


class FileResponse(BaseModel):
    detail: list