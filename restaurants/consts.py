from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Активен'
    DRAFT = 'draft', 'Доработка'
    CHECK = 'check', 'Проверяется'
    HIDDEN = 'hidden', 'Скрыт'
