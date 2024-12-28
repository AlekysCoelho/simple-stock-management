import pytest
from pytest_factoryboy import register

from tests.factories import CategoryFactory, ProductFactory, UserFactory

register(UserFactory)
register(CategoryFactory)
register(ProductFactory)


@pytest.fixture
def new_user(db, user_factory):
    return user_factory()


@pytest.fixture
def new_category(db, category_factory):
    return category_factory()


@pytest.fixture
def new_product(db, product_factory):
    return product_factory()
