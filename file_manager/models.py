from datetime import datetime
from django.db import models
from django.conf import settings


def user_directory_path(instance, filename):
    return 'uploads/{0}/{1}/{2}'.format(instance.owner.username, datetime.now().strftime("%Y/%m/%d"), filename)


class UserFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="responsável", on_delete=models.PROTECT)
    public = models.BooleanField("público", default=False)
    upload = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return str(self.upload)
