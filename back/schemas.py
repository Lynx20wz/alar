from datetime import datetime
from enum import Enum
from typing import Generic, Optional, TypeVar, Union

from fastapi import Response, UploadFile
from pydantic import BaseModel, EmailStr, Field

T = TypeVar('T')


class LikesType(str, Enum):
    users = 'users'
    posts = 'posts'
    comments = 'comments'


class TotalInfo(BaseModel):
    total: int = 0


class LikesInfo(TotalInfo):
    type: LikesType = Field(default=LikesType.users)
    objects: list[Union['UserShortInfo', 'PostShortInfo', 'CommentInfo']] = []

    model_config = {
        'from_attributes': True,
    }


class UserShortInfo(BaseModel):
    id: int
    username: str

    model_config = {
        'from_attributes': True,
    }


class UserInfo(UserShortInfo):
    email: EmailStr
    bio: Optional[str]
    follows: LikesInfo = Field(default_factory=LikesInfo)
    followers: LikesInfo = Field(default_factory=LikesInfo)
    posts: list['PostShortInfo'] = []
    comments: list['CommentInfo'] = []
    social_links: list['SocialLinkInfo'] = []
    stacks: list['StackInfo'] = []


class PostCreateInfo(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str
    image: Optional[UploadFile] = None


class PostShortInfo(BaseModel):
    id: int
    author: UserShortInfo | None
    created_at: datetime
    title: str
    views: int
    is_liked: bool = False
    hasImage: bool = False
    likes: LikesInfo = Field(default_factory=LikesInfo)

    model_config = {
        'from_attributes': True,
    }


class PostInfo(PostShortInfo):
    content: str
    comments: list['CommentInfo'] = []


class CommentCreateInfo(BaseModel):
    content: str
    post_id: int

    model_config = {
        'from_attributes': True,
    }


class CommentShortInfo(CommentCreateInfo):
    id: int
    author: UserShortInfo
    created_at: datetime


class CommentInfo(CommentShortInfo):
    post: PostShortInfo


class SocialLinkInfo(BaseModel):
    id: int
    user_id: int
    platform: str
    url: str

    model_config = {
        'from_attributes': True,
    }


class StackInfo(BaseModel):
    id: int
    user_id: int
    title: str
    icon: Optional[bytes] = None
    url: str

    model_config = {
        'from_attributes': True,
    }


# Requests
class UserLoginData(BaseModel):
    username: str
    password: str


class UserRegisterData(UserLoginData):
    email: EmailStr
    avatar: Optional[UploadFile] = None
    banner: Optional[UploadFile] = None


# Responses
class BaseResponse(BaseModel, Generic[T]):
    data: Optional[T] = None


class UserExistsResponse(BaseModel):
    exists: bool


class FileResponse(Response):
    def __init__(self, file: bytes, filename: str = 'img.png', cache_seconds: int = 3600):
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Cache-Control': f'public, max-age={cache_seconds}',
        }

        super().__init__(content=file, media_type='image/png', headers=headers)
