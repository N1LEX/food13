from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Email and password is required. Other fields are optional.
    """
    class RoleTypeChoices(models.TextChoices):
        MANAGER = 'manager', 'Управляющий'
        EMPLOYEE = 'employee', 'Сотрудник'
        COURIER = 'courier', 'Курьер'
        CUSTOMER = 'customer', 'Покупатель'

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=True,
        null=True,
    )
    email = models.EmailField(
        'Email',
        unique=True,
        error_messages={
            'unique': "Пользователь с таким email уже существует",
        },
    )
    phone = models.CharField('Номер телефона', max_length=12)
    delivery_address = models.TextField('Адрес доставки', max_length=150, null=True, blank=True)
    role = models.CharField(
        'Роль',
        choices=RoleTypeChoices.choices,
        max_length=13,
        blank=True,
        default=RoleTypeChoices.CUSTOMER,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'User: {self.email}, Role: {self.role}'

    class Meta(AbstractUser.Meta):
        unique_together = ('email', 'phone')
