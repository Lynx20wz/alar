__all__ = ('UserLoginData', 'UserRegisterData')

from typing import Optional
from pydantic import BaseModel
from fastapi import UploadFile

class UserLoginData(BaseModel):
    username: str
    password: str

class UserRegisterData(UserLoginData):
    email: str
    avatar: Optional[UploadFile] = None
    banner: Optional[UploadFile] = None