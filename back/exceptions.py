from fastapi import HTTPException


class AppException(HTTPException):
    status_code: int = 400
    detail: str = 'Unexpected error'

    def __init__(self, detail: str | None = None, object_id: int | None = None):
        self.object_id = object_id
        if detail:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFoundError(AppException):
    status_code: int = 404
    object_id: int | None = None
    detail: str = 'Not found'


class UserNotFound(NotFoundError):
    object_id: int | None = None
    detail: str = 'User not found'


class PostNotFound(NotFoundError):
    object_id: int | None = None
    detail: str = 'Post not found'


class ImageNotFound(NotFoundError):
    object_id: int | None = None
    detail: str = 'Image not found'


class CommentNotFound(NotFoundError):
    object_id: int | None = None
    detail: str = 'Comment not found'


class UserAlreadyExists(AppException):
    status_code: int = 409
    detail: str = 'User already exists'


class NotCorrectPassword(AppException):
    status_code: int = 401
    detail: str = 'Incorrect password'
