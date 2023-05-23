from django.db import models
from django.contrib.auth.models import User


class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email_verification = models.OneToOneField('main.EmailVerification', on_delete=models.CASCADE, null=True)

    middle_name = models.CharField('Отчество', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=50)
    position = models.CharField('Должность', max_length=50, blank=True)
    juridical_name = models.CharField('Юридическое лицо', max_length=50, blank=True)
    inn = models.CharField('ИНН', max_length=50, blank=True)

    def __str__(self):
        if self.user is not None:
            return f'{self.user.first_name} {self.user.last_name} {self.middle_name}'
        return f'Ожидание подтверждения {self.email_verification.email}'

    class Meta:
        verbose_name = 'Организатор'
        verbose_name_plural = 'Организаторы'


class Entry(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    platform = models.ForeignKey('platforms.Platform', on_delete=models.CASCADE)

    date_start = models.DateTimeField('Дата начала записи')
    date_end = models.DateTimeField('Дата окончания записи')

    def __str__(self):
        return f'Запись на {self.date_start}, до {date_end}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
