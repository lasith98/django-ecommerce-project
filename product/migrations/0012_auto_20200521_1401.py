# Generated by Django 2.2.12 on 2020-05-21 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_product_maximum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='maximum',
            field=models.IntegerField(default=10),
        ),
    ]