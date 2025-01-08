import pytest
from pytest_factoryboy import register

from tests.factories import (
    CategoryFactory,
    CustomDiscountProductFactory,
    DiscountedProductFactory,
    MaxDiscountProductFactory,
    MinDiscountProductFactory,
    NoDiscountProductFactory,
    ProductFactory,
    UserFactory,
    ZeroDiscountProductFactory,
)

register(UserFactory)
register(CategoryFactory)
register(ProductFactory)
register(NoDiscountProductFactory)
register(DiscountedProductFactory)


@pytest.fixture
def new_user(db, user_factory):
    return user_factory()


@pytest.fixture
def new_category(db, category_factory):
    return category_factory()


@pytest.fixture
def basic_product(db, product_factory):
    return product_factory()


@pytest.fixture
def no_discount_product(db, no_discount_product_factory):
    return no_discount_product_factory()


@pytest.fixture
def discounted_product(db, discounted_product_factory):
    return discounted_product_factory()


@pytest.fixture
def low_stock_product(db, product_factory):
    return product_factory(stock=5)


@pytest.fixture
def zero_stock_product(db, product_factory):
    return product_factory(stock=0)
