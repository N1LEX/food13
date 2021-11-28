from random import randint

from django.core.management.base import BaseCommand

from restaurants.consts import StatusChoices
from restaurants.models import Kitchen, Restaurant, Category, Product, ProductPortion
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        self._create_users()
        self._create_kitchen()
        self._create_restaurant()
        self._create_category()
        self._create_product()
        self._create_product_portion()

    def _create_users(self):
        self.stdout.write(self.style.SUCCESS('Создание пользователей'))
        try:
            su = User.objects.create(email="admin@example.com", is_staff=True, is_superuser=True, role="developer")
            su.set_password("123321")
            su.save()
            for r, _ in User.RoleTypeChoices.choices:
                u = User.objects.create(username=r, role=r, email=f"{r}@example.com")
                u.set_password("123321")
                u.save()
            self.stdout.write(self.style.SUCCESS('Юзеры созданы'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания пользователей: {e}'))

    def _create_kitchen(self):
        self.stdout.write(self.style.SUCCESS('Создание кухни'))
        try:
            kitchens = "Русская", "Азиатская", "Фастфуд", "Суши"
            for kitchen in kitchens:
                Kitchen.objects.create(name=kitchen)
            self.stdout.write(self.style.SUCCESS('Кухня создана'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания кухни: {e}'))

    def _create_restaurant(self):
        self.stdout.write(self.style.SUCCESS('Создание ресторана'))
        try:
            r = Restaurant.objects.create(
                name="РЫГАЛОВКА СТЭЙШН",
                status=StatusChoices.ACTIVE,
                delivery_min=700,
                delivery_time=90,
                website="https://rigalovka.station/",
            )
            r.users.add(User.objects.filter(role=User.RoleTypeChoices.MANAGER).first())
            r.users.add(User.objects.filter(role=User.RoleTypeChoices.EMPLOYEE).first())
            r.kitchen.add(Kitchen.objects.first())
            self.stdout.write(self.style.SUCCESS('Ресторан создан'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания ресторана: {e}'))

    def _create_category(self):
        self.stdout.write(self.style.SUCCESS('Создание категорий'))
        try:
            r = Restaurant.objects.first()
            for c in ('Плотно похавать', 'Закусон', 'Бухич'):
                Category.objects.create(name=c, restaurant=r)
            self.stdout.write(self.style.SUCCESS('Категория создана'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания категорий: {e}'))

    def _create_product(self):
        self.stdout.write(self.style.SUCCESS('Создание меню'))
        try:
            r = Restaurant.objects.first()
            for c in Category.objects.filter(restaurant=r):
                Product.objects.create(
                    name=f"Хавчик {c.name}",
                    category=c,
                    status=StatusChoices.ACTIVE,
                )
            self.stdout.write(self.style.SUCCESS('Меню создано'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания меню: {e}'))

    def _create_product_portion(self):
        self.stdout.write(self.style.SUCCESS('Создание меню'))
        try:
            for p in Product.objects.all():
                for _ in range(3):
                    ProductPortion.objects.create(
                        product=p,
                        price=randint(300, 2700),
                        weight=randint(200, 2000),
                        status=StatusChoices.ACTIVE,
                    )
            self.stdout.write(self.style.SUCCESS('Меню создано'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания меню: {e}'))
