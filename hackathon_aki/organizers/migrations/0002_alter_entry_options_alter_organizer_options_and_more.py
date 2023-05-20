# Generated by Django 4.2.1 on 2023-05-20 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
        migrations.AlterModelOptions(
            name='organizer',
            options={'verbose_name': 'Организатор', 'verbose_name_plural': 'Организаторы'},
        ),
        migrations.AddField(
            model_name='entry',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата записи'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='e_mail',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Электронная почта'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='inn',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ИНН'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='juridical_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Юридическое лицо'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Пароль'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='position',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='surname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия'),
        ),
    ]
