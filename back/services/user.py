from repository import UserRepository
from .base import BaseService


class UserService(BaseService[UserRepository]):
    repo = UserRepository