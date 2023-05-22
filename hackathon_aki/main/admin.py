from django.contrib import admin
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from .models import File, PlatformAttachment
from platforms.models import Platform


@receiver(pre_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(pre_delete, sender=PlatformAttachment)
def platform_attachment_delete(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(pre_delete, sender=Platform)
def platform_delete(sender, instance, **kwargs):
    instance.agreement.delete(False)


admin.site.register(PlatformAttachment)
admin.site.register(File)
