from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {"example": {"username": "user", "password": "weakpassword"}}


class UserInCreate(User):
    password: str


class UserInUpdate(User):
    password: Optional[str] = None


class UserInDB(User):
    class Config:
        orm_mode = True


class UserToken(BaseModel):
    token: str
