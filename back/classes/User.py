from ..database.models import UserModel


class User:
    def __init__(self, id_: int, email: str, password: str):
        self.id = id_
        self.email = email
        self.password = password

    @property
    def to_model(self) -> UserModel:
        return UserModel(email=self.email, password=self.password)
