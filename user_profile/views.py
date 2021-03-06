import json

from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator

from django.views.generic import ListView, FormView, UpdateView
from django.views.generic.base import View

from user_profile.forms import UserProfileAdminForm
from .models import UserFile, UserProfile
from .forms import UserProfileForm

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


class UserList(ListView):
    template_name = "user_profile/user_list.html"
    model = UserProfile
    paginate_by = 30

    @method_decorator(permission_required("user_profile.can_manage_user_information"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserProfileCreateView(FormView):
    form_class = UserProfileAdminForm
    template_name = "user_profile/profile_edit_admin.html"
    success_url = '.'

    @method_decorator(permission_required("user_profile.can_manage_user_information"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        instance = form.save()
        messages.success(self.request, "Informações atualizadas com sucesso")
        return HttpResponseRedirect("/usuarios/%s" % instance.id)


class UserProfileAdminEditView(UpdateView):
    form_class = UserProfileAdminForm
    template_name = "user_profile/profile_edit_admin.html"
    success_url = '.'
    pk_url_kwarg = "user_profile_id"
    model = UserProfile

    @method_decorator(permission_required("user_profile.can_manage_user_information"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        instance = form.save()
        messages.success(self.request, "Informações atualizadas com sucesso")
        return HttpResponseRedirect("/usuarios/%s" % instance.id)


class UserFileList(ListView):
    template_name = "user_profile/user_file_list.html"
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
            if request.user.userprofile.upload_volume_limit is not None:
                file_size = len(upload)/(1024*1024)
                final_usage_estimate = request.user.userprofile.get_volume_of_user_files() + file_size
                if final_usage_estimate > request.user.userprofile.upload_volume_limit:
                    messages.add_message(request, messages.ERROR, "O tamanho do arquivo excede o seu limite de armazenamento")
                    return HttpResponseRedirect(next_url)
            if request.user.userprofile.upload_number_limit is not None:
                if request.user.userprofile.get_number_of_user_files() > request.user.userprofile.upload_number_limit:
                    messages.add_message(request, messages.ERROR, "Você está excedendo seu limite de envio de arquivos")
                    return HttpResponseRedirect(next_url)

            public = request.POST.get("public")
            UserFile.objects.create(
                owner=request.user,
                public=bool(public),
                upload=upload
            )
            messages.add_message(request, messages.SUCCESS, "Arquivo inserido com sucesso")
        return HttpResponseRedirect(next_url)


class UserFileListAdmin(ListView):
    template_name = "user_profile/user_file_list_admin.html"
    model = UserFile
    paginate_by = 30

    @method_decorator(permission_required("user_profile.can_see_all_files"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs['user_profile_id'])
        return self.model.objects.filter(owner=user)


class PublicFileListView(ListView):
    template_name = "user_profile/user_file_public.html"
    model = UserFile
    paginate_by = 30

    def get_queryset(self):
        return self.model.objects.filter(public=True)


class UserFileInformationApi(View):
    def get(self, request):
        data = [{"nome": upfl.user.get_full_name(),
                 "volume-utilizado": upfl.get_volume_of_user_files(),
                 "numero-arquivos": upfl.get_number_of_user_files(),
                 } for upfl in UserProfile.objects.all()]
        return JsonResponse(data, safe=False)


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

