from datetime import datetime
from typing import TypeVar

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, EmailStr, Field

T = TypeVar('T')


# SocialLink
class SocialLinkBaseSchema(BaseModel):
    platform: str = Field(..., max_length=50)
    url: str = Field(..., max_length=255)


class SocialLinkCreateSchema(SocialLinkBaseSchema):
    pass


class SocialLinkReadSchema(SocialLinkBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Stack
class StackBaseSchema(BaseModel):
    title: str = Field(..., max_length=50)


class StackCreateSchema(StackBaseSchema):
    pass


class StackReadSchema(StackBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


# User
class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    bio: str | None = Field(..., max_length=255)


class UserRegisterSchema(UserBaseSchema):
    password: str = Field(..., min_length=3)
    avatar: UploadFile | None
    banner: UploadFile | None


class UserLoginSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3)


class UserReadSchema(UserBaseSchema):
    id: int
    social_links: list[SocialLinkReadSchema] = []
    stacks: list[StackReadSchema] = []

    model_config = ConfigDict(from_attributes=True)


class UserShortReadSchema(UserBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    bio: str | None = None
    avatar: UploadFile | None = None
    banner: UploadFile | None = None


class UserExistsResponse(BaseModel):
    username: str
    exists: bool


# Post
class PostBaseSchema(BaseModel):
    title: str = Field(..., max_length=255)
    content: str = Field(...)


class PostCreateSchema(PostBaseSchema):
    image: UploadFile | None


class PostReadSchema(PostBaseSchema):
    id: int
    author_id: int
    is_liked: bool = False
    image: bytes | None
    created_at: datetime
    views: int = 0

    model_config = ConfigDict(from_attributes=True)


class PostWithCommentsReadSchema(PostReadSchema):
    comments: list[CommentReadSchema] = []


# Comments
class CommentBaseSchema(BaseModel):
    content: str = Field(...)


class CommentCreateSchema(CommentBaseSchema):
    post_id: int


class CommentReadSchema(CommentBaseSchema):
    id: int
    author_id: int
    post_id: int
    likes_count: int = 0
    is_liked: bool = False

    model_config = ConfigDict(from_attributes=True)
