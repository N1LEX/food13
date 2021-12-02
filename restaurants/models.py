from datetime import time

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel

from restaurants.consts import StatusChoices
from restaurants.managers import (
    RestaurantManager,
    CategoryManager,
    ProductManager,
    ProductPortionManager,
)


class RestaurantBaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    status = models.CharField('Статус', choices=StatusChoices.choices, default=StatusChoices.CHECK, max_length=20)

    def set_status(self, new_status: StatusChoices) -> None:
        """
        Установка нового статуса.
        """
        self.status = new_status
        self.save()

    class Meta:
        abstract = True


class Restaurant(RestaurantBaseModel):
    name = models.CharField('Название', max_length=100, db_index=True, unique=True)
    description = models.TextField('Описание', max_length=700, blank=True, null=True)
    logo = models.ImageField('Логотип', upload_to='rest_logos', blank=True, null=True)
    delivery_min = models.PositiveIntegerField('Минимальная сумма для заказа')
    delivery_time = models.PositiveSmallIntegerField('Время доставки', null=True, default=90)
    open_time = models.TimeField('Время открытия', default=time(hour=10), blank=True)
    close_time = models.TimeField('Время закрытия', default=time(hour=22), blank=True)
    self_pickup_discount = models.PositiveSmallIntegerField(
        'Скидка на самовывоз',
        blank=True,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(99)],
    )
    kitchen = models.ManyToManyField('Kitchen', verbose_name='Кухня', related_name='restaurants')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Сотрудники', related_name='restaurants')

    # Contact info
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес', null=True, blank=True)
    vk = models.CharField('VK', max_length=100, null=True, blank=True)
    instagram = models.CharField('instagram', max_length=100, null=True, blank=True)
    telegram = models.CharField('telegram', max_length=100, null=True, blank=True)
    website = models.CharField('website', max_length=100, null=True, blank=True)

    objects = RestaurantManager()

    def __str__(self):
        return self.name


class Kitchen(models.Model):
    name = models.CharField('Название', max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Category(RestaurantBaseModel):
    name = models.CharField('Название', max_length=100, db_index=True)
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='categories',
        verbose_name='Ресторан',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='categories',
        on_delete=models.SET_NULL,
        null=True,
    )

    objects = CategoryManager()

    def __str__(self):
        return f"{self.restaurant.name}: {self.name}"

    class Meta:
        unique_together = ('name', 'restaurant')


class Product(RestaurantBaseModel):
    name = models.CharField('Название', max_length=100, db_index=True)
    description = models.TextField('Описание', max_length=1000)
    logo = models.ImageField('Логотип', upload_to='product_logos', blank=True, null=True)
    is_available = models.BooleanField('В наличие', default=True, blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='products',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
    )

    objects = ProductManager()

    def __str__(self):
        return f"{self.category.name}: {self.name}"

    class Meta:
        unique_together = ('name', 'category')


class ProductPortion(RestaurantBaseModel):
    product = models.ForeignKey(Product, related_name='portions', on_delete=models.CASCADE)
    weight = models.PositiveIntegerField('Вес порции', null=True, blank=True)
    price = models.PositiveIntegerField('Цена')
    discount = models.PositiveSmallIntegerField(
        'Скидка',
        blank=True,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='product_portions',
        on_delete=models.SET_NULL,
        null=True,
    )

    objects = ProductPortionManager()

    @property
    def total_price(self) -> int:
        """
        Расчет стоимости порции с учетом скидки
        """
        discount_sum = 0
        if self.discount:
            discount_sum = round(self.price * self.discount / 100)
        return self.price - discount_sum

    def __str__(self):
        return f"{str(self.product)}: {self.price}р, {self.weight}гр."

    class Meta:
        unique_together = ('product', 'weight', 'price')
