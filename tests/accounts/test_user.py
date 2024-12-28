import pytest

from app.accounts.models import Users


@pytest.mark.django_db
def test_create_user():
    user = Users.objects.create_user(
        username="testuser1",
        email="testuser1@gmail.com",
        password="test1@password123",
        bio="test bio test",
    )
    assert user.username == "testuser1"
    assert user.email == "testuser1@gmail.com"
    assert user.bio == "test bio test"
