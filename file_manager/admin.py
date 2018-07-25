from django.contrib import admin
from .models import UserFile


class UserFileAdmin(admin.ModelAdmin):
    raw_id_fields = ('owner',)


admin.site.register(UserFile, UserFileAdmin)
