from fastapi import HTTPException


class AppException(HTTPException):
    status_code: int = 400
    detail: str = 'Unexpected error'

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class NotFoundError(AppException):
    status_code: int = 404


class UserNotFound(NotFoundError):
    detail: str = 'User not found'


class PostNotFound(NotFoundError):
    detail: str = 'Post not found'


class ImageNotFound(NotFoundError):
    detail: str = 'Image not found'


class CommentNotFound(NotFoundError):
    detail: str = 'Comment not found'


class UserAlreadyExists(AppException):
    status_code: int = 409
    detail: str = 'User already exists'


class NotCorrectPassword(AppException):
    status_code: int = 401
    detail: str = 'Incorrect password'
