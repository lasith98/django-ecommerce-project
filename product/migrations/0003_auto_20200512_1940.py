# Generated by Django 2.2.12 on 2020-05-12 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20200512_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='expired',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
