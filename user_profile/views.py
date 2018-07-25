from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from file_manager.models import UserFile


class UserFileList(ListView):
    template_name = "file_manager/user_file_list.html"
    model = UserFile

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(owner=user)
