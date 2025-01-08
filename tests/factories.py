from decimal import Decimal

import factory
import faker
from faker import Faker

from app.accounts.models import Users
from app.products.models import Category, Product

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users
        django_get_or_create = (
            "username",
            "email",
        )

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False
    is_superuser = False


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Faker("word")
    description = factory.Faker("text")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n} - {faker.word()}")
    description = factory.LazyFunction(lambda: faker.paragraph(nb_sentences=3))
    category = factory.SubFactory(CategoryFactory)
    price = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True, min_value=1
    )
    stock = factory.Faker("random_int", min=1, max=100)
    discount = factory.Faker("random_int", min=0, max=50)


class NoDiscountProductFactory(ProductFactory):
    discount = 0
    final_price = factory.LazyAttribute(
        lambda x: x.price - (x.price * x.discount / 100)
    )


class DiscountedProductFactory(ProductFactory):
    discount = factory.Faker("random_int", min=1, max=50)
    final_price = factory.LazyAttribute(
        lambda x: x.price - (x.price * x.discount / 100)
    )


class MaxDiscountProductFactory(ProductFactory):
    discount = 50
    final_price = factory.LazyAttribute(
        lambda x: x.price - (x.price * x.discount / 100)
    )


class MinDiscountProductFactory(ProductFactory):
    discount = 1
    final_price = factory.LazyAttribute(
        lambda x: x.price - (x.price * x.discount / 100)
    )


class ZeroDiscountProductFactory(ProductFactory):
    discount = 0
    final_price = factory.LazyAttribute(
        lambda x: x.price - (x.price * x.discount / 100)
    )


class CustomDiscountProductFactory(ProductFactory):
    discount = factory.Sequence(lambda n: n)
    final_price = factory.LazyAttribute(
        lambda x: x.price - (x.price * x.discount / 100)
    )


class LowStockProductFactory(ProductFactory):
    stock = factory.Faker("random_int", min=1, max=10)
