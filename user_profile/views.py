from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from file_manager.models import UserFile


class UserFileList(ListView):
    template_name = "file_manager/user_file_list.html"
    model = UserFile
    paginate_by = 30

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(owner=user)


def delete_file(request, upload_id):
    next_url = request.GET.get("next", "/uplads")
    get_object_or_404(UserFile, pk=upload_id, owner=request.user).delete()
    messages.add_message(request, messages.SUCCESS, "Arquivo removido com sucesso")
    return HttpResponseRedirect(next_url)

