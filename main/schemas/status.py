from pydantic import BaseModel


class Status(BaseModel):
    success: bool = True
    version: str
    message: str
