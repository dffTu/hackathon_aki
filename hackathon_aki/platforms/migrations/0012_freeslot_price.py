# Generated by Django 4.2.1 on 2023-05-23 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0011_platform_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='freeslot',
            name='price',
            field=models.IntegerField(null=True, verbose_name='Цена'),
        ),
    ]
