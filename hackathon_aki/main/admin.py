from django.contrib import admin
from .models import File, PlatformAttachment


admin.site.register(PlatformAttachment)
admin.site.register(File)
