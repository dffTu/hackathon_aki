# Generated by Django 4.2.1 on 2023-05-24 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0015_alter_comment_rating_alter_freeslot_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platform',
            name='category',
        ),
        migrations.AddField(
            model_name='platform',
            name='categories',
            field=models.CharField(blank=True, max_length=250, verbose_name='Категории'),
        ),
    ]
