from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from app.products.models import Product


def test_create_product_successfully_no_discount(no_discount_product, db):
    """Test creating a new product"""

    assert no_discount_product.name
    assert no_discount_product.description
    assert no_discount_product.category
    assert no_discount_product.price > 0
    assert no_discount_product.stock >= 0
    assert isinstance(no_discount_product, Product)
    assert no_discount_product.final_price == no_discount_product.price


def test_create_product_successfully_with_discount(discounted_product, db):
    """Test creating a new product with discount"""

    assert discounted_product.name
    assert discounted_product.description
    assert discounted_product.category
    assert discounted_product.price > 0
    assert discounted_product.stock >= 0
    assert isinstance(discounted_product, Product)
    assert discounted_product.final_price is not None

    expected_final_price = discounted_product.price * (
        Decimal("1") - (discounted_product.discount / Decimal("100"))
    )
    assert discounted_product.final_price == expected_final_price
    assert discounted_product.final_price < discounted_product.price


def test_create_product_with_invalid_price(product_factory, db):
    """Test creating a new product with invalid price"""

    with pytest.raises(ValidationError, match="Price must be greater than zero."):
        product_factory(price=0).full_clean()
    with pytest.raises(ValidationError, match="Price must be greater than zero."):
        product_factory(price=-1).full_clean()


def test_create_product_with_invalid_discount(product_factory, db):
    """Test creating a new product with invalid discount"""

    with pytest.raises(
        ValidationError, match="Discount must be greater than or equal to zero."
    ):
        product_factory(discount=-10).full_clean()
    with pytest.raises(
        ValidationError, match="Discount must be less than or equal to 100."
    ):
        product_factory(discount=120).full_clean()


def test_create_product_with_invalid_stock(db, product_factory):
    """Test creating a product with invalid stock"""
    with pytest.raises(
        ValidationError, match="Stock must be greater than or equal to zero"
    ):
        product_factory(stock=-1).full_clean()


def test_adjust_increase_price_successfully(discounted_product, db):
    """Test adjusting the price of a product"""

    percentage = 10
    discounted_product.adjust_price(percentage)

    expected_final_price = discounted_product.price * (
        Decimal("1") - (discounted_product.discount / Decimal("100"))
    )
    assert discounted_product.final_price == expected_final_price
    assert discounted_product.final_price < discounted_product.price


def test_adjust_decrease_price_successfully(discounted_product, db):
    """Test adjusting the price of a product"""

    percentage = -10
    discounted_product.adjust_price(percentage)

    expected_final_price = discounted_product.price * (
        Decimal("1") - (discounted_product.discount / Decimal("100"))
    )
    assert discounted_product.final_price == expected_final_price
    assert discounted_product.final_price < discounted_product.price
