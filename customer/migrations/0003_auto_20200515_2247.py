# Generated by Django 2.2.12 on 2020-05-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20200515_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ManyToManyField(to='product.Product'),
        ),
    ]
