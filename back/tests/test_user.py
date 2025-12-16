# from unittest.mock import AsyncMock, Mock

# from fastapi.testclient import TestClient
# from pytest import fixture

# from main import app

# client = TestClient(app)


# class TestUser:
#     @fixture(autouse=True)
#     def setup(self):
#         self.mock_service = AsyncMock()
#         self.mock_user = Mock()
#         self.mock_user.configure_mock(
#             id=1,
#             username='test123',
#             email='test@development.com',
#             avatar_url=None,
#         )

#         self.mock_service.get_by.return_value = self.mock_user

#         app.dependency_overrides.clear()
