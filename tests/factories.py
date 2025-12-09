import factory
from django.contrib.auth import get_user_model
from products.models import Product
import random

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@test.com")
    password = factory.PostGenerationMethodCall('set_password', '123456')
    role = 'CLIENTE'


class AdminFactory(UserFactory):
    role = 'ADMIN'


class StaffFactory(UserFactory):
    role = 'STAFF'


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=1, max=100)
    is_public = True
    owner = factory.SubFactory(UserFactory)
