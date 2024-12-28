import pytest

from app.products.models import Category, Product

# @pytest.mark.django_db
# def test_create_product():
#     product = Product.objects.create(
#         name="test product",
#         description="test product description",
#         category=Category.objects.create(name="test category"),
#         price=1000.00,
#         stock=10,
#     )
#     assert product.name == "test product"
#     assert product.description == "test product description"
#     assert product.category.name == "test category"
#     assert product.price == 1000
#     assert product.stock == 10

#     expected_product_str = f"{product.name} - {product.category.name}"
#     assert str(product) == expected_product_str


def test_create_product(new_product, db):
    """Test creating a new product"""
    assert new_product.name
    assert new_product.description
    assert new_product.category
    assert new_product.price
    assert new_product.stock
    assert isinstance(new_product, Product)
