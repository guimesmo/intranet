from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from django.views.generic import ListView
from django.views.generic.base import View

from file_manager.models import UserFile
from user_profile.forms import UserProfileForm

User = get_user_model()


class UserProfileView(View):
    template_name = 'contact.html'


    def get(self, request, user_id=None):
        if user_id:
            if request.user.has_perm("user_profile", "can_manage_user_information"):
                user = User.objects.get(pk=user_id)
            else:
                return HttpResponseForbidden("Você não tem permissão para executar esta ação")
        else:
            user = request.user
        form = UserProfileForm(instance=user.userprofile)
        return render(request, "user_profile/profile_edit.html", context={"form": form, "user": user})

    def post(self, request, user_id=None):
        if user_id:
            if request.user.has_perm("user_profile", "can_manage_user_information"):
                user = User.objects.get(pk=user_id)
                form = UserProfileForm(instance=user.userprofile, data=request.POST)
            else:
                return HttpResponseForbidden("Você não tem permissão para executar esta ação")
        else:
            user = request.user
            form = UserProfileForm(instance=user.userprofile, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, "Informações atualizadas com sucesso")
            return HttpResponseRedirect(request.path)

        return render(request, "user_profile/profile_edit.html", context={"form": form, "user": user})


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


def toogle_visibility(request, upload_id):
    next_url = request.GET.get("next", "/uplads")
    user_file = get_object_or_404(UserFile, pk=upload_id, owner=request.user)
    user_file.public = not user_file.public
    user_file.save()
    messages.add_message(request, messages.SUCCESS, "Visibilidade atualizada")
    return HttpResponseRedirect(next_url)

