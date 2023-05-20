from django.db import models


class Platform(models.Model):
    organizer = models.ForeignKey('organizers.Organizer', on_delete=models.CASCADE, null=True, blank=True)
    agreement = models.ForeignKey('main.File', on_delete=models.SET_NULL, related_name='platform_agreement', null=True, blank=True)
    photo = models.ForeignKey('main.File', on_delete=models.SET_NULL, related_name='platform_photo', null=True, blank=True)

    name = models.CharField('Имя', max_length=50, null=True, blank=True)
    description = models.TextField('Описание площадки', null=True, blank=True)
    schedule = models.JSONField('Расписание', null=True, blank=True)
    rating = models.FloatField('Рейтинг', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'


class FreeSlot(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True, blank=True)

    date = models.DateField('Свободная дата', null=True, blank=True)

    def __str__(self):
        return f'Свободно {self.date}'

    class Meta:
        verbose_name = 'Свободный слот'
        verbose_name_plural = 'Свободные слоты'


class Comment(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, null=True, blank=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True, blank=True)
    attachment = models.ForeignKey('main.File', on_delete=models.SET_NULL, null=True, blank=True)

    text = models.TextField('Текст отзыва', null=True, blank=True)
    rating = models.FloatField('Рейтинг', null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
