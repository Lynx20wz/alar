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


class UserTokenResponse(BaseModel):
    username: str
    token: Optional[str]
    detail: str


class UserResponse(BaseModel):
    username: str
    email: str


class UserExistsResponse(BaseModel):
    username: str
    exists: bool
