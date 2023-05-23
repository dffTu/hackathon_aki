from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email_verification = models.OneToOneField('main.EmailVerification', on_delete=models.CASCADE, null=True)

    middle_name = models.CharField('Отчество', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=50)

    def __str__(self):
        if self.user is not None:
            return f'{self.user.first_name} {self.user.last_name} {self.middle_name}'
        return f'Ожидание подтверждения {self.email_verification.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
