# Generated by Django 4.2.1 on 2023-05-28 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0012_alter_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='price',
            field=models.IntegerField(default=1, verbose_name='Цена'),
        ),
    ]
