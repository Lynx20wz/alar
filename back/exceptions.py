from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class AppException(Exception):
    status_code: int = 400
    detail: str = 'Unexpected error'

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class NotFoundError(AppException):
    status_code = 404


class UserNotFound(NotFoundError):
    detail = 'User not found'


class PostNotFound(NotFoundError):
    detail = 'Post not found'


class CommentNotFound(NotFoundError):
    detail = 'Comment not found'


class NotCorrectPassword(AppException):
    status_code = 401
    detail = 'Incorrect password'


class ErrorResponse(BaseModel):
    detail: str


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={'detail': exc.detail},
        )
