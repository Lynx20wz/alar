from typing import Optional
from pydantic import BaseModel
from fastapi import UploadFile

class UserBaseData(BaseModel):
    email: str
    password: str

class UserRegisterData(UserBaseData):
    username: str
    avatar: Optional[UploadFile] = None
    banner: Optional[UploadFile] = None