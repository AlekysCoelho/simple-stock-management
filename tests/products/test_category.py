import pytest

from app.products.models import Category

# @pytest.mark.django_db
# def test_create_category():
#     category = Category.objects.create(
#         name="test category", description="test description"
#     )
#     assert category.name == "test category"
#     assert category.description == "test description"

#     assert str(category) == "test category"


def test_create_category(new_category, db):
    """Test creating a new category"""
    assert new_category.name
    assert new_category.description
