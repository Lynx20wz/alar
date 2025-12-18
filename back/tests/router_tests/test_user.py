from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from pytest import fixture, mark

from deps import jwt_factory, user_factory, user_service_factory
from exceptions import UserNotFound
from main import app

client = TestClient(app)


class TestUser:
    @fixture(autouse=True)
    def setup(self, get_mock_user):
        self.mock_service = AsyncMock()

        self.mock_jwt = AsyncMock()
        self.mock_jwt.__call__ = lambda: ...

        app.dependency_overrides[user_service_factory] = lambda: self.mock_service
        app.dependency_overrides[jwt_factory] = lambda: self.mock_jwt
        app.dependency_overrides[user_factory] = lambda: get_mock_user

    def test_get_user_success(self, get_mock_user):
        self.mock_service.get_user_by_username.return_value = get_mock_user

        response = client.get('/users?u=test123')

        self.mock_service.get_user_by_username.assert_called_once_with('test123')

        json_response = response.json()

        assert response.status_code == 200
        assert json_response['data']['id'] == 1

    def test_get_user_not_found(self):
        self.mock_service.get_user_by_username.side_effect = UserNotFound()

        response = client.get('/users?u=test')

        self.mock_service.get_user_by_username.assert_called_once_with('test')

        assert response.status_code == 404
        assert response.json()['detail'] == 'User not found'

    def test_get_me_success(self):
        response = client.get('/users/')

        json_response = response.json()

        assert response.status_code == 200
        assert json_response['data']['id'] == 1

    @mark.parametrize('endpoint', ['avatar', 'banner'])
    def test_get_user_image_success(self, get_mock_user, endpoint):
        self.mock_service.get_user_by_username.return_value = get_mock_user

        response = client.get(f'/users/{endpoint}?u=test123')

        self.mock_service.get_user_by_username.assert_called_once_with('test123')
        assert response.status_code == 200
        assert response.content == b'x'

    @mark.parametrize('endpoint', ['avatar', 'banner'])
    def test_get_user_image_user_not_found(self, endpoint):
        self.mock_service.get_user_by_username.side_effect = UserNotFound()

        response = client.get(f'/users/{endpoint}?u=nonexistent')

        self.mock_service.get_user_by_username.assert_called_once_with('nonexistent')
        assert response.status_code == 404
        assert response.json()['detail'] == 'User not found'

    @mark.parametrize('endpoint', ['avatar', 'banner'])
    def test_get_user_image_not_found(self, get_mock_user, endpoint):
        mock_user = get_mock_user
        setattr(mock_user, endpoint, None)
        self.mock_service.get_user_by_username.return_value = mock_user

        response = client.get(f'/users/{endpoint}?u=test123')

        self.mock_service.get_user_by_username.assert_called_once_with('test123')
        assert response.status_code == 404
        assert response.json()['detail'] == 'Image not found'
