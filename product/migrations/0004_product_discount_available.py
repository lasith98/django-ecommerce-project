# Generated by Django 2.2.12 on 2020-05-12 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200512_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_available',
            field=models.BooleanField(default=False),
        ),
    ]
