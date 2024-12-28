import pytest

from app.products.models import Product


@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(
        name="test product",
        description="test product description",
        category="test category",
        price=1000,
        stock=10,
    )
    assert product.name == "test product"
    assert product.description == "test product description"
    assert product.category == "test category"
    assert product.price == 1000
    assert product.stock == 10
