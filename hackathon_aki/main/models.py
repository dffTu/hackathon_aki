from django.db import models


class EmailVerification(models.Model):
    email = models.CharField('E-mail', max_length=254)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Не подтверждённый e-mail'
        verbose_name_plural = 'Не подтверждённые e-mail'


class PlatformAttachment(models.Model):
    platform = models.ForeignKey('platforms.Platform', on_delete=models.CASCADE)

    file = models.FileField('Файл')

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Закреплённый файл площадки'
        verbose_name_plural = 'Закреплённые файлы площадок'


class File(models.Model):
    file = models.FileField('Файл', null=True)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
