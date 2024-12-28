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

    name = factory.Faker("name")
    description = factory.Faker("text")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("name")
    description = factory.Faker("text")
    category = factory.SubFactory(CategoryFactory)
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    stock = factory.Faker("random_int", min=1, max=100)
