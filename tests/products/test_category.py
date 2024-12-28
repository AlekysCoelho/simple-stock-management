import pytest

from app.products.models import Category


@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(name="test category")
    assert category.name == "test category"
