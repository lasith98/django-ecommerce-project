# Generated by Django 2.2.12 on 2020-05-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ManyToManyField(blank=True, null=True, to='product.Product'),
        ),
    ]