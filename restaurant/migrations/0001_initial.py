# Generated by Django 3.2.9 on 2021-11-07 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('description', models.JSONField(blank=True, null=True, verbose_name='Описание')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='rest_logos', verbose_name='Логотип')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Адрес')),
                ('delivery_min', models.PositiveIntegerField(blank=True, null=True, verbose_name='Минимальная сумма для заказа')),
                ('delivery_time', models.PositiveSmallIntegerField(verbose_name='Время доставки')),
                ('average_check', models.FloatField(blank=True, null=True, verbose_name='Средний чек')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Управляющий')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.JSONField(verbose_name='Описание')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('is_available', models.BooleanField(blank=True, default=True, verbose_name='В наличие')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='restaurant.category', verbose_name='Категория')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='restaurant.restaurant', verbose_name='Ресторан'),
        ),
    ]