# Generated by Django 4.1.5 on 2023-01-08 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('category', models.CharField(choices=[('other', 'Другое'), ('fishing', 'Рыбалка'), ('hunting', 'Охота'), ('skiing', 'Лыжи и сноуборд'), ('diving', 'Подводное снаряжение')], default='other', max_length=50, verbose_name='Категория')),
                ('balance', models.PositiveIntegerField(verbose_name='Остаток')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Стоимость')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'items',
            },
        ),
    ]
