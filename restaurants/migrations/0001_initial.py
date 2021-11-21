# Generated by Django 3.2.9 on 2021-11-21 13:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kitchen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Активен'), ('draft', 'Доработка'), ('check', 'Проверяется'), ('hidden', 'Скрыт')], default='check', max_length=20, verbose_name='Статус')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=700, null=True, verbose_name='Описание')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='rest_logos', verbose_name='Логотип')),
                ('delivery_min', models.PositiveIntegerField(verbose_name='Минимальная сумма для заказа')),
                ('delivery_time', models.PositiveSmallIntegerField(verbose_name='Время доставки')),
                ('opens_in', models.TimeField(default=datetime.time(10, 0), null=True, verbose_name='Время открытия')),
                ('closes_in', models.TimeField(default=datetime.time(22, 0), null=True, verbose_name='Время закрытия')),
                ('self_pickup_discount', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Скидка на самовывоз')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Адрес')),
                ('vk', models.CharField(blank=True, max_length=100, null=True, verbose_name='VK')),
                ('instagram', models.CharField(blank=True, max_length=100, null=True, verbose_name='instagram')),
                ('telegram', models.CharField(blank=True, max_length=100, null=True, verbose_name='telegram')),
                ('website', models.CharField(blank=True, max_length=100, null=True, verbose_name='website')),
                ('kitchen', models.ManyToManyField(related_name='restaurants', to='restaurants.Kitchen', verbose_name='Кухня')),
                ('users', models.ManyToManyField(related_name='restaurants', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудники')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Активен'), ('draft', 'Доработка'), ('check', 'Проверяется'), ('hidden', 'Скрыт')], default='check', max_length=20, verbose_name='Статус')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='restaurants.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'unique_together': {('name', 'restaurant')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Активен'), ('draft', 'Доработка'), ('check', 'Проверяется'), ('hidden', 'Скрыт')], default='check', max_length=20, verbose_name='Статус')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название')),
                ('description', models.TextField(max_length=1000, verbose_name='Описание')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='product_logos', verbose_name='Логотип')),
                ('weight', models.PositiveIntegerField(blank=True, null=True, verbose_name='Вес порции')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('is_available', models.BooleanField(blank=True, default=True, verbose_name='В наличие')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='restaurants.category', verbose_name='Категория')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'category')},
            },
        ),
    ]
