from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from pytest import fixture

from deps import user_service_factory
from exceptions import NotCorrectPassword, UserAlreadyExists, UserNotFound
from main import app
from schemas import UserRegisterData

client = TestClient(app)


class TestAuth:
    @fixture(autouse=True)
    def setup(self, get_mock_user):
        self.mock_service = AsyncMock()
        self.mock_user = get_mock_user

        app.dependency_overrides[user_service_factory] = lambda: self.mock_service

    def test_login_success(self):
        self.mock_service.login.return_value = self.mock_user

        response = client.post(
            '/auth/login',
            data={'username': 'test123', 'password': 'test123'},
        )

        cookies = response.cookies

        self.mock_service.login.assert_called_once_with('test123', 'test123')

        json_response = response.json()

        assert response.status_code == 200
        assert json_response['data']['id'] == 1
        assert cookies.get('token')
        assert cookies.get('username')

    def test_login_without_password(self):
        response = client.post(
            '/auth/login',
            data={'username': 'test123'},
        )

        self.mock_service.login.assert_not_called()

        assert response.status_code == 422

    def test_login_wrong_password(self):
        self.mock_service.login.side_effect = NotCorrectPassword()

        response = client.post(
            '/auth/login',
            data={'username': 'test123', 'password': 'test123'},
        )

        self.mock_service.login.assert_called_once_with('test123', 'test123')

        json_response = response.json()

        assert response.status_code == 401
        assert json_response['detail'] == 'Incorrect password'

    def test_login_user_not_exists(self):
        self.mock_service.login.side_effect = UserNotFound()

        response = client.post(
            '/auth/login',
            data={'username': 'test123', 'password': 'test123'},
        )

        self.mock_service.login.assert_called_once_with('test123', 'test123')

        json_response = response.json()

        assert response.status_code == 404
        assert json_response['detail'] == 'User not found'

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

        self.mock_service.add_user.assert_called_once_with(
            UserRegisterData(username='test123', password='test123', email='test@development.com')
        )

        json_response = response.json()

        assert response.status_code == 201
        assert json_response['data']['id'] == 1

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

        self.mock_service.add_user.assert_called_once_with(
            UserRegisterData(username='test123', password='test123', email='test@development.com')
        )

        json_response = response.json()

        assert response.status_code == 409
        assert json_response['detail'] == 'User already exists'

    def test_check_user_exists_exists(self):
        self.mock_service.check_exists.return_value = True

        response = client.get('/auth/exists?u=test123')

        self.mock_service.check_exists.assert_called_once_with('test123')

        json_response = response.json()

        assert response.status_code == 200
        assert json_response['exists']

    def test_check_user_exists_not_exists(self):
        self.mock_service.check_exists.return_value = False

        response = client.get('/auth/exists?u=test123')

        self.mock_service.check_exists.assert_called_once_with('test123')

        json_response = response.json()

        assert response.status_code == 200
        assert not json_response['exists']
