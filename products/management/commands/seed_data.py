from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from products.models import Product
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Crea 5 usuarios falsos y 20 productos falsos"

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write(self.style.WARNING("Eliminando datos anteriores..."))
        Product.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        roles = ["ADMIN", "STAFF", "CLIENTE"]
        users = []

        self.stdout.write(self.style.SUCCESS("Creando usuarios..."))

        for i in range(5):
            role = random.choice(roles)

            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="123456",
                role=role,
            )

            users.append(user)

            self.stdout.write(f"✅ Usuario creado: {user.username} | Rol: {role}")

        self.stdout.write(self.style.SUCCESS("Creando productos..."))

        for _ in range(20):
            owner = random.choice(users)

            Product.objects.create(
                name=fake.word().title(),
                price=round(random.uniform(10, 500), 2),
                stock=random.randint(1, 100),
                owner=owner,
                is_public=random.choice([True, False]),
            )

        self.stdout.write(self.style.SUCCESS("✅ Seeder ejecutado correctamente"))
