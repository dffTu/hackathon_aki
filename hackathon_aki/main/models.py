from django.db import models


class EmailVerification(models.Model):
    email = models.CharField('E-mail', max_length=250, blank=True)
    first_name = models.CharField('Имя', max_length=250, blank=True)
    last_name = models.CharField('Фамилия', max_length=250, blank=True)
    password = models.CharField('Пароль', max_length=250, blank=True)
    verification_code = models.CharField('Код подтверждения', max_length=250, unique=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'

    class Meta:
        verbose_name = 'Не подтверждённый аккаунт'
        verbose_name_plural = 'Не подтверждённые аккаунты'


class PlatformAttachment(models.Model):
    platform = models.ForeignKey('platforms.Platform', on_delete=models.CASCADE)

    file = models.FileField('Файл')

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Закреплённый файл площадки'
        verbose_name_plural = 'Закреплённые файлы площадок'


class CommentAttachment(models.Model):
    comment = models.ForeignKey('platforms.Comment', on_delete=models.CASCADE)

    file = models.FileField('Файл')

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Закреплённый файл отзыва'
        verbose_name_plural = 'Закреплённые файлы отзывов'
