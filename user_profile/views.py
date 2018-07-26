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

    def post(self, request):
        next_url = request.GET.get("next", "/uploads")

        upload = request.FILES.get("upload")
        if not upload:
            messages.add_message(request, messages.ERROR, "Falha ao enviar arquivo. Por favor, verifique ")
        else:
            public = request.POST.get("public")
            user_file = UserFile.objects.create(
                owner=request.user,
                public=bool(public),
                upload=upload
            )
            messages.add_message(request, messages.SUCCESS, "Arquivo inserido com sucesso")
        return HttpResponseRedirect(next_url)


def delete_file(request, upload_id):
    next_url = request.GET.get("next", "/uplads")
    get_object_or_404(UserFile, pk=upload_id, owner=request.user).delete()
    messages.add_message(request, messages.SUCCESS, "Arquivo removido com sucesso")
    return HttpResponseRedirect(next_url)

