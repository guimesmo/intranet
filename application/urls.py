"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import logout
from django.urls import path
from django.views.generic import RedirectView

from user_profile.views import UserFileList, delete_file, toogle_visibility, UserProfileView, UserList, \
    UserProfileCreateView, UserProfileAdminEditView, UserFileListAdmin, PublicFileListView, UserFileInformationApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url="/uploads/")),
    path('uploads/', login_required(UserFileList.as_view())),
    path('uploads/<upload_id>/delete', login_required(delete_file)),
    path('uploads/<upload_id>/toogle-visibility', login_required(toogle_visibility)),

    # user profile
    path('perfil/', login_required(UserProfileView.as_view())),
    path('usuarios/', login_required(UserList.as_view())),
    path('usuarios/novo/', login_required(UserProfileCreateView.as_view())),
    path('usuarios/<user_profile_id>/', UserProfileAdminEditView.as_view()),
    path('usuarios/<user_profile_id>/uploads/', UserFileListAdmin.as_view()),

    # public
    path('publico/', login_required(PublicFileListView.as_view())),
    path('api/utilizacao/', UserFileInformationApi.as_view()),


    # account actions
    path('login/', LoginView.as_view(template_name='login.html')),
    path('logout/', logout, {"next_page": '/login'}),
]
