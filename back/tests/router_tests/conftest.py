from types import SimpleNamespace

from pytest import fixture


@fixture
def get_mock_user():
    return SimpleNamespace(
        id=1,
        username='test123',
        email='test@development.com',
        _password='$2b$12$K/L403O4yazJjSSdjEi1wOFe0SyeOM0g4QJeyny9fcWJqJtUJISZG',  # 111
        banner=None,
        avatar=None,
        bio=None,
        posts=[],
        comments=[],
        social_links=[],
        stacks=[],
    )
