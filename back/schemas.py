from typing import Optional, Union, List
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from fastapi import UploadFile
from enum import Enum


class LikesType(str, Enum):
    users = 'users'
    posts = 'posts'
    comments = 'comments'


class TotalInfo(BaseModel):
    total: int = 0


class LikesInfo(TotalInfo):
    type: LikesType = Field(default=LikesType.users)
    objects: List[Union['UserShortInfo', 'PostShortInfo', 'CommentInfo']] = []

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
    posts: List['PostShortInfo'] = []
    comments: List['CommentInfo'] = []
    social_links: List['SocialLinkInfo'] = []
    stacks: List['StackInfo'] = []


class PostCreateInfo(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str
    image: Optional[UploadFile] = None


class PostShortInfo(BaseModel):
    id: int
    author: UserShortInfo
    created_at: datetime
    title: str
    views: int
    is_liked: bool = False
    likes: LikesInfo = Field(default_factory=LikesInfo)

    model_config = {
        'from_attributes': True,
    }


class PostInfo(PostShortInfo):
    content: str
    image: Optional[UploadFile] = None
    comments: List['CommentInfo'] = []


class CommentInfo(BaseModel):
    id: int
    author: UserShortInfo
    created_at: datetime
    content: str

    model_config = {
        'from_attributes': True,
    }


class CommentInfoWithPost(CommentInfo):
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
class BaseResponse(BaseModel):
    success: bool = True
    detail: dict = {'msg': 'Success'}


class UserResponse(BaseResponse):
    user: UserInfo
    model_config = {'from_attributes': True}


class UserExistsResponse(BaseModel):
    exists: bool
    username: str
