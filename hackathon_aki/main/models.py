from django.db import models


class File(models.Model):
    file_name = models.CharField('Имя', max_length=50)
    file_data = models.BinaryField('Данные', null=True)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
