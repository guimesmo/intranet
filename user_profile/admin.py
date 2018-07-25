from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", )


admin.site.register(UserProfile, UserProfileAdmin)
