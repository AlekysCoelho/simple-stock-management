import pytest

from app.accounts.models import Users

# @pytest.mark.django_db
# def test_create_user():
#     user = Users.objects.create_user(
#         username="testuser1",
#         email="testuser1@gmail.com",
#         password="test1@password123",
#         bio="test bio test",
#     )
#     assert user.username == "testuser1"
#     assert user.email == "testuser1@gmail.com"
#     assert user.bio == "test bio test"

# @pytest.mark.django_db
# def test_create_multiple_users(user_factory):
#     """Test creating multiple users"""
#     users = user_factory.create_batch(3)
#     assert len(users) == 3
#     assert all(isinstance(user, Users) for user in users)


def test_create_user(new_user, db):
    """Test creating a new user"""
    assert new_user.username
    assert new_user.email
    assert isinstance(new_user, Users)


def test_user_str(new_user, db):
    """Test the user string representation"""
    assert str(new_user) == new_user.username


def test_create_multiple_users(user_factory, db):
    """Test creating multiple users"""
    users = user_factory.create_batch(3)
    assert len(users) == 3
    assert all(isinstance(user, Users) for user in users)
