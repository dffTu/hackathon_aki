from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    middle_name = models.CharField('Отчество', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=50, unique=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.middle_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
