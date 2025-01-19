from decimal import ROUND_DOWN, Decimal

import pytest
from ninja.testing import TestClient

from tests.factories import CategoryFactory, ProductFactory

# API Test
# @pytest.mark.django_db
# def test_simple_api(api_client: TestClient):
#     response = api_client.get("/products")
#     assert response.status_code == 200


@pytest.mark.django_db
class TestProducsAPI:

    def test_get_products_list(
        self, api_client: TestClient, product_factory: ProductFactory
    ) -> None:
        products = [product_factory(name=f"Test Product {i}") for i in range(5)]

        response = api_client.get("/products/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

        # Sort products and data by ID to ensure correct comparison
        sorted_products = sorted(products, key=lambda x: x.id)
        sorted_data = sorted(data, key=lambda x: x["id"])

        for product_data, product in zip(sorted_data, sorted_products):

            assert product_data["name"] == product.name
            assert product_data["description"] == product.description
            assert product_data["stock"] == product.stock
            assert Decimal(f"{product_data['discount']}") == Decimal(
                f"{product.discount}"
            )
            assert Decimal(f"{product_data['final_price']}") == Decimal(
                f"{product.final_price}"
            ).quantize(Decimal(".01"))

    def test_get_products_by_categories(
        self,
        api_client: TestClient,
        product_factory: ProductFactory,
        category_factory: CategoryFactory,
    ) -> None:
        category1 = category_factory(name="Electronics")
        category2 = category_factory(name="Books")

        electronics_products = [product_factory(category=category1) for _ in range(5)]

        books_products = [product_factory(category=category2) for _ in range(3)]

        response = api_client.get(f"/products/?category={category1.name}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        # assert all(product["category"]["name"] == "Electronics" for product in data)

    def test_get_products_with_discount(
        self, api_client: TestClient, product_factory: ProductFactory
    ) -> None:
        products = [product_factory(price=200.00, discount=30) for _ in range(5)]

        response = api_client.get("/products/")

        assert response.status_code == 200
        data = response.json()

        for product_data in data:
            assert "final_price" in product_data
            expected_price = Decimal(product_data["price"]) * (
                1 - (Decimal(product_data["discount"]) / Decimal(100))
            )
            assert Decimal(product_data["final_price"]) == Decimal(
                f"{expected_price}"
            ).quantize(Decimal("0.01"))

    def test_get_products_with_filter_by_min_price(
        self, api_client: TestClient, product_factory: ProductFactory
    ) -> None:
        product1 = product_factory(price=100.00, stock=5)
        product2 = product_factory(price=200.00, stock=30)
        product3 = product_factory(price=400.00, stock=50)

        response = api_client.get("/products/?min_price=150")

        assert response.status_code == 200
        data = response.json()
        print(data)
        assert len(data) == 2
        assert all(
            Decimal(product["price"]).quantize(Decimal("0.01")) >= 150
            for product in data
        )

    def test_get_products_with_filter_by_max_price(
        self, api_client: TestClient, product_factory: ProductFactory
    ) -> None:
        product1 = product_factory(price=1000.00, stock=5)
        product2 = product_factory(price=670.00, stock=15)
        product3 = product_factory(price=350.00, stock=30)
        product4 = product_factory(price=410.00, stock=50)
        product5 = product_factory(price=430.00, stock=50)

        response = api_client.get("/products/?max_price=450")

        assert response.status_code == 200
        data = response.json()
        print(data)
        assert len(data) == 3
        assert all(
            Decimal(product["price"]).quantize(Decimal("0.01")) <= 450
            for product in data
        )
