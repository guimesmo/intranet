from django.contrib import admin

from .models import UserProfile, UserFile


class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", )


class UserFileAdmin(admin.ModelAdmin):
    raw_id_fields = ('owner',)


admin.site.register(UserFile, UserFileAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
