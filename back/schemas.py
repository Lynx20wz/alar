from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field
from fastapi import UploadFile


class LikesShortInfo(BaseModel):
    total: int = 0


class LikesInfo(LikesShortInfo):
    users: list['UserShortInfo'] = Field(default_factory=list)


class UserShortInfo(BaseModel):
    id: int
    username: str

    model_config = {
        'from_attributes': True,
    }


class UserInfo(UserShortInfo):
    email: str
    follows: list['UserShortInfo'] = Field(default_factory=list)
    followers: list['UserShortInfo'] = Field(default_factory=list)
    posts: list['PostShortInfo'] = Field(default_factory=list)
    comments: list['CommentInfo'] = Field(default_factory=list)


class PostShortInfo(BaseModel):
    id: int
    author: UserShortInfo
    created_at: datetime
    title: str
    likes: LikesShortInfo = Field(default_factory=LikesShortInfo)

    model_config = {
        'from_attributes': True,
    }


class PostInfo(PostShortInfo):
    content: str
    is_liked: bool = False
    likes: LikesInfo = Field(default_factory=LikesInfo)
    image: Optional[UploadFile] = None
    comments: list['CommentInfo'] = Field(default_factory=list)


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


# Requests
class UserLoginData(BaseModel):
    username: str
    password: str


class UserRegisterData(UserLoginData):
    email: str
    avatar: Optional[UploadFile] = None
    banner: Optional[UploadFile] = None


# Responses
class BaseResponse(BaseModel):
    success: bool = True
    detail: str = 'Success'


class UserTokenResponse(BaseResponse):
    pass


class UserResponse(BaseResponse):
    user: UserInfo | None = None
    model_config = {'from_attributes': True}


class UserExistsResponse(BaseModel):
    exists: bool
    username: str
