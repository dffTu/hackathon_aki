from django.db import models


class Platform(models.Model):
    organizer = models.ForeignKey('organizers.Organizer', on_delete=models.CASCADE)

    verified = models.BooleanField('Подтверждена', default=False)
    name = models.CharField('Имя', max_length=250, blank=True)
    categories = models.CharField('Категории', max_length=250, blank=True)
    short_description = models.TextField('Краткое описание', blank=True)
    description = models.TextField('Описание площадки', blank=True)
    rating = models.FloatField('Рейтинг', blank=True)
    schedule = models.JSONField('Расписание', null=True, blank=True)
    address = models.JSONField('Адрес', null=True, blank=True)

    agreement = models.FileField('Соглашение', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'


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
