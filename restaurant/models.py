from django.db import models
from django.contrib.gis.db import models as gis
from django.contrib.auth.models import User


class Restaurant(models.Model):
    title = models.CharField('Название', max_length=255, unique=True)
    description = models.JSONField('Описание', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20)
    logo = models.ImageField('Логотип', upload_to='rest_logos', blank=True, null=True)
    address = models.TextField('Адрес', null=True, blank=True)
    # geo = gis.PointField('Координаты', null=True, blank=True)
    delivery_min = models.PositiveIntegerField('Минимальная сумма для заказа', blank=True, null=True)
    delivery_time = models.PositiveSmallIntegerField('Время доставки')
    average_check = models.FloatField('Средний чек', null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name='Управляющий', on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField('Категория', max_length=50)
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='categories',
        verbose_name='Ресторан',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.restaurant}: {self.title}"


class Product(models.Model):
    title = models.CharField('Название', max_length=150)
    description = models.JSONField('Описание')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='products',
        on_delete=models.CASCADE
    )
    price = models.PositiveIntegerField('Цена')
    is_available = models.BooleanField('В наличие', default=True, blank=True)

    def __str__(self):
        return f"{self.category.title}: {self.title}"
