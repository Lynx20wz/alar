from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from pytest import fixture

from deps import user_service_factory
from exceptions import NotCorrectPassword, UserAlreadyExists, UserNotFound
from main import app
from models import UserModel
from schemas import UserRegisterData

client = TestClient(app)


class TestAuth:
    @fixture(autouse=True)
    def setup(self):
        self.mock_service = AsyncMock()
        self.mock_user = UserModel(
            id=1,
            username='test123',
            email='test@development.com',
        )

        app.dependency_overrides[user_service_factory] = lambda: self.mock_service

    def test_login_success(self):
        self.mock_service.login.return_value = self.mock_user

        response = client.post(
            '/auth/login',
            data={'username': 'test123', 'password': 'test123'},
        )

        cookies = response.cookies

        assert response.status_code == 200
        assert response.json()['success']
        assert response.json()['msg'] == 'Success'
        assert response.json()['data']['id'] == 1
        assert cookies.get('token')
        assert cookies.get('username')

        self.mock_service.login.assert_called_once_with('test123', 'test123')

    def test_login_without_password(self):
        response = client.post(
            '/auth/login',
            data={'username': 'test123'},
        )

        assert response.status_code == 422
        self.mock_service.login.assert_not_called()

    def test_login_wrong_password(self):
        self.mock_service.login.side_effect = NotCorrectPassword()

        response = client.post(
            '/auth/login',
            data={'username': 'test123', 'password': 'test123'},
        )

        assert response.status_code == 200
        assert not response.json()['success']
        assert response.json()['msg'] == 'Not correct password'
        self.mock_service.login.assert_called_once_with('test123', 'test123')

    def test_login_user_not_exists(self):
        self.mock_service.login.side_effect = UserNotFound()

        response = client.post(
            '/auth/login',
            data={'username': 'test123', 'password': 'test123'},
        )

        assert response.status_code == 200
        assert not response.json()['success']
        assert response.json()['msg'] == 'User not found'
        self.mock_service.login.assert_called_once_with('test123', 'test123')

    def test_register_success(self):
        self.mock_service.add_user.return_value = self.mock_user

        response = client.post(
            '/auth/user',
            data={
                'username': 'test123',
                'password': 'test123',
                'email': 'test@development.com',
            },
        )

        assert response.status_code == 201
        assert response.json()['success']
        assert response.json()['msg'] == 'Success'
        assert response.json()['data']['id'] == 1

        self.mock_service.add_user.assert_called_once_with(
            UserRegisterData(username='test123', password='test123', email='test@development.com')
        )

    def test_register_user_exists(self):
        self.mock_service.add_user.side_effect = UserAlreadyExists()

        response = client.post(
            '/auth/user',
            data={
                'username': 'test123',
                'password': 'test123',
                'email': 'test@development.com',
            },
        )

        assert response.status_code == 201
        assert not response.json()['success']
        assert response.json()['msg'] == 'User already exists'
        self.mock_service.add_user.assert_called_once_with(
            UserRegisterData(username='test123', password='test123', email='test@development.com')
        )
