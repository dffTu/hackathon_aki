from django.db import models


class Platform(models.Model):
    organizer = models.ForeignKey('organizers.Organizer', on_delete=models.CASCADE)

    name = models.CharField('Имя', max_length=250, blank=True)
    category = models.CharField('Категория', max_length=250, blank=True)
    short_description = models.TextField('Краткое описание', blank=True)
    description = models.TextField('Описание площадки', blank=True)
    schedule = models.JSONField('Расписание', null=True)
    rating = models.FloatField('Рейтинг')

    agreement = models.FileField('Соглашение', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'


class FreeSlot(models.Model):
    platform = models.ForeignKey('platforms.Platform', on_delete=models.CASCADE)

    date = models.DateField('Свободная дата', blank=True)
    price = models.IntegerField('Цена', blank=True)

    def __str__(self):
        return f'Свободно {self.date}'

    class Meta:
        verbose_name = 'Свободный слот'
        verbose_name_plural = 'Свободные слоты'


class Comment(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    platform = models.ForeignKey('platforms.Platform', on_delete=models.CASCADE)

    text = models.TextField('Текст отзыва', blank=True)
    rating = models.FloatField('Рейтинг', blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
