import os

from django.db import models
from django.conf import settings

from file_manager.models import UserFile

USER_PROFILE_COMMON = 101
USER_PROFILE_ADMIN = 102

USER_PROFILE_CHOICES = (
    (USER_PROFILE_COMMON, "FUNCIONARIO"),
    (USER_PROFILE_ADMIN, "GESTOR"),
)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    profile_type = models.PositiveIntegerField("Tipo de usuário", choices=USER_PROFILE_CHOICES)

    full_address = models.CharField("Endereço completo", max_length=255)
    city_state = models.CharField("Cidade - UF", max_length=50)

    upload_volume_limit = models.PositiveIntegerField("limite de volume de arquivos", blank=True, null=True,
                                                      help_text="Volume de dados máximo de arquivos do usuário")
    upload_number_limit = models.PositiveIntegerField("limite de máximo de arquivos", blank=True, null=True,
                                                      help_text="Número máximo de arquivos do usuário")

    class Meta:
        verbose_name = "perfil de usuário"
        verbose_name_plural = "perfis de usuários"
        permissions = (
            ("can_see_all_files", "Ver todos os arquivos"),
            ("can_manage_user_information", "Gerenciar informações de usuários"),
            ("can_read_usage_information", "Ver informações de utilização"),
            ("can_manage_upload_limit", "Gerenciar limite de upload"),
            ("can_change_own_name", "Alterar o próprio nome"),
            ("can_change_own_email", "Alterar o próprio email")
        )

    def __str__(self):
        return self.user.get_full_name() or "Nome não informado"

    def get_user_files(self):
        return UserFile.objects.filter(owner=self.user)

    def get_number_of_user_files(self):
        return self.get_user_files().count()

    def get_volume_of_user_files(self):
        file_paths = self.get_user_files().values_list("upload", flat=True)
        volume_bytes = sum([os.path.getsize(os.path.join(settings.MEDIA_ROOT, f)) for f in file_paths])
        volume_megabytes = volume_bytes / (1024*1024)
        return volume_megabytes
