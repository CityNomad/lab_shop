# Generated by Django 4.1.5 on 2023-01-10 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_order_alter_item_options_alter_item_balance_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Basket',
        ),
    ]
