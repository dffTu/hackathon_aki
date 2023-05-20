from django.db import models


class Client(models.Model):
    e_mail = models.EmailField('Электронная почта', null=True, blank=True)
    password = models.CharField('Пароль', max_length=50, null=True, blank=True)
    name = models.CharField('Имя', max_length=50, null=True, blank=True)
    surname = models.CharField('Фамилия', max_length=50, null=True, blank=True)
    middle_name = models.CharField('Отчество', max_length=50, null=True, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.middle_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
