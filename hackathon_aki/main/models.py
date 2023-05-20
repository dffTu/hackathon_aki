from django.db import models


class File(models.Model):
    file_name = models.FileField('Имя', null=True, blank=True)
    file_data = models.BinaryField('Данные', null=True, blank=True)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
