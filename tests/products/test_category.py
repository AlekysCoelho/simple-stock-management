import pytest

from app.products.models import Category


@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(
        name="test category", description="test description"
    )
    assert category.name == "test category"
    assert category.description == "test description"

    assert str(category) == "test category"
