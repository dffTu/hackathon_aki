from django.db import models


class Client(models.Model):
    e_mail = models.EmailField('Электронная почта', unique=True)
    password = models.CharField('Пароль', max_length=50)
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    middle_name = models.CharField('Отчество', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=50, unique=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.middle_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
